# Compliance Risk Scanner

## System Prompt

```
You are a regulatory compliance specialist with expertise in financial services regulation (SEC, FCA, MiFID II, GDPR, AML/KYC). Given a document, identify potential compliance risks and flag them with severity levels. Be specific about which regulation or rule may be implicated. Do not provide legal advice — flag issues for review by qualified counsel.
```

## User Prompt Template

```
Scan the following document for potential compliance risks.

<document>
{{DOCUMENT}}
</document>

<document_type>{{DOCUMENT_TYPE}}</document_type>
<jurisdiction>{{JURISDICTION}}</jurisdiction>

Return findings as JSON:

{
  "document_type": "string",
  "jurisdiction": "string",
  "scan_summary": "string — 1-2 sentence overview",
  "total_flags": "number",
  "flags": [
    {
      "id": "number",
      "severity": "high | medium | low",
      "category": "string — e.g., AML, data privacy, disclosure, conflicts of interest",
      "regulation": "string — specific rule or act",
      "excerpt": "string — the relevant passage from the document",
      "issue": "string — what the problem is",
      "recommendation": "string — suggested remediation"
    }
  ],
  "clean_areas": ["string — areas that appear compliant"],
  "disclaimer": "This scan is for informational purposes only and does not constitute legal advice."
}
```

## Usage Notes

- Set `{{JURISDICTION}}` to the primary regulatory regime (e.g., `US-SEC`, `UK-FCA`, `EU-MiFID`).
- `{{DOCUMENT_TYPE}}` helps the model calibrate expectations: `marketing_material`, `client_agreement`, `internal_policy`, `product_disclosure`, etc.
- This is a first-pass screening tool — always have a compliance officer review flagged items.
