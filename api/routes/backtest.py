from fastapi import APIRouter
import api.db as db
import api.core as core
from data.pea_universe import CORE_ANCHOR, get_etf_metadata
from portfolio.optimizer import run_backtest
from strategy.factors import build_all_signals

router = APIRouter(tags=["backtest"])


@router.get("/backtest")
def get_backtest():
    settings  = db.get_settings()
    capital   = float(settings.get("capital", 10_000))
    top_n     = int(settings.get("top_n", 5))
    histories = core.load_histories(settings)
    meta      = get_etf_metadata()

    def signals_fn(snap):
        return build_all_signals(snap, meta)

    result = run_backtest(
        histories=histories,
        signals_fn=signals_fn,
        capital=capital,
        top_n=top_n,
        core_ticker=CORE_ANCHOR,
    )

    def to_series(s):
        return [{"date": str(d.date()), "value": round(v, 2)} for d, v in s.items()]

    return {
        "equity_curve":     to_series(result["equity_curve"]),
        "benchmark_curve":  to_series(result["benchmark_curve"]),
        "ending_value":     round(result["ending_value"], 2),
        "benchmark_value":  round(result["benchmark_value"], 2),
        "cagr":             round(result["cagr"], 4),
        "benchmark_cagr":   round(result["benchmark_cagr"], 4),
        "max_drawdown":     round(result["max_drawdown"], 4),
        "benchmark_max_dd": round(result["benchmark_max_dd"], 4),
        "sharpe":           round(result["sharpe"], 3),
        "benchmark_sharpe": round(result["benchmark_sharpe"], 3),
        "alpha":            round(result["alpha"], 4),
        "trade_count":      result["trade_count"],
        "n_days":           result["n_days"],
    }
