from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import api.db as db

router = APIRouter(tags=["settings"])


class SettingsIn(BaseModel):
    data_source:   Optional[str]   = None
    eodhd_api_key: Optional[str]   = None
    capital:       Optional[float] = None
    top_n:         Optional[int]   = None
    history_years: Optional[int]   = None


@router.get("/settings")
def get_settings():
    return db.get_settings()


@router.put("/settings")
def update_settings(body: SettingsIn):
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    return db.set_settings(updates)


@router.post("/cache/clear")
def clear_cache():
    db.clear_cache()
    return {"ok": True, "message": "Cache vidé — prochain appel rechargera les prix"}
