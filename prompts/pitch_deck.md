# Pitch Deck Outliner

## System Prompt

```
You are an experienced startup advisor who has helped dozens of companies raise seed and Series A rounds. Given information about a startup, create a compelling pitch deck outline that follows best practices from top-tier VC firms. Be specific — generic platitudes don't win funding rounds.
```

## User Prompt Template

```
Create a pitch deck outline for the following startup.

<startup_info>
Company: {{COMPANY_NAME}}
Stage: {{STAGE}}
Sector: {{SECTOR}}
One-liner: {{ONE_LINER}}
Problem: {{PROBLEM}}
Solution: {{SOLUTION}}
Traction: {{TRACTION}}
Team: {{TEAM}}
Ask: {{FUNDRAISE_ASK}}
</startup_info>

Produce a slide-by-slide outline in JSON:

{
  "deck_title": "string",
  "total_slides": "number",
  "slides": [
    {
      "slide_number": "number",
      "title": "string",
      "purpose": "string — what this slide should accomplish",
      "key_content": ["string — bullet points for the slide"],
      "visual_suggestion": "string — chart, screenshot, diagram, etc.",
      "speaker_notes": "string — what the founder should say"
    }
  ],
  "appendix_suggestions": ["string — extra slides to have ready for Q&A"]
}

Aim for 10-14 slides. Follow this general arc:
1. Hook / Title
2. Problem
3. Solution
4. Market size (TAM/SAM/SOM)
5. Product demo / screenshots
6. Business model
7. Traction / metrics
8. Competition / differentiation
9. Go-to-market
10. Team
11. Financials / projections
12. The Ask
```

## Usage Notes

- The more specific `{{TRACTION}}` and `{{TEAM}}` are, the better the output. Include real numbers and backgrounds.
- The `visual_suggestion` field is helpful if you're handing this to a designer.
- Combine with `revenue_forecast.md` to auto-generate the financials slide content.

## Example Variables

| Variable | Example Value |
|---|---|
| `{{COMPANY_NAME}}` | `PayFlow` |
| `{{STAGE}}` | `Seed` |
| `{{SECTOR}}` | `B2B Payments / Fintech` |
| `{{ONE_LINER}}` | `Instant cross-border payroll for remote teams` |
| `{{FUNDRAISE_ASK}}` | `$3M seed at $15M post-money` |
