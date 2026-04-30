"""
Alloc — PEA Radar  (Streamlit edition)
Stratégie momentum 80/20 sur ETF éligibles PEA Euronext Paris.
"""

from __future__ import annotations

import math
from functools import partial

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import api.db as price_db
from data.pea_universe import CORE_ANCHOR, get_etf_metadata, get_all_tickers
from portfolio.optimizer import build_proposal, build_rebalance_orders, run_backtest
from portfolio.store import (
    DEFAULT_SETTINGS, delete_holding, enrich_holdings_with_prices,
    get_holdings, get_settings, load, save, upsert_holding,
)
from strategy.factors import build_all_signals, signals_to_dataframe

# ── Colors ────────────────────────────────────────────────────────────────────
C = {
    "bg":       "#F5F0E7",
    "surface":  "#FFFCF5",
    "text":     "#17201A",
    "text2":    "#5C6760",
    "green":    "#156B49",
    "green2":   "#3A8C62",
    "amber":    "#BD6E1B",
    "red":      "#BD3A33",
    "neutral":  "#8A9290",
    "graphite": "#2C3830",
    "border":   "#DDD8CE",
}

ACTION_COLORS = {"buy": C["green"], "sell": C["red"], "hold": C["neutral"]}
ACTION_LABELS = {"buy": "Acheter", "sell": "Vendre", "hold": "Conserver"}

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PEA Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
  /* Global reset to warm ivory */
  .stApp {{ background-color: {C['bg']}; }}
  section[data-testid="stSidebar"] {{ background: {C['graphite']} !important; }}
  section[data-testid="stSidebar"] * {{ color: #E8E3DA !important; }}
  section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
  section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
  section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{ color: #9AADA4 !important; font-size: 0.78rem !important; }}

  /* Cards */
  .pea-card {{
    background: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
  }}
  .pea-metric-value {{
    font-size: 1.6rem;
    font-weight: 700;
    color: {C['text']};
    font-variant-numeric: tabular-nums;
  }}
  .pea-metric-label {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: {C['text2']};
    margin-bottom: 0.15rem;
  }}
  .pea-pill {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
  }}
  .pea-pill-green  {{ background: #D6EDE5; color: {C['green']}; }}
  .pea-pill-amber  {{ background: #F5E8D6; color: {C['amber']}; }}
  .pea-pill-red    {{ background: #F5D9D7; color: {C['red']};   }}
  .pea-pill-neutral{{ background: #E8E5E0; color: {C['neutral']}; }}

  .pea-divider {{ border-top: 1px solid {C['border']}; margin: 1rem 0; }}

  /* Rebalance order rows */
  .order-row {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid {C['border']};
    font-size: 0.85rem;
  }}
  .order-row:last-child {{ border-bottom: none; }}

  /* Table tweaks */
  .stDataFrame {{ border-radius: 8px; overflow: hidden; }}
  thead tr th {{ background: {C['surface']} !important; }}

  h2, h3 {{ color: {C['text']} !important; font-weight: 700; }}
  .stTabs [data-baseweb="tab"] {{ font-size: 0.9rem; font-weight: 600; }}
  .stTabs [data-baseweb="tab"][aria-selected="true"] {{ color: {C['green']} !important; border-bottom-color: {C['green']} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "doc" not in st.session_state:
    st.session_state.doc = load()
if "histories" not in st.session_state:
    st.session_state.histories = {}
if "signals" not in st.session_state:
    st.session_state.signals = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "data_badge" not in st.session_state:
    st.session_state.data_badge = ""


def _doc() -> dict:   return st.session_state.doc
def _settings() -> dict: return get_settings(_doc())
def _holdings() -> list: return get_holdings(_doc())
def _save():
    save(st.session_state.doc)


def _load_cached_histories() -> dict:
    price_db.init_db()
    histories = {}
    for ticker in get_all_tickers():
        df = price_db.load_prices(ticker)
        if df is not None and len(df) >= 20:
            histories[ticker] = df
    return histories


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## 📡 PEA Radar")
    st.markdown(f"<div style='color:#7A9E8E;font-size:0.78rem;margin-bottom:1rem'>Stratégie momentum 80/20</div>", unsafe_allow_html=True)

    cfg = _settings()

    capital_input = st.number_input(
        "Capital à allouer (€)",
        min_value=100.0,
        max_value=10_000_000.0,
        value=float(cfg["capital"]),
        step=500.0,
        format="%.0f",
    )

    top_n_input = st.slider(
        "ETF momentum (satellite)", 1, 10, int(cfg["top_n"]),
        help="Nombre d'ETF à sélectionner pour la poche 20 %",
    )

    st.markdown("---")

    db_settings = price_db.get_settings()
    source_label = db_settings.get("data_source", cfg.get("data_source", "cache"))
    years_input = int(db_settings.get("history_years", cfg.get("history_years", 2)))
    st.caption(f"Données en cache SQLite : {source_label} • {years_input} ans")

    st.markdown("---")

    if st.button("🔄 Lire le cache", type="primary", use_container_width=True):
        with st.spinner("Lecture des prix en cache…"):
            histories = _load_cached_histories()
            st.session_state.histories = histories
            meta_df = get_etf_metadata()
            st.session_state.signals = build_all_signals(histories, meta_df)
            st.session_state.data_loaded = True
            ok = len(histories)
            st.session_state.data_badge = f"✅ {ok} ETF chargés depuis SQLite — {source_label}"
        st.rerun()

    if st.session_state.data_badge:
        st.caption(st.session_state.data_badge)

    # Auto-load on first run from SQLite cache.
    if not st.session_state.data_loaded:
        with st.spinner("Lecture du cache…"):
            histories = _load_cached_histories()
            st.session_state.histories = histories
            meta_df = get_etf_metadata()
            st.session_state.signals = build_all_signals(histories, meta_df)
            st.session_state.data_loaded = True
            st.session_state.data_badge = f"⚡ Cache SQLite — {len(histories)} ETF"

    # Persist settings on change
    new_settings = {
        "broker_name":   cfg["broker_name"],
        "data_source":   source_label,
        "eodhd_api_key": cfg.get("eodhd_api_key", ""),
        "capital":       capital_input,
        "top_n":         top_n_input,
        "currency":      cfg["currency"],
        "history_years": years_input,
    }
    if new_settings != cfg:
        st.session_state.doc["settings"] = new_settings
        _save()


# ── Shortcuts ─────────────────────────────────────────────────────────────────
signals   = st.session_state.signals
histories = st.session_state.histories
settings  = _settings()
capital   = settings["capital"]
top_n     = settings["top_n"]
meta_df   = get_etf_metadata()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _pct(v: float) -> str:
    return f"{v*100:+.1f}%" if not math.isnan(v) else "—"

def _eur(v: float) -> str:
    return f"{v:,.0f} €"

def _pill(label: str, kind: str = "neutral") -> str:
    return f'<span class="pea-pill pea-pill-{kind}">{label}</span>'

def _rec_pill(rec: str) -> str:
    label = {"buy": "Fort", "hold": "Stable", "trim": "Faible", "avoid": "Éviter"}.get(rec, rec)
    kind  = {"buy": "green", "hold": "green", "trim": "amber", "avoid": "red"}.get(rec, "neutral")
    return _pill(label, kind)

def _score_color(score: float) -> str:
    if score >= 70: return C["green"]
    if score >= 55: return C["green2"]
    if score >= 40: return C["amber"]
    return C["red"]


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_strat, tab_etf, tab_portf, tab_settings = st.tabs([
    "📐 Stratégie",
    "📡 ETF & Scores",
    "💼 Portefeuille",
    "⚙️ Réglages",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — STRATÉGIE
# ══════════════════════════════════════════════════════════════════════════════
with tab_strat:
    if not signals:
        st.info("Cliquez sur **Charger les données** dans la barre latérale.")
        st.stop()

    proposal = build_proposal(signals, capital, CORE_ANCHOR, top_n)
    lines    = proposal["lines"]

    # ── KPIs ─────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    def _kpi(col, label, value, sub=""):
        col.markdown(f"""
        <div class="pea-card" style="text-align:center">
          <div class="pea-metric-label">{label}</div>
          <div class="pea-metric-value">{value}</div>
          {"<div style='font-size:0.78rem;color:"+C['text2']+"'>"+sub+"</div>" if sub else ""}
        </div>""", unsafe_allow_html=True)

    _kpi(k1, "Capital alloué",    _eur(capital))
    _kpi(k2, "Rend. attendu",     _pct(proposal["expected_return"]),  "estimation annualisée")
    _kpi(k3, "Volatilité est.",   _pct(proposal["expected_vol"]),     "annualisée")
    _kpi(k4, "Satellites actifs", str(proposal["n_satellites"]),
         "filtre 12M positif" if proposal["n_satellites"] > 0 else "filtre cash activé")

    # ── Allocation bar ────────────────────────────────────────────────────────
    core_w = 0.80
    sat_w  = 0.20 - proposal["cash_reserve_pct"]
    cash_w = proposal["cash_reserve_pct"]

    fig_bar = go.Figure()
    if core_w > 0:
        fig_bar.add_trace(go.Bar(x=[core_w * 100], y=[""], orientation="h",
                                 marker_color=C["green"], name="Socle Monde",
                                 text=f"80% Monde", textposition="inside",
                                 insidetextanchor="middle"))
    if sat_w > 0:
        fig_bar.add_trace(go.Bar(x=[sat_w * 100], y=[""], orientation="h",
                                 marker_color=C["amber"], name="Momentum",
                                 text=f"{sat_w*100:.0f}% Momentum", textposition="inside",
                                 insidetextanchor="middle"))
    if cash_w > 0:
        fig_bar.add_trace(go.Bar(x=[cash_w * 100], y=[""], orientation="h",
                                 marker_color=C["green2"], name="Liquidités",
                                 text=f"{cash_w*100:.0f}% Cash", textposition="inside",
                                 insidetextanchor="middle"))

    fig_bar.update_layout(
        barmode="stack", height=70,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False),
        font=dict(color=C["surface"], size=13, family="sans-serif"),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"<div style='font-size:0.78rem;color:{C['text2']};margin-bottom:1rem'>{proposal['rationale']}</div>",
                unsafe_allow_html=True)

    # ── Allocation table ──────────────────────────────────────────────────────
    st.markdown("### Plan d'allocation")
    for line in lines:
        sleeve_pill = {
            "core":       _pill("Socle", "green"),
            "aggressive": _pill("Momentum", "amber"),
            "cash":       _pill("Liquidités", "neutral"),
            "defensive":  _pill("Défensif", "neutral"),
        }.get(line["sleeve"], "")

        score_str = f"{line['score']:.1f}" if line["score"] is not None else "—"
        score_color = _score_color(line["score"]) if line["score"] is not None else C["neutral"]

        st.markdown(f"""
        <div class="pea-card" style="padding:0.75rem 1.25rem">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              {sleeve_pill}
              <span style="margin-left:0.5rem;font-weight:700;font-size:0.95rem">{line['ticker']}</span>
              <span style="margin-left:0.5rem;color:{C['text2']};font-size:0.85rem">{line['name']}</span>
            </div>
            <div style="text-align:right">
              <span style="font-weight:700;font-size:1.05rem;font-variant-numeric:tabular-nums">
                {line['weight']*100:.0f}%
              </span>
              <span style="margin-left:0.75rem;color:{C['text2']}">
                {_eur(line['value'])}
              </span>
              {"<span style='margin-left:0.75rem;font-size:0.8rem;color:"+score_color+";font-weight:600'>score "+score_str+"</span>" if line['score'] is not None else ""}
            </div>
          </div>
          <div style="margin-top:0.25rem;font-size:0.77rem;color:{C['text2']}">{line['rationale']}</div>
        </div>""", unsafe_allow_html=True)

    # ── Rebalance orders (if holdings) ────────────────────────────────────────
    holdings = _holdings()
    if holdings:
        enriched = enrich_holdings_with_prices(holdings, histories)
        orders   = build_rebalance_orders(enriched, proposal)
        active_orders = [o for o in orders if o["action"] != "hold" or o["current_value"] > 0]

        st.markdown("### Plan de rebalancement")
        st.markdown(f"<div class='pea-card'>", unsafe_allow_html=True)
        for o in active_orders:
            action_color = ACTION_COLORS[o["action"]]
            action_label = ACTION_LABELS[o["action"]]
            delta_str = (_eur(o["delta_value"]) if o["delta_value"] >= 0
                         else f"−{_eur(abs(o['delta_value']))}")
            st.markdown(f"""
            <div class="order-row">
              <div style="display:flex;align-items:center;gap:0.6rem">
                <span style="font-weight:700;color:{action_color};min-width:68px">{action_label}</span>
                <span style="font-weight:600">{o['ticker']}</span>
                <span style="color:{C['text2']};font-size:0.82rem">{o['name'][:30]}</span>
              </div>
              <div style="text-align:right;font-variant-numeric:tabular-nums;font-size:0.85rem">
                <span style="color:{C['text2']}">{o['current_weight']*100:.1f}% → </span>
                <span style="font-weight:600">{o['target_weight']*100:.1f}%</span>
                <span style="margin-left:0.5rem;color:{action_color};font-weight:600">{delta_str}</span>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Backtest ──────────────────────────────────────────────────────────────
    st.markdown("### Backtest — rebalancement mensuel")
    st.markdown(f"<div style='font-size:0.8rem;color:{C['text2']};margin-bottom:0.75rem'>"
                "Simulation sur données historiques. Les performances passées ne préjugent pas des futures.</div>",
                unsafe_allow_html=True)

    if st.button("▶ Lancer le backtest", type="primary"):
        with st.spinner("Backtest en cours…"):
            from strategy.factors import build_all_signals as _bsig

            def _signals_fn(snap):
                return _bsig(snap, meta_df)

            bt = run_backtest(
                histories, _signals_fn,
                capital=capital, top_n=top_n, core_ticker=CORE_ANCHOR,
            )

        if bt["n_days"] < 20:
            st.warning("Pas assez d'historique pour un backtest significatif.")
        else:
            eq  = bt["equity_curve"]
            bm  = bt["benchmark_curve"]

            fig_bt = go.Figure()
            fig_bt.add_trace(go.Scatter(
                x=eq.index, y=eq.values,
                name="Stratégie 80/20", fill="tozeroy",
                line=dict(color=C["green"], width=2),
                fillcolor="rgba(21,107,73,0.08)",
            ))
            fig_bt.add_trace(go.Scatter(
                x=bm.index, y=bm.values,
                name="Benchmark (ew)", line=dict(color=C["neutral"], width=1.5, dash="dash"),
            ))
            fig_bt.update_layout(
                height=360, hovermode="x unified",
                margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=C["text"]),
                legend=dict(orientation="h", y=1.05),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor=C["border"], tickprefix="€"),
            )
            st.plotly_chart(fig_bt, use_container_width=True)

            b1, b2, b3, b4, b5 = st.columns(5)
            def _bt_kpi(col, label, val, sub="", color=None):
                c = color or C["text"]
                col.markdown(f"""
                <div class="pea-card" style="text-align:center">
                  <div class="pea-metric-label">{label}</div>
                  <div style="font-size:1.25rem;font-weight:700;color:{c};font-variant-numeric:tabular-nums">{val}</div>
                  {"<div style='font-size:0.72rem;color:"+C['text2']+"'>"+sub+"</div>" if sub else ""}
                </div>""", unsafe_allow_html=True)

            _bt_kpi(b1, "TCAM stratégie",     _pct(bt["cagr"]),
                    f"BM {_pct(bt['benchmark_cagr'])}", C["green"] if bt["alpha"] > 0 else C["red"])
            _bt_kpi(b2, "Alpha",               _pct(bt["alpha"]),
                    color=C["green"] if bt["alpha"] > 0 else C["red"])
            _bt_kpi(b3, "Max Drawdown",        _pct(bt["max_drawdown"]),
                    f"BM {_pct(bt['benchmark_max_dd'])}", C["red"])
            _bt_kpi(b4, "Sharpe",              f"{bt['sharpe']:.2f}",
                    f"BM {bt['benchmark_sharpe']:.2f}")
            _bt_kpi(b5, "Transactions",        str(bt["trade_count"]))


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ETF & SCORES
# ══════════════════════════════════════════════════════════════════════════════
with tab_etf:
    if not signals:
        st.info("Cliquez sur **Charger les données**.")
        st.stop()

    sig_df = signals_to_dataframe(signals)

    # ── Momentum podium (top 3) ───────────────────────────────────────────────
    st.markdown("### 🏆 Podium momentum")
    podium_sigs = [s for s in signals if s["sleeve"] == "aggressive"][:3]
    podium_cols = st.columns(3)
    icons = ["🥇", "🥈", "🥉"]
    for i, (col, sig) in enumerate(zip(podium_cols, podium_sigs)):
        r12 = _pct(sig["r12M"]) if not math.isnan(sig["r12M"]) else "—"
        with col:
            st.markdown(f"""
            <div class="pea-card" style="text-align:center">
              <div style="font-size:2rem">{icons[i]}</div>
              <div style="font-weight:700;font-size:1rem;margin:0.25rem 0">{sig['ticker']}</div>
              <div style="font-size:0.78rem;color:{C['text2']};margin-bottom:0.5rem">{sig['name'][:30]}</div>
              <div style="font-size:1.4rem;font-weight:700;color:{_score_color(sig['score'])}">{sig['score']:.1f}</div>
              <div style="font-size:0.72rem;color:{C['text2']}">score composite</div>
              <div style="margin-top:0.4rem">{_rec_pill(sig['recommendation'])}</div>
              <div style="margin-top:0.3rem;font-size:0.78rem;color:{C['text2']}">12M : {r12}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='pea-divider'></div>", unsafe_allow_html=True)

    # ── Score detail for selected ETF ─────────────────────────────────────────
    st.markdown("### Analyse détaillée")
    col_sel, _ = st.columns([2, 3])
    with col_sel:
        all_tickers_list = [s["ticker"] for s in signals]
        selected = st.selectbox("Choisir un ETF", all_tickers_list,
                                format_func=lambda t: f"{t} — {next((s['name'] for s in signals if s['ticker']==t), t)}")

    sig = next((s for s in signals if s["ticker"] == selected), None)
    if sig:
        c1, c2 = st.columns([1, 1])
        with c1:
            # Score decomposition
            st.markdown(f"""
            <div class="pea-card">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem">
                <div>
                  <span style="font-weight:700;font-size:1.05rem">{sig['ticker']}</span>
                  <span style="margin-left:0.5rem;color:{C['text2']};font-size:0.85rem">{sig['name']}</span>
                </div>
                {_rec_pill(sig['recommendation'])}
              </div>
              <div style="font-size:2rem;font-weight:700;color:{_score_color(sig['score'])};font-variant-numeric:tabular-nums">
                {sig['score']:.1f}
              </div>
              <div style="font-size:0.72rem;color:{C['text2']};margin-bottom:1rem">score composite</div>
              <div class="pea-divider"></div>
              <div style="display:flex;justify-content:space-between;padding:0.4rem 0;font-size:0.85rem">
                <span style="color:{C['text2']}">Composante momentum</span>
                <span style="font-weight:600;color:{C['green'] if sig['momentum_component']>0 else C['red']}">{sig['momentum_component']:+.1f} pts</span>
              </div>
              <div style="display:flex;justify-content:space-between;padding:0.4rem 0;font-size:0.85rem">
                <span style="color:{C['text2']}">Tendance (SMA 200)</span>
                <span style="font-weight:600;color:{C['green'] if sig['above_sma200'] else C['red']}">{sig['trend_component']:+.1f} pts — {'au-dessus' if sig['above_sma200'] else 'en-dessous'}</span>
              </div>
              <div style="display:flex;justify-content:space-between;padding:0.4rem 0;font-size:0.85rem">
                <span style="color:{C['text2']}">Pénalité risque</span>
                <span style="font-weight:600;color:{C['amber']}">−{sig['risk_penalty']:.1f} pts</span>
              </div>
              <div style="display:flex;justify-content:space-between;padding:0.4rem 0;font-size:0.78rem;color:{C['text2']}">
                <span>Volatilité ann.</span>
                <span>{sig['annual_vol']*100:.1f}%</span>
              </div>
              <div style="display:flex;justify-content:space-between;padding:0.4rem 0;font-size:0.78rem;color:{C['text2']}">
                <span>Max drawdown (12M)</span>
                <span>{sig['max_drawdown']*100:.1f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)

            # Returns table
            rows = [
                ("1 mois",  sig["r1M"], None),
                ("3 mois",  sig["r3M"], 0.10),
                ("6 mois",  sig["r6M"], 0.18),
                ("12-1 mois", sig.get("r12_1M", math.nan), 0.45),
                ("12 mois", sig["r12M"], None),
            ]
            st.markdown(f"""
            <div class="pea-card">
              <div style="font-weight:700;margin-bottom:0.75rem">Rendements par période</div>
              {"".join(f'''
              <div style="display:flex;justify-content:space-between;padding:0.4rem 0;
                          border-bottom:1px solid {C['border']};font-size:0.85rem">
                <span style="color:{C['text2']}">{label} {f'<span style="font-size:0.72rem">(w={w:.0%})</span>' if w is not None else ''}</span>
                <span style="font-weight:600;color:{C['green'] if not math.isnan(r) and r>0 else C['red']}">{_pct(r)}</span>
              </div>''' for label, r, w in rows)}
            </div>""", unsafe_allow_html=True)

        with c2:
            # Price chart
            if selected in histories:
                hist = histories[selected]
                fig_price = go.Figure()
                fig_price.add_trace(go.Scatter(
                    x=hist.index, y=hist["close"],
                    name="Cours", fill="tozeroy",
                    line=dict(color=C["green"], width=1.5),
                    fillcolor="rgba(21,107,73,0.07)",
                ))
                if len(hist) >= 200:
                    sma = hist["close"].rolling(200).mean()
                    fig_price.add_trace(go.Scatter(
                        x=hist.index, y=sma,
                        name="SMA 200", line=dict(color=C["amber"], width=1, dash="dash"),
                    ))
                fig_price.update_layout(
                    title=f"{selected} — cours",
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=C["text"]),
                    legend=dict(orientation="h", y=1.1),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor=C["border"]),
                    hovermode="x unified",
                )
                st.plotly_chart(fig_price, use_container_width=True)

    # ── Full ranking table ────────────────────────────────────────────────────
    st.markdown("### Classement complet")
    display_cols = ["name", "category", "score", "momentum_component",
                    "trend_component", "risk_penalty", "r1M", "r3M", "r6M", "r12M",
                    "annual_vol", "rec_label"]
    display_df = sig_df[display_cols].copy()
    pct_cols = ["r1M", "r3M", "r6M", "r12M", "annual_vol"]
    for c in pct_cols:
        display_df[c] = display_df[c].apply(lambda v: f"{v*100:+.1f}%" if not math.isnan(v) else "—")
    float_cols = ["score", "momentum_component", "trend_component", "risk_penalty"]
    for c in float_cols:
        display_df[c] = display_df[c].apply(lambda v: f"{v:.1f}")
    display_df.columns = ["Nom", "Catégorie", "Score", "Mom.", "Tendance", "Pénalité",
                          "1M", "3M", "6M", "12M", "Vol ann.", "Signal"]
    st.dataframe(display_df, use_container_width=True, height=420)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PORTEFEUILLE
# ══════════════════════════════════════════════════════════════════════════════
with tab_portf:
    holdings = _holdings()
    enriched = enrich_holdings_with_prices(holdings, histories) if holdings else []

    # ── Summary KPIs ──────────────────────────────────────────────────────────
    if enriched:
        total_mv    = sum(h["market_value"] for h in enriched)
        total_cost  = sum(h["cost_basis"] for h in enriched)
        total_pnl   = total_mv - total_cost
        total_pnl_p = total_pnl / total_cost if total_cost else 0.0
        day_pnl     = sum(h.get("day_change", 0) * h["market_value"] for h in enriched)

        p1, p2, p3, p4 = st.columns(4)
        pnl_color = C["green"] if total_pnl >= 0 else C["red"]
        _kpi(p1, "Valeur marché",    _eur(total_mv))
        _kpi(p2, "P&L total",        f"{'+' if total_pnl>=0 else ''}{_eur(total_pnl)}",
             f"{_pct(total_pnl_p)}")
        _kpi(p3, "P&L jour (est.)",  f"{'+' if day_pnl>=0 else ''}{_eur(day_pnl)}")
        _kpi(p4, "Nb lignes",        str(len(enriched)))

        # Holdings table
        st.markdown("### Positions actuelles")
        rows = []
        for h in enriched:
            rows.append({
                "Ticker":       h["ticker"],
                "Nom":          h["name"],
                "Sleeve":       h["sleeve"],
                "Qté":          h["quantity"],
                "Px moy":       f"{h['avg_cost']:.2f} €",
                "Cours":        f"{h['latest_price']:.2f} €" if h["latest_price"] else "—",
                "Val. marché":  _eur(h["market_value"]),
                "P&L":          f"{'+' if h['pnl']>=0 else ''}{_eur(h['pnl'])} ({_pct(h['pnl_pct'])})",
                "Alloc.":       f"{h['allocation_pct']*100:.1f}%",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Allocation bar vs target
        st.markdown("### Allocation actuelle vs cible")
        proposal_tmp = build_proposal(signals, total_mv, CORE_ANCHOR, top_n) if signals else None
        if proposal_tmp:
            target_map = {l["ticker"]: l["weight"] for l in proposal_tmp["lines"]}
            comp_rows = []
            for h in enriched:
                target = target_map.get(h["ticker"], 0.0)
                actual = h["allocation_pct"]
                comp_rows.append({
                    "ticker": h["ticker"], "Actuel": actual * 100, "Cible": target * 100,
                })
            comp_df = pd.DataFrame(comp_rows).set_index("ticker")

            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=comp_df.index, y=comp_df["Actuel"],
                name="Actuel", marker_color=C["green"],
            ))
            fig_comp.add_trace(go.Bar(
                x=comp_df.index, y=comp_df["Cible"],
                name="Cible", marker_color=C["amber"], opacity=0.6,
            ))
            fig_comp.update_layout(
                barmode="group", height=280,
                margin=dict(l=0, r=0, t=20, b=20),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=C["text"]),
                legend=dict(orientation="h", y=1.05),
                yaxis=dict(ticksuffix="%", showgrid=True, gridcolor=C["border"]),
                xaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_comp, use_container_width=True)

    # ── Add / Edit holding ────────────────────────────────────────────────────
    st.markdown("### Ajouter / Modifier une position")
    all_tickers_meta = get_etf_metadata()
    universe_choices = [f"{t} — {all_tickers_meta.loc[t, 'name']}" for t in all_tickers_meta.index]

    with st.form("add_holding", clear_on_submit=True):
        h_col1, h_col2, h_col3 = st.columns(3)
        with h_col1:
            h_ticker_full = st.selectbox("ETF", universe_choices)
            h_ticker = h_ticker_full.split(" — ")[0]
        with h_col2:
            h_qty  = st.number_input("Quantité", min_value=0.001, value=1.0, step=0.001, format="%.3f")
        with h_col3:
            h_cost = st.number_input("Prix moyen d'achat (€)", min_value=0.01, value=100.0, step=0.01, format="%.2f")

        submitted = st.form_submit_button("💾 Enregistrer la position", type="primary", use_container_width=True)
        if submitted and h_ticker:
            meta_row = all_tickers_meta.loc[h_ticker].to_dict()
            new_holding = {
                "ticker":   h_ticker,
                "name":     meta_row["name"],
                "quantity": h_qty,
                "avg_cost": h_cost,
                "sleeve":   meta_row["sleeve"],
                "category": meta_row["category"],
            }
            st.session_state.doc = upsert_holding(st.session_state.doc, new_holding)
            _save()
            st.success(f"{h_ticker} enregistré.")
            st.rerun()

    # Delete
    if holdings:
        st.markdown("### Supprimer une position")
        del_ticker = st.selectbox("Position à supprimer", [h["ticker"] for h in holdings])
        if st.button("🗑 Supprimer", type="secondary"):
            st.session_state.doc = delete_holding(st.session_state.doc, del_ticker)
            _save()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RÉGLAGES
# ══════════════════════════════════════════════════════════════════════════════
with tab_settings:
    st.markdown("### Réglages du compte")
    cfg = _settings()

    with st.form("settings_form"):
        broker = st.text_input("Nom du courtier", value=cfg["broker_name"])
        currency = st.selectbox("Devise", ["EUR", "USD"], index=0 if cfg["currency"] == "EUR" else 1)
        init_cap = st.number_input("Capital initial (€)", min_value=0.0, value=float(cfg["capital"]), step=100.0)

        st.markdown("---")
        st.markdown("**Source de données**")
        db_settings = price_db.get_settings()
        st.caption(
            f"Cache SQLite : {db_settings.get('data_source', 'cache')} • "
            f"{db_settings.get('history_years', '—')} ans"
        )

        saved = st.form_submit_button("💾 Enregistrer", type="primary")
        if saved:
            st.session_state.doc["settings"] = {
                **cfg,
                "broker_name":   broker,
                "currency":      currency,
                "capital":       init_cap,
                "data_source":   db_settings.get("data_source", cfg.get("data_source", "cache")),
                "eodhd_api_key": cfg.get("eodhd_api_key", ""),
            }
            _save()
            st.success("Réglages sauvegardés.")

    st.markdown("---")
    st.markdown("### Univers PEA")
    st.markdown(f"**{len(all_tickers_meta)} ETF** éligibles PEA chargés. "
                f"**{len(histories)} ETF** avec données disponibles.")

    disp = all_tickers_meta.copy()
    disp.index.name = "Ticker"
    disp.columns = ["Nom", "Sleeve", "Catégorie", "Poids cible", "Notes"]
    disp["Poids cible"] = disp["Poids cible"].map("{:.0%}".format)
    st.dataframe(disp, use_container_width=True)
