"""
Portfolio persistence — holdings + settings stored in data/portfolio.json.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

STORE_PATH = Path(__file__).parent.parent / "data" / "portfolio.json"

DEFAULT_SETTINGS = {
    "broker_name":   "Boursobank PEA",
    "data_source":   "Yahoo Finance",
    "eodhd_api_key": "69ecfa7ed81d63.29086352",
    "capital":       10_000.0,
    "top_n":         5,
    "currency":      "EUR",
    "history_years": 2,
}


def load() -> dict:
    if STORE_PATH.exists():
        try:
            return json.loads(STORE_PATH.read_text())
        except Exception:
            pass
    return {"settings": DEFAULT_SETTINGS.copy(), "holdings": []}


def save(doc: dict) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(doc, indent=2, default=str))


def get_settings(doc: dict) -> dict:
    s = DEFAULT_SETTINGS.copy()
    s.update(doc.get("settings", {}))
    return s


def get_holdings(doc: dict) -> list[dict]:
    return doc.get("holdings", [])


def upsert_holding(doc: dict, holding: dict) -> dict:
    holdings = get_holdings(doc)
    idx = next((i for i, h in enumerate(holdings) if h["ticker"] == holding["ticker"]), None)
    if idx is not None:
        holdings[idx] = holding
    else:
        holdings.append(holding)
    doc["holdings"] = holdings
    return doc


def delete_holding(doc: dict, ticker: str) -> dict:
    doc["holdings"] = [h for h in get_holdings(doc) if h["ticker"] != ticker]
    return doc


def enrich_holdings_with_prices(
    holdings: list[dict],
    histories: dict[str, "pd.DataFrame"],
) -> list[dict]:
    """Add market_value, pnl, pnl_pct, day_change to each holding."""
    import math
    enriched = []
    for h in holdings:
        h = h.copy()
        t = h["ticker"]
        if t in histories and len(histories[t]) >= 1:
            hist = histories[t]
            price = float(hist["close"].iloc[-1])
            prev  = float(hist["close"].iloc[-2]) if len(hist) >= 2 else price
            h["latest_price"] = price
            h["market_value"] = price * h["quantity"]
            h["cost_basis"]   = h["avg_cost"] * h["quantity"]
            h["pnl"]          = h["market_value"] - h["cost_basis"]
            h["pnl_pct"]      = (h["pnl"] / h["cost_basis"]) if h["cost_basis"] else 0.0
            h["day_change"]   = (price - prev) / prev if prev else 0.0
        else:
            h["latest_price"] = None
            h["market_value"] = h["avg_cost"] * h["quantity"]
            h["cost_basis"]   = h["avg_cost"] * h["quantity"]
            h["pnl"]          = 0.0
            h["pnl_pct"]      = 0.0
            h["day_change"]   = 0.0
        enriched.append(h)

    total_mv = sum(h["market_value"] for h in enriched)
    for h in enriched:
        h["allocation_pct"] = h["market_value"] / total_mv if total_mv > 0 else 0.0

    return enriched
