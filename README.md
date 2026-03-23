# 🧠 Claude Skills for Fintech

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Anthropic SDK](https://img.shields.io/badge/anthropic--sdk-latest-blueviolet)](https://docs.claude.com/en/api/overview)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Collection of reusable Claude/Anthropic prompt patterns, tools, and agent skills for building intelligent fintech agents.

---

## Why This Repo?

Building AI-powered fintech tools means writing the same boilerplate over and over — parsing earnings calls, generating forecasts, structuring pitch decks, running compliance checks. This repo packages those patterns into **drop-in prompt templates** and **ready-to-run Python scripts** so you can skip straight to the interesting part.

```
claude-skills/
├── prompts/          # Markdown prompt templates (copy-paste or load programmatically)
├── scripts/          # Python scripts using the Anthropic SDK
├── notebooks/        # Jupyter notebooks with worked examples
├── agents/           # Multi-step agent patterns (tool use, chains)
├── examples/         # Sample data files for demos
└── .github/          # CI config
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install anthropic pandas jupyter
```

### 2. Set your API key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Run a script

```bash
python scripts/financial_analysis.py --ticker AAPL --report examples/aapl_10k_excerpt.txt
```

### 4. Or load a prompt template in your own code

```python
from anthropic import Anthropic
from pathlib import Path

client = Anthropic()
prompt = Path("prompts/financial_analysis.md").read_text()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": prompt.replace("{{REPORT}}", your_report_text)}
    ],
)
print(message.content[0].text)
```

---

## Prompt Templates

| Template | File | Use Case |
|---|---|---|
| Financial Statement Analysis | [`prompts/financial_analysis.md`](prompts/financial_analysis.md) | Parse 10-K/10-Q filings and extract key metrics |
| Revenue Forecasting | [`prompts/revenue_forecast.md`](prompts/revenue_forecast.md) | Generate multi-scenario revenue projections |
| Pitch Deck Outliner | [`prompts/pitch_deck.md`](prompts/pitch_deck.md) | Structure a seed/Series A pitch deck |
| Earnings Call Summariser | [`prompts/earnings_call.md`](prompts/earnings_call.md) | Distil earnings transcripts into structured briefs |
| Compliance Risk Scanner | [`prompts/compliance_scanner.md`](prompts/compliance_scanner.md) | Flag potential regulatory issues in documents |

Each template uses `{{PLACEHOLDER}}` variables — swap them out manually or with the helper in `scripts/utils.py`.

---

## Scripts

| Script | What It Does |
|---|---|
| `scripts/financial_analysis.py` | Loads a filing, runs the analysis prompt, outputs structured JSON |
| `scripts/forecast_runner.py` | Generates bear/base/bull revenue scenarios from historical data |
| `scripts/pitch_deck_agent.py` | Multi-turn agent that asks clarifying questions then drafts a full outline |
| `scripts/utils.py` | Template loader, token counter, retry helpers |

---

## Notebooks

| Notebook | Description |
|---|---|
| [`notebooks/01_financial_analysis.ipynb`](notebooks/01_financial_analysis.ipynb) | Walk-through: analysing a 10-K excerpt end to end |
| [`notebooks/02_forecasting.ipynb`](notebooks/02_forecasting.ipynb) | Build and compare multi-scenario forecasts |
| [`notebooks/03_agent_tool_use.ipynb`](notebooks/03_agent_tool_use.ipynb) | Build a fintech agent with Claude tool use |

---

## Agent Patterns

The `agents/` directory contains composable patterns for multi-step workflows:

- **`agents/tool_use_financial.py`** — Agent with tool definitions for looking up stock data, calculating ratios, and generating charts.
- **`agents/chain_of_analysis.py`** — Sequential chain: ingest → extract → analyse → summarise.

---

## Configuration

All scripts respect these environment variables:

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Your API key (required) |
| `CLAUDE_MODEL` | `claude-sonnet-4-20250514` | Model to use |
| `MAX_TOKENS` | `4096` | Max output tokens |

---

## Contributing

PRs welcome. If you have a fintech prompt pattern that keeps coming up in your work, open an issue or submit a template.

1. Fork the repo
2. Create a branch (`git checkout -b feat/my-new-prompt`)
3. Add your template to `prompts/` and a matching script if applicable
4. Submit a PR

---

## License

MIT — see [LICENSE](LICENSE).

---

## Resources

- [Anthropic API Docs](https://docs.claude.com/en/api/overview)
- [Prompt Engineering Guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Tool Use Documentation](https://docs.claude.com/en/docs/build-with-claude/tool-use/overview)
