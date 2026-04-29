"""
Shared business logic: price loading + signal computation.
Keeps routes thin — just HTTP concerns.
"""
from __future__ import annotations

import math

import api.db as db
from data.market_data import DataSource, fetch_all
from data.pea_universe import get_all_tickers, get_etf_metadata
from strategy.factors import build_all_signals


def _source(s: str) -> DataSource:
    return {
        "eodhd": DataSource.EODHD,
        "yahoo": DataSource.YAHOO,
    }.get(s.lower(), DataSource.MOCK)


def load_histories(settings: dict) -> dict:
    """
    Return {ticker: DataFrame} for the full universe.
    Uses SQLite price cache (12 h TTL); fetches missing / stale tickers.
    """
    source_str = settings.get("data_source", "mock")
    source     = _source(source_str)
    api_key    = settings.get("eodhd_api_key", "")
    years      = int(settings.get("history_years", 2))

    tickers    = get_all_tickers()
    histories: dict = {}
    to_fetch:  list = []

    for ticker in tickers:
        if db.is_cache_fresh(ticker, source_str):
            df = db.load_prices(ticker)
            if df is not None and len(df) >= 20:
                histories[ticker] = df
                continue
        to_fetch.append(ticker)

    if to_fetch:
        fresh = fetch_all(to_fetch, source, api_key, years, use_cache=False)
        for ticker, df in fresh.items():
            db.save_prices(ticker, df, source_str)
            histories[ticker] = df

    return histories


def compute_signals(settings: dict) -> list[dict]:
    """Load histories, compute signals, replace NaN with None for JSON."""
    histories = load_histories(settings)
    meta      = get_etf_metadata()
    raw       = build_all_signals(histories, meta)
    return [
        {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in s.items()}
        for s in raw
    ]
