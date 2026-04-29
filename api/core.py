"""
Shared business logic: price loading + signal computation.
Keeps routes thin — just HTTP concerns.
"""
from __future__ import annotations

import math

import pandas as pd
import api.db as db
from data.pea_universe import get_all_tickers, get_etf_metadata
from strategy.factors import build_all_signals


def load_histories(settings: dict | None = None) -> dict:
    """
    Return {ticker: DataFrame} for the full universe from SQLite only.
    Market downloads are intentionally handled by scripts/fetch_market_data.py.
    """
    tickers    = get_all_tickers()
    histories: dict = {}

    for ticker in tickers:
        df = db.load_prices(ticker)
        if df is not None and len(df) >= 20:
            histories[ticker] = df

    return histories


def compute_signals(settings: dict) -> list[dict]:
    """Load histories, compute signals, replace non-finite floats for JSON."""
    histories = load_histories(settings)
    meta_list = get_etf_metadata()
    meta      = pd.DataFrame(meta_list).set_index("ticker")
    raw       = build_all_signals(histories, meta)

    def json_value(v):
        if isinstance(v, float) and not math.isfinite(v):
            return None
        return v

    return [
        {k: json_value(v) for k, v in s.items()}
        for s in raw
    ]
