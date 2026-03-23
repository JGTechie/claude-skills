#!/usr/bin/env python3
"""
pitch_deck_agent.py — Interactive agent that gathers startup info, then drafts
a pitch deck outline using Claude.

Usage:
    python pitch_deck_agent.py
    python pitch_deck_agent.py --non-interactive --info startup_info.json
"""

import argparse
import json
from pathlib import Path

from utils import (
    call_claude,
    extract_json,
    extract_system_prompt,
    extract_user_prompt,
    fill_template,
    load_template,
)

REQUIRED_FIELDS = {
    "COMPANY_NAME": "Company name",
    "STAGE": "Funding stage (pre-seed / seed / Series A / etc.)",
    "SECTOR": "Sector or industry",
    "ONE_LINER": "One-line description of the company",
    "PROBLEM": "Problem you're solving",
    "SOLUTION": "Your solution",
    "TRACTION": "Traction metrics (users, revenue, growth, etc.)",
    "TEAM": "Team background (founders + key hires)",
    "FUNDRAISE_ASK": "How much you're raising and at what valuation",
}


def gather_interactively() -> dict[str, str]:
    """Prompt the user for each required field."""
    print("\n🚀 Pitch Deck Outliner — let's gather your startup info.\n")
    info: dict[str, str] = {}
    for key, description in REQUIRED_FIELDS.items():
        value = input(f"  {description}: ").strip()
        info[key] = value or "Not provided"
    return info


def load_from_file(path: str) -> dict[str, str]:
    """Load startup info from a JSON file."""
    raw = json.loads(Path(path).read_text())
    return {k: raw.get(k, "Not provided") for k in REQUIRED_FIELDS}


def main() -> None:
    parser = argparse.ArgumentParser(description="Pitch deck outline generator")
    parser.add_argument(
        "--non-interactive", action="store_true",
        help="Skip interactive prompts; load info from --info file",
    )
    parser.add_argument("--info", default=None, help="JSON file with startup info")
    parser.add_argument("--output", default=None, help="Save outline JSON to file")
    args = parser.parse_args()

    if args.non_interactive:
        if not args.info:
            print("Error: --info is required in non-interactive mode")
            return
        variables = load_from_file(args.info)
    else:
        variables = gather_interactively()

    template = load_template("pitch_deck")
    system_prompt = extract_system_prompt(template)
    user_prompt = extract_user_prompt(template)
    user_prompt = fill_template(user_prompt, variables)

    print("\nGenerating pitch deck outline...")
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
