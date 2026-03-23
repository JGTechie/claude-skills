#!/usr/bin/env python3
"""
forecast_runner.py — Generate bear/base/bull revenue forecasts.

Usage:
    python forecast_runner.py --company "Stripe" --data path/to/revenue.csv --quarters 4
"""

import argparse
import json
import sys
from pathlib import Path

from utils import (
    call_claude,
    extract_json,
    extract_system_prompt,
    extract_user_prompt,
    fill_template,
    load_template,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-scenario revenue forecast")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--data", required=True, help="CSV file with historical revenue (quarter,revenue)")
    parser.add_argument("--context", default="", help="Optional business context string")
    parser.add_argument("--quarters", type=int, default=4, help="Forecast horizon in quarters")
    parser.add_argument("--output", default=None, help="Save JSON output to file")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found — {data_path}")
        sys.exit(1)

    csv_data = data_path.read_text()

    template = load_template("revenue_forecast")
    system_prompt = extract_system_prompt(template)
    user_prompt = extract_user_prompt(template)
    user_prompt = fill_template(user_prompt, {
        "COMPANY_NAME": args.company,
        "HISTORICAL_REVENUE_CSV": csv_data,
        "BUSINESS_CONTEXT": args.context or "No additional context provided.",
        "FORECAST_QUARTERS": str(args.quarters),
    })

    print(f"Generating {args.quarters}-quarter forecast for {args.company}...")
    raw = call_claude(user_prompt, system_prompt=system_prompt)

    try:
        result = extract_json(raw)
        formatted = json.dumps(result, indent=2)
    except ValueError:
        formatted = raw

    print("\n" + formatted)

    if args.output:
        Path(args.output).write_text(formatted)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
