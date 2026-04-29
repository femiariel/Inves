"""
PEA-eligible ETF universe — Euronext Paris.
All ETFs use synthetic (swap-based) replication or are European-domiciled
to remain éligibles PEA (Plan d'Épargne en Actions).
Sources: Amundi, Lyxor (now Amundi), iShares/BNP swap, BNP Paribas Easy,
         SPDR (State Street), Xtrackers (DWS), Vanguard, VanEck.
"""

from __future__ import annotations
import pandas as pd

# ── Sleeve constants ───────────────────────────────────────────────────────────
SLEEVE_CORE       = "core"
SLEEVE_AGGRESSIVE = "aggressive"
SLEEVE_DEFENSIVE  = "defensive"

# ── Category constants ─────────────────────────────────────────────────────────
CAT_WORLD    = "Monde"
CAT_US       = "États-Unis"
CAT_NASDAQ   = "Tech / Nasdaq"
CAT_EUROPE   = "Europe"
CAT_FRANCE   = "France"
CAT_GERMANY  = "Allemagne"
CAT_UK       = "Royaume-Uni"
CAT_JAPAN    = "Japon"
CAT_ASIA     = "Asie Pacifique"
CAT_EM       = "Émergents"
CAT_SMALL    = "Small Cap"
CAT_SECTOR   = "Sectoriel"
CAT_ESG      = "ESG / SRI"
CAT_FACTOR   = "Facteur"
CAT_DIVIDEND = "Dividendes"
CAT_BOND     = "Obligations"
CAT_MONEY    = "Monétaire"

# ticker → {name, sleeve, category, target_weight, notes}
PEA_UNIVERSE: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════════════
    # MONDE / GLOBAL — MSCI World et All Country World
    # ══════════════════════════════════════════════════════════════════════════
    "DCAM.PA": {
        "name": "Amundi PEA Monde MSCI World",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.30,
        "notes": "Ancre principale — synthétique swap PEA éligible",
    },
    "CW8.PA": {
        "name": "Amundi MSCI World EUR Acc",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.10,
        "notes": "MSCI World swap — très liquide, TER 0.38%",
    },
    "WPEA.PA": {
        "name": "Amundi MSCI World Acc PEA",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.08,
        "notes": "Variante monde accumulation éligible PEA",
    },
    "MWRD.PA": {
        "name": "Lyxor Core MSCI World DR UCITS",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.05,
        "notes": "Réplication directe MSCI World — physique optimisé",
    },
    "WLD.PA": {
        "name": "Lyxor MSCI World UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.05,
        "notes": "Lyxor MSCI World classique — swap",
    },
    "LCWD.PA": {
        "name": "Lyxor Core MSCI World UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.04,
        "notes": "Core serie Lyxor — faibles frais",
    },
    "SWLD.PA": {
        "name": "SPDR MSCI World UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": CAT_WORLD, "target_weight": 0.04,
        "notes": "State Street MSCI World — TER compétitif",
    },
    "EWLD.PA": {
        "name": "Lyxor MSCI All Country World UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_WORLD, "target_weight": 0.04,
        "notes": "ACWI — inclut ~10% marchés émergents",
    },
    "ACWE.PA": {
        "name": "iShares MSCI ACWI UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_WORLD, "target_weight": 0.03,
        "notes": "iShares All Country World — swap PEA",
    },
    "IMIE.PA": {
        "name": "iShares MSCI World Mid Cap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_WORLD, "target_weight": 0.02,
        "notes": "Mid cap mondial — complément au large cap",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ÉTATS-UNIS — S&P 500 et MSCI USA
    # ══════════════════════════════════════════════════════════════════════════
    "PSP5.PA": {
        "name": "Amundi PEA S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.06,
        "notes": "S&P 500 synthétique — PEA éligible Amundi",
    },
    "ESE.PA": {
        "name": "BNP Paribas Easy S&P 500 UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.05,
        "notes": "BNP Easy S&P 500 — swap PEA éligible",
    },
    "SP5.PA": {
        "name": "Amundi S&P 500 ESG UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.05,
        "notes": "S&P 500 ESG screened — synthétique PEA",
    },
    "PUST.PA": {
        "name": "Amundi PEA MSCI USA UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.05,
        "notes": "MSCI USA synthétique — éligible PEA Amundi",
    },
    "USE.PA": {
        "name": "Amundi MSCI USA UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.04,
        "notes": "MSCI USA large cap — accumulation",
    },
    "XSPU.PA": {
        "name": "Xtrackers S&P 500 Swap UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.04,
        "notes": "S&P 500 Xtrackers — swap DWS",
    },
    "SPXS.PA": {
        "name": "SPDR S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.03,
        "notes": "State Street S&P 500 — part Acc",
    },
    "IUS3.PA": {
        "name": "iShares Core S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.03,
        "notes": "iShares Core S&P 500 — réplication synthétique PEA",
    },
    "LCUS.PA": {
        "name": "Lyxor Core MSCI USA DR UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.03,
        "notes": "MSCI USA Lyxor Core — réplication directe",
    },
    "SPXD.PA": {
        "name": "Invesco S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_US, "target_weight": 0.02,
        "notes": "S&P 500 Invesco — swap PEA",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # NASDAQ / TECH USA
    # ══════════════════════════════════════════════════════════════════════════
    "PANX.PA": {
        "name": "Amundi PEA Nasdaq-100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_NASDAQ, "target_weight": 0.07,
        "notes": "Nasdaq-100 synthétique — éligible PEA Amundi",
    },
    "ANX.PA": {
        "name": "Amundi Nasdaq-100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_NASDAQ, "target_weight": 0.05,
        "notes": "Nasdaq-100 Amundi — accumulation, swap",
    },
    "NSDQ.PA": {
        "name": "Lyxor Nasdaq-100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_NASDAQ, "target_weight": 0.04,
        "notes": "Lyxor Nasdaq-100 — swap PEA éligible",
    },
    "WTEC.PA": {
        "name": "Lyxor MSCI World Information Technology",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_NASDAQ, "target_weight": 0.04,
        "notes": "Tech mondiale — au-delà du Nasdaq, inclut Europe",
    },
    "LQQ.PA": {
        "name": "Amundi Nasdaq-100 Daily 2× Leveraged",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_NASDAQ, "target_weight": 0.01,
        "notes": "⚠️ Levier ×2 — usage tactique uniquement, risque élevé",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # EUROPE — Indices larges
    # ══════════════════════════════════════════════════════════════════════════
    "CS51.PA": {
        "name": "Amundi EURO STOXX 50 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.05,
        "notes": "Euro Stoxx 50 — 50 leaders zone euro",
    },
    "MEUD.PA": {
        "name": "Lyxor Core STOXX Europe 600 UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.04,
        "notes": "Stoxx 600 — 600 valeurs Europe large+mid+small",
    },
    "MEU.PA": {
        "name": "iShares Core MSCI Europe UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.04,
        "notes": "iShares MSCI Europe — réplication directe",
    },
    "LCEU.PA": {
        "name": "Lyxor Core MSCI Europe DR UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.03,
        "notes": "Lyxor MSCI Europe — Core serie réplication directe",
    },
    "MSEE.PA": {
        "name": "Amundi MSCI Europe UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.03,
        "notes": "MSCI Europe Amundi — accumulation",
    },
    "ERO.PA": {
        "name": "Lyxor EURO STOXX 300 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.03,
        "notes": "Euro Stoxx 300 — zone euro élargie",
    },
    "MTD.PA": {
        "name": "Amundi MSCI EMU UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.03,
        "notes": "MSCI EMU — zone euro seulement",
    },
    "XESC.PA": {
        "name": "Xtrackers EURO STOXX 50 Swap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.03,
        "notes": "Xtrackers Euro Stoxx 50 — swap DWS",
    },
    "VEUR.PA": {
        "name": "Vanguard FTSE Developed Europe ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.03,
        "notes": "Vanguard Europe — TER très faible 0.10%",
    },
    "SPYE.PA": {
        "name": "SPDR MSCI Europe UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.02,
        "notes": "State Street MSCI Europe",
    },
    "IESE.PA": {
        "name": "iShares Core Euro STOXX 50 UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.02,
        "notes": "iShares Core Euro Stoxx 50 — DR physique",
    },
    "XSTR.PA": {
        "name": "Xtrackers STOXX Europe 600 UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EUROPE, "target_weight": 0.02,
        "notes": "Stoxx 600 Xtrackers — swap",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # FRANCE — CAC 40
    # ══════════════════════════════════════════════════════════════════════════
    "CAC.PA": {
        "name": "Amundi ETF CAC 40 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FRANCE, "target_weight": 0.03,
        "notes": "CAC 40 — 40 plus grandes valeurs françaises",
    },
    "CG1.PA": {
        "name": "Amundi ETF DAX UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FRANCE, "target_weight": 0.02,
        "notes": "Lyxor CAC 40 — actif phare Euronext Paris",
    },
    "C40.PA": {
        "name": "BNP Paribas Easy CAC 40 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FRANCE, "target_weight": 0.02,
        "notes": "BNP Easy CAC 40 — swap PEA éligible",
    },
    "CACC.PA": {
        "name": "iShares CAC 40 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FRANCE, "target_weight": 0.02,
        "notes": "iShares CAC 40 — swap BNP Paribas PEA",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ALLEMAGNE — DAX
    # ══════════════════════════════════════════════════════════════════════════
    "XDAX.PA": {
        "name": "Xtrackers DAX UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_GERMANY, "target_weight": 0.02,
        "notes": "DAX — 40 plus grandes valeurs allemandes",
    },
    "DAX.PA": {
        "name": "Amundi ETF DAX Daily UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_GERMANY, "target_weight": 0.02,
        "notes": "DAX Amundi — exposition Allemagne directe",
    },
    "DBXD.PA": {
        "name": "Xtrackers DAX Income 1D UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_GERMANY, "target_weight": 0.02,
        "notes": "DAX Xtrackers — distributif — dividendes trimestriels",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ROYAUME-UNI — FTSE 100
    # ══════════════════════════════════════════════════════════════════════════
    "FTSE.PA": {
        "name": "Lyxor FTSE 100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_UK, "target_weight": 0.02,
        "notes": "FTSE 100 — UK large cap — libellé EUR",
    },
    "UKDV.PA": {
        "name": "iShares UK Dividend UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_UK, "target_weight": 0.02,
        "notes": "UK dividendes — haut rendement",
    },
    "ISF.PA": {
        "name": "iShares Core FTSE 100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_UK, "target_weight": 0.02,
        "notes": "FTSE 100 iShares — réplication directe",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # JAPON — TOPIX & MSCI Japan
    # ══════════════════════════════════════════════════════════════════════════
    "PTPXH.PA": {
        "name": "Amundi PEA Japan TOPIX Hedged EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_JAPAN, "target_weight": 0.05,
        "notes": "TOPIX couvert EUR — PEA éligible Amundi",
    },
    "TNO.PA": {
        "name": "Lyxor Japan (TOPIX) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_JAPAN, "target_weight": 0.03,
        "notes": "TOPIX Lyxor — non couvert, exposé JPY",
    },
    "JPN.PA": {
        "name": "Amundi Japan TOPIX UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_JAPAN, "target_weight": 0.03,
        "notes": "TOPIX Amundi — accumulation JPY non couvert",
    },
    "PJPN.PA": {
        "name": "Amundi PEA MSCI Japan UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_JAPAN, "target_weight": 0.02,
        "notes": "MSCI Japan swap — éligible PEA",
    },
    "XJPN.PA": {
        "name": "Xtrackers MSCI Japan UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_JAPAN, "target_weight": 0.02,
        "notes": "MSCI Japan Xtrackers — swap non couvert",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ASIE PACIFIQUE (hors Japon)
    # ══════════════════════════════════════════════════════════════════════════
    "AASI.PA": {
        "name": "Amundi MSCI Pacific ex Japan UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ASIA, "target_weight": 0.02,
        "notes": "Asie-Pacifique hors Japon — AUS, HK, SG, NZ",
    },
    "PAEJ.PA": {
        "name": "Amundi PEA Asie Emergente UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ASIA, "target_weight": 0.02,
        "notes": "Asie émergente — Chine, Corée, Taiwan, ASEAN",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MARCHÉS ÉMERGENTS
    # ══════════════════════════════════════════════════════════════════════════
    "PAEEM.PA": {
        "name": "Amundi PEA MSCI EM ESG UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.05,
        "notes": "EM ESG — swap PEA — Chine/Inde/Brésil/Taiwan",
    },
    "AEEM.PA": {
        "name": "Amundi MSCI Emerging Markets UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.04,
        "notes": "MSCI EM large cap — sans filtre ESG",
    },
    "LEME.PA": {
        "name": "Lyxor MSCI Emerging Markets UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.03,
        "notes": "MSCI EM Lyxor — swap PEA éligible",
    },
    "XMEM.PA": {
        "name": "Xtrackers MSCI Emerging Markets Swap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.03,
        "notes": "EM Xtrackers — swap DWS",
    },
    "GEM.PA": {
        "name": "Amundi MSCI Emerging ESG Leaders",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.02,
        "notes": "EM ESG Leaders — meilleurs élèves extra-financiers",
    },
    "INSE.PA": {
        "name": "Lyxor MSCI India UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.02,
        "notes": "Inde — 1.4Md habitants, croissance structurelle",
    },
    "CHNA.PA": {
        "name": "Amundi MSCI China UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.02,
        "notes": "Chine large cap — forte volatilité réglementaire",
    },
    "BRLE.PA": {
        "name": "Lyxor MSCI Brazil UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_EM, "target_weight": 0.02,
        "notes": "Brésil — exposition matières premières et banques",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PETITES CAPITALISATIONS
    # ══════════════════════════════════════════════════════════════════════════
    "CSEM.PA": {
        "name": "iShares MSCI Europe Small Cap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SMALL, "target_weight": 0.04,
        "notes": "Small cap Europe — prime de taille documentée",
    },
    "RS2K.PA": {
        "name": "Lyxor Russell 2000 UCITS PEA ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SMALL, "target_weight": 0.03,
        "notes": "Russell 2000 — 2000 small cap US swap PEA",
    },
    "SMAE.PA": {
        "name": "Amundi MSCI Europe Small Cap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SMALL, "target_weight": 0.03,
        "notes": "Small cap Europe Amundi — prime de taille",
    },
    "USSC.PA": {
        "name": "SPDR MSCI USA Small Cap UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SMALL, "target_weight": 0.02,
        "notes": "Small cap USA SPDR — exposition large",
    },
    "CUSP.PA": {
        "name": "Amundi MSCI USA Small Cap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SMALL, "target_weight": 0.02,
        "notes": "Small cap USA Amundi — swap PEA",
    },
    "WSML.PA": {
        "name": "iShares MSCI World Small Cap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SMALL, "target_weight": 0.02,
        "notes": "Small cap mondial — exposition globale",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # SECTORIEL — Thèmes et secteurs
    # ══════════════════════════════════════════════════════════════════════════
    "BNKE.PA": {
        "name": "Lyxor STOXX Europe 600 Banks UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Banques européennes — cyclique, sensible aux taux",
    },
    "HLTE.PA": {
        "name": "iShares STOXX Europe 600 Health Care",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Santé Europe — défensif, vieillissement population",
    },
    "INRG.PA": {
        "name": "iShares Global Clean Energy UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Énergies renouvelables mondiales — éolien, solaire",
    },
    "DFEN.PA": {
        "name": "Amundi ETF Defense & Aerospace UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Défense/Aérospatial — contexte géopolitique favorable",
    },
    "WELTU.PA": {
        "name": "Amundi MSCI World Luxury UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Luxe mondial — LVMH, Hermès, Richemont",
    },
    "FOOD.PA": {
        "name": "Amundi STOXX Europe 600 Food UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Alimentation boissons Europe — défensif récurrent",
    },
    "ROBX.PA": {
        "name": "Amundi Robotics & AI UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Robotique et IA — thème de croissance long terme",
    },
    "PSCH.PA": {
        "name": "Lyxor MSCI Europe Semiconductors UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Semi-conducteurs Europe — ASML, Infineon, STMicro",
    },
    "LYXE.PA": {
        "name": "Lyxor New Energy UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Nouvelles énergies — éolien, solaire, hydrogène",
    },
    "DGTL.PA": {
        "name": "iShares Digital Security UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Cybersécurité et sécurité numérique mondiale",
    },
    "XCLD.PA": {
        "name": "Xtrackers MSCI World Comm Services",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Télécoms et médias — GAFA, Netflix, Disney",
    },
    "WATL.PA": {
        "name": "BNP Paribas Easy MSCI Water UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Gestion de l'eau — ressource rare, croissance défensive",
    },
    "EPOL.PA": {
        "name": "Lyxor MSCI Europe Energy UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Énergie Europe — Total Energies, Shell, BP",
    },
    "IMAT.PA": {
        "name": "iShares STOXX Europe 600 Materials",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Matériaux de base — mines, chimie, acier",
    },
    "AERO.PA": {
        "name": "Amundi STOXX Europe 600 Aerospace",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_SECTOR, "target_weight": 0.02,
        "notes": "Aérospatial Europe — Airbus, Safran, Thales",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # ESG / SRI — Investissement responsable
    # ══════════════════════════════════════════════════════════════════════════
    "SUSW.PA": {
        "name": "iShares MSCI World SRI UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": CAT_ESG, "target_weight": 0.03,
        "notes": "MSCI World SRI — filtre ESG strict 25% best-in-class",
    },
    "WLDSR.PA": {
        "name": "Amundi MSCI World SRI PAB UCITS",
        "sleeve": SLEEVE_CORE, "category": CAT_ESG, "target_weight": 0.03,
        "notes": "MSCI World SRI Paris-Aligned Benchmark",
    },
    "ESGL.PA": {
        "name": "iShares MSCI Europe SRI UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ESG, "target_weight": 0.02,
        "notes": "MSCI Europe SRI — 25% meilleurs par secteur",
    },
    "SRIC.PA": {
        "name": "Amundi MSCI Europe SRI PAB UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ESG, "target_weight": 0.02,
        "notes": "Europe SRI aligné Accord de Paris",
    },
    "USSE.PA": {
        "name": "Amundi MSCI USA SRI PAB UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ESG, "target_weight": 0.02,
        "notes": "USA SRI Amundi — 25% best-in-class",
    },
    "CLIM.PA": {
        "name": "Amundi MSCI World Climate UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ESG, "target_weight": 0.02,
        "notes": "Transition climatique — faible empreinte carbone",
    },
    "PABW.PA": {
        "name": "Xtrackers MSCI World Paris Aligned",
        "sleeve": SLEEVE_CORE, "category": CAT_ESG, "target_weight": 0.02,
        "notes": "Paris-Aligned Benchmark — objectif net-zéro 2050",
    },
    "SGHL.PA": {
        "name": "Lyxor MSCI World ESG Trends UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_ESG, "target_weight": 0.02,
        "notes": "ESG Trends — tiltage vers meilleurs scores ESG",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # FACTEURS — Smart Beta / Factor Investing
    # ══════════════════════════════════════════════════════════════════════════
    "IWMO.PA": {
        "name": "iShares MSCI World Momentum UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FACTOR, "target_weight": 0.03,
        "notes": "Momentum factor mondial — rebalancement semestriel",
    },
    "IWQU.PA": {
        "name": "iShares MSCI World Quality UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FACTOR, "target_weight": 0.03,
        "notes": "Quality factor — ROE élevé, faible levier, stable",
    },
    "IWVL.PA": {
        "name": "iShares MSCI World Value Factor UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FACTOR, "target_weight": 0.03,
        "notes": "Value factor — P/B et P/E faibles",
    },
    "MVOL.PA": {
        "name": "iShares MSCI World Min Vol UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_FACTOR, "target_weight": 0.03,
        "notes": "Minimum volatilité mondiale — défensif bear market",
    },
    "EUMF.PA": {
        "name": "iShares MSCI Europe Multifactor UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FACTOR, "target_weight": 0.02,
        "notes": "Multi-facteur Europe — value + quality + momentum",
    },
    "SVAL.PA": {
        "name": "SPDR MSCI Europe Value UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FACTOR, "target_weight": 0.02,
        "notes": "Value Europe SPDR — tilté P/B faible",
    },
    "SMOT.PA": {
        "name": "SPDR MSCI Europe Momentum UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_FACTOR, "target_weight": 0.02,
        "notes": "Momentum Europe SPDR — rebalancement mensuel",
    },
    "XDEV.PA": {
        "name": "Xtrackers MSCI World Minimum Volatility",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_FACTOR, "target_weight": 0.02,
        "notes": "Min Vol mondial Xtrackers — alternative à MVOL",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # DIVIDENDES — Revenus réguliers
    # ══════════════════════════════════════════════════════════════════════════
    "DJEA.PA": {
        "name": "Lyxor DJ Euro STOXX Select Div 30",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_DIVIDEND, "target_weight": 0.03,
        "notes": "30 valeurs à plus hauts dividendes zone euro",
    },
    "IDVY.PA": {
        "name": "iShares Euro Dividend UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_DIVIDEND, "target_weight": 0.02,
        "notes": "Dividendes zone euro — iShares — distributif",
    },
    "TDIV.PA": {
        "name": "VanEck Morningstar Dev Markets Div",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_DIVIDEND, "target_weight": 0.02,
        "notes": "Dividendes marchés développés — Morningstar screened",
    },
    "SPYD.PA": {
        "name": "SPDR S&P US Dividend Aristocrats UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_DIVIDEND, "target_weight": 0.02,
        "notes": "Aristocrates du dividende US — 25+ ans de hausse",
    },
    "ADER.PA": {
        "name": "Amundi STOXX Europe High Div UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_DIVIDEND, "target_weight": 0.02,
        "notes": "Haut rendement Europe Amundi — PEA compatible",
    },
    "EUDV.PA": {
        "name": "SPDR S&P Euro Dividend Aristocrats",
        "sleeve": SLEEVE_AGGRESSIVE, "category": CAT_DIVIDEND, "target_weight": 0.02,
        "notes": "Aristocrates dividende zone euro — 10+ ans hausse",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # OBLIGATIONS — Fixed Income PEA-compatible
    # ══════════════════════════════════════════════════════════════════════════
    "GOVR.PA": {
        "name": "iShares Euro Govt Bond 1-3yr UCITS",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_BOND, "target_weight": 0.03,
        "notes": "Obligations d'État court terme zone euro",
    },
    "XGLE.PA": {
        "name": "Xtrackers Euro Govt Bond UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_BOND, "target_weight": 0.02,
        "notes": "Obli d'État euro Xtrackers — toutes maturités",
    },
    "CB5.PA": {
        "name": "iShares Euro Corporate Bond UCITS",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_BOND, "target_weight": 0.02,
        "notes": "Obligations corporate investment grade zone euro",
    },
    "AGGH.PA": {
        "name": "iShares Core Global Agg Bond Hdg EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_BOND, "target_weight": 0.02,
        "notes": "Agrégat mondial couvert EUR — souverain + corporate",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # MONÉTAIRE PEA — Substitut cash dans le PEA
    # ══════════════════════════════════════════════════════════════════════════
    "OBLI.PA": {
        "name": "Amundi PEA Euro Court Terme UCITS",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_MONEY, "target_weight": 0.04,
        "notes": "Parking monétaire PEA — substitut liquidités dans PEA",
    },
    "MMOE.PA": {
        "name": "BNP Paribas Easy € Corp Bond SRI PAB",
        "sleeve": SLEEVE_DEFENSIVE, "category": CAT_MONEY, "target_weight": 0.02,
        "notes": "Corporate court terme zone euro — SRI filtré",
    },
}

# Anchor ticker for the 80% core sleeve
CORE_ANCHOR = "DCAM.PA"


def get_etf_metadata() -> pd.DataFrame:
    rows = [{"ticker": t, **m} for t, m in PEA_UNIVERSE.items()]
    return pd.DataFrame(rows).set_index("ticker")


def get_satellite_tickers() -> list[str]:
    return [t for t, m in PEA_UNIVERSE.items() if m["sleeve"] == SLEEVE_AGGRESSIVE]


def get_all_tickers() -> list[str]:
    return list(PEA_UNIVERSE.keys())


def get_categories() -> list[str]:
    seen: list[str] = []
    for m in PEA_UNIVERSE.values():
        if m["category"] not in seen:
            seen.append(m["category"])
    return seen
