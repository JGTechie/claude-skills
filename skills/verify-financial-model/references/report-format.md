# Review Report Format

Return in chat by default. Create a standalone report only if requested or the host's artifact workflow requires it; never modify the workbook to store the report without permission.

## Executive summary

- Workbook/version, review date, mode, scope and evidence source.
- Overall result: mechanical issues found / incomplete verification / no mechanical issues found within tested scope.
- Highest-priority findings and business consequences, in plain English.
- Coverage: checks and ranges tested, sampling, missing sources, unsupported features, live recalculation performed or not.
- Explicit commercial/accounting/tax/legal questions still requiring the responsible owner. Human review remains necessary before delivery.

## Findings

| ID | Priority | Status | Sheet/cell or range | Finding | Expected vs observed | Evidence/method | Proposed next step / owner |
|---|---|---|---|---|---|---|---|

Use P1 for material output defects or delivery blockers, P2 for other substantive issues, P3 for clarity/usability. State why material; do not invent a materiality threshold. NOT RUN can be a blocker without being a detected defect.

For each numerical finding record units, period, source values, expected relationship, tolerance, observed value and delta. Cite sources as well as destination cells. Quoted figures must actually have been read; never fabricate cell references to make a report look precise.

## Coverage register

| Check ID | Status | Ranges tested | Test method | Evidence/result | Limitation or applicability reason |
|---|---|---|---|---|---|

Include C01-C12 for delivery mode; for change mode list selected tests and excluded modules. Split partially tested modules into subchecks rather than assigning a blanket PASS. Summarize counts only from the register, not intuition. Use NOT APPLICABLE only for genuinely absent features, not inaccessible evidence.

## Behavior evidence, if authorized

| Test | Copy identity | Input before/after | Prediction | Recalculation evidence | Observed output before/after | Baseline restored |
|---|---|---|---|---|---|---|

## Next actions

Separate formula fixes, missing information and owner judgments. Record what has not been changed. If fixes were explicitly authorized, include before/after references and retest results. Do not turn recommended actions into claimed completions.

## Fictional example, not a result from a client workbook

**Result: mechanical issues found; behavior verification incomplete.**

- P1 / FAIL / Cash!F12: closing cash shown as 90; expected 60 (GBP thousands). Independently recomputed from Cash!F5 opening cash 100, F7 receipts 50, F8 payments -80 and F9 capex -10. Delta +30; tolerance 0.001. Inspect the F12 formula for omitted/incorrect movements.
- P1 / FAIL / Summary!C8: ARR shown as 780; expected 1,200 (GBP thousands) under the stated closing-MRR x 12 definition, using Revenue!N20 closing MRR 100. The output instead links to annual recognized revenue. No conclusion on revenue-recognition policy.
- NOT RUN / C03: latest management-approved forecast assumptions were not supplied; current inputs cannot be reconciled to approval evidence.
- NEEDS JUDGMENT / C05: sales ramp is mechanically implemented but customer evidence and launch timing require management confirmation.
- NOT RUN / C10: no permission for a test copy; no scenario response has been observed. Original workbook unchanged.
