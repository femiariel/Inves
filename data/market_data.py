"""
Market data fetching: EODHD (primary) → Yahoo Finance (fallback) → Mock (offline).
Returns per-ticker DataFrames with a DatetimeIndex and a 'close' column.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from datetime import date, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests
import yfinance as yf

CACHE_DIR = Path(__file__).parent / "price_cache"
CACHE_TTL_HOURS = 12


class DataSource(str, Enum):
    EODHD = "EODHD"
    YAHOO = "Yahoo Finance"
    MOCK  = "Hors-ligne (démo)"


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_all(
    tickers: list[str],
    source: DataSource,
    api_key: str = "",
    years: int = 2,
    use_cache: bool = True,
) -> dict[str, pd.DataFrame]:
    """
    Fetch historical close prices for every ticker.
    Returns {ticker: DataFrame(index=date, columns=['close'])}.
    Silently drops tickers that fail to load.
    """
    results: dict[str, pd.DataFrame] = {}
    for ticker in tickers:
        try:
            df = _fetch_one(ticker, source, api_key, years, use_cache)
            if df is not None and len(df) >= 20:
                results[ticker] = df
        except Exception:
            pass
    return results


def invalidate_cache(ticker: Optional[str] = None) -> None:
    if not CACHE_DIR.exists():
        return
    if ticker:
        p = CACHE_DIR / f"{ticker.replace('.', '_')}.json"
        if p.exists():
            p.unlink()
    else:
        for p in CACHE_DIR.glob("*.json"):
            p.unlink()


# ── Internal ──────────────────────────────────────────────────────────────────

def _fetch_one(
    ticker: str,
    source: DataSource,
    api_key: str,
    years: int,
    use_cache: bool,
) -> Optional[pd.DataFrame]:
    if use_cache:
        cached = _load_cache(ticker)
        if cached is not None:
            return cached

    if source == DataSource.MOCK:
        df = _mock(ticker, years * 252)
    elif source == DataSource.EODHD:
        df = _eodhd(ticker, api_key, years) or _yahoo(ticker, years) or _mock(ticker, years * 252)
    else:
        df = _yahoo(ticker, years) or _mock(ticker, years * 252)

    if df is not None and use_cache:
        _save_cache(ticker, df)
    return df


def _eodhd(ticker: str, api_key: str, years: int) -> Optional[pd.DataFrame]:
    if not api_key:
        return None
    from_date = (date.today() - timedelta(days=years * 365 + 30)).isoformat()
    url = (
        f"https://eodhd.com/api/eod/{ticker}"
        f"?from={from_date}&period=d&api_token={api_key}&fmt=json"
    )
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data or not isinstance(data, list):
            return None
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        price_col = "adjusted_close" if "adjusted_close" in df.columns else "close"
        df = df[[price_col]].rename(columns={price_col: "close"})
        return df.dropna()
    except Exception:
        return None


def _yahoo(ticker: str, years: int) -> Optional[pd.DataFrame]:
    period_map = {1: "1y", 2: "2y", 3: "3y", 5: "5y"}
    period = period_map.get(years, "2y")
    try:
        raw = yf.download(ticker, period=period, auto_adjust=True, progress=False, threads=False)
        if raw.empty:
            return None
        if isinstance(raw.columns, pd.MultiIndex):
            df = raw["Close"].to_frame("close")
        else:
            df = raw[["Close"]].rename(columns={"Close": "close"})
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df.dropna()
    except Exception:
        return None


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


# ── Cache helpers ─────────────────────────────────────────────────────────────

def _cache_path(ticker: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{ticker.replace('.', '_')}.json"


def _load_cache(ticker: str) -> Optional[pd.DataFrame]:
    p = _cache_path(ticker)
    if not p.exists():
        return None
    try:
        payload = json.loads(p.read_text())
        age_h = (time.time() - payload["ts"]) / 3600
        if age_h > CACHE_TTL_HOURS:
            return None
        df = pd.DataFrame(payload["data"])
        df.index = pd.to_datetime(df.index)
        df.index.name = "date"
        return df
    except Exception:
        return None


def _save_cache(ticker: str, df: pd.DataFrame) -> None:
    p = _cache_path(ticker)
    payload = {
        "ts": time.time(),
        "data": df.to_dict(orient="dict"),
    }
    p.write_text(json.dumps(payload))
