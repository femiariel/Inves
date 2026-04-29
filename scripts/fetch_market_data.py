"""
Fetch ETF market data once and write it to the local SQLite cache.

Examples:
  python scripts/fetch_market_data.py --source yahoo --years 2
  EODHD_API_KEY=... python scripts/fetch_market_data.py --source eodhd --years 5
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
    "mock": DataSource.MOCK,
    "yahoo": DataSource.YAHOO,
    "eodhd": DataSource.EODHD,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch ETF prices and store them in data/alloc.db."
    )
    parser.add_argument(
        "--source",
        choices=SOURCE_CHOICES,
        default="yahoo",
        help="Data source to request. EODHD falls back to Yahoo per ticker.",
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
        default=os.environ.get("EODHD_API_KEY", ""),
        help="EODHD API key. Can also be provided through EODHD_API_KEY.",
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

    print(f"Fetching {len(tickers)} ETF tickers from {args.source} ({args.years}y)...")
    fetched = fetch_all_with_sources(
        tickers,
        source=requested_source,
        api_key=args.api_key,
        years=args.years,
    )

    if not fetched:
        print("No prices were fetched. Existing cache was left unchanged.")
        return 1

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

    return 0 if fetched else 1


if __name__ == "__main__":
    raise SystemExit(main())
