"""
Sleeve A universe: 22 active UCITS ETFs + 1 defensive (XEON).
These trade on LSE / XETRA via Saxo — NOT PEA-eligible.

EODHD symbol format: TICKER.LSE or TICKER.XETRA
ISINs must be verified on Saxo before live execution.
"""
from __future__ import annotations

REGIME_FILTER_TICKER = "IWDA"
DEFENSIVE_TICKER = "XEON"

# Each entry: eodhd_symbol, full name, category
ETF_UNIVERSE: dict[str, dict] = {
    # ── 11 sectoriels US S&P 500 ─────────────────────────────────────────
    "IUIT": {
        "name": "iShares S&P 500 IT Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUIT.LSE",
    },
    "IUFS": {
        "name": "iShares S&P 500 Financials Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUFS.LSE",
    },
    "IUES": {
        "name": "iShares S&P 500 Energy Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUES.LSE",
    },
    "IUHC": {
        "name": "iShares S&P 500 Health Care Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUHC.LSE",
    },
    "IUCD": {
        "name": "iShares S&P 500 Consumer Discretionary UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUCD.LSE",
    },
    "IUIS": {
        "name": "iShares S&P 500 Industrials Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUIS.LSE",
    },
    "IUCS": {
        "name": "iShares S&P 500 Consumer Staples UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUCS.LSE",
    },
    "IUUS": {
        "name": "iShares S&P 500 Utilities Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUUS.LSE",
    },
    "IUMS": {
        "name": "iShares S&P 500 Materials Sector UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUMS.LSE",
    },
    "IURE": {
        "name": "iShares S&P 500 Real Estate UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUSP.LSE",
    },
    "IUCM": {
        "name": "iShares S&P 500 Communication Services UCITS ETF",
        "category": "Sectoriel US",
        "eodhd": "IUCM.LSE",
    },
    # ── 5 géographiques ──────────────────────────────────────────────────
    "IWDA": {
        "name": "iShares Core MSCI World UCITS ETF",
        "category": "Monde",
        "eodhd": "IWDA.LSE",
    },
    "EIMI": {
        "name": "iShares Core MSCI EM IMI UCITS ETF",
        "category": "Émergents",
        "eodhd": "EIMI.LSE",
    },
    "SJPA": {
        "name": "iShares Core MSCI Japan IMI UCITS ETF",
        "category": "Japon",
        "eodhd": "SJPA.LSE",
    },
    "CEU": {
        "name": "iShares Core MSCI Europe UCITS ETF",
        "category": "Europe",
        "eodhd": "SMEA.LSE",
    },
    "NDIA": {
        "name": "iShares MSCI India UCITS ETF",
        "category": "Inde",
        "eodhd": "NDIA.LSE",
    },
    # ── 3 factor / style ─────────────────────────────────────────────────
    "IUSM": {
        "name": "iShares S&P SmallCap 600 UCITS ETF",
        "category": "Small Cap",
        "eodhd": "IUSM.XETRA",
    },
    "IS3R": {
        "name": "iShares Edge MSCI World Momentum Factor UCITS ETF",
        "category": "Facteur",
        "eodhd": "IS3R.XETRA",
    },
    "IWQU": {
        "name": "iShares Edge MSCI World Quality Factor UCITS ETF",
        "category": "Facteur",
        "eodhd": "IWQU.LSE",
    },
    # ── 2 thématiques ────────────────────────────────────────────────────
    "SEMI": {
        "name": "VanEck Semiconductor UCITS ETF",
        "category": "Thématique",
        "eodhd": "SEMI.AS",
    },
    "WBIO": {
        "name": "Rize Medical Innovation UCITS ETF",
        "category": "Thématique",
        "eodhd": "WBIO.LSE",
    },
    # ── 1 or ─────────────────────────────────────────────────────────────
    "SGLD": {
        "name": "Invesco Physical Gold ETC",
        "category": "Or",
        "eodhd": "SGLD.LSE",
    },
    # ── défensif (hors univers actif, refuge régime OFF) ─────────────────
    "XEON": {
        "name": "Xtrackers EUR Overnight Rate Swap UCITS ETF",
        "category": "Défensif",
        "eodhd": "XEON.XETRA",
    },
}

ACTIVE_TICKERS: list[str] = [t for t in ETF_UNIVERSE if t != DEFENSIVE_TICKER]
ALL_TICKERS: list[str] = list(ETF_UNIVERSE.keys())


def get_eodhd_symbol(ticker: str) -> str:
    return ETF_UNIVERSE[ticker]["eodhd"]


def get_metadata(ticker: str) -> dict:
    entry = ETF_UNIVERSE[ticker]
    return {
        "ticker": ticker,
        "name": entry["name"],
        "category": entry["category"],
        "eodhd": entry["eodhd"],
        "is_active": ticker != DEFENSIVE_TICKER,
        "is_defensive": ticker == DEFENSIVE_TICKER,
        "is_regime_filter": ticker == REGIME_FILTER_TICKER,
    }


def get_all_metadata() -> list[dict]:
    return [get_metadata(t) for t in ALL_TICKERS]