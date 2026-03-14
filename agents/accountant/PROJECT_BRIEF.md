# WISE Bank Reconciliation Project

## Objective
Categorize 2113 WISE transactions (2019-2026) to Xero account codes for Leif Oh Leif Distribution.

## Progress Summary
- **Total transactions:** 2113
- **Mapped:** ~2104
- **Still needs review:** 509
- **Current file:** `reconciliation_current.csv` (v28)

## Work Completed
1. ✅ Mapped sales receipts → 200 (Sales)
2. ✅ Mapped supplier payments → 630 (Inventory)
3. ✅ Mapped currency conversions → 850 (Suspense - temporary clearing)
4. ✅ Mapped ATM withdrawals → 880 (Owner A Drawings)
5. ✅ Mapped various expense patterns:
   - Office expenses → 453
   - Travel → 493/494
   - Subscriptions → 485
   - Motor vehicle → 449
   - Freight → 425
   - And others (see chart of accounts)

## Current Challenge
**509 card transactions need categorization**, mostly:
- Groceries (personal vs business?)
- Cafes/restaurants (meals, meetings?)
- Fuel/car expenses
- Car rental
- Travel expenses
- SaaS/subscriptions
- Other miscellaneous purchases

## Context
- Business: Product distribution/import
- Owner: Morgan (Australia)
- Banking: WISE multi-currency account
- Currencies: AUD (primary), EUR, USD, CNY, GBP, HKD, AED

## Mapping Rules Created
- Income from "LEIF OH LEIF DISTRIBUTION PTY LTD" → 200 Sales
- Payments to suppliers (Marleen, Iveta, Thorsten, etc.) → 630 Inventory
- Currency conversions → 850 Suspense
- ATM withdrawals (Volksbank, Deutsche Bank, etc.) → 880 Owner A Drawings
- Owner transfers → 850 Suspense (temporary clearing)
- Card fees, Wise fees → mapped as appropriate

## Next Steps
Categorize remaining card transactions with consideration for:
1. GST treatment
2. Personal vs business use
3. Appropriate expense categorization
4. Owner drawings vs company expenses
5. Documentation/substantiation requirements (ATO)

## Files
- **Chart of accounts:** `xero-chart-of-accounts.txt`
- **Current reconciliation:** `reconciliation_current.csv`
- **Source statements:** `/Users/userclaw/.openclaw/workspace/inbox/wise/statement_*.pdf`
