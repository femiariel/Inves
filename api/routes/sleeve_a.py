from fastapi import APIRouter, Query
from strategy.sleeve_a import compute_sleeve_a, CORR_THRESHOLD

router = APIRouter(tags=["sleeve_a"])


@router.get("/sleeve-a")
def get_sleeve_a(
    corr_threshold: float = Query(default=CORR_THRESHOLD, ge=0.0, le=1.0),
):
    """
    Full Sleeve A snapshot: regime status, signals (22 ETFs ranked by 6M momentum),
    and allocation (top-2 with correlation guardrail, or 100% XEON if regime OFF).
    """
    return compute_sleeve_a(corr_threshold=corr_threshold)