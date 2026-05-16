"""
Financial news via EODHD — cached 30 min in memory.
GET /api/news            → general market news (no ticker filter)
GET /api/news/{ticker}   → news for a Sleeve A ETF (mapped to US benchmark)
"""
from __future__ import annotations

import os
import time
from datetime import date, timedelta
from pathlib import Path

import requests
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["news"])

_cache: dict[str, tuple[list, float]] = {}
CACHE_TTL = 1800  # 30 min

# Sleeve A ETF → US benchmark ticker for news lookup
SLEEVE_A_NEWS_MAP: dict[str, str] = {
    "IUIT": "XLK.US",
    "IUFS": "XLF.US",
    "IUES": "XLE.US",
    "IUHC": "XLV.US",
    "IUCD": "XLY.US",
    "IUIS": "XLI.US",
    "IUCS": "XLP.US",
    "IUUS": "XLU.US",
    "IUMS": "XLB.US",
    "IURE": "XLRE.US",
    "IUCM": "XLC.US",
    "IWDA": "SPY.US",
    "EIMI": "EEM.US",
    "SJPA": "EWJ.US",
    "CEU":  "IEV.US",
    "NDIA": "INDA.US",
    "IUSM": "IJR.US",
    "IS3R": "MTUM.US",
    "IWQU": "QUAL.US",
    "SEMI": "SOXX.US",
    "WBIO": "IBB.US",
    "SGLD": "GLD.US",
    "XEON": "SHY.US",
}


def _api_key() -> str:
    if os.environ.get("EODHD_API_KEY"):
        return os.environ["EODHD_API_KEY"]
    env_path = Path(__file__).resolve().parents[2] / ".env"
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


def _fetch_news(ticker: str | None, limit: int, offset: int = 0) -> list[dict]:
    cache_key = f"{ticker or '__general__'}:{limit}:{offset}"
    now = time.time()
    if cache_key in _cache:
        articles, ts = _cache[cache_key]
        if now - ts < CACHE_TTL:
            return articles

    api_key = _api_key()
    if not api_key:
        return []

    params: dict = {"api_token": api_key, "limit": limit, "offset": offset, "fmt": "json"}
    if ticker:
        params["s"] = ticker

    try:
        resp = requests.get("https://eodhd.com/api/news", params=params, timeout=15)
        if resp.status_code != 200:
            return []
        raw: list[dict] = resp.json()
        if not isinstance(raw, list):
            return []

        articles = [_normalize(a) for a in raw]
        _cache[cache_key] = (articles, now)
        return articles
    except Exception:
        return []


def _sentiment_label(polarity: float | None) -> str:
    if polarity is None:
        return "neutral"
    if polarity > 0.1:
        return "positive"
    if polarity < -0.1:
        return "negative"
    return "neutral"


def _normalize(raw: dict) -> dict:
    sentiment = raw.get("sentiment") or {}
    polarity = sentiment.get("polarity")
    return {
        "date": raw.get("date", ""),
        "title": raw.get("title", ""),
        "content": (raw.get("content") or "")[:300].strip(),
        "link": raw.get("link", ""),
        "symbols": (raw.get("symbols") or [])[:8],
        "tags": [t for t in (raw.get("tags") or []) if len(t) < 30][:6],
        "sentiment": {
            "polarity": round(polarity, 3) if polarity is not None else None,
            "label": _sentiment_label(polarity),
        },
    }


@router.get("/news")
def get_market_news(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """General market news feed — no ticker filter. Supports pagination via offset."""
    articles = _fetch_news(None, limit, offset)
    return {"articles": articles, "source": "general", "cached_at": time.time()}


@router.get("/news/{ticker}")
def get_ticker_news(
    ticker: str,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    """News for a Sleeve A ETF, mapped to its US benchmark ticker for EODHD lookup."""
    ticker = ticker.upper()
    us_ticker = SLEEVE_A_NEWS_MAP.get(ticker)
    if not us_ticker:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not in Sleeve A universe")

    articles = _fetch_news(us_ticker, limit, offset)
    return {
        "articles": articles,
        "source": ticker,
        "us_benchmark": us_ticker,
        "cached_at": time.time(),
    }