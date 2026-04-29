from fastapi import APIRouter
import api.db as db
import api.core as core

router = APIRouter(tags=["signals"])


@router.get("/signals")
def get_signals():
    """Compute signals for all 111 ETFs. Prices served from SQLite cache (12 h TTL)."""
    return core.compute_signals(db.get_settings())
