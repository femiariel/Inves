"""
Sleeve A — Cross-Sectional Momentum with Absolute Trend Filter.

Engine rules (immutable by design):
  Regime filter : IWDA price >= SMA(200)  → ON ; below → OFF
  Signal        : 6-month (126 trading days) total return, cross-sectional rank
  Selection     : Top-2 by 6M return, correlation guardrail (abs corr > threshold skips candidate)
  Allocation    : Regime ON → 50% / 50% on selected pair ; Regime OFF → 100% XEON
  Rebalancing   : Monthly, last trading day of month
"""
from __future__ import annotations

import math
import time
from datetime import date, timedelta
from typing import Optional

import pandas as pd
import requests

import api.db as db
from data.sleeve_a_universe import (
    ACTIVE_TICKERS,
    DEFENSIVE_TICKER,
    ETF_UNIVERSE,
    REGIME_FILTER_TICKER,
    get_eodhd_symbol,
)

LOOKBACK_MOMENTUM = 126   # 6 months in trading days
LOOKBACK_CORR = 126       # correlation window
CORR_THRESHOLD = 0.80     # skip candidate if abs(corr) > threshold with any selected ETF
TOP_N = 2                 # max positions in regime ON
MIN_HISTORY = 130         # minimum rows needed to compute a valid signal

_fetch_cache: dict[str, tuple[pd.DataFrame, float]] = {}
_CACHE_TTL = 3600


# ── Data loading ──────────────────────────────────────────────────────────────

def _env_api_key() -> str:
    import os
    from pathlib import Path
    if os.environ.get("EODHD_API_KEY"):
        return os.environ["EODHD_API_KEY"]
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == "EODHD_API_KEY":
            return v.strip().strip('"').strip("'")
    return ""


def _fetch_eodhd(eodhd_symbol: str, years: int = 3) -> pd.DataFrame | None:
    cache_key = eodhd_symbol
    now = time.time()
    if cache_key in _fetch_cache:
        df, ts = _fetch_cache[cache_key]
        if now - ts < _CACHE_TTL:
            return df

    api_key = _env_api_key()
    if not api_key or api_key == "demo":
        return None

    from_date = (date.today() - timedelta(days=years * 365 + 30)).isoformat()
    try:
        resp = requests.get(
            f"https://eodhd.com/api/eod/{eodhd_symbol}",
            params={"from": from_date, "period": "d", "api_token": api_key, "fmt": "json"},
            timeout=15,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data or not isinstance(data, list):
            return None
        raw = pd.DataFrame(data)
        if "date" not in raw.columns:
            return None
        price_col = "adjusted_close" if "adjusted_close" in raw.columns else "close"
        if price_col not in raw.columns:
            return None
        raw["date"] = pd.to_datetime(raw["date"])
        df = raw.set_index("date").sort_index()[[price_col]].rename(columns={price_col: "close"})
        df = df.dropna()
        if df.empty:
            return None
        _fetch_cache[cache_key] = (df, now)
        return df
    except Exception:
        return None


def load_histories() -> dict[str, pd.DataFrame]:
    """
    Load prices for all Sleeve A tickers.
    Priority: SQLite cache (populated by fetch script) → live EODHD fetch.
    """
    histories: dict[str, pd.DataFrame] = {}

    for ticker in ETF_UNIVERSE:
        # Try SQLite first (keyed by the short ticker)
        df = db.load_prices(ticker)
        if df is not None and len(df) >= MIN_HISTORY:
            histories[ticker] = df
            continue

        # Try SQLite with the EODHD symbol key (e.g. "IUIT.LSE")
        eodhd_sym = get_eodhd_symbol(ticker)
        df = db.load_prices(eodhd_sym)
        if df is not None and len(df) >= MIN_HISTORY:
            histories[ticker] = df
            continue

        # Live fetch as fallback (cached in-process 1h)
        df = _fetch_eodhd(eodhd_sym)
        if df is not None and len(df) >= MIN_HISTORY:
            histories[ticker] = df

    return histories


# ── Core computations ─────────────────────────────────────────────────────────

def get_regime(histories: dict[str, pd.DataFrame]) -> dict:
    """
    IWDA vs its 200-day SMA.
    Returns a dict with regime status and raw values.
    """
    out = {
        "regime": "unknown",
        "filter_ticker": REGIME_FILTER_TICKER,
        "price": None,
        "sma200": None,
        "ratio": None,
        "data_available": False,
    }

    df = histories.get(REGIME_FILTER_TICKER)
    if df is None or len(df) < 201:
        return out

    prices = df["close"]
    price = float(prices.iloc[-1])
    sma200 = float(prices.tail(200).mean())
    ratio = price / sma200

    out.update({
        "data_available": True,
        "price": round(price, 4),
        "sma200": round(sma200, 4),
        "ratio": round(ratio, 4),
        "regime": "on" if price >= sma200 else "off",
    })
    return out


def compute_signals(histories: dict[str, pd.DataFrame]) -> list[dict]:
    """
    6-month total return for each of the 22 active ETFs.
    Returns a list sorted by mom_6m descending (nulls last).
    """
    results: list[dict] = []
    meta = {t: ETF_UNIVERSE[t] for t in ACTIVE_TICKERS}

    for ticker in ACTIVE_TICKERS:
        entry = meta[ticker]
        df = histories.get(ticker)

        if df is None or len(df) < MIN_HISTORY:
            results.append({
                "ticker": ticker,
                "name": entry["name"],
                "category": entry["category"],
                "mom_6m": None,
                "latest_price": None,
                "data_available": False,
                "rank": None,
            })
            continue

        prices = df["close"]
        latest = float(prices.iloc[-1])

        if len(prices) >= LOOKBACK_MOMENTUM + 1:
            price_126d_ago = float(prices.iloc[-(LOOKBACK_MOMENTUM + 1)])
            mom_6m = (latest / price_126d_ago - 1) if price_126d_ago > 0 else None
        else:
            mom_6m = None

        results.append({
            "ticker": ticker,
            "name": entry["name"],
            "category": entry["category"],
            "mom_6m": round(mom_6m * 100, 2) if mom_6m is not None else None,
            "latest_price": round(latest, 4),
            "data_available": True,
            "rank": None,
        })

    # Assign ranks (only ETFs with valid momentum)
    valid = sorted(
        [r for r in results if r["mom_6m"] is not None],
        key=lambda x: x["mom_6m"],
        reverse=True,
    )
    for i, r in enumerate(valid, start=1):
        r["rank"] = i

    return sorted(results, key=lambda x: (x["mom_6m"] is None, -(x["mom_6m"] or 0)))


def select_top2(
    signals: list[dict],
    histories: dict[str, pd.DataFrame],
    corr_threshold: float = CORR_THRESHOLD,
    lookback: int = LOOKBACK_CORR,
) -> list[dict]:
    """
    Greedy top-N selection with correlation guardrail.
    Iterates ranked candidates; skips any whose abs correlation to an
    already-selected ETF exceeds corr_threshold over the last `lookback` days.
    Returns at most TOP_N entries (list of signal dicts).
    """
    ranked = [r for r in signals if r["mom_6m"] is not None]
    # Already sorted descending by compute_signals, but be explicit
    ranked = sorted(ranked, key=lambda x: x["mom_6m"], reverse=True)

    selected: list[dict] = []
    selected_tickers: list[str] = []

    for candidate in ranked:
        if len(selected) >= TOP_N:
            break

        ticker = candidate["ticker"]

        if not selected_tickers:
            selected.append(candidate)
            selected_tickers.append(ticker)
            continue

        # Correlation check vs every already-selected ETF
        df_c = histories.get(ticker)
        if df_c is None:
            continue

        ret_c = df_c["close"].pct_change().dropna()
        too_correlated = False

        for sel_ticker in selected_tickers:
            df_s = histories.get(sel_ticker)
            if df_s is None:
                continue
            ret_s = df_s["close"].pct_change().dropna()
            common_idx = ret_c.index.intersection(ret_s.index)
            if len(common_idx) > 20:
                window = common_idx[-lookback:]
                corr = abs(ret_c.loc[window].corr(ret_s.loc[window]))
                if not math.isnan(corr) and corr > corr_threshold:
                    too_correlated = True
                    break

        if not too_correlated:
            selected.append(candidate)
            selected_tickers.append(ticker)

    return selected


def build_allocation(
    regime: dict,
    selected: list[dict],
    histories: dict[str, pd.DataFrame],
    corr_threshold: float = CORR_THRESHOLD,
) -> dict:
    """
    Regime ON  → 50/50 on selected pair (or 100% if only one passes corr guard).
    Regime OFF → 100% XEON.
    """
    def _corr_matrix(tickers: list[str]) -> list[dict]:
        rows: list[dict] = []
        for t1 in tickers:
            for t2 in tickers:
                if t1 >= t2:
                    continue
                df1 = histories.get(t1)
                df2 = histories.get(t2)
                if df1 is None or df2 is None:
                    continue
                r1 = df1["close"].pct_change().dropna()
                r2 = df2["close"].pct_change().dropna()
                common = r1.index.intersection(r2.index)[-LOOKBACK_CORR:]
                if len(common) > 20:
                    corr = float(r1.loc[common].corr(r2.loc[common]))
                    if not math.isnan(corr):
                        rows.append({"t1": t1, "t2": t2, "corr": round(corr, 3)})
        return rows

    if regime["regime"] == "off" or not selected:
        xeon_meta = ETF_UNIVERSE[DEFENSIVE_TICKER]
        df_xeon = histories.get(DEFENSIVE_TICKER)
        xeon_price = float(df_xeon["close"].iloc[-1]) if df_xeon is not None and len(df_xeon) > 0 else None
        return {
            "regime": regime,
            "positions": [{
                "ticker": DEFENSIVE_TICKER,
                "name": xeon_meta["name"],
                "category": xeon_meta["category"],
                "weight": 1.0,
                "rationale": "Régime OFF — IWDA sous SMA200. Fuite vers le monétaire XEON.",
                "latest_price": xeon_price,
            }],
            "corr_pairs": [],
            "guardrail_applied": False,
        }

    weight = 1.0 / len(selected)
    positions = []
    for sig in selected:
        positions.append({
            "ticker": sig["ticker"],
            "name": sig["name"],
            "category": sig["category"],
            "weight": round(weight, 4),
            "mom_6m": sig["mom_6m"],
            "rank": sig["rank"],
            "rationale": f"Top-{sig['rank']} momentum 6M ({sig['mom_6m']:+.1f}%)",
            "latest_price": sig["latest_price"],
        })

    selected_tickers = [s["ticker"] for s in selected]
    guardrail_applied = len(selected) < min(TOP_N, len([r for r in [] if r]))

    return {
        "regime": regime,
        "positions": positions,
        "corr_pairs": _corr_matrix(selected_tickers),
        "guardrail_applied": guardrail_applied,
        "corr_threshold": corr_threshold,
    }


# ── Top-level entrypoint ──────────────────────────────────────────────────────

def compute_sleeve_a(corr_threshold: float = CORR_THRESHOLD) -> dict:
    """Full Sleeve A computation: load → regime → signals → selection → allocation."""
    histories = load_histories()

    regime = get_regime(histories)
    signals = compute_signals(histories)

    if regime["regime"] == "on":
        selected = select_top2(signals, histories, corr_threshold=corr_threshold)
    else:
        selected = []

    allocation = build_allocation(regime, selected, histories, corr_threshold=corr_threshold)

    available_count = sum(1 for s in signals if s["data_available"])

    return {
        "regime": regime,
        "signals": signals,
        "allocation": allocation,
        "data_coverage": {
            "available": available_count,
            "total": len(ACTIVE_TICKERS),
        },
        "computed_at": time.time(),
    }