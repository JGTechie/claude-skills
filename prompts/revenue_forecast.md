# Revenue Forecasting — Multi-Scenario

## System Prompt

```
You are a quantitative financial analyst specialising in revenue modelling. Given historical revenue data and context about a company, produce bear / base / bull revenue forecasts for the requested horizon. Show your assumptions clearly and explain the drivers behind each scenario.
```

## User Prompt Template

```
Generate a multi-scenario revenue forecast for {{COMPANY_NAME}}.

<historical_data>
{{HISTORICAL_REVENUE_CSV}}
</historical_data>

<context>
{{BUSINESS_CONTEXT}}
</context>

<horizon>{{FORECAST_QUARTERS}} quarters</horizon>

For each scenario (bear, base, bull), provide:

1. Quarterly revenue projections as a CSV table (quarter, revenue, yoy_growth_pct)
2. Key assumptions (2-3 bullet points per scenario)
3. Primary risk or upside driver

Format your response as JSON:

{
  "company": "string",
  "horizon_quarters": "number",
  "scenarios": {
    "bear": {
      "assumptions": ["string"],
      "primary_driver": "string",
      "projections": [
        {"quarter": "string", "revenue": "number", "yoy_growth_pct": "number"}
      ]
    },
    "base": { ... },
    "bull": { ... }
  },
  "methodology_note": "string — brief description of how you arrived at these numbers"
}
```

## Usage Notes

- Supply at least 4-8 quarters of historical data in CSV form (columns: `quarter, revenue`).
- The `{{BUSINESS_CONTEXT}}` field should include sector, recent product launches, macro headwinds, competitive landscape — anything that shapes the outlook.
- Pair this with `financial_analysis.md` output for a more grounded forecast.

## Example Variables

| Variable | Example Value |
|---|---|
| `{{COMPANY_NAME}}` | `Stripe` |
| `{{FORECAST_QUARTERS}}` | `4` |
| `{{HISTORICAL_REVENUE_CSV}}` | `quarter,revenue\nQ1-2024,4200\nQ2-2024,4500\n...` |
| `{{BUSINESS_CONTEXT}}` | `B2B payments, expanding into lending, strong developer adoption...` |
