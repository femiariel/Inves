"""
PEA Radar factor engine.

The score is a robust cross-sectional ranking, not a return forecast:
  1. compute raw factors for every ETF
  2. reject bad data and unsuitable allocation products
  3. winsorize each factor to limit outliers
  4. normalize factors with robust z-scores
  5. combine them into a bounded 0-100 score

The main momentum leg is 12-1M: the 12-month return excluding the most
recent month. This keeps the signal focused on the established trend instead
of rewarding a late news spike too aggressively.

Score interpretation:
  50 = neutral relative to the valid universe
  70+ = strong
  55-70 = stable / constructive
  40-55 = weak
  <40 = avoid

Current raw score:
  0.45 * z(12-1M momentum)
+ 0.18 * z(6M momentum)
+ 0.10 * z(3M momentum)
+ 0.17 * z(price / SMA200)
- 0.06 * z(63D annualized volatility)
- 0.04 * z(12M max drawdown)
- overheat penalty based on extreme 1M momentum
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np
import pandas as pd


# Trading-day lookbacks
TD_1M  = 21
TD_3M  = 63
TD_6M  = 126
TD_12M = 252

# Score thresholds on the final 0-100 scale
THRESHOLD_BUY  = 70.0
THRESHOLD_HOLD = 55.0
THRESHOLD_TRIM = 40.0

# Trend
SMA_PERIOD = 200

# Data quality / sanity guards. Yahoo can occasionally expose bad adjusted
# histories on European ETC/leveraged products, producing fake +20,000% returns.
MIN_OBSERVATIONS      = TD_12M + 1
MAX_ABS_DAILY_RETURN  = 1.00  # one-day move above 100% is treated as bad data
MAX_ABS_LOOKBACK_RET  = 3.00  # +/-300% over a lookback is not normal ETF data
MAX_ANNUAL_VOL        = 3.00  # 300% annualized volatility
BAD_DATA_SCORE        = 0.0

# Robust ranking constants
WINSOR_LOWER = 0.01
WINSOR_UPPER = 0.99
MAX_ABS_Z    = 3.0

FACTOR_WEIGHTS = {
    "momentum_12_1m": 0.45,
    "momentum_6m":    0.18,
    "momentum_3m":    0.10,
    "trend":          0.17,
    "vol":           -0.06,
    "drawdown":      -0.04,
}

OVERHEAT_Z_START       = 1.5
OVERHEAT_PENALTY_PER_Z = 0.40

REC_LABELS = {
    "buy":   "Fort",
    "hold":  "Stable",
    "trim":  "Faible",
    "avoid": "Eviter",
}
REC_COLORS = {
    "buy":   "#156B49",
    "hold":  "#3A8C62",
    "trim":  "#BD6E1B",
    "avoid": "#BD3A33",
}

EXCLUDED_PRODUCT_KEYWORDS = (
    "leveraged",
    "daily 2",
    "2x",
    "short",
    "inverse",
    "bear",
    "ultrashort",
    "natural gas",
    "crude oil",
    "brent",
    "wti",
    "wheat",
    "silver",
    "gold",
    "bullion",
    "precious metals",
    "commodity",
    "commodities",
    "copper",
    "carbon",
)


def build_signal(ticker: str, history: pd.DataFrame, meta: Optional[dict] = None) -> dict:
    """
    Compute one signal. For production ranking, prefer build_all_signals so the
    score is normalized against the full universe.
    """
    return _score_signals([_build_raw_signal(ticker, history, meta or {})])[0]


def build_all_signals(
    histories: dict[str, pd.DataFrame],
    meta_df: pd.DataFrame,
) -> list[dict]:
    """
    Build signals for all tickers and return them sorted by final score.
    """
    raw = []
    for ticker, history in histories.items():
        meta = meta_df.loc[ticker].to_dict() if ticker in meta_df.index else {}
        raw.append(_build_raw_signal(ticker, history, meta))

    signals = _score_signals(raw)
    signals.sort(key=lambda s: s["score"], reverse=True)
    return signals


def signals_to_dataframe(signals: list[dict]) -> pd.DataFrame:
    cols = [
        "ticker", "name", "category", "sleeve",
        "score", "factor_score", "momentum_component", "trend_component", "risk_penalty",
        "momentum_z", "momentum_12_1m_z", "momentum_6m_z", "momentum_3m_z",
        "trend_z", "vol_z", "drawdown_z", "overheat_penalty",
        "r1M", "r3M", "r6M", "r12M", "r12_1M",
        "annual_vol", "max_drawdown", "above_sma200",
        "recommendation", "rec_label", "momentum_filter_ok",
        "data_quality_ok", "allocation_eligible",
        "latest_price", "lookback_summary",
    ]
    return pd.DataFrame(signals, columns=cols).set_index("ticker")


def _build_raw_signal(ticker: str, history: pd.DataFrame, meta: dict) -> dict:
    closes = history["close"].dropna()
    n = len(closes)
    latest_price: Optional[float] = float(closes.iloc[-1]) if n > 0 else None

    def _ret(td: int) -> float:
        if n < td + 1:
            return math.nan
        start = closes.iloc[-(td + 1)]
        if start <= 0:
            return math.nan
        return float(closes.iloc[-1] / start - 1)

    def _ret_excluding_recent(total_td: int, skip_td: int) -> float:
        if n < total_td + 1 or total_td <= skip_td:
            return math.nan
        end = closes.iloc[-(skip_td + 1)]
        start = closes.iloc[-(total_td + 1)]
        if start <= 0:
            return math.nan
        return float(end / start - 1)

    r1M  = _ret(TD_1M)
    r3M  = _ret(TD_3M)
    r6M  = _ret(TD_6M)
    r12M = _ret(TD_12M)
    r12_1M = _ret_excluding_recent(TD_12M, TD_1M)

    daily_rets = closes.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
    recent_daily_rets = daily_rets.tail(TD_12M)

    momentum_raw = r12_1M
    momentum_component = momentum_raw * 100 if math.isfinite(momentum_raw) else math.nan

    above_sma200 = False
    trend_raw = math.nan
    if n >= SMA_PERIOD and latest_price is not None:
        sma200 = float(closes.tail(SMA_PERIOD).mean())
        if sma200 > 0:
            trend_raw = latest_price / sma200 - 1
            above_sma200 = latest_price > sma200

    annual_vol = math.nan
    max_drawdown = math.nan
    max_abs_daily = math.nan
    if len(recent_daily_rets) > 0:
        annual_vol = float(recent_daily_rets.std() * math.sqrt(252))
        max_abs_daily = float(recent_daily_rets.abs().max())
        rolling_max = closes.tail(TD_12M).cummax()
        dd_series = (closes.tail(TD_12M) / rolling_max) - 1
        max_drawdown = abs(float(dd_series.min()))

    lookback_returns = [r for r in [r1M, r3M, r6M, r12M, r12_1M] if not math.isnan(r)]
    data_quality_ok = (
        latest_price is not None
        and n >= MIN_OBSERVATIONS
        and _finite_all([r3M, r6M, r12_1M, trend_raw, annual_vol, max_drawdown, max_abs_daily])
        and annual_vol <= MAX_ANNUAL_VOL
        and max_abs_daily <= MAX_ABS_DAILY_RETURN
        and all(abs(r) <= MAX_ABS_LOOKBACK_RET for r in lookback_returns)
    )
    allocation_eligible = _is_allocation_eligible(ticker, meta)
    scoring_eligible = data_quality_ok and allocation_eligible

    return {
        "ticker": ticker,
        "name": meta["name"] if meta else ticker,
        "sleeve": meta["sleeve"] if meta else "",
        "category": meta["category"] if meta else "",
        "latest_price": latest_price,
        "r1M": r1M,
        "r3M": r3M,
        "r6M": r6M,
        "r12M": r12M,
        "r12_1M": r12_1M,
        "momentum_raw": momentum_raw,
        "trend_raw": trend_raw,
        "momentum_component": momentum_component,
        "trend_component": math.nan,
        "risk_penalty": math.nan,
        "above_sma200": above_sma200,
        "annual_vol": annual_vol,
        "max_drawdown": max_drawdown,
        "max_abs_daily_return": max_abs_daily,
        "data_quality_ok": data_quality_ok,
        "allocation_eligible": allocation_eligible,
        "scoring_eligible": scoring_eligible,
        "lookback_summary": _lookback_summary(r1M, r3M, r6M, r12M, r12_1M),
    }


def _score_signals(raw_signals: list[dict]) -> list[dict]:
    valid_idx = [i for i, s in enumerate(raw_signals) if s["scoring_eligible"]]

    factor_values = {
        "momentum_12_1m": [raw_signals[i]["r12_1M"] for i in valid_idx],
        "momentum_6m":    [raw_signals[i]["r6M"] for i in valid_idx],
        "momentum_3m":    [raw_signals[i]["r3M"] for i in valid_idx],
        "momentum_1m":    [raw_signals[i]["r1M"] for i in valid_idx],
        "trend":          [raw_signals[i]["trend_raw"] for i in valid_idx],
        "vol":            [raw_signals[i]["annual_vol"] for i in valid_idx],
        "drawdown":       [raw_signals[i]["max_drawdown"] for i in valid_idx],
    }
    z_scores = {name: _robust_z(values) for name, values in factor_values.items()}

    scored = []
    valid_pos = {idx: pos for pos, idx in enumerate(valid_idx)}

    for i, sig in enumerate(raw_signals):
        sig = sig.copy()
        if i not in valid_pos:
            sig.update(_invalid_score_fields())
            scored.append(_finalize_signal(sig))
            continue

        pos = valid_pos[i]
        momentum_12_1m_z = z_scores["momentum_12_1m"][pos]
        momentum_6m_z = z_scores["momentum_6m"][pos]
        momentum_3m_z = z_scores["momentum_3m"][pos]
        momentum_1m_z = z_scores["momentum_1m"][pos]
        trend_z = z_scores["trend"][pos]
        vol_z = z_scores["vol"][pos]
        drawdown_z = z_scores["drawdown"][pos]
        overheat_penalty = max(0.0, momentum_1m_z - OVERHEAT_Z_START) * OVERHEAT_PENALTY_PER_Z
        factor_score = (
            FACTOR_WEIGHTS["momentum_12_1m"] * momentum_12_1m_z
            + FACTOR_WEIGHTS["momentum_6m"] * momentum_6m_z
            + FACTOR_WEIGHTS["momentum_3m"] * momentum_3m_z
            + FACTOR_WEIGHTS["trend"] * trend_z
            + FACTOR_WEIGHTS["vol"] * vol_z
            + FACTOR_WEIGHTS["drawdown"] * drawdown_z
            - overheat_penalty
        )
        score = max(0.0, min(100.0, 50.0 + 15.0 * factor_score))

        sig.update({
            "momentum_z": momentum_12_1m_z,
            "momentum_12_1m_z": momentum_12_1m_z,
            "momentum_6m_z": momentum_6m_z,
            "momentum_3m_z": momentum_3m_z,
            "trend_z": trend_z,
            "vol_z": vol_z,
            "drawdown_z": drawdown_z,
            "overheat_penalty": overheat_penalty,
            "factor_score": factor_score,
            "score": score,
            "raw_score": factor_score,
            "trend_component": trend_z * 10.0,
            "risk_penalty": max(
                0.0,
                (
                    -FACTOR_WEIGHTS["vol"] * vol_z
                    - FACTOR_WEIGHTS["drawdown"] * drawdown_z
                    + overheat_penalty
                ) * 15.0,
            ),
        })
        scored.append(_finalize_signal(sig))

    return scored


def _finalize_signal(sig: dict) -> dict:
    score = sig["score"]
    if score >= THRESHOLD_BUY:
        recommendation = "buy"
    elif score >= THRESHOLD_HOLD:
        recommendation = "hold"
    elif score >= THRESHOLD_TRIM:
        recommendation = "trim"
    else:
        recommendation = "avoid"

    r12_1M = sig["r12_1M"]
    sig["recommendation"] = recommendation
    sig["rec_label"] = REC_LABELS[recommendation]
    sig["rec_color"] = REC_COLORS[recommendation]
    sig["momentum_filter_ok"] = (
        sig["scoring_eligible"]
        and sig["above_sma200"]
        and not math.isnan(r12_1M)
        and r12_1M > 0
    )
    return sig


def _invalid_score_fields() -> dict:
    return {
        "momentum_z": 0.0,
        "momentum_12_1m_z": 0.0,
        "momentum_6m_z": 0.0,
        "momentum_3m_z": 0.0,
        "trend_z": 0.0,
        "vol_z": 0.0,
        "drawdown_z": 0.0,
        "overheat_penalty": 0.0,
        "factor_score": 0.0,
        "score": BAD_DATA_SCORE,
        "raw_score": 0.0,
        "trend_component": 0.0,
        "risk_penalty": 100.0,
    }


def _robust_z(values: list[float]) -> list[float]:
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return []

    finite = arr[np.isfinite(arr)]
    if len(finite) == 0:
        return [0.0 for _ in arr]

    lo, hi = np.quantile(finite, [WINSOR_LOWER, WINSOR_UPPER])
    capped = np.clip(arr, lo, hi)
    median = float(np.median(capped))
    mad = float(np.median(np.abs(capped - median)))
    scale = 1.4826 * mad
    if scale <= 1e-12:
        scale = float(np.std(capped))
    if scale <= 1e-12:
        return [0.0 for _ in capped]

    z = np.clip((capped - median) / scale, -MAX_ABS_Z, MAX_ABS_Z)
    return [float(x) if math.isfinite(float(x)) else 0.0 for x in z]


def _is_allocation_eligible(ticker: str, meta: dict) -> bool:
    text = f"{ticker} {meta.get('name', '')} {meta.get('category', '')}".lower()
    return not any(keyword in text for keyword in EXCLUDED_PRODUCT_KEYWORDS)


def _finite_all(values: list[float]) -> bool:
    return all(isinstance(v, (int, float)) and math.isfinite(v) for v in values)


def _lookback_summary(r1M: float, r3M: float, r6M: float, r12M: float, r12_1M: float) -> str:
    def _fmt(r: float) -> str:
        return f"{r*100:+.1f}%" if not math.isnan(r) else "n/a"

    return f"1M {_fmt(r1M)} • 3M {_fmt(r3M)} • 6M {_fmt(r6M)} • 12-1M {_fmt(r12_1M)} • 12M {_fmt(r12M)}"
