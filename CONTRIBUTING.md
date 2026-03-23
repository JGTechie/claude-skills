# Contributing to Claude Skills for Fintech

Thanks for your interest in contributing! Here's how to get started.

## Adding a New Prompt Template

1. Create a markdown file in `prompts/` following the existing structure:
   - `## System Prompt` — fenced code block with the system message
   - `## User Prompt Template` — fenced code block with `{{PLACEHOLDER}}` variables
   - `## Usage Notes` — when to use, tips, gotchas
   - `## Example Variables` — table of sample values

2. (Optional) Add a matching script in `scripts/` that loads and runs the template.

3. Update the table in `README.md`.

## Adding a Script or Agent

- Keep imports minimal — `anthropic`, `pandas`, and stdlib only where possible.
- Use the helpers in `scripts/utils.py` (template loading, retry, JSON extraction).
- Add a docstring with usage examples at the top of the file.
- Make sure it runs with `python scripts/your_script.py --help`.

## Code Style

- We use [ruff](https://github.com/astral-sh/ruff) for linting.
- Run `ruff check scripts/ agents/` before submitting.
- Type hints are encouraged but not required.

## Pull Request Process

1. Fork and branch (`feat/my-prompt` or `fix/json-parsing`).
2. Make your changes.
3. Run the linter.
4. Open a PR with a clear description of what you added and why.

## Questions?

Open an issue — happy to help.
