"""
SQLite persistence layer.
DB path: /app/data/alloc.db (mounted Docker volume → survives restarts).
"""
from __future__ import annotations

import os
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

DB_PATH = Path(os.environ.get("DB_PATH", Path(__file__).parent.parent / "data" / "alloc.db"))
CACHE_TTL = 12 * 3600  # 12 h

DEFAULT_SETTINGS: dict[str, str] = {
    "data_source":   "eodhd",
    "eodhd_api_key": "",
    "capital":       "10000",
    "top_n":         "5",
    "history_years": "2",
}


# ── Connection ─────────────────────────────────────────────────────────────────

def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def get_db():
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Schema ─────────────────────────────────────────────────────────────────────

def init_db() -> None:
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS price_cache (
                ticker  TEXT NOT NULL,
                date    TEXT NOT NULL,
                close   REAL NOT NULL,
                PRIMARY KEY (ticker, date)
            );
            CREATE TABLE IF NOT EXISTS cache_meta (
                ticker     TEXT PRIMARY KEY,
                last_fetch INTEGER NOT NULL,
                source     TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS holdings (
                ticker     TEXT PRIMARY KEY,
                name       TEXT NOT NULL,
                quantity   REAL NOT NULL,
                avg_cost   REAL NOT NULL,
                sleeve     TEXT NOT NULL DEFAULT 'aggressive',
                added_at   TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        """)
        for k, v in DEFAULT_SETTINGS.items():
            conn.execute(
                "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v)
            )


# ── Settings ───────────────────────────────────────────────────────────────────

def get_settings() -> dict[str, str]:
    with get_db() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    s = DEFAULT_SETTINGS.copy()
    s.update({r["key"]: r["value"] for r in rows})
    return s


def set_settings(updates: dict) -> dict[str, str]:
    with get_db() as conn:
        for k, v in updates.items():
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (k, str(v)),
            )
    return get_settings()


# ── Price cache ────────────────────────────────────────────────────────────────

def is_cache_fresh(ticker: str, source: str) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT last_fetch, source FROM cache_meta WHERE ticker = ?", (ticker,)
        ).fetchone()
    if row is None:
        return False
    if row["source"] != source:
        return False
    return (time.time() - row["last_fetch"]) < CACHE_TTL


def load_prices(ticker: str) -> pd.DataFrame | None:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT date, close FROM price_cache WHERE ticker = ? ORDER BY date",
            (ticker,),
        ).fetchall()
    if not rows:
        return None
    df = pd.DataFrame(rows, columns=["date", "close"])
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")


def save_prices(ticker: str, df: pd.DataFrame, source: str) -> None:
    rows = [
        (ticker, str(idx.date()), float(c))
        for idx, c in df["close"].items()
    ]
    with get_db() as conn:
        conn.execute("DELETE FROM price_cache WHERE ticker = ?", (ticker,))
        conn.executemany(
            "INSERT OR REPLACE INTO price_cache (ticker, date, close) VALUES (?, ?, ?)",
            rows,
        )
        conn.execute(
            "INSERT OR REPLACE INTO cache_meta (ticker, last_fetch, source) VALUES (?, ?, ?)",
            (ticker, int(time.time()), source),
        )


def clear_cache(ticker: str | None = None) -> None:
    with get_db() as conn:
        if ticker:
            conn.execute("DELETE FROM price_cache WHERE ticker = ?", (ticker,))
            conn.execute("DELETE FROM cache_meta  WHERE ticker = ?", (ticker,))
        else:
            conn.execute("DELETE FROM price_cache")
            conn.execute("DELETE FROM cache_meta")


# ── Holdings ───────────────────────────────────────────────────────────────────

def get_holdings() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM holdings ORDER BY ticker").fetchall()
    return [dict(r) for r in rows]


def upsert_holding(
    ticker: str, name: str, quantity: float, avg_cost: float, sleeve: str
) -> dict:
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO holdings (ticker, name, quantity, avg_cost, sleeve, updated_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(ticker) DO UPDATE SET
                name       = excluded.name,
                quantity   = excluded.quantity,
                avg_cost   = excluded.avg_cost,
                sleeve     = excluded.sleeve,
                updated_at = datetime('now')
            """,
            (ticker, name, quantity, avg_cost, sleeve),
        )
    return next(h for h in get_holdings() if h["ticker"] == ticker)


def delete_holding(ticker: str) -> None:
    with get_db() as conn:
        conn.execute("DELETE FROM holdings WHERE ticker = ?", (ticker,))
