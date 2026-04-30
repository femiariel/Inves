"""
PEA 80/20 strategy — port of PEAStore business logic.

Rules:
  • 80% → core anchor (DCAM.PA by default, MSCI World)
  • 20% → top-N satellite ETFs with momentum_filter_ok (12-1M > 0 and above SMA 200)
  • If no satellite passes the filter → 20% cash reserve
  • Monthly rebalancing in backtest
"""

from __future__ import annotations

import math
from typing import Optional

import numpy as np
import pandas as pd


# ── Proposal ──────────────────────────────────────────────────────────────────

def build_proposal(
    signals: list[dict],
    capital: float,
    core_ticker: str = "DCAM.PA",
    top_n: int = 5,
) -> dict:
    """
    Generate a portfolio proposal from ranked signals.
    Returns a dict with 'lines', 'cash_reserve_pct', 'metrics', 'rationale'.
    """
    core_sig = next((s for s in signals if s["ticker"] == core_ticker), None)
    satellite_pool = [
        s for s in signals
        if s["ticker"] != core_ticker
        and s["sleeve"] == "aggressive"
        and s["momentum_filter_ok"]
    ]
    top_satellites = satellite_pool[:top_n]

    lines = []

    # ── Core line ─────────────────────────────────────────────────────────────
    core_name = core_sig["name"] if core_sig else core_ticker
    lines.append({
        "ticker":       core_ticker,
        "name":         core_name,
        "sleeve":       "core",
        "category":     "Monde",
        "weight":       0.80,
        "value":        capital * 0.80,
        "score":        core_sig["score"] if core_sig else None,
        "rationale":    "Socle monde — 80 % du portefeuille, ancre long terme",
    })

    # ── Satellite lines ───────────────────────────────────────────────────────
    cash_reserve_pct = 0.0
    if top_satellites:
        sat_each = 0.20 / len(top_satellites)
        for s in top_satellites:
            r12_1m = s.get("r12_1M", math.nan)
            r12_1m_str = f"{r12_1m*100:+.1f}%" if not math.isnan(r12_1m) else "n/a"
            lines.append({
                "ticker":    s["ticker"],
                "name":      s["name"],
                "sleeve":    "aggressive",
                "category":  s["category"],
                "weight":    sat_each,
                "value":     capital * sat_each,
                "score":     s["score"],
                "rationale": f"Momentum score {s['score']:.1f} • 12-1M {r12_1m_str}",
            })
    else:
        cash_reserve_pct = 0.20
        lines.append({
            "ticker":    "LIQUIDITÉS",
            "name":      "Réserve de liquidités",
            "sleeve":    "cash",
            "category":  "Cash",
            "weight":    0.20,
            "value":     capital * 0.20,
            "score":     None,
            "rationale": "Aucun ETF satellite avec régime positif — filtre cash activé",
        })

    # ── Expected return / risk estimates ─────────────────────────────────────
    core_exp_ret  = 0.085   # long-run MSCI World average
    core_exp_vol  = 0.145
    sat_exp_ret   = 0.11    # momentum premium estimate
    sat_exp_vol   = 0.18
    cash_exp_ret  = 0.035

    exp_ret = 0.80 * core_exp_ret + (0.20 - cash_reserve_pct) * sat_exp_ret + cash_reserve_pct * cash_exp_ret
    exp_vol = math.sqrt((0.80 * core_exp_vol)**2 + ((0.20 - cash_reserve_pct) * sat_exp_vol)**2)

    n_sat = len(top_satellites)
    rationale = (
        f"80% Monde • 20% momentum top {n_sat} • filtre 12M positif"
        if n_sat > 0
        else "80% Monde • 20% liquidités — filtre 12M : aucun signal positif"
    )

    return {
        "lines":              lines,
        "cash_reserve_pct":   cash_reserve_pct,
        "cash_reserve_value": capital * cash_reserve_pct,
        "capital":            capital,
        "n_satellites":       n_sat,
        "expected_return":    exp_ret,
        "expected_vol":       exp_vol,
        "expected_sharpe":    (exp_ret - 0.03) / exp_vol if exp_vol > 0 else 0,
        "rationale":          rationale,
    }


# ── Rebalance orders ──────────────────────────────────────────────────────────

def build_rebalance_orders(
    current_holdings: list[dict],
    proposal: dict,
    tolerance: float = 0.01,
) -> list[dict]:
    """
    Compare current holdings vs. proposal target weights.
    Returns a list of rebalance actions sorted by |delta| descending.
    current_holdings: list of {ticker, name, quantity, avg_cost, sleeve, ...}
    """
    total_value = sum(
        h.get("market_value", h["quantity"] * h["avg_cost"])
        for h in current_holdings
    )
    capital = proposal["capital"]

    current_map: dict[str, dict] = {}
    for h in current_holdings:
        mv = h.get("market_value", h["quantity"] * h["avg_cost"])
        current_map[h["ticker"]] = {
            "value":  mv,
            "weight": mv / total_value if total_value > 0 else 0,
        }

    orders = []
    all_tickers = set(l["ticker"] for l in proposal["lines"]) | set(current_map.keys())

    for ticker in all_tickers:
        target_line = next((l for l in proposal["lines"] if l["ticker"] == ticker), None)
        target_w  = target_line["weight"] if target_line else 0.0
        target_v  = capital * target_w
        current_v = current_map.get(ticker, {}).get("value", 0.0)
        current_w = current_map.get(ticker, {}).get("weight", 0.0)
        delta_v   = target_v - current_v
        delta_w   = target_w - current_w

        if abs(delta_w) < tolerance:
            action = "hold"
        elif delta_v > 0:
            action = "buy"
        else:
            action = "sell"

        name = (target_line["name"] if target_line
                else next((h["name"] for h in current_holdings if h["ticker"] == ticker), ticker))

        orders.append({
            "ticker":         ticker,
            "name":           name,
            "action":         action,
            "current_weight": current_w,
            "target_weight":  target_w,
            "current_value":  current_v,
            "target_value":   target_v,
            "delta_value":    delta_v,
            "priority":       abs(delta_w),
        })

    orders.sort(key=lambda o: o["priority"], reverse=True)
    return orders


# ── Backtest ──────────────────────────────────────────────────────────────────

def run_backtest(
    histories: dict[str, pd.DataFrame],
    signals_fn,                    # callable(histories_up_to_date) → list[dict]
    capital: float = 10_000.0,
    top_n: int = 5,
    core_ticker: str = "DCAM.PA",
    rebal_freq: str = "ME",
) -> dict:
    """
    Monthly-rebalancing backtest of the 80/20 strategy.
    signals_fn: function that builds signals from a price snapshot.
    Returns dict with equity_curve, benchmark_curve, stats.
    """
    # Build a combined price DataFrame
    combined = _merge_histories(histories)
    if combined.empty or len(combined) < 60:
        return _empty_backtest(capital)

    rebal_dates = combined.resample(rebal_freq).last().index
    portfolio_val = capital
    benchmark_val = capital
    equity: dict[pd.Timestamp, float] = {}
    bench:  dict[pd.Timestamp, float] = {}
    prev_weights_port: Optional[dict[str, float]] = None
    prev_weights_bm:   Optional[dict[str, float]] = None
    trade_count = 0

    for i, rebal_date in enumerate(sorted(rebal_dates)):
        snap = {t: df.loc[:rebal_date] for t, df in histories.items() if rebal_date in df.index or df.index[-1] >= rebal_date}
        snap = {t: df.loc[df.index <= rebal_date] for t, df in snap.items() if len(df.loc[df.index <= rebal_date]) >= 60}

        if not snap:
            continue

        # Build signals on the snapshot
        try:
            sigs = signals_fn(snap)
        except Exception:
            continue

        proposal = build_proposal(sigs, 1.0, core_ticker, top_n)  # unit capital for weights

        # Strategy weights
        new_weights_port: dict[str, float] = {}
        for line in proposal["lines"]:
            if line["ticker"] != "LIQUIDITÉS":
                new_weights_port[line["ticker"]] = line["weight"]

        # Benchmark: equal-weight all available tickers
        avail = list(snap.keys())
        new_weights_bm = {t: 1.0 / len(avail) for t in avail}

        if prev_weights_port is not None:
            trade_count += sum(1 for t in set(new_weights_port) | set(prev_weights_port)
                               if abs(new_weights_port.get(t, 0) - prev_weights_port.get(t, 0)) > 0.01)

        prev_weights_port = new_weights_port
        prev_weights_bm   = new_weights_bm

        # Compute period return until next rebalance
        next_date = (sorted(rebal_dates)[i + 1]
                     if i + 1 < len(rebal_dates)
                     else combined.index[-1])

        period_rets = combined.loc[rebal_date:next_date].pct_change().dropna()
        if period_rets.empty:
            continue

        for d, row in period_rets.iterrows():
            port_r = sum(new_weights_port.get(t, 0) * row.get(t, 0) for t in new_weights_port)
            bm_r   = sum(new_weights_bm.get(t, 0) * row.get(t, 0) for t in new_weights_bm)
            portfolio_val *= (1 + port_r)
            benchmark_val *= (1 + bm_r)
            equity[d] = portfolio_val
            bench[d]  = benchmark_val

    nav_s   = pd.Series(equity, name="strategie")
    bench_s = pd.Series(bench,  name="benchmark")

    if nav_s.empty:
        return _empty_backtest(capital)

    # ── Stats ─────────────────────────────────────────────────────────────────
    n_days = len(nav_s)
    years  = n_days / 252

    def _cagr(series: pd.Series) -> float:
        if len(series) < 2 or years == 0:
            return 0.0
        return float((series.iloc[-1] / capital) ** (1 / years) - 1)

    def _max_dd(series: pd.Series) -> float:
        dd = (series / series.cummax()) - 1
        return float(dd.min())

    def _sharpe(series: pd.Series, rf: float = 0.03) -> float:
        daily = series.pct_change().dropna()
        if daily.std() == 0:
            return 0.0
        return float((daily.mean() * 252 - rf) / (daily.std() * math.sqrt(252)))

    return {
        "equity_curve":       nav_s,
        "benchmark_curve":    bench_s,
        "ending_value":       float(nav_s.iloc[-1]),
        "benchmark_value":    float(bench_s.iloc[-1]),
        "cagr":               _cagr(nav_s),
        "benchmark_cagr":     _cagr(bench_s),
        "max_drawdown":       _max_dd(nav_s),
        "benchmark_max_dd":   _max_dd(bench_s),
        "sharpe":             _sharpe(nav_s),
        "benchmark_sharpe":   _sharpe(bench_s),
        "alpha":              _cagr(nav_s) - _cagr(bench_s),
        "excess_return":      float(nav_s.iloc[-1]) - float(bench_s.iloc[-1]),
        "trade_count":        trade_count,
        "n_days":             n_days,
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _merge_histories(histories: dict[str, pd.DataFrame]) -> pd.DataFrame:
    frames = {t: df["close"].rename(t) for t, df in histories.items()}
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames.values(), axis=1).sort_index().ffill().dropna(how="all")
    return combined


def _empty_backtest(capital: float) -> dict:
    return {
        "equity_curve":     pd.Series(dtype=float),
        "benchmark_curve":  pd.Series(dtype=float),
        "ending_value":     capital,
        "benchmark_value":  capital,
        "cagr":             0.0,
        "benchmark_cagr":   0.0,
        "max_drawdown":     0.0,
        "benchmark_max_dd": 0.0,
        "sharpe":           0.0,
        "benchmark_sharpe": 0.0,
        "alpha":            0.0,
        "excess_return":    0.0,
        "trade_count":      0,
        "n_days":           0,
    }
