"""
Market data fetching: EODHD (primary) → Yahoo Finance (fallback) → Mock (offline).
Returns per-ticker DataFrames with a DatetimeIndex and a 'close' column.

Yahoo fetches all tickers in one batch call to avoid per-ticker rate limiting.
"""

from __future__ import annotations

import hashlib
import math
import time
from datetime import date, timedelta
from enum import Enum
from typing import Optional

import numpy as np
import pandas as pd
import requests
import yfinance as yf


class DataSource(str, Enum):
    EODHD = "EODHD"
    YAHOO = "Yahoo Finance"
    MOCK  = "Hors-ligne (démo)"


YAHOO_CHUNK = 100  # tickers per batch request

SOURCE_MOCK = "mock"
SOURCE_YAHOO = "yahoo"
SOURCE_EODHD = "eodhd"


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_all(
    tickers: list[str],
    source: DataSource,
    api_key: str = "",
    years: int = 2,
) -> dict[str, pd.DataFrame]:
    """
    Fetch historical close prices for every ticker.
    Returns {ticker: DataFrame(index=date, columns=['close'])}.
    Silently drops tickers that fail to load.
    """
    return {ticker: df for ticker, (df, _) in fetch_all_with_sources(tickers, source, api_key, years).items()}


def fetch_all_with_sources(
    tickers: list[str],
    source: DataSource,
    api_key: str = "",
    years: int = 2,
) -> dict[str, tuple[pd.DataFrame, str]]:
    """
    Fetch historical close prices and keep the actual source used per ticker.
    Returns {ticker: (DataFrame(index=date, columns=['close']), source_key)}.
    """
    if source == DataSource.MOCK:
        return {t: (_mock(t, years * 252), SOURCE_MOCK) for t in tickers}

    if source == DataSource.EODHD:
        return _fetch_all_eodhd_with_sources(tickers, api_key, years)

    # Yahoo (default)
    return {
        ticker: (df, SOURCE_YAHOO)
        for ticker, df in _fetch_all_yahoo(tickers, years).items()
    }


def invalidate_cache(*_: object) -> None:
    pass  # cache now handled by SQLite in api/db.py


# ── Yahoo batch ───────────────────────────────────────────────────────────────

def _fetch_all_yahoo(tickers: list[str], years: int) -> dict[str, pd.DataFrame]:
    period_map = {1: "1y", 2: "2y", 3: "3y", 5: "5y"}
    period = period_map.get(years, "2y")
    results: dict[str, pd.DataFrame] = {}

    for i in range(0, len(tickers), YAHOO_CHUNK):
        chunk = tickers[i : i + YAHOO_CHUNK]
        try:
            raw = yf.download(chunk, period=period, auto_adjust=True, progress=False, threads=True)
            if raw.empty:
                continue

            if isinstance(raw.columns, pd.MultiIndex):
                # Multiple tickers → MultiIndex columns (field, ticker)
                close_key = "Close" if "Close" in raw.columns.get_level_values(0) else "Adj Close"
                close = raw[close_key]
                for t in chunk:
                    if t in close.columns:
                        s = close[t].dropna()
                        if len(s) >= 20:
                            df = s.to_frame("close")
                            df.index = pd.to_datetime(df.index).tz_localize(None)
                            results[t] = df
            else:
                # Single ticker in chunk
                t = chunk[0]
                col = "Close" if "Close" in raw.columns else "Adj Close"
                s = raw[col].dropna()
                if len(s) >= 20:
                    df = s.to_frame("close")
                    df.index = pd.to_datetime(df.index).tz_localize(None)
                    results[t] = df

        except Exception:
            pass

        if i + YAHOO_CHUNK < len(tickers):
            time.sleep(1)  # be gentle between chunks

    return results


# ── EODHD individual + Yahoo fallback ─────────────────────────────────────────

def _fetch_all_eodhd(tickers: list[str], api_key: str, years: int) -> dict[str, pd.DataFrame]:
    return {ticker: df for ticker, (df, _) in _fetch_all_eodhd_with_sources(tickers, api_key, years).items()}


def _fetch_all_eodhd_with_sources(
    tickers: list[str],
    api_key: str,
    years: int,
) -> dict[str, tuple[pd.DataFrame, str]]:
    if not api_key or api_key == "demo":
        return {
            ticker: (df, SOURCE_YAHOO)
            for ticker, df in _fetch_all_yahoo(tickers, years).items()
        }

    results: dict[str, tuple[pd.DataFrame, str]] = {}
    quota_exceeded = False

    for ticker in tickers:
        if quota_exceeded:
            break

        df, exceeded = _eodhd_one(ticker, api_key, years)
        if exceeded:
            quota_exceeded = True
            break
        if df is not None:
            results[ticker] = (df, SOURCE_EODHD)

    # Remaining tickers (quota hit or not fetched) → Yahoo batch
    remaining = [t for t in tickers if t not in results]
    if remaining:
        yahoo_results = _fetch_all_yahoo(remaining, years)
        results.update({
            ticker: (df, SOURCE_YAHOO)
            for ticker, df in yahoo_results.items()
        })

    return results


def _eodhd_one(ticker: str, api_key: str, years: int) -> tuple[Optional[pd.DataFrame], bool]:
    """Returns (df_or_None, quota_exceeded)."""
    from_date = (date.today() - timedelta(days=years * 365 + 30)).isoformat()
    url = (
        f"https://eodhd.com/api/eod/{ticker}"
        f"?from={from_date}&period=d&api_token={api_key}&fmt=json"
    )
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 402:
            return None, True  # quota exceeded → switch to Yahoo
        if resp.status_code != 200:
            return None, False
        data = resp.json()
        if not data or not isinstance(data, list):
            return None, False
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        price_col = "adjusted_close" if "adjusted_close" in df.columns else "close"
        df = df[[price_col]].rename(columns={price_col: "close"})
        return df.dropna(), False
    except Exception:
        return None, False


# ── Mock ──────────────────────────────────────────────────────────────────────

def _mock(ticker: str, n_days: int = 504) -> pd.DataFrame:
    seed = int(hashlib.md5(ticker.encode()).hexdigest()[:8], 16) % (2**31)
    rng = np.random.default_rng(seed)
    start_price = 80 + (seed % 120)
    drift = 0.00035
    vol = 0.010 + (seed % 7) * 0.0015
    t = np.arange(n_days)
    cycle = 0.12 * np.sin(2 * math.pi * t / 252 + seed % 6)
    noise = rng.normal(drift, vol, n_days).cumsum()
    prices = start_price * np.exp(noise + cycle * 0.05)
    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=n_days,
        freq="B",
    )
    return pd.DataFrame({"close": prices}, index=dates)
