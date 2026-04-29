from fastapi import APIRouter
from data.pea_universe import PEA_UNIVERSE, get_categories

router = APIRouter(tags=["universe"])


@router.get("/universe")
def list_universe():
    return [{"ticker": t, **m} for t, m in PEA_UNIVERSE.items()]


@router.get("/universe/categories")
def list_categories():
    return get_categories()
