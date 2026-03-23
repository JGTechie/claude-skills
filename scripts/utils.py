"""
utils.py — Shared helpers for claude-skills scripts.

Template loading, token estimation, retry logic, and JSON extraction.
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Any

from anthropic import Anthropic, APIError, RateLimitError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
DEFAULT_MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def get_client() -> Anthropic:
    """Return an Anthropic client (reads ANTHROPIC_API_KEY from env)."""
    return Anthropic()


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------


def load_template(name: str) -> str:
    """
    Load a prompt template from the prompts/ directory.

    Args:
        name: Filename with or without .md extension.
              e.g. "financial_analysis" or "financial_analysis.md"

    Returns:
        The raw markdown content of the template file.
    """
    if not name.endswith(".md"):
        name += ".md"
    path = PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text()


def fill_template(template: str, variables: dict[str, str]) -> str:
    """
    Replace {{PLACEHOLDER}} variables in a template string.

    Args:
        template:  Raw template text with {{VAR}} placeholders.
        variables: Mapping of variable names (without braces) to values.

    Returns:
        The template with all matched placeholders replaced.
    """
    for key, value in variables.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template


def extract_user_prompt(template_md: str) -> str:
    """
    Extract the user prompt block from a template markdown file.

    Looks for the first fenced code block under a heading containing
    'User Prompt'.
    """
    in_section = False
    in_code = False
    lines: list[str] = []
    for line in template_md.splitlines():
        if re.match(r"^##\s+.*[Uu]ser\s+[Pp]rompt", line):
            in_section = True
            continue
        if in_section and line.strip().startswith("```") and not in_code:
            in_code = True
            continue
        if in_code and line.strip().startswith("```"):
            break
        if in_code:
            lines.append(line)
    return "\n".join(lines)


def extract_system_prompt(template_md: str) -> str:
    """
    Extract the system prompt block from a template markdown file.
    """
    in_section = False
    in_code = False
    lines: list[str] = []
    for line in template_md.splitlines():
        if re.match(r"^##\s+.*[Ss]ystem\s+[Pp]rompt", line):
            in_section = True
            continue
        if in_section and line.strip().startswith("```") and not in_code:
            in_code = True
            continue
        if in_code and line.strip().startswith("```"):
            break
        if in_code:
            lines.append(line)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------


def call_claude(
    user_prompt: str,
    system_prompt: str | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    retries: int = 3,
    backoff: float = 2.0,
) -> str:
    """
    Send a message to Claude with automatic retry on rate-limit errors.

    Returns the text content of the first response block.
    """
    client = get_client()
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    for attempt in range(retries):
        try:
            response = client.messages.create(**kwargs)
            return response.content[0].text
        except RateLimitError:
            if attempt < retries - 1:
                wait = backoff ** (attempt + 1)
                print(f"Rate limited — retrying in {wait:.0f}s...")
                time.sleep(wait)
            else:
                raise
        except APIError as e:
            print(f"API error: {e}")
            raise

    return ""  # unreachable, but keeps type checkers happy


def extract_json(text: str) -> dict | list:
    """
    Extract JSON from a Claude response that may contain markdown fences.
    """
    # Try to find a JSON code block first
    match = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1).strip())

    # Fall back to finding the first { ... } or [ ... ]
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(text)):
            if text[i] == start_char:
                depth += 1
            elif text[i] == end_char:
                depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])

    raise ValueError("No JSON found in response")


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------


def estimate_tokens(text: str) -> int:
    """
    Rough token count (~4 chars per token). Use the Anthropic tokeniser
    for precise counts in production.
    """
    return len(text) // 4
