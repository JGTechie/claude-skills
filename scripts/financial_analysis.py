#!/usr/bin/env python3
"""
financial_analysis.py — Analyse a financial report using Claude.

Usage:
    python financial_analysis.py --ticker AAPL --report path/to/10k_excerpt.txt
    python financial_analysis.py --ticker AAPL --report path/to/10k_excerpt.txt --output results.json
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
    parser = argparse.ArgumentParser(description="Analyse a financial filing with Claude")
    parser.add_argument("--ticker", required=True, help="Company ticker symbol")
    parser.add_argument("--report", required=True, help="Path to the report text file")
    parser.add_argument("--period", default="Latest", help="Fiscal period (e.g., FY2025 Q1)")
    parser.add_argument("--output", default=None, help="Save JSON output to this file")
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Error: report file not found — {report_path}")
        sys.exit(1)

    report_text = report_path.read_text()
    print(f"Loaded report: {len(report_text):,} chars from {report_path.name}")

    # Load and fill the prompt template
    template = load_template("financial_analysis")
    system_prompt = extract_system_prompt(template)
    user_prompt = extract_user_prompt(template)
    user_prompt = fill_template(user_prompt, {
        "REPORT": report_text,
        "COMPANY_NAME": args.ticker,
        "FISCAL_PERIOD": args.period,
    })

    print(f"Calling Claude ({args.ticker}, {args.period})...")
    raw = call_claude(user_prompt, system_prompt=system_prompt)

    try:
        result = extract_json(raw)
        formatted = json.dumps(result, indent=2)
    except ValueError:
        print("Warning: could not parse JSON from response. Returning raw text.")
        formatted = raw

    print("\n" + "=" * 60)
    print(formatted)
    print("=" * 60)

    if args.output:
        Path(args.output).write_text(formatted)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
