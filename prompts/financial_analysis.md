# Financial Statement Analysis

## System Prompt

```
You are a senior financial analyst. Given a company filing excerpt, produce a structured analysis covering the sections below. Be precise with numbers — cite page or section references where possible. If data is missing, say so explicitly rather than guessing.
```

## User Prompt Template

```
Analyse the following financial report excerpt and produce a structured brief.

<report>
{{REPORT}}
</report>

<company>{{COMPANY_NAME}}</company>
<period>{{FISCAL_PERIOD}}</period>

Return your analysis as JSON with these keys:

{
  "company": "string",
  "period": "string",
  "revenue": {
    "total": "number or null",
    "yoy_growth_pct": "number or null",
    "segments": [{"name": "string", "revenue": "number"}]
  },
  "profitability": {
    "gross_margin_pct": "number or null",
    "operating_margin_pct": "number or null",
    "net_margin_pct": "number or null"
  },
  "balance_sheet_highlights": {
    "total_assets": "number or null",
    "total_debt": "number or null",
    "cash_and_equivalents": "number or null",
    "debt_to_equity": "number or null"
  },
  "cash_flow": {
    "operating_cf": "number or null",
    "capex": "number or null",
    "free_cash_flow": "number or null"
  },
  "key_risks": ["string"],
  "analyst_notes": "string — your 2-3 sentence overall assessment"
}
```

## Usage Notes

- Works best with 10-K and 10-Q excerpts. For earnings call transcripts, use `earnings_call.md` instead.
- The JSON output schema makes it easy to pipe results into dashboards or downstream agents.
- For very long filings, chunk the document and run this prompt per-section, then use a second pass to merge.

## Example Variables

| Variable | Example Value |
|---|---|
| `{{COMPANY_NAME}}` | `Apple Inc.` |
| `{{FISCAL_PERIOD}}` | `FY2025 Q1` |
| `{{REPORT}}` | *(paste 10-K excerpt)* |
