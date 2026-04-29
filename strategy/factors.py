"""
PEA Radar signal engine — exact port of PEAStore.SignalEngine.

Score formula (in percentage points):
  momentumComponent = 0.12×r1M + 0.25×r3M + 0.30×r6M + 0.33×r12M  (returns ×100)
  trendComponent    = +18 if price > SMA200, else -18
  riskPenalty       = min(35, (annualVol × 0.08 + maxDrawdown × 0.22) × 100)
  score             = momentumComponent + trendComponent − riskPenalty

Recommendation tiers:
  score ≥ 12  → buy   (Fort)
  score ≥  3  → hold  (Stable)
  score ≥ -8  → trim  (Faible)
  else        → avoid (Éviter)

Momentum filter for satellite sleeve: r12M must be > 0.
"""

from __future__ import annotations

import math
import numpy as np
import pandas as pd
from typing import Optional

# Momentum period weights
W_1M  = 0.12
W_3M  = 0.25
W_6M  = 0.30
W_12M = 0.33

# Trading-day lookbacks
TD_1M  = 21
TD_3M  = 63
TD_6M  = 126
TD_12M = 252

# Score thresholds
THRESHOLD_BUY  =  12.0
THRESHOLD_HOLD =   3.0
THRESHOLD_TRIM =  -8.0

# Trend bonus
TREND_BONUS = 18.0
SMA_PERIOD  = 200

REC_LABELS = {
    "buy":   "Fort",
    "hold":  "Stable",
    "trim":  "Faible",
    "avoid": "Éviter",
}
REC_COLORS = {
    "buy":   "#156B49",
    "hold":  "#3A8C62",
    "trim":  "#BD6E1B",
    "avoid": "#BD3A33",
}


def build_signal(ticker: str, history: pd.DataFrame, meta: Optional[dict] = None) -> dict:
    """
    Compute the full AssetSignal for one ETF.
    history: DataFrame with DatetimeIndex and 'close' column.
    Returns a dict with all score components.
    """
    closes = history["close"].dropna()
    n = len(closes)

    latest_price: Optional[float] = float(closes.iloc[-1]) if n > 0 else None

    # ── Returns ──────────────────────────────────────────────────────────────
    def _ret(td: int) -> float:
        if n < td + 1:
            return math.nan
        return float(closes.iloc[-1] / closes.iloc[-(td + 1)] - 1)

    r1M  = _ret(TD_1M)
    r3M  = _ret(TD_3M)
    r6M  = _ret(TD_6M)
    r12M = _ret(TD_12M)

    # ── Momentum component (in pct-points, returns already ×100) ─────────────
    present = [(w, r) for w, r in [(W_1M, r1M), (W_3M, r3M), (W_6M, r6M), (W_12M, r12M)]
               if not math.isnan(r)]
    if present:
        total_w = sum(w for w, _ in present)
        mom_component = sum(w * r * 100 for w, r in present) / total_w * sum(w for w, _ in present)
    else:
        mom_component = 0.0

    # ── Trend component ───────────────────────────────────────────────────────
    above_sma200 = False
    if n >= SMA_PERIOD and latest_price is not None:
        sma200 = float(closes.tail(SMA_PERIOD).mean())
        above_sma200 = latest_price > sma200
    trend_component = TREND_BONUS if above_sma200 else -TREND_BONUS

    # ── Risk penalty ──────────────────────────────────────────────────────────
    annual_vol = 0.0
    max_drawdown = 0.0
    if n >= 2:
        daily_rets = closes.pct_change().dropna().tail(TD_12M)
        annual_vol = float(daily_rets.std() * math.sqrt(252))
        rolling_max = closes.tail(TD_12M).cummax()
        dd_series = (closes.tail(TD_12M) / rolling_max) - 1
        max_drawdown = abs(float(dd_series.min()))

    raw_penalty = annual_vol * 0.08 + max_drawdown * 0.22
    risk_penalty = min(0.35, raw_penalty) * 100

    # ── Score (missing price penalty if no current price) ─────────────────────
    missing_penalty = -35.0 if latest_price is None else 0.0
    score = mom_component + trend_component - risk_penalty + missing_penalty

    # ── Recommendation ────────────────────────────────────────────────────────
    if latest_price is not None and score >= THRESHOLD_BUY:
        recommendation = "buy"
    elif score >= THRESHOLD_HOLD:
        recommendation = "hold"
    elif score >= THRESHOLD_TRIM:
        recommendation = "trim"
    else:
        recommendation = "avoid"

    # ── Lookback summary string ───────────────────────────────────────────────
    def _fmt(r: float) -> str:
        return f"{r*100:+.1f}%" if not math.isnan(r) else "n/a"

    lookback_summary = (
        f"1M {_fmt(r1M)} • 3M {_fmt(r3M)} • 6M {_fmt(r6M)} • 12M {_fmt(r12M)}"
    )

    return {
        "ticker":            ticker,
        "name":              meta["name"] if meta else ticker,
        "sleeve":            meta["sleeve"] if meta else "",
        "category":          meta["category"] if meta else "",
        "latest_price":      latest_price,
        "r1M":               r1M,
        "r3M":               r3M,
        "r6M":               r6M,
        "r12M":              r12M,
        "momentum_component": mom_component,
        "trend_component":   trend_component,
        "risk_penalty":      risk_penalty,
        "score":             score,
        "above_sma200":      above_sma200,
        "annual_vol":        annual_vol,
        "max_drawdown":      max_drawdown,
        "recommendation":    recommendation,
        "rec_label":         REC_LABELS[recommendation],
        "rec_color":         REC_COLORS[recommendation],
        "lookback_summary":  lookback_summary,
        "momentum_filter_ok": (not math.isnan(r12M) and r12M > 0),
    }


def build_all_signals(
    histories: dict[str, pd.DataFrame],
    meta_df: pd.DataFrame,
) -> list[dict]:
    """
    Build signals for all tickers and return them sorted by score descending.
    """
    signals = []
    for ticker, history in histories.items():
        m = meta_df.loc[ticker].to_dict() if ticker in meta_df.index else {}
        sig = build_signal(ticker, history, m)
        signals.append(sig)
    signals.sort(key=lambda s: s["score"], reverse=True)
    return signals


def signals_to_dataframe(signals: list[dict]) -> pd.DataFrame:
    cols = [
        "ticker", "name", "category", "sleeve",
        "score", "momentum_component", "trend_component", "risk_penalty",
        "r1M", "r3M", "r6M", "r12M",
        "annual_vol", "max_drawdown", "above_sma200",
        "recommendation", "rec_label", "momentum_filter_ok",
        "latest_price", "lookback_summary",
    ]
    return pd.DataFrame(signals, columns=cols).set_index("ticker")
