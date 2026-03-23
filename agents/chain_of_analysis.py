#!/usr/bin/env python3
"""
chain_of_analysis.py — Sequential analysis chain: ingest → extract → analyse → summarise.

Demonstrates breaking a complex analysis into discrete steps, where each step's
output feeds the next. This pattern gives you visibility into intermediate
results and makes each step independently testable.

Usage:
    python chain_of_analysis.py --report path/to/filing.txt
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from utils import call_claude, extract_json  # noqa: E402


# ---------------------------------------------------------------------------
# Chain steps
# ---------------------------------------------------------------------------


def step_1_extract(report_text: str) -> dict:
    """Extract raw financial data points from the filing."""
    print("  [1/4] Extracting data points...")
    raw = call_claude(
        user_prompt=f"""Extract all quantitative financial data from this report.
Return JSON with keys: revenue, costs, margins, assets, liabilities, cash_flow,
headcount, and any other numeric data you find.

<report>
{report_text}
</report>""",
        system_prompt="You are a data extraction specialist. Return only valid JSON.",
    )
    return extract_json(raw)


def step_2_calculate(extracted: dict) -> dict:
    """Compute derived metrics from extracted data."""
    print("  [2/4] Computing derived metrics...")
    raw = call_claude(
        user_prompt=f"""Given these extracted financials, calculate derived metrics:
- Growth rates (YoY if prior period available)
- Margins (gross, operating, net)
- Efficiency ratios (revenue per employee, asset turnover)
- Liquidity ratios if balance sheet data present

Input data:
{json.dumps(extracted, indent=2)}

Return JSON with a "derived_metrics" key.""",
        system_prompt="You are a quantitative analyst. Compute ratios precisely. Return only valid JSON.",
    )
    return extract_json(raw)


def step_3_analyse(extracted: dict, metrics: dict) -> dict:
    """Generate qualitative analysis from the numbers."""
    print("  [3/4] Running qualitative analysis...")
    raw = call_claude(
        user_prompt=f"""You have the following financial data and derived metrics for a company.
Produce a qualitative analysis covering: strengths, weaknesses, opportunities, threats,
and an overall health assessment (score 1-10).

Extracted data:
{json.dumps(extracted, indent=2)}

Derived metrics:
{json.dumps(metrics, indent=2)}

Return JSON with keys: strengths, weaknesses, opportunities, threats, health_score, rationale.""",
        system_prompt="You are a senior equity analyst. Be specific and evidence-based. Return only valid JSON.",
    )
    return extract_json(raw)


def step_4_summarise(analysis: dict) -> str:
    """Produce a concise executive summary."""
    print("  [4/4] Writing executive summary...")
    return call_claude(
        user_prompt=f"""Write a 3-paragraph executive summary based on this analysis.
Paragraph 1: Company financial health overview.
Paragraph 2: Key risks and opportunities.
Paragraph 3: Recommendation and outlook.

Analysis:
{json.dumps(analysis, indent=2)}""",
        system_prompt="You are a financial writer. Be clear, concise, and actionable.",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Chain-of-analysis pipeline")
    parser.add_argument("--report", required=True, help="Path to report text file")
    parser.add_argument("--output", default=None, help="Save full chain output to JSON")
    args = parser.parse_args()

    report_text = Path(args.report).read_text()
    print(f"Running analysis chain on {args.report} ({len(report_text):,} chars)\n")

    extracted = step_1_extract(report_text)
    metrics = step_2_calculate(extracted)
    analysis = step_3_analyse(extracted, metrics)
    summary = step_4_summarise(analysis)

    print("\n" + "=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)
    print(summary)

    if args.output:
        output = {
            "extracted_data": extracted,
            "derived_metrics": metrics,
            "analysis": analysis,
            "executive_summary": summary,
        }
        Path(args.output).write_text(json.dumps(output, indent=2))
        print(f"\nFull chain output saved to {args.output}")


if __name__ == "__main__":
    main()
