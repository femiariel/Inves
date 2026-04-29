from fastapi import APIRouter
import api.db as db
import api.core as core
from data.pea_universe import CORE_ANCHOR
from portfolio.optimizer import build_proposal, build_rebalance_orders

router = APIRouter(tags=["proposal"])


@router.get("/proposal")
def get_proposal():
    settings = db.get_settings()
    capital  = float(settings.get("capital", 10_000))
    top_n    = int(settings.get("top_n", 5))

    signals  = core.compute_signals(settings)
    proposal = build_proposal(signals, capital, CORE_ANCHOR, top_n)

    holdings = db.get_holdings()
    orders   = build_rebalance_orders(holdings, proposal) if holdings else []

    return {
        "proposal": {
            **proposal,
            "expected_return": round(proposal["expected_return"], 4),
            "expected_vol":    round(proposal["expected_vol"], 4),
            "expected_sharpe": round(proposal["expected_sharpe"], 4),
        },
        "orders": orders,
    }
