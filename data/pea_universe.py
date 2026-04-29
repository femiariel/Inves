"""
PEA-eligible ETF universe — Euronext Paris.
Source réelle : EODHD Exchange Symbol List (PA).
Données récupérées et classifiées automatiquement.
"""

from __future__ import annotations
import pandas as pd

SLEEVE_CORE       = "core"
SLEEVE_AGGRESSIVE = "aggressive"
SLEEVE_DEFENSIVE  = "defensive"

CORE_ANCHOR = "DCAM.PA"

PEA_UNIVERSE: dict[str, dict] = {

    # ══════════════════════════════════════════════════════════════════════
    # MONDE
    # ══════════════════════════════════════════════════════════════════════
    "ACWE.PA": {
        "name": "SSgA SPDR MSCI ACWI",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "ACWI.PA": {
        "name": "Multi Units Luxembourg - Lyxor MSCI All Country World UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "CLWD.PA": {
        "name": "Amundi MSCI World ESG Climate Net Zero Ambition CTB UCITS ETF Dis",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "CM9.PA": {
        "name": "Amundi ETF MSCI World ex EMU UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "DCAM.PA": {
        "name": "Amundi PEA Monde (MSCI World) UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "EMWE.PA": {
        "name": "BNP Paribas Easy MSCI World SRI S-Series PAB 5% Capped UCITS ETF EUR Capitalisation",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "FINSW.PA": {
        "name": "Multi Units Luxembourg - Lyxor MSCI World Financials TR UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "FINW.PA": {
        "name": "Lyxor MSCI World Financials TR UCITS ETF - C-EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "HIWS.PA": {
        "name": "HSBC MSCI World Islamic Screened UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "HLTW.PA": {
        "name": "Amundi MSCI World Health Care UCITS ETF EUR Acc",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "HWOE.PA": {
        "name": "HSBC MSCI World UCITS ETF EUR Hedged (Acc) EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "IMIE.PA": {
        "name": "SPDR MSCI ACWI IMI",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "IWDS.PA": {
        "name": "iShares MSCI World Swap UCITS ETF USD Acc",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "LWCR.PA": {
        "name": "Amundi MSCI World ESG Climate Net Zero Ambition CTB UCITS ETF Acc EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "LWLD.PA": {
        "name": "Amundi MSCI World (2x) Leveraged UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "MWRD.PA": {
        "name": "Amundi MSCI World UCITS ETF DR USD Acc (EUR)",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "PABW.PA": {
        "name": "Amundi MSCI World Climate Paris Aligned UCITS ETF - Acc EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "TNOW.PA": {
        "name": "Amundi MSCI World Information Technology UCITS ETF EUR Acc EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WEMT2.PA": {
        "name": "BNP Paribas Easy MSCI World ESG Filtered Min TE UCITS ETF EUR Cap",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WESE.PA": {
        "name": "Amundi MSCI World SRI Climate Net Zero Ambition PAB UCITS ETF EUR Hedged Acc EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WEWEU.PA": {
        "name": "BNP PARIBAS Easy ICAV - BNP Paribas Easy MSCI World Equal Weight Select UCITS ETF EUR CAPITALISATION",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WLD.PA": {
        "name": "Lyxor UCITS MSCI World D-EUR",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WLDC.PA": {
        "name": "Lyxor MSCI World UCITS ETF Acc",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WLDH.PA": {
        "name": "Amundi MSCI World II UCITS ETF EUR Hedged Dist",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WLDHC.PA": {
        "name": "Amundi MSCI World II UCITS ETF EUR Hedged Acc",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WPEA.PA": {
        "name": "iShares MSCI World Swap PEA UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },
    "WRD.PA": {
        "name": "HSBC MSCI World UCITS ETF",
        "sleeve": SLEEVE_CORE, "category": "Monde",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ÉTATS-UNIS
    # ══════════════════════════════════════════════════════════════════════
    "CL2.PA": {
        "name": "Amundi ETF Leveraged MSCI USA Daily UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "EKLDC.PA": {
        "name": "BNP Paribas Easy MSCI USA SRI PAB UCITS ETF EUR Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "EKUS.PA": {
        "name": "BNP Paribas Easy MSCI USA SRI S-Series PAB 5% Capped UCITS ETF EUR Distribution",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "ENAM.PA": {
        "name": "BNP Paribas Easy MSCI North America ESG Filtered Min TE UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "ESE.PA": {
        "name": "EasyETF - BNP Paribas Easy S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "ESEH.PA": {
        "name": "BNP Paribas Easy S&P 500 UCITS ETF EUR H",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "EWSP.PA": {
        "name": "iShares S&P 500 Equal Weight UCITS ETF USD (Acc)",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "HDLV.PA": {
        "name": "Invesco S&P 500 High Dividend Low Volatility UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "HHH.PA": {
        "name": "HSBC S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "HIUS.PA": {
        "name": "HSBC MSCI USA Islamic Screened UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "HSPA.PA": {
        "name": "HSBC S&P 500 UCITS ETF USD (Acc) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "LOWV.PA": {
        "name": "SPDR S&P 500 Low Volatility UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "MUS.PA": {
        "name": "HSBC MSCI USA UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "MUSA.PA": {
        "name": "iShares MSCI USA Swap UCITS ETF USD (Acc) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "NRAM.PA": {
        "name": "AMUNDI MSCI North America ESG Climate Net Zero Ambition CTB UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "P500H.PA": {
        "name": "Amundi ETF PEA S&P 500 UCITS ETF Daily Hedged EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "PABH.PA": {
        "name": "Amundi S&P 500 Climate Paris Aligned UCITS ETF Acc EUR HEDGED",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "PABU.PA": {
        "name": "Amundi S&P 500 Climate Paris Aligned UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "PE500.PA": {
        "name": "Amundi ETF PEA S&P 500 UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "PSP5.PA": {
        "name": "Lyxor PEA S&P 500 UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "PSPH.PA": {
        "name": "Lyxor PEA S&P 500 UCITS ETF Couverte en EUR Capi",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "S500.PA": {
        "name": "Amundi S&P 500 ESG UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "S500H.PA": {
        "name": "Amundi S&P 500 Screened UCITS ETF - Acc EUR HEDGED",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "SP5.PA": {
        "name": "Amundi Core S&P 500 Swap UCITS ETF EUR Dist",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "SP5C.PA": {
        "name": "Amundi Core S&P 500 Swap UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "SP5H.PA": {
        "name": "Amundi S&P 500 II UCITS ETF EUR Hedged Dist EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "SPEA.PA": {
        "name": "iShares S&P 500 Swap PEA UCITS ETF EUR (Acc)",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "SPEEU.PA": {
        "name": "BNP Paribas Easy S&P 500 ESG UCITS ETF EUR Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "SPY5.PA": {
        "name": "SPDR S&P 500 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "USA.PA": {
        "name": "Lyxor UCITS MSCI USA D-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "USAC.PA": {
        "name": "Amundi MSCI USA ESG Climate Net Zero Ambition CTB UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "USAS.PA": {
        "name": "Amundi MSCI USA Screened UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },
    "USVE.PA": {
        "name": "AMUNDI PEA MSCI USA VALUE ESG UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "États-Unis",
    },

    # ══════════════════════════════════════════════════════════════════════
    # TECH / NASDAQ
    # ══════════════════════════════════════════════════════════════════════
    "EQQQ.PA": {
        "name": "Invesco EQQQ NASDAQ-100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Tech / Nasdaq",
    },
    "NDXH.PA": {
        "name": "Amundi Nasdaq-100 EUR Hedged Daily UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Tech / Nasdaq",
    },
    "PANX.PA": {
        "name": "Amundi ETF PEA Nasdaq-100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Tech / Nasdaq",
    },
    "PNAS.PA": {
        "name": "Amundi PEA Nasdaq-100 UCITS ETF S-Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Tech / Nasdaq",
    },
    "PUST.PA": {
        "name": "Lyxor PEA Nasdaq 100 UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Tech / Nasdaq",
    },
    "UST.PA": {
        "name": "Amundi Nasdaq-100 II UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Tech / Nasdaq",
    },

    # ══════════════════════════════════════════════════════════════════════
    # EUROPE
    # ══════════════════════════════════════════════════════════════════════
    "50E.PA": {
        "name": "HSBC EURO STOXX 50 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "BNK.PA": {
        "name": "Lyxor Index Fund - Lyxor Stoxx Europe 600 Banks UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "BNKE.PA": {
        "name": "Amundi Euro Stoxx Banks UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "BRES.PA": {
        "name": "Multi Units Luxembourg - Amundi STOXX Europe 600 Basic Resources UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "BSX.PA": {
        "name": "Lyxor UCITS Stoxx 50 Daily Short",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "BXX.PA": {
        "name": "Lyxor UCITS Stoxx 50 Daily Double Short",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "CD8.PA": {
        "name": "Amundi ETF MSCI EMU High Dividend UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "CD9.PA": {
        "name": "Amundi MSCI Europe High Dividend UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "CHM.PA": {
        "name": "Amundi STOXX Europe 600 Basic Materials UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "CMU.PA": {
        "name": "Amundi MSCI EMU ESG Leaders Select UCITS ETF DR EUR (C)",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "CU9.PA": {
        "name": "Amundi ETF MSCI Europe ex EMU UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "EEMU.PA": {
        "name": "BNP Paribas Easy MSCI EMU Ex CW UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "EESG.PA": {
        "name": "Amundi MSCI EMU SRI Climate Paris Aligned - UCITS ETF DR (C) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "EEUE.PA": {
        "name": "BNP Paribas Easy MSCI Europe ESG Filtered Min TE UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "EMUE.PA": {
        "name": "State Street SPDR MSCI EMU UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ENRG.PA": {
        "name": "Multi Units Luxembourg - Amundi STOXX Europe 600 Energy ESG Screened UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ERO.PA": {
        "name": "SPDR MSCI Europe UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ESGE.PA": {
        "name": "Amundi MSCI Europe ESG Selection UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ESGH.PA": {
        "name": "Amundi MSCI Europe ESG Selection UCITS ETF EUR Hedged Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ETBB.PA": {
        "name": "BNP Paribas Easy Euro Stoxx 50 UCITS ETF EUR C/D",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ETDD.PA": {
        "name": "BNP Paribas Easy Euro Stoxx 50 UCITS ETF EUR C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ETZ.PA": {
        "name": "BNP Paribas Easy Stoxx Europe 600 UCITS ETF EUR C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "ETZD.PA": {
        "name": "BNP Paribas Easy Stoxx Europe 600 UCITS H",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "EUHD.PA": {
        "name": "PowerShares EURO STOXX High Dividend Low Volatility UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "FOO.PA": {
        "name": "Lyxor Index Fund - Lyxor Stoxx Europe 600 Food & Beverage UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "HEU.PA": {
        "name": "HSBC MSCI Europe UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "HIPS.PA": {
        "name": "HSBC MSCI Europe Islamic Screened UCITS ETF EUR Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "HLT.PA": {
        "name": "Lyxor Index Fund - Lyxor STOXX Europe 600 Healthcare UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "IND.PA": {
        "name": "Lyxor Index Fund - Lyxor STOXX Europe 600 Industrial Goods & Services UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "INS.PA": {
        "name": "Lyxor Index Fund - Lyxor STOXX Europe 600 Insurance UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "LWCE.PA": {
        "name": "Amundi MSCI Europe Climate Paris Aligned UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MEU.PA": {
        "name": "Lyxor UCITS MSCI Europe D-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MEUD.PA": {
        "name": "Amundi Stoxx Europe 600 UCITS ETF C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MFE.PA": {
        "name": "Lyxor UCITS MSCI EMU",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MFEC.PA": {
        "name": "Amundi MSCI EMU UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MFED.PA": {
        "name": "Amundi MSCI EMU ESG CTB Net Zero Ambition UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MSE.PA": {
        "name": "Amundi EURO STOXX 50 II UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MSES.PA": {
        "name": "Amundi EuroStoxx 50 II UCITS ETF S-Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "MUSRI.PA": {
        "name": "BNP Paribas Easy MSCI EMU SRI PAB UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "PABZ.PA": {
        "name": "Amundi MSCI EMU Climate Paris Aligned UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "PCEU.PA": {
        "name": "Amundi ETF PEA MSCI Europe UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "S6EW.PA": {
        "name": "Ossiam Stoxx Europe 600 Equal Weight NR UCITS 1C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "SRIE.PA": {
        "name": "BNP Paribas Easy MSCI Europe SRI S-Series PAB 5% Capped UCITS ETF Distribution",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "SRIEC.PA": {
        "name": "BNP Paribas Easy MSCI Europe SRI PAB UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STK.PA": {
        "name": "SPDR MSCI Europe Technology UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STN.PA": {
        "name": "SPDR MSCI Europe Energy UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STP.PA": {
        "name": "SSgA SPDR ETFs Europe II Public Limited Company - SPDR MSCI Europe Materials UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STQ.PA": {
        "name": "SPDR MSCI Europe Industrials UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STR.PA": {
        "name": "SPDR MSCI Europe Consumer Discretionary UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STS.PA": {
        "name": "SSgA SPDR ETFs Europe II Public Limited Company - SPDR MSCI Europe Consumer Staples UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STT.PA": {
        "name": "SSgA SPDR ETFs Europe II Public Limited Company - SPDR MSCI Europe Telecommunications UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STU.PA": {
        "name": "State Street SPDR MSCI Europe Utilities UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STW.PA": {
        "name": "SPDR MSCI Europe Health Care UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "STZ.PA": {
        "name": "SSgA SPDR ETFs Europe II Public Limited Company - SPDR MSCI Europe Financials UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "TELE.PA": {
        "name": "Lyxor Index Fund - Lyxor Stoxx Europe 600 Telecommunications UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "TNO.PA": {
        "name": "Multi Units Luxembourg - Amundi STOXX Europe 600 Technology UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "TRV.PA": {
        "name": "Amundi STOXX Europe 600 Consumer Discretionary UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "UTI.PA": {
        "name": "Lyxor Index Fund - Lyxor Stoxx Europe 600 Utilities UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "VAL.PA": {
        "name": "Lyxor Index Fund - Lyxor MSCI EMU Value (DR) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },
    "XEU.PA": {
        "name": "Xtrackers MSCI Europe UCITS ETF 1C EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Europe",
    },

    # ══════════════════════════════════════════════════════════════════════
    # FRANCE
    # ══════════════════════════════════════════════════════════════════════
    "BX4.PA": {
        "name": "Lyxor UCITS CAC 40 Daily Double Short",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "France",
    },
    "CA40.PA": {
        "name": "Amundi CAC 40 UCITS ETF S Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "France",
    },
    "CAC.PA": {
        "name": "Amundi CAC 40 UCITS ETF Dist",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "France",
    },
    "CACC.PA": {
        "name": "Lyxor CAC 40 (DR) UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "France",
    },
    "E40.PA": {
        "name": "BNP Paribas Easy CAC 40 ESG UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "France",
    },
    "LVC.PA": {
        "name": "Lyxor UCITS Daily Leverage CAC 40",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "France",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ALLEMAGNE
    # ══════════════════════════════════════════════════════════════════════
    "CG1.PA": {
        "name": "Amundi ETF DAX UCITS ETF DR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Allemagne",
    },
    "DAX.PA": {
        "name": "Multi Units Luxembourg - Lyxor DAX (DR) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Allemagne",
    },
    "DSD.PA": {
        "name": "Lyxor UCITS Daily ShortDAX x2 C-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Allemagne",
    },
    "LVD.PA": {
        "name": "Multi Units Luxembourg - Lyxor Daily LevDAX UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Allemagne",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ROYAUME-UNI
    # ══════════════════════════════════════════════════════════════════════
    "100H.PA": {
        "name": "Amundi FTSE 100 UCITS ETF EUR Hedged Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Royaume-Uni",
    },
    "C1U.PA": {
        "name": "Amundi FTSE 100 UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Royaume-Uni",
    },
    "L100.PA": {
        "name": "Multi Units Luxembourg - Lyxor FTSE 100 UCITS Fund",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Royaume-Uni",
    },
    "UKX.PA": {
        "name": "HSBC FTSE 100 UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Royaume-Uni",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ESPAGNE
    # ══════════════════════════════════════════════════════════════════════
    "CS1.PA": {
        "name": "Amundi IBEX 35 UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Espagne",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ITALIE
    # ══════════════════════════════════════════════════════════════════════
    "MIB.PA": {
        "name": "Lyxor FTSE MIB (DR) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Italie",
    },

    # ══════════════════════════════════════════════════════════════════════
    # JAPON
    # ══════════════════════════════════════════════════════════════════════
    "EJAH.PA": {
        "name": "BNP Paribas Easy MSCI Japan ESG Filtered Min TE UCITS ETF H EUR Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "EJAP.PA": {
        "name": "BNP Paribas Easy MSCI Japan ex CW UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "HPJP.PA": {
        "name": "HSBC MSCI Japan Climate Paris Aligned UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "JPN.PA": {
        "name": "Lyxor UCITS Japan (Topix) D-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "JPNH.PA": {
        "name": "Lyxor UCITS Japan Topix Daily Hedged D-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "MJP.PA": {
        "name": "HSBC MSCI Japan UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "PTPXE.PA": {
        "name": "Amundi ETF PEA Japan Topix UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "PTPXH.PA": {
        "name": "Amundi ETF PEA Japan Topix UCITS ETF Daily Hedged EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "SRIJ.PA": {
        "name": "BNP Paribas Easy MSCI Japan SRI S-Series PAB 5% Capped UCITS ETF Distribution",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },
    "SRIJC.PA": {
        "name": "BNP Paribas Easy MSCI Japan SRI PAB UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Japon",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ASIE PACIFIQUE
    # ══════════════════════════════════════════════════════════════════════
    "APX.PA": {
        "name": "Lyxor UCITS MSCI Asia Ex Japan C-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },
    "CP9.PA": {
        "name": "Amundi Index MSCI Pacific Ex Japen SRI PAB - UCITS ETF DR - EUR C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },
    "EPEJ.PA": {
        "name": "BNP Paribas Easy MSCI Pacific ex Japan ESG Filtered Min TE UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },
    "HSXD.PA": {
        "name": "HSBC Asia Pacific Ex Japan Screened Equity UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },
    "MXJ.PA": {
        "name": "HSBC MSCI Pacific ex Japan UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },
    "OP6E.PA": {
        "name": "Ossiam Lux Bloomberg Asia Pacific Ex Japan PAB NR C EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },
    "PAXJ.PA": {
        "name": "Lyxor MSCI Pacific Ex Japan UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Asie Pacifique",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ÉMERGENTS
    # ══════════════════════════════════════════════════════════════════════
    "ASI.PA": {
        "name": "Lyxor MSCI China ESG Leaders Extra (DR) UCITS ETF - Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "CC1.PA": {
        "name": "Amundi MSCI China Tech UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "CHINE.PA": {
        "name": "BNP PARIBAS EASY - MSCI China Min TE UCITS ETF EUR Acculumation EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "CNAA.PA": {
        "name": "Lyxor Fortune SG UCITS MSCI China A DR C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "CNY.PA": {
        "name": "HSBC MSCI China UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "CYEA.PA": {
        "name": "iShares China CNY Bond UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EEMK.PA": {
        "name": "BNP Paribas Easy MSCI Emerging ESG Filtered Min TE UCITS ETF EUR Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EISR.PA": {
        "name": "BNP Paribas Easy MSCI Emerging SRI S-Series PAB 5% Capped UCITS ETF EUR Distribution",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMHD.PA": {
        "name": "Invesco Markets III plc - Invesco FTSE Emerging Markets High Dividend Low Volatility UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMIS.PA": {
        "name": "BNP Paribas Easy MSCI Emerging SRI S-Series PAB 5% Capped UCITS ETF EUR Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMLD.PA": {
        "name": "SSgA SPDR ETFs Europe I Public Limited Company - SPDR Barclays Emerging Markets Local Bond UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMQQ.PA": {
        "name": "EMQQ Emerging Markets Internet UCITS ETF - Accumulating EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMRG.PA": {
        "name": "SSgA SPDR MSCI Emerging Markets UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMSRI.PA": {
        "name": "Amundi Index MSCI Emerging Markets SRI UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "EMXC.PA": {
        "name": "Amundi MSCI Emerging Ex China UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HCAS.PA": {
        "name": "HSBC MSCI CHINA A UCITS ETF USD (Acc) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HEMA.PA": {
        "name": "HSBC MSCI Emerging Markets UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HESS.PA": {
        "name": "HSBC MSCI Emerging Markets Small Cap Screened UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HEVS.PA": {
        "name": "HSBC MSCI Emerging Markets Value Screened UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HIES.PA": {
        "name": "HSBC MSCI Emerging Markets Islamic Screened Capped UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HSEM.PA": {
        "name": "HSBC Emerging Market Screened Equity UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "HYEM.PA": {
        "name": "VanEck Emerging Markets High Yield Bond UCITS ETF A USD",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "INR.PA": {
        "name": "Multi Units France - Lyxor MSCI India UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "LCCN.PA": {
        "name": "Amundi MSCI China UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "LEM.PA": {
        "name": "Multi Units France - Lyxor MSCI Emerging Markets UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "MTPI.PA": {
        "name": "iShares MSCI EM ex China UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "PAASI.PA": {
        "name": "Amundi ETF PEA MSCI Emerging Asia UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "PAEEM.PA": {
        "name": "Amundi ETF PEA MSCI Emerging Markets UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "PASI.PA": {
        "name": "Lyxor PEA China Enterprise HSCEI UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "PEMS.PA": {
        "name": "Amundi PEA MSCI Emerging ESG Transition UCITS ETF S-Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "PINR.PA": {
        "name": "Lyxor PEA Inde (MSCI India) UCITS ETF Capi",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "PLEM.PA": {
        "name": "Lyxor PEA MSCI Emerging Markets UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },
    "RIO.PA": {
        "name": "Lyxor MSCI Brazil UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Émergents",
    },

    # ══════════════════════════════════════════════════════════════════════
    # SMALL CAP
    # ══════════════════════════════════════════════════════════════════════
    "CEM.PA": {
        "name": "Amundi MSCI Europe Small Cap ESG Climate Net Zero Ambition CTB ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Small Cap",
    },
    "EESM.PA": {
        "name": "BNP Paribas Easy MSCI Europe Small Caps SRI S-Series PAB 5% Capped UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Small Cap",
    },
    "MMS.PA": {
        "name": "Amundi MSCI EMU Small Cap ESG CTB Net Zero Ambition UCITS ETF D EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Small Cap",
    },
    "R2US.PA": {
        "name": "SSgA SPDR ETFs Europe II Public Limited Company - SPDR Russell 2000 U.S. Small Cap UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Small Cap",
    },
    "SMC.PA": {
        "name": "SPDR MSCI Europe Small Cap UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Small Cap",
    },

    # ══════════════════════════════════════════════════════════════════════
    # MID CAP
    # ══════════════════════════════════════════════════════════════════════
    "SPY4.PA": {
        "name": "SSgA SPDR S&P 400 US Mid Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Mid Cap",
    },

    # ══════════════════════════════════════════════════════════════════════
    # SECTORIEL
    # ══════════════════════════════════════════════════════════════════════
    "AWAT.PA": {
        "name": "Amundi PEA Eau (MSCI Water) UCITS ETF Capi",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "CLMA.PA": {
        "name": "Guinness Sustainable Energy UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "CNB.PA": {
        "name": "Lyxor UCITS Euro Corporate Bond ex Financials C-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "CODW.PA": {
        "name": "Amundi S&P Global Consumer Discretionary ESG UCITS ETF DR EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "COSE.PA": {
        "name": "Amundi PEA S&P US Consumer Staples Screened UCITS ETF - Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "COSW.PA": {
        "name": "Amundi S&P Global Consumer Staples ESG UCITS ETF DR EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "DEFS.PA": {
        "name": "Amundi Stoxx Europe Defense UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "DFNS.PA": {
        "name": "VanEck Defense UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "DIGI.PA": {
        "name": "Digital Infrastructure and Connectivity UCITS ETF - Accumulating EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "DJE.PA": {
        "name": "Lyxor UCITS Dow Jones Industrial Average D-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "EMEH.PA": {
        "name": "BNP Paribas Easy Energy & Metals Enhanced Roll",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "ENG.PA": {
        "name": "BNP Paribas EASY ECPI Global ESG Infrastructure UCITS ETF EUR EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "GOAI.PA": {
        "name": "Amundi Stoxx Global Artificial Intelligence",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "GUARD.PA": {
        "name": "BNP Paribas Easy Bloomberg Europe Defense UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "INDW.PA": {
        "name": "Amundi S&P Global Industrials ESG UCITS ETF DR EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "INRE.PA": {
        "name": "iShares Global Clean Energy Transition UCITS ETF USD (Acc) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "MATW.PA": {
        "name": "Amundi S&P Global Materials ESG UCITS ETF DR EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "NRGW.PA": {
        "name": "Amundi S&P Global Energy Carbon Reduced UCITS ETF DR EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "NRJ.PA": {
        "name": "Multi Units France - Lyxor New Energy (DR) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "NRJC.PA": {
        "name": "Amundi MSCI New Energy UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "PDJE.PA": {
        "name": "Lyxor PEA Dow Jones Industrial Average UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "TELW.PA": {
        "name": "Amundi S&P Global Communication Services ESG UCITS ETF DR EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "UNIC.PA": {
        "name": "Amundi MSCI Disruptive Technology UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "WAT.PA": {
        "name": "Multi Units France - Lyxor World Water UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },
    "WELL.PA": {
        "name": "Harbor Health Care UCITS ETF - Accumulating EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Sectoriel",
    },

    # ══════════════════════════════════════════════════════════════════════
    # DIVIDENDES
    # ══════════════════════════════════════════════════════════════════════
    "EDIV.PA": {
        "name": "Amundi S&P Eurozone Dividend Aristocrat Screened UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Dividendes",
    },
    "EUDV.PA": {
        "name": "SSgA SPDR ETFs Europe I Public Limited Company - SPDR S&P Euro Dividend Aristocrats UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Dividendes",
    },
    "SEL.PA": {
        "name": "Lyxor UCITS Stoxx Europe Select Dividend 30",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Dividendes",
    },
    "TDIV.PA": {
        "name": "VanEck Morningstar Developed Markets Dividend Leaders UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Dividendes",
    },

    # ══════════════════════════════════════════════════════════════════════
    # FACTEUR
    # ══════════════════════════════════════════════════════════════════════
    "ELLE.PA": {
        "name": "Amundi Global Gender Equality ETF Accumulation EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Facteur",
    },
    "SGQE.PA": {
        "name": "Lyxor SG European Quality Income NTR UCITS D",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Facteur",
    },
    "SGQI.PA": {
        "name": "Multi Units Luxembourg - Lyxor SG Global Quality Income NTR UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Facteur",
    },

    # ══════════════════════════════════════════════════════════════════════
    # ESG / SRI
    # ══════════════════════════════════════════════════════════════════════
    "BSRIC.PA": {
        "name": "Bnp Paribas Easy -  Aggregate Bond Sri Fossil Free",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "BSRID.PA": {
        "name": "Bnp Paribas Easy -  Aggregate Bond Sri Fossil Free",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "CHIP.PA": {
        "name": "Lyxor MSCI Semiconductors ESG Filtered UCITS ETF - Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "CMUD.PA": {
        "name": "AM EMU ESG LEAD D",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EDEU.PA": {
        "name": "BNP Paribas Easy ESG Equity Dividend Europe UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EGRO.PA": {
        "name": "BNP Paribas Easy ESG Growth Europe UCITS ETF EUR Cap EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EMBH.PA": {
        "name": "BNP Paribas Easy JPM ESG EMBI Global Diversified Composite UCITS ETF H EUR Capitalisation EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EPAB.PA": {
        "name": "Amundi S&P Eurozone Climate Paris Aligned UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EQUA.PA": {
        "name": "BNP Paribas Easy ESG Equity Quality Europe UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EUDIV.PA": {
        "name": "Lyxor S&P Eurozone ESG Dividend Aristocrats (DR) UCITS ETF EUR Dis",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EUMV.PA": {
        "name": "Ossiam Europe ESG Machine Learning ETF UCITS 1C (EUR)",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EVAE.PA": {
        "name": "BNP Paribas Easy ESG Equity Value Europe UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "EVOE.PA": {
        "name": "BNP Paribas Easy ESG Equity Low Vol Europe UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "GEMU.PA": {
        "name": "BNP Paribas Easy JPM ESG EMU Government Bond IG 3-5 Y UCITS ETF Capitalisation EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "GEU3C.PA": {
        "name": "BNP Paribas Easy JPM ESG EMU Government Bond IG 1-3Y UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "GEU3D.PA": {
        "name": "BNP Paribas Easy JPM ESG EMU Government Bond IG 1-3Y",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "GSSBD.PA": {
        "name": "BNP PARIBAS EASY - JPM ESG Green Social & Sustainability IG Bond UCITS ETF EUR Capitalisation EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "GSSBO.PA": {
        "name": "BNP PARIBAS EASY - JPM ESG Green Social & Sustainability IG Bond UCITS ETF EUR Distribution",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "HSRID.PA": {
        "name": "BNPP EHY SRI D ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "HYDRO.PA": {
        "name": "BNP Paribas Easy ECPI Global ESG Hydrogen Economy UCITS ETF EUR Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "HYSRI.PA": {
        "name": "BNP Paribas Easy € High Yield SRI Fossil Free UCITS ETF EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "IQEC.PA": {
        "name": "IndexIQ Factors Sustainable Corporate Euro Bond UCITS ETF Dis",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "IQEE.PA": {
        "name": "IndexIQ Factors Sustainable Europe Equity UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "IQJP.PA": {
        "name": "IndexIQ Factors Sustainable Japan Equity UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "JBEM.PA": {
        "name": "BNP Paribas Easy JPM ESG EMU Govt Bd IG UCITS ETF Capitalisation",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "MOAT.PA": {
        "name": "VanEck Morningstar US ESG Wide Moat UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "QUED.PA": {
        "name": "BNP Paribas Easy ESG Equity Quality Europe UCITS ETF Dis",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "SRIC.PA": {
        "name": "BNP Paribas Easy € Corp Bond SRI PAB UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "SRIC3.PA": {
        "name": "BNP Paribas Easy € Corp Bond SRI PAB 1-3Y UCITS ETF Inc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "SRIC5.PA": {
        "name": "BNP Paribas Easy € Corp Bond SRI PAB 3-5Y UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "SRIC6.PA": {
        "name": "BNP Paribas Easy € Corp Bond SRI PAB 3-5Y UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "SRICD.PA": {
        "name": "BNP Paribas Easy € Corp Bond SRI PAB UCITS ETF Distribution EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "VALD.PA": {
        "name": "BNP Paribas Easy ESG Equity Value Europe UCITS ETF Dis",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },
    "VLED.PA": {
        "name": "BNP Paribas Easy ESG Equity Low Vol Europe UCITS ETF Dis",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "ESG / SRI",
    },

    # ══════════════════════════════════════════════════════════════════════
    # OBLIGATIONS
    # ══════════════════════════════════════════════════════════════════════
    "26ID.PA": {
        "name": "iShares iBonds Dec 2026 Term $ Corp UCITS ETF USD Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "28ID.PA": {
        "name": "iShares iBonds Dec 2028 Term $ Corp UCITS ETF USD Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "28IY.PA": {
        "name": "iShares iBonds Dec 2028 Term EUR Italy Government Bond UCITS ETF EUR (Dist)",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "B26A.PA": {
        "name": "iShares iBonds Dec 2026 Term € Corp UCITS ETF EUR (Acc) EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "B28A.PA": {
        "name": "iShares iBonds Dec 2028 Term € Corp UCITS ETF EUR (Acc) EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "C53D.PA": {
        "name": "Amundi Euro Government Bond 5-7Y UCITS ETF Dist EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "CLIM.PA": {
        "name": "Lyxor Green Bond DR UCITS C-EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "CRP.PA": {
        "name": "Lyxor UCITS Corporate Bond C-EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "DI27.PA": {
        "name": "iShares V PLC - iShares iBonds Dec 2027 Term $ Corp UCITS ETF USD Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "EAGG.PA": {
        "name": "SPDR Barclays Euro Aggregate Bond UCITS",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "EMGA.PA": {
        "name": "iShares J.P. Morgan EM Local Govt Bond UCITS ETF USD (Acc)",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "ERTH.PA": {
        "name": "Amundi Euro Government Green Bond UCITS ETF Acc EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "EUCO.PA": {
        "name": "SPDR Barclays Euro Corporate Bond UCITS",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "FM26.PA": {
        "name": "Amundi Fixed Maturity 2026 Euro Government Bond Broad UCITS ETF Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "FM27.PA": {
        "name": "Amundi Fixed Maturity 2027 Euro Government Bond Broad UCITS ETF Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "FM29.PA": {
        "name": "Amundi Fixed Maturity 2029 Euro Government Bond Broad UCITS ETF Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "GILS.PA": {
        "name": "Lyxor UCITS Iboxx GBP Gilts",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "GOVS.PA": {
        "name": "SPDR Barclays Capital 1-3 Yr Euro Govt Bond",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "IB27.PA": {
        "name": "iShares V PLC - iShares iBonds Dec 2027 Term € Corp UCITS ETF EUR Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "IBE7.PA": {
        "name": "iShares V PLC - iShares iBonds Dec 2027 Term € Corp UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "IU29-EUR.PA": {
        "name": "iShares iBonds Dec 2029 Term $",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "JNKE.PA": {
        "name": "SSgA SPDR ETFs Europe I Public Limited Company - SPDR Barclays Euro High Yield Bond UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MA13.PA": {
        "name": "Lyxor UCITS EuroMTS Highest Rated Macro-Weighted Govt Bond 1-3Y DR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MA35.PA": {
        "name": "Lyxor UCITS EuroMTS Highest Rated Macro-Weighted Govt Bond 3-5Y DR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MAA.PA": {
        "name": "Lyxor EuroMTS Highest Rated Macro-Weighted Government Bond DR UCITS C",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MTA.PA": {
        "name": "Amundi Euro Government Bond 1-3Y UCITS ETF Acc EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MTB.PA": {
        "name": "Amundi Euro Government Bond 3-5Y UCITS ETF Acc EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MTD.PA": {
        "name": "Amundi Euro Government Bond 7-10Y UCITS ETF Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MTE.PA": {
        "name": "MULTI-UNITS LUXEMBOURG - Lyxor Euro Government Bond 10-15Y (DR) UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "MTH.PA": {
        "name": "Amundi Euro Government Bond 25+Y UCITS ETF Acc",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "PLAN.PA": {
        "name": "Multi Units Luxembourg - Lyxor Corporate Green Bond (DR) UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "SEUC.PA": {
        "name": "SSgA SPDR ETFs Europe I plc - SPDR Barclays 0-3 Year Euro Corporate Bond UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "TSYE.PA": {
        "name": "SPDR Barclays Cap US Treasury Bond",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "US13.PA": {
        "name": "Lyxor UCITS iBoxx USD Treasuries 1-3Y DR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "US37.PA": {
        "name": "Lyxor US Treasury 3-7Y (DR) UCITS ETF EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "USHY.PA": {
        "name": "Lyxor BofAML $ High Yield Bond UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "USIH.PA": {
        "name": "Amundi USD Corporate Bond PAB Net Zero Ambition UCITS ETF EUR Hedged D",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },
    "X1GD.PA": {
        "name": "Amundi Govt Bond Lowest Rated EuroMTS Investment Grade UCITS D",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Obligations",
    },

    # ══════════════════════════════════════════════════════════════════════
    # MONÉTAIRE
    # ══════════════════════════════════════════════════════════════════════
    "CSH2.PA": {
        "name": "Multi Units Luxembourg - Amundi Smart Overnight Return UCITS ETF Acc EUR",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Monétaire",
    },
    "OBLI.PA": {
        "name": "Amundi PEA Euro Court Terme UCITS ETF",
        "sleeve": SLEEVE_DEFENSIVE, "category": "Monétaire",
    },

    # ══════════════════════════════════════════════════════════════════════
    # AUTRES
    # ══════════════════════════════════════════════════════════════════════
    "5OGE.PA": {
        "name": "Ossiam Shiller Barclays Cape Global Sector Value Fund 1C (EUR) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "AEJ.PA": {
        "name": "Lyxor UCITS MSCI AC Asia-Pacific Ex Japan C-E",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "AIGPP.PA": {
        "name": "WisdomTree Precious Metals EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "ANRJ.PA": {
        "name": "Amundi Global Hydrogen UCITS ETF - Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "BRNT.PA": {
        "name": "WT Brent Crude Oil",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "BULLP.PA": {
        "name": "WisdomTree Gold EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "C3M.PA": {
        "name": "Amundi ETF Govies 0-6 Months EuroMTS Investment Grade UCITS ETF DR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "C5E.PA": {
        "name": "Amundi Stoxx Europe 50 UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CAPE.PA": {
        "name": "Ossiam Shiller Barclays Cape Europe Sector Value TR UCITS",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CAPU.PA": {
        "name": "Ossiam Shiller Barclays Cape US Sector Value TR 1C (EUR)",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CEC.PA": {
        "name": "Multi Units Luxembourg - Lyxor MSCI Eastern Europe Ex Russia UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CF1.PA": {
        "name": "Amundi ETF MSCI France UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "COMO.PA": {
        "name": "Amundi Bl Equal-weight Comm ex-A UE A",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "COPAP.PA": {
        "name": "WisdomTree Copper EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CRB.PA": {
        "name": "Lyxor Commodities Refinitiv/CoreCommodity CRB TR UCITS ETF - Acc-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CRUDP.PA": {
        "name": "WisdomTree WTI Crude Oil EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "CSH.PA": {
        "name": "Lyxor Euro Cash UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "DBMFE.PA": {
        "name": "iMGP DBi Managed Futures R EUR ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "DFND.PA": {
        "name": "iShares Global Aerospace & Defence UCITS ETF USD (Acc)",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "DGGE.PA": {
        "name": "iShares Digital Entertainment and Education UCITS ETF USD (Acc) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "EBUY.PA": {
        "name": "Amundi MSCI Digital Economy UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "ECN.PA": {
        "name": "BNP Paribas Easy Low Carbon 100 Europe PAB UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "EEA.PA": {
        "name": "BNP Paribas Easy FTSE EPRA/NAREIT Eurozone Capped UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "EEE.PA": {
        "name": "BNP Paribas Easy FTSE EPRA/NAREIT Eurozone Capped UCITS ETF QD Dis",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "ELCR.PA": {
        "name": "Amundi MSCI Smart Mobility UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "ESGO.PA": {
        "name": "AuAg Gold Mining UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "FGBL.PA": {
        "name": "First Trust Global Equity Income UCITS ETF Class A USD",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GBS.PA": {
        "name": "Gold Bullion Securities ETC",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GDIG.PA": {
        "name": "VanEck S&P Global Mining UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GDX.PA": {
        "name": "VanEck Gold Miners UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GDXJ.PA": {
        "name": "VanEck Junior Gold Miners UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GILI.PA": {
        "name": "Lyxor FTSE Actuaries UK Gilts Inflation-Linked (DR) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GOLD-EUR.PA": {
        "name": "Amundi Physical Gold ETC C EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GOLD.PA": {
        "name": "Amundi Physical Gold ETC C EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GRCTB.PA": {
        "name": "BNP Paribas EASY FTSE EPRA Nareit Global Developed Green CTB UCITS ETF EUR Cap EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GRE.PA": {
        "name": "Multi Units France - Lyxor MSCI Greece UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "GREAL.PA": {
        "name": "BNP Paribas Easy FTSE EPRA Nareit Developed Europe Green CTB UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "HSEU.PA": {
        "name": "HSBC Europe Screened Equity UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "HSJA.PA": {
        "name": "HSBCJAPNSUSUSDDIST",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "HSTE.PA": {
        "name": "HSBC ETFS PLC - HSBC Hang Seng Tech UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "HSUD.PA": {
        "name": "HSBC USA Screened Equity UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "HSUK.PA": {
        "name": "HSBC UK SUS EQ ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "HSWD.PA": {
        "name": "HSBC Developed World Screened Equity UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "IART.PA": {
        "name": "iShares AI Innovation Active UCITS ETF USD (Acc) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "IEMID.PA": {
        "name": "Indépendance AM Europe Mid UCITS ETF E (C) EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "INDEP.PA": {
        "name": "Amundi European Strategic Auton",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "INDO.PA": {
        "name": "Lyxor MSCI Indonesia UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "INFL.PA": {
        "name": "Lyxor EUR 2-10 Inflation Expectations UCITS C-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "INFU.PA": {
        "name": "Lyxor US$ 10Y Inflation Expectations UCITS ETF - C-USD EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "ITEK.PA": {
        "name": "HAN-GINS Tech Megatrend Equal Weight UCITS ETF - Accumulating EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "IU28-EUR.PA": {
        "name": "IU28-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "JEDI.PA": {
        "name": "VanEck Space Innovators UCITS ETF A USD Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "LCWLD.PA": {
        "name": "BNP PARIBAS EASY - Low Carbon 300 World PAB UCITS ETF EUR Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MEH.PA": {
        "name": "Lyxor UCITS FTSE EPRA/NAREIT Developed Europe D-EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MGT.PA": {
        "name": "Amundi DJ Global Titans 50 UCITS ETF Dist",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MILL.PA": {
        "name": "Amundi MSCI Millennials UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MLUX.PA": {
        "name": "Amundi PEA Luxe Mnd UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MSTY.PA": {
        "name": "Yieldmax MSTR Option Income Strategy ETC",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MTC.PA": {
        "name": "Multi Units Luxembourg - Lyxor EuroMTS 5-7Y Investment Grade (DR) UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MTF.PA": {
        "name": "Lyxor EuroMTS 15+Y Investment Grade UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MTI.PA": {
        "name": "Lyxor UCITS EuroMTS Inflation Linked Investment Grade DR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "MWO.PA": {
        "name": "Amundi FTSE EPRA/NAREIT Global Developed UCITS ETF D",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "NGASP.PA": {
        "name": "WisdomTree Natural Gas EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "NUCL.PA": {
        "name": "VanEck Uranium and Nuclear Technologies UCITS ETF A USD Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "OP2E.PA": {
        "name": "OSSIAM BLOOMBERG EUROZONE PAB NR EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "OP4E.PA": {
        "name": "OSSIAM BLOOMBERG EUROPE ex EUROZONE PAB NR 1C EUR EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "OP5E.PA": {
        "name": "OSSIAM BLOOMBERG JAPAN PAB NR EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "OP7H.PA": {
        "name": "Ossiam Bloomberg USA PAB UCITS ETF - 1A EUR Hedged Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "PAEJ.PA": {
        "name": "Lyxor PEA MSCI AC Asia-Pacific ex Japan UCITS C",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "PALAT.PA": {
        "name": "Amundi ETF PEA MSCI EM Latin America UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "PEU.PA": {
        "name": "Invesco Markets III plc - Invesco EuroMTS Cash 3 Months UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "PFT.PA": {
        "name": "Invesco FTSE RAFI US 1000 UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "PMEH.PA": {
        "name": "Amundi PEA Immobilier Europe (FTSE EPRA/NAREIT) UCITS ETF Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "PSPS.PA": {
        "name": "Amundi PEA SP 500 Scrn UCITS ETF S-Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "REMX.PA": {
        "name": "VanEck Rare Earth and Strategic Metals UCITS ETF A USD Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "REUSE.PA": {
        "name": "BNP Paribas Easy ECPI Circular Economy Leaders UCITS ETF Cap",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "RMAU.PA": {
        "name": "Royal Mint Responsibly Sourced Physical Gold ETC EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "SEME.PA": {
        "name": "iShares MSCI Global Semiconductors UCITS ETF USD Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "SLVRP.PA": {
        "name": "WisdomTree Silver EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "STPU.PA": {
        "name": "Amundi US Curve steepening 2-10Y UCITS ETF Acc EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "TRYP.PA": {
        "name": "HANetf ICAV - US Global Investors Travel UCITS ETF EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "TUR.PA": {
        "name": "MULTI UNITS LUXEMBOURG - Lyxor MSCI Turkey UCITS ETF",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "TWN.PA": {
        "name": "Multi Units Luxembourg - Lyxor Msci Taiwan Ucits Etf",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "VRTC.PA": {
        "name": "VRTC",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "VVMX.PA": {
        "name": "VanEck Rare Earth and Strategic Metals UCITS ETF A USD Acc",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },
    "WEATP.PA": {
        "name": "WisdomTree Wheat EUR",
        "sleeve": SLEEVE_AGGRESSIVE, "category": "Autres",
    },

}


def get_etf_metadata() -> list[dict]:
    """Return list of all ETF metadata dicts."""
    return [
        {"ticker": k, **v}
        for k, v in PEA_UNIVERSE.items()
    ]


def get_all_tickers() -> list[str]:
    return list(PEA_UNIVERSE.keys())


def get_satellite_tickers() -> list[str]:
    """All non-core tickers (aggressive + defensive, excluding the anchor)."""
    return [
        t for t, m in PEA_UNIVERSE.items()
        if m["sleeve"] != SLEEVE_CORE and t != CORE_ANCHOR
    ]


def get_categories() -> list[str]:
    seen = []
    for m in PEA_UNIVERSE.values():
        c = m["category"]
        if c not in seen:
            seen.append(c)
    return seen
