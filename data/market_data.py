"""
Market data fetching: EODHD only.
Returns per-ticker DataFrames with a DatetimeIndex and a 'close' column.

A failed ticker is left missing after retries rather than silently mixing
providers.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from typing import Optional

import pandas as pd
import requests


class DataSource(str, Enum):
    EODHD = "EODHD"


EODHD_MAX_ATTEMPTS = 3
EODHD_RETRY_SLEEP = 1.0

SOURCE_EODHD = "eodhd"

EODHD_OK = "ok"
EODHD_RETRYABLE_FAILURE = "retryable_failure"
EODHD_NO_DATA = "no_data"
EODHD_AUTH_ERROR = "auth_error"
EODHD_QUOTA_EXCEEDED = "quota_exceeded"


@dataclass(frozen=True)
class EodhdAttempt:
    df: Optional[pd.DataFrame]
    status: str
    message: str = ""


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_all(
    tickers: list[str],
    source: DataSource,
    api_key: str = "",
    years: int = 2,
    progress: Optional[Callable[[dict], None]] = None,
) -> dict[str, pd.DataFrame]:
    """
    Fetch historical close prices for every ticker.
    Returns {ticker: DataFrame(index=date, columns=['close'])}.
    Silently drops tickers that fail to load.
    """
    return {
        ticker: df
        for ticker, (df, _) in fetch_all_with_sources(
            tickers, source, api_key, years, progress=progress
        ).items()
    }


def fetch_all_with_sources(
    tickers: list[str],
    source: DataSource,
    api_key: str = "",
    years: int = 2,
    progress: Optional[Callable[[dict], None]] = None,
) -> dict[str, tuple[pd.DataFrame, str]]:
    """
    Fetch historical close prices and keep the actual source used per ticker.
    Returns {ticker: (DataFrame(index=date, columns=['close']), source_key)}.
    """
    if source == DataSource.EODHD:
        return _fetch_all_eodhd_with_sources(tickers, api_key, years, progress=progress)

    raise ValueError("Only EODHD market data is supported.")


def invalidate_cache(*_: object) -> None:
    pass  # cache now handled by SQLite in api/db.py


# ── EODHD individual ──────────────────────────────────────────────────────────

def _fetch_all_eodhd(
    tickers: list[str],
    api_key: str,
    years: int,
    progress: Optional[Callable[[dict], None]] = None,
) -> dict[str, pd.DataFrame]:
    return {
        ticker: df
        for ticker, (df, _) in _fetch_all_eodhd_with_sources(
            tickers, api_key, years, progress=progress
        ).items()
    }


def _fetch_all_eodhd_with_sources(
    tickers: list[str],
    api_key: str,
    years: int,
    progress: Optional[Callable[[dict], None]] = None,
) -> dict[str, tuple[pd.DataFrame, str]]:
    if not api_key or api_key == "demo":
        raise ValueError("EODHD API key is required when source=eodhd.")

    results: dict[str, tuple[pd.DataFrame, str]] = {}

    total = len(tickers)
    for index, ticker in enumerate(tickers, start=1):
        df, status, attempts = _eodhd_one_with_retries(ticker, api_key, years)
        if df is not None:
            results[ticker] = (df, SOURCE_EODHD)
            if progress:
                progress({
                    "index": index,
                    "total": total,
                    "ticker": ticker,
                    "status": EODHD_OK,
                    "attempts": attempts,
                    "rows": len(df),
                })
            continue

        if progress:
            progress({
                "index": index,
                "total": total,
                "ticker": ticker,
                "status": status,
                "attempts": attempts,
                "rows": 0,
            })

        if status in {EODHD_AUTH_ERROR, EODHD_QUOTA_EXCEEDED}:
            break

    return results


def _eodhd_one_with_retries(
    ticker: str,
    api_key: str,
    years: int,
    max_attempts: int = EODHD_MAX_ATTEMPTS,
) -> tuple[Optional[pd.DataFrame], str, int]:
    """Returns (df_or_None, final_status, attempts_used)."""
    last_status = EODHD_RETRYABLE_FAILURE
    for attempt in range(1, max_attempts + 1):
        result = _eodhd_one_attempt(ticker, api_key, years)
        last_status = result.status

        if result.status == EODHD_OK:
            return result.df, EODHD_OK, attempt

        if result.status in {EODHD_AUTH_ERROR, EODHD_QUOTA_EXCEEDED, EODHD_NO_DATA}:
            return None, result.status, attempt

        if attempt < max_attempts:
            time.sleep(EODHD_RETRY_SLEEP * attempt)

    return None, last_status, max_attempts


def _eodhd_one_attempt(ticker: str, api_key: str, years: int) -> EodhdAttempt:
    """One EODHD request. Retry decisions are handled by _eodhd_one_with_retries."""
    from_date = (date.today() - timedelta(days=years * 365 + 30)).isoformat()
    url = (
        f"https://eodhd.com/api/eod/{ticker}"
        f"?from={from_date}&period=d&api_token={api_key}&fmt=json"
    )
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code in {401, 403}:
            return EodhdAttempt(None, EODHD_AUTH_ERROR, f"auth failed ({resp.status_code})")
        if resp.status_code == 402:
            return EodhdAttempt(None, EODHD_QUOTA_EXCEEDED, "quota exceeded")
        if resp.status_code == 404:
            return EodhdAttempt(None, EODHD_NO_DATA, "symbol not found")
        if resp.status_code == 429 or resp.status_code >= 500:
            return EodhdAttempt(None, EODHD_RETRYABLE_FAILURE, f"http {resp.status_code}")
        if resp.status_code != 200:
            return EodhdAttempt(None, EODHD_NO_DATA, f"http {resp.status_code}")

        data = resp.json()
        if not data or not isinstance(data, list):
            return EodhdAttempt(None, EODHD_NO_DATA, "empty response")
        df = pd.DataFrame(data)
        if "date" not in df.columns:
            return EodhdAttempt(None, EODHD_NO_DATA, "missing date column")
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        price_col = "adjusted_close" if "adjusted_close" in df.columns else "close"
        if price_col not in df.columns:
            return EodhdAttempt(None, EODHD_NO_DATA, "missing price column")
        df = df[[price_col]].rename(columns={price_col: "close"})
        df = df.dropna()
        if df.empty:
            return EodhdAttempt(None, EODHD_NO_DATA, "no usable prices")
        return EodhdAttempt(df, EODHD_OK)
    except requests.RequestException as exc:
        return EodhdAttempt(None, EODHD_RETRYABLE_FAILURE, str(exc))
    except ValueError as exc:
        return EodhdAttempt(None, EODHD_NO_DATA, str(exc))
