from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import api.db as db
from data.pea_universe import PEA_UNIVERSE

router = APIRouter(tags=["portfolio"])


class HoldingIn(BaseModel):
    ticker:   str
    quantity: float
    avg_cost: float


@router.get("/holdings")
def get_holdings():
    holdings = db.get_holdings()
    enriched = []

    for h in holdings:
        ticker = h["ticker"]
        df     = db.load_prices(ticker)
        if df is not None and len(df) >= 1:
            price = float(df["close"].iloc[-1])
            prev  = float(df["close"].iloc[-2]) if len(df) >= 2 else price
            h["latest_price"] = price
            h["market_value"] = price * h["quantity"]
            h["cost_basis"]   = h["avg_cost"] * h["quantity"]
            h["pnl"]          = h["market_value"] - h["cost_basis"]
            h["pnl_pct"]      = h["pnl"] / h["cost_basis"] if h["cost_basis"] else 0.0
            h["day_change"]   = (price - prev) / prev if prev else 0.0
        else:
            mv = h["avg_cost"] * h["quantity"]
            h["latest_price"] = None
            h["market_value"] = mv
            h["cost_basis"]   = mv
            h["pnl"]          = 0.0
            h["pnl_pct"]      = 0.0
            h["day_change"]   = 0.0
        enriched.append(h)

    total_mv = sum(h["market_value"] for h in enriched)
    for h in enriched:
        h["allocation_pct"] = h["market_value"] / total_mv if total_mv > 0 else 0.0

    return enriched


@router.post("/holdings", status_code=201)
def upsert_holding(body: HoldingIn):
    meta   = PEA_UNIVERSE.get(body.ticker, {})
    name   = meta.get("name", body.ticker)
    sleeve = meta.get("sleeve", "aggressive")
    return db.upsert_holding(body.ticker, name, body.quantity, body.avg_cost, sleeve)


@router.delete("/holdings/{ticker}")
def delete_holding(ticker: str):
    db.delete_holding(ticker)
    return {"ok": True}
