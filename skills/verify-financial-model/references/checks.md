# Check Catalogue

Use applicable modules, not a universal financial-model architecture. Record applicability for all IDs in delivery mode. No balance sheet means C07 is NOT APPLICABLE and three-statement integration cannot be claimed.

## C01: Workbook integrity and calculation evidence

Inventory accessible visible/hidden sheets, names, links, connections, macros, calculation mode and iterative settings. Scan accessible used ranges for formula errors and broken references, including defined names and external dependencies. Log data tables, unsupported functions, protected/unreadable sheets and inaccessible links as coverage limits, not automatic formula failures.

Check stale/manual-calculation risks. Record the last demonstrable recalculation, not a guessed timestamp. A missing saved formula value is NOT RUN for value validation, not proof the formula is broken. An error hidden by IFERROR may still invalidate the model; trace error-suppression formulas on material outputs. Do not launch macros or fetch links to investigate.

## C02: Periods, units and actual/forecast boundary

Check each period label in the covered horizon for gaps, duplicates, fiscal-year differences and date/text inconsistencies. Establish currency, GBP vs GBP thousands, percentages, monthly vs annual rates, and inflow/outflow conventions. Ensure historical periods are not overwritten by forecast assumptions and actuals are not counted again in forecasts. Inspect the boundary and first/last forecast periods explicitly.

## C03: Source and version reconciliation

Tie imported actuals to identified source reports by entity, account, currency and period. Reconcile revenue, operating profit and closing cash where sources permit. Compare prior/current versions when supplied, separating authorized input changes, formula changes and unexplained differences. Identify pending/unapproved assumptions and source timestamps. Do not silently promote the latest file or sales draft to management-approved status.

Example: an MRR schedule and accounting revenue are different bases. Quantify and explain their reconciliation; do not automatically declare their difference an error or equate MRR with recognized revenue.

## C04: Formula continuity and hardcodes

Compare formulas across time and segments, using relative-reference patterns where available. Inspect references to wrong months, omitted segments, anchored inputs, range endpoints, circularity and hardcoded outputs in formula sequences. Trace first/middle/last periods and every detected exception. Sampling those periods alone is not a full continuity scan. Historical hardcodes and intentional phase changes can be valid; confirm intent before classifying.

## C05: Revenue drivers and recurring metrics

Independently test the intended model, not a forced SaaS template:
- Price x quantity/units, contract start, ramp, milestones, renewal, churn, probability and capacity as applicable.
- Segment totals to group totals; distinguish revenue recognition, bookings, billing and collections.
- Customer/subscription roll-forwards: opening + new - churn, with expansion/contraction separately where defined. Avoid double-counting overlapping movements.
- MRR and ARR according to documented definitions. If ARR = period-end MRR x 12, compare to that relationship, not annual recognized revenue or summed monthly ARR.
- Recurring licensing vs ongoing services vs one-off project revenue, with explicit classification assumptions. A multi-year contract alone does not prove recurrence or recognition timing.
- Commercial milestones such as TRLs need approved input assumptions. Do not invent probabilities, prices, market sizes or launch dates to fill gaps.

Separate mechanical implementation from whether management's forecast is credible. Abrupt growth needs an evidenced explanation, not smoothing merely to match a target.

## C06: Costs, hiring and margins

Recompute headcount/FTE x compensation x start-date proration and relevant taxes/benefits, respecting the documented basis. Check COGS/variable cost drivers, capex vs expense, depreciation timing and profit subtotals. Test that costs remain when revenue is delayed if the plan still incurs those costs. A removed revenue vertical does not automatically remove associated research or hiring costs.

## C07: Statement integration, if present

Test assets = liabilities + equity by period. Reconcile retained earnings using the actual model's profit, distribution and other movement conventions. Reconcile debt, fixed assets/depreciation and working-capital schedules to the statements. Test cash-flow closing cash to balance-sheet cash. Trace unexplained plugs: a balancing cash/debt/equity figure can hide a missing relationship. A zero balance check is necessary but not sufficient.

## C08: Cash flow and runway

Verify every covered period: opening cash + signed net movements = closing cash; next opening = prior closing. Recompute net movements from independently identified receipts, payments, investment and financing lines. Check collection/payment lags, receivables/payables roll-forwards, deposits, restricted cash, minimum cash and financing timing where modeled. Distinguish accrued expenses from payments and profit from cash.

For indirect cash flow, reconcile profit, noncash adjustments and signed working-capital changes; avoid adding both revenue and customer receipts. For direct cash flow, reconcile receipts/payment schedules instead of treating revenue as cash.

Report runway using the documented liquidity threshold and forecast cash path. Do not infer "no funding needed" from a funding plug or divide current cash by one month's burn when burn varies substantially.

## C09: Annual summaries, dashboards and handover

Reconcile output cells and charts to the correct scenario, version, period and schedules. Sum flows (revenue/expense) across included months; use period-end stocks (cash/debt/ARR where defined); calculate averages and ratios on their defined basis. Do not sum rates or average margins when a weighted ratio is required. Check fiscal-year range endpoints and investor vs operating metrics separately.

Check whether input cells, sources, units, limitations and version history are clear enough for a new operator. Do not add tabs or formatting as part of the review.

## C10: Controlled behavior tests

Only after authorization for a disposable copy and with demonstrated recalculation. These are test candidates, not universal truths; adapt to the model's design and predict exceptions before executing.

| Perturbation | Expected behavior to define and observe |
|---|---|
| Raise unit price 10%, all else fixed | Relevant revenue rises as specified; confirm discounts, caps and currency treatment; collections follow billing/payment terms. |
| Delay a contract start one month | Revenue shifts according to the recognition design; cash follows collection terms, not necessarily the same month. |
| Extend collection lag by one month | Collections shift, early cash may fall and receivables may rise; accounting revenue stays unchanged if recognition is independent. |
| Add one hire at a specified start date | Payroll and cash change on their respective timing bases, including related benefits/taxes where modeled. |
| Set new sales to zero or increase churn | New-business contribution changes; existing contracted revenue need not disappear. |
| Switch scenario, then restore baseline | Intended drivers and outputs respond; the restored baseline matches recorded values and formulas. |

Run relevant tests, ideally including a timing test and a boundary case. Record input before/after, prediction, recalculation method, outputs before/after, and restoration. If the user's permitted scope excludes perturbations, retain them as NOT RUN rather than silently omitting them.

## C11: Consolidation and intercompany, if present

Inspect entity mapping, FX basis, intra-group balances/transactions and elimination schedules. Compare both sides of each identified intercompany relationship; quantify residual differences. Investigate impacts on P&L, balance sheet and cash flow separately. Non-netting balances can reflect currency, timing, missing entries or misclassification; they do not prove any one cause.

Identify mechanics and evidence gaps only. Do not infer that absence of a transfer-pricing policy makes all consolidation impossible, or that a balanced elimination is tax-compliant. Correction periods, recognition policy, transfer pricing and returns require appropriate professional review.

## C12: Funding and cap table, if present

Check ownership denominators, share classes, options, existing instruments, proceeds vs fees, interest accrual, maturity and conversion mechanics against supplied terms. Independently recompute at least one conversion/dilution case when enough contractual detail exists. Distinguish pre-/post-money definitions and whether other instruments/options enter the denominator. Do not assume a SAFE is a convertible loan or assume standard terms.

With missing cap/discount/interest/conversion terms, mark affected calculations NOT RUN. Commercial valuation judgments and legal interpretations are NEEDS JUDGMENT. Illustrative sensitivity outputs are not a defensible investment recommendation by themselves.
