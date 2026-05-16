"""
ETF universe: curated list of liquid ETFs traded on Euronext (Paris, Amsterdam, Brussels, Lisbon).
Tickers use EODHD exchange suffixes: .PA (Paris), .AS (Amsterdam), .BR (Brussels).
"""

from __future__ import annotations

import pandas as pd
from pathlib import Path

CACHE_PATH = Path(__file__).parent / "etf_cache.json"

# Broad, liquid Euronext ETF universe covering major asset classes and factors
EURONEXT_ETFS = {
    # --- Equity: World / Global ---
    "CW8.PA":    {"name": "Amundi MSCI World",              "category": "Equity",   "region": "World"},
    "EWLD.PA":   {"name": "Lyxor MSCI World",               "category": "Equity",   "region": "World"},
    "MWRD.PA":   {"name": "iShares MSCI World",             "category": "Equity",   "region": "World"},
    "IWDA.AS":   {"name": "iShares Core MSCI World",        "category": "Equity",   "region": "World"},
    "SWRD.PA":   {"name": "SPDR MSCI World",                "category": "Equity",   "region": "World"},
    "ACWI.PA":   {"name": "Amundi MSCI ACWI",               "category": "Equity",   "region": "World"},
    "IMIE.PA":   {"name": "iShares MSCI World Small Cap",   "category": "Equity",   "region": "World"},

    # --- Equity: Europe ---
    "ESE.PA":    {"name": "Amundi STOXX Europe 600",        "category": "Equity",   "region": "Europe"},
    "CS51.PA":   {"name": "Amundi EURO STOXX 50",           "category": "Equity",   "region": "Europe"},
    "CAC.PA":    {"name": "Amundi CAC 40",                  "category": "Equity",   "region": "Europe"},
    "EXW1.PA":   {"name": "iShares Core EURO STOXX 50",     "category": "Equity",   "region": "Europe"},
    "MEUD.PA":   {"name": "Lyxor Core STOXX Europe 600",    "category": "Equity",   "region": "Europe"},
    "SMAE.PA":   {"name": "Amundi MSCI Europe Small Cap",   "category": "Equity",   "region": "Europe"},
    "DX2J.PA":   {"name": "Xtrackers MSCI Europe",          "category": "Equity",   "region": "Europe"},

    # --- Equity: USA ---
    "SP5.PA":    {"name": "Amundi S&P 500",                 "category": "Equity",   "region": "USA"},
    "500.PA":    {"name": "Lyxor S&P 500",                  "category": "Equity",   "region": "USA"},
    "CSPX.AS":   {"name": "iShares Core S&P 500",           "category": "Equity",   "region": "USA"},
    "SPPW.PA":   {"name": "SPDR S&P 500",                   "category": "Equity",   "region": "USA"},
    "NASD.PA":   {"name": "Lyxor Nasdaq-100",               "category": "Equity",   "region": "USA"},
    "AAPL.PA":   {"name": "Amundi Nasdaq-100",              "category": "Equity",   "region": "USA"},
    "RS2K.PA":   {"name": "Lyxor Russell 2000",             "category": "Equity",   "region": "USA"},

    # --- Equity: Emerging Markets ---
    "AEEM.PA":   {"name": "Amundi MSCI Emerging Markets",   "category": "Equity",   "region": "EM"},
    "PAEEM.PA":  {"name": "Lyxor MSCI Emerging Markets",    "category": "Equity",   "region": "EM"},
    "EIMI.AS":   {"name": "iShares Core MSCI EM",           "category": "Equity",   "region": "EM"},
    "AASI.PA":   {"name": "Amundi MSCI Asia ex Japan",      "category": "Equity",   "region": "EM"},

    # --- Equity: Sectors ---
    "PANX.PA":   {"name": "Lyxor MSCI World Technology",    "category": "Equity",   "region": "Sector"},
    "TECH.PA":   {"name": "Amundi MSCI World Technology",   "category": "Equity",   "region": "Sector"},
    "HLTH.PA":   {"name": "Amundi MSCI World Healthcare",   "category": "Equity",   "region": "Sector"},
    "GLDM.PA":   {"name": "Lyxor MSCI World Financials",    "category": "Equity",   "region": "Sector"},
    "INRG.PA":   {"name": "iShares Global Clean Energy",    "category": "Equity",   "region": "Sector"},
    "WCOA.PA":   {"name": "Amundi World Consumer Disc.",    "category": "Equity",   "region": "Sector"},
    "ENER.PA":   {"name": "Lyxor MSCI World Energy",        "category": "Equity",   "region": "Sector"},

    # --- Equity: Factor / Smart Beta ---
    "IWMO.AS":   {"name": "iShares MSCI World Momentum",    "category": "Factor",   "region": "World"},
    "IWVL.AS":   {"name": "iShares MSCI World Value",       "category": "Factor",   "region": "World"},
    "IWQU.AS":   {"name": "iShares MSCI World Quality",     "category": "Factor",   "region": "World"},
    "MVOL.PA":   {"name": "iShares MSCI World Min Vol",     "category": "Factor",   "region": "World"},
    "EUMV.PA":   {"name": "iShares MSCI Europe Min Vol",    "category": "Factor",   "region": "Europe"},
    "IEVD.AS":   {"name": "iShares MSCI Europe Value",      "category": "Factor",   "region": "Europe"},
    "EUMO.PA":   {"name": "Amundi MSCI Europe Momentum",    "category": "Factor",   "region": "Europe"},

    # --- Fixed Income: Government ---
    "MTH.PA":    {"name": "Lyxor Euro Govt Bond 1-3Y",      "category": "Bond",     "region": "Europe"},
    "MTS.PA":    {"name": "Amundi Euro Govt Bond 3-5Y",     "category": "Bond",     "region": "Europe"},
    "MTM.PA":    {"name": "Lyxor Euro Govt Bond 7-10Y",     "category": "Bond",     "region": "Europe"},
    "MTLA.PA":   {"name": "Lyxor Euro Govt Bond 10Y+",      "category": "Bond",     "region": "Europe"},
    "IBTE.AS":   {"name": "iShares EUR Govt Bond 1-3Y",     "category": "Bond",     "region": "Europe"},
    "IBGM.AS":   {"name": "iShares EUR Govt Bond 5-10Y",    "category": "Bond",     "region": "Europe"},
    "SEGA.PA":   {"name": "SPDR Euro Govt Bond",            "category": "Bond",     "region": "Europe"},

    # --- Fixed Income: Corp / HY ---
    "CRPE.PA":   {"name": "Lyxor EUR Corp Bond",            "category": "Bond",     "region": "Europe"},
    "IEAC.AS":   {"name": "iShares Core EUR Corp Bond",     "category": "Bond",     "region": "Europe"},
    "HYB.PA":    {"name": "Amundi EUR High Yield",          "category": "Bond",     "region": "Europe"},
    "IHYG.AS":   {"name": "iShares EUR High Yield Corp",    "category": "Bond",     "region": "Europe"},

    # --- Commodities ---
    "LYTR.PA":   {"name": "Lyxor Commodities Thomson Reuters", "category": "Commodity", "region": "Global"},
    "ACOM.PA":   {"name": "Amundi Bloomberg Commodity",     "category": "Commodity", "region": "Global"},
    "GBS.PA":    {"name": "Amundi Physical Gold",           "category": "Commodity", "region": "Global"},
    "GOLD.PA":   {"name": "Lyxor Gold",                     "category": "Commodity", "region": "Global"},
    "SGLD.PA":   {"name": "Invesco Physical Gold",          "category": "Commodity", "region": "Global"},

    # --- Real Estate ---
    "REEU.PA":   {"name": "Amundi FTSE EPRA Europe RE",     "category": "Real Estate", "region": "Europe"},
    "IPRP.AS":   {"name": "iShares European Property",      "category": "Real Estate", "region": "Europe"},
    "EPRE.PA":   {"name": "Lyxor FTSE EPRA Global RE",      "category": "Real Estate", "region": "Global"},
}


def get_etf_metadata() -> pd.DataFrame:
    """Return the static ETF universe as a DataFrame."""
    rows = [
        {"ticker": ticker, **meta}
        for ticker, meta in EURONEXT_ETFS.items()
    ]
    return pd.DataFrame(rows).set_index("ticker")


def fetch_prices(
    tickers: list[str] | None = None,
    period: str = "2y",
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Deprecated compatibility shim.

    Use scripts/fetch_market_data.py with EODHD instead. This module now only
    owns static Euronext metadata.
    """
    raise RuntimeError("Use scripts/fetch_market_data.py --source eodhd to fetch prices.")


def invalidate_cache():
    if CACHE_PATH.exists():
        CACHE_PATH.unlink()
