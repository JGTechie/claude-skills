# Verify Financial Model

A reusable Claude skill for reviewing startup financial models before delivery or after changes.

## What it does

- Maps sources, assumptions, schedules, statements and outputs.
- Applies 12 check modules, including formula continuity, revenue drivers, cash flow, statement integration, consolidation and funding mechanics where applicable.
- Reports exact cell references, expected versus observed results, missing evidence and questions requiring human judgment.
- Separates static checks from demonstrated recalculation and behavior testing.

## Files

- [SKILL.md](SKILL.md): workflow and safety boundaries.
- [Check catalogue](references/checks.md): C01-C12 procedures.
- [Report format](references/report-format.md): findings and coverage register.
- [Acceptance tests](acceptance-tests.md): synthetic test specifications, not executed test results.

## Use

Load the complete skill folder into a host that supports custom skills, retaining the references subfolder. For an upload interface that accepts a skill ZIP, create the package from the repository root:

```sh
cd skills
zip -r verify-financial-model.zip verify-financial-model
```

Use the host's documented skill-installation process. This repository does not install or enable the skill automatically.

Provide the workbook and any authorized source reports, approved assumptions or prior version needed for the review. Example request:

> Use verify-financial-model to review this workbook before delivery. Keep the original unchanged. Report findings with cell-level evidence, distinguish missing evidence from failures, and disclose checks you cannot run. Ask before creating or changing a test copy.

For a narrower review:

> Review only the changed revenue assumptions and downstream cash-flow effects. Clearly label this a partial review.

## Limits and validation

This is a procedure, not an Excel integration, calculation engine or audit service. It requires a host with appropriate workbook-reading tools. Behavior tests require an authorized disposable copy and working recalculation; otherwise they must be reported as NOT RUN.

The default is read-only. The skill does not certify a model or endorse accounting, tax, legal or investment judgments. Do not upload confidential workbooks without authorization.

Run the acceptance tests with synthetic or sanitized data in your intended host before relying on the workflow for client delivery. No host acceptance-test results or general accuracy guarantee are claimed here.

Version: 1.0. Licensed under the repository's [MIT license](../../LICENSE).
