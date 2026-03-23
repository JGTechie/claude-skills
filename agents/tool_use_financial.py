#!/usr/bin/env python3
"""
tool_use_financial.py — Financial agent with Claude tool use.

Demonstrates how to define tools (stock lookup, ratio calculator, chart
generator) and let Claude decide when to call them during a multi-turn
conversation.

Usage:
    python tool_use_financial.py
"""

import json
import os

from anthropic import Anthropic

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

# ---------------------------------------------------------------------------
# Tool definitions — these tell Claude what's available
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "get_stock_price",
        "description": (
            "Look up the current stock price and basic stats for a given ticker symbol. "
            "Returns price, market cap, P/E ratio, and 52-week range."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol, e.g. AAPL",
                }
            },
            "required": ["ticker"],
        },
    },
    {
        "name": "calculate_ratios",
        "description": (
            "Calculate financial ratios from provided numbers. "
            "Supports: debt_to_equity, current_ratio, quick_ratio, roe, roa."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "ratio": {
                    "type": "string",
                    "enum": ["debt_to_equity", "current_ratio", "quick_ratio", "roe", "roa"],
                },
                "values": {
                    "type": "object",
                    "description": "Key-value pairs of the inputs needed for the ratio",
                },
            },
            "required": ["ratio", "values"],
        },
    },
    {
        "name": "generate_chart_data",
        "description": (
            "Generate chart-ready JSON data for a time series. "
            "Takes a list of (label, value) pairs and returns a structure "
            "suitable for Chart.js or similar libraries."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "chart_type": {
                    "type": "string",
                    "enum": ["line", "bar", "pie"],
                },
                "data_points": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "value": {"type": "number"},
                        },
                    },
                },
            },
            "required": ["title", "chart_type", "data_points"],
        },
    },
]

# ---------------------------------------------------------------------------
# Tool implementations (stubs — replace with real APIs in production)
# ---------------------------------------------------------------------------


def get_stock_price(ticker: str) -> dict:
    """Stub: In production, call a real market data API."""
    demo_data = {
        "AAPL": {"price": 198.50, "market_cap": "3.07T", "pe_ratio": 31.2, "range_52w": "164.08–199.62"},
        "GOOGL": {"price": 176.30, "market_cap": "2.18T", "pe_ratio": 24.8, "range_52w": "130.67–180.42"},
        "MSFT": {"price": 425.80, "market_cap": "3.16T", "pe_ratio": 36.5, "range_52w": "366.50–430.82"},
    }
    return demo_data.get(ticker.upper(), {"error": f"No data for {ticker}"})


def calculate_ratios(ratio: str, values: dict) -> dict:
    """Calculate a financial ratio from provided values."""
    try:
        match ratio:
            case "debt_to_equity":
                result = values["total_debt"] / values["total_equity"]
            case "current_ratio":
                result = values["current_assets"] / values["current_liabilities"]
            case "quick_ratio":
                result = (values["current_assets"] - values["inventory"]) / values["current_liabilities"]
            case "roe":
                result = values["net_income"] / values["shareholders_equity"]
            case "roa":
                result = values["net_income"] / values["total_assets"]
            case _:
                return {"error": f"Unknown ratio: {ratio}"}
        return {"ratio": ratio, "result": round(result, 4)}
    except (KeyError, ZeroDivisionError) as e:
        return {"error": str(e)}


def generate_chart_data(title: str, chart_type: str, data_points: list[dict]) -> dict:
    """Wrap data in a Chart.js-compatible structure."""
    return {
        "type": chart_type,
        "data": {
            "labels": [dp["label"] for dp in data_points],
            "datasets": [
                {
                    "label": title,
                    "data": [dp["value"] for dp in data_points],
                }
            ],
        },
    }


TOOL_DISPATCH = {
    "get_stock_price": lambda inp: get_stock_price(inp["ticker"]),
    "calculate_ratios": lambda inp: calculate_ratios(inp["ratio"], inp["values"]),
    "generate_chart_data": lambda inp: generate_chart_data(
        inp["title"], inp["chart_type"], inp["data_points"]
    ),
}

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------


def run_agent(user_message: str) -> str:
    """
    Run a single-turn agent loop: send the user message, handle any tool
    calls Claude makes, return the final text response.
    """
    client = Anthropic()
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=(
                "You are a financial analysis assistant with access to stock data, "
                "ratio calculators, and charting tools. Use the tools when they would "
                "help answer the user's question. Be concise and data-driven."
            ),
            tools=TOOLS,
            messages=messages,
        )

        # If the model is done (no more tool calls), return the text
        if response.stop_reason == "end_turn":
            return "".join(
                block.text for block in response.content if hasattr(block, "text")
            )

        # Otherwise, process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                fn = TOOL_DISPATCH.get(block.name)
                if fn:
                    result = fn(block.input)
                else:
                    result = {"error": f"Unknown tool: {block.name}"}

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                )

        # Feed results back and loop
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("💹 Financial Agent (type 'quit' to exit)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"quit", "exit", "q"}:
            break
        if not user_input:
            continue
        print(f"\nAgent: {run_agent(user_input)}\n")
