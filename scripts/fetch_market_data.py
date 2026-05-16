"""
Fetch ETF market data once and write it to the local SQLite cache.

Examples:
  EODHD_API_KEY=... python scripts/fetch_market_data.py --source eodhd --years 5
  python scripts/fetch_market_data.py --source eodhd --years 5  # reads .env
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.db as db
from data.market_data import DataSource, fetch_all_with_sources
from data.pea_universe import get_all_tickers


SOURCE_CHOICES = {
    "eodhd": DataSource.EODHD,
}

BAR_WIDTH = 34


def env_value(key: str, default: str = "") -> str:
    if os.environ.get(key):
        return os.environ[key]

    env_path = ROOT / ".env"
    if not env_path.exists():
        return default

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == key:
            return v.strip().strip('"').strip("'")
    return default


def progress_bar(done: int, total: int, width: int = BAR_WIDTH) -> str:
    if total <= 0:
        return "[" + "-" * width + "]"
    filled = int(width * done / total)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch ETF prices and store them in data/alloc.db."
    )
    parser.add_argument(
        "--source",
        choices=SOURCE_CHOICES,
        default="eodhd",
        help="Data source to request. Only EODHD is supported.",
    )
    parser.add_argument(
        "--years",
        type=int,
        choices=[1, 2, 3, 5],
        default=2,
        help="Historical window to fetch.",
    )
    parser.add_argument(
        "--api-key",
        default=env_value("EODHD_API_KEY"),
        help="EODHD API key. Can also be provided through EODHD_API_KEY or .env.",
    )
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Keep existing cached prices for tickers that fail to reload.",
    )
    parser.add_argument(
        "--min-rows",
        type=int,
        default=252,
        help="Minimum number of daily prices required to save a ticker.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    tickers = get_all_tickers()
    requested_source = SOURCE_CHOICES[args.source]

    db.init_db()

    if requested_source == DataSource.EODHD and (not args.api_key or args.api_key == "demo"):
        print(
            "EODHD API key missing. Set EODHD_API_KEY in .env, export it, "
            "or pass --api-key.",
            file=sys.stderr,
        )
        return 2

    print(f"Fetching {len(tickers)} ETF tickers from {args.source} ({args.years}y)...", flush=True)

    progress_counts: Counter[str] = Counter()
    failures_by_ticker: dict[str, dict] = {}

    def show_progress(event: dict) -> None:
        status = event["status"]
        progress_counts[status] += 1
        if status != "ok":
            failures_by_ticker[event["ticker"]] = event
        done = int(event["index"])
        total = int(event["total"])
        percent = done / total * 100 if total else 100.0
        ok = progress_counts["ok"]
        missing = done - ok
        detail = f"{event['rows']} rows" if status == "ok" else status.replace("_", " ")
        print(
            "\r"
            f"{progress_bar(done, total)} "
            f"{percent:6.2f}% "
            f"{done:>3}/{total:<3} "
            f"{event['ticker']:<12} "
            f"{detail:<18} "
            f"ok={ok:<3} missing={missing:<3} attempts={event['attempts']}",
            end="",
            flush=True,
        )

    try:
        fetched = fetch_all_with_sources(
            tickers,
            source=requested_source,
            api_key=args.api_key,
            years=args.years,
            progress=show_progress,
        )
    except ValueError as exc:
        print()
        print(str(exc), file=sys.stderr)
        return 2

    print()

    if not fetched:
        print("No prices were fetched. Existing cache was left unchanged.")
        return 1

    too_short = {
        ticker: len(frame)
        for ticker, (frame, _) in fetched.items()
        if len(frame) < args.min_rows
    }

    fetched = {
        ticker: (frame, actual_source)
        for ticker, (frame, actual_source) in fetched.items()
        if len(frame) >= args.min_rows
    }

    if not fetched:
        print(
            f"No tickers met the minimum history requirement "
            f"({args.min_rows} rows). Existing cache was left unchanged."
        )
        return 1

    if not args.keep_existing:
        db.clear_cache()

    source_counts: Counter[str] = Counter()
    for ticker, (frame, actual_source) in fetched.items():
        db.save_prices(ticker, frame, actual_source)
        source_counts[actual_source] += 1

    db.set_settings({
        "data_source": args.source,
        "history_years": args.years,
        "eodhd_api_key": args.api_key if args.source == "eodhd" else "",
    })

    missing = sorted(set(tickers) - set(fetched))
    print(f"Saved prices for {len(fetched)}/{len(tickers)} ETFs with >= {args.min_rows} rows.")
    for source, count in sorted(source_counts.items()):
        print(f"  {source}: {count}")
    if missing:
        preview = ", ".join(missing[:20])
        suffix = "..." if len(missing) > 20 else ""
        print(f"Missing {len(missing)} tickers: {preview}{suffix}")
        print("Missing details:")
        for ticker in missing:
            if ticker in too_short:
                print(f"  {ticker}: history too short ({too_short[ticker]} rows < {args.min_rows})")
            elif ticker in failures_by_ticker:
                status = failures_by_ticker[ticker]["status"].replace("_", " ")
                attempts = failures_by_ticker[ticker]["attempts"]
                print(f"  {ticker}: {status} after {attempts} attempt(s)")
            else:
                print(f"  {ticker}: not returned by EODHD")

    return 0 if fetched else 1


if __name__ == "__main__":
    raise SystemExit(main())
