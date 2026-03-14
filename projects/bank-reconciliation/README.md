# WISE Bank Reconciliation Project

## Current Status
**Latest file:** `output/wise_reconciliation_v28.csv`  
**Progress:** 2104/2113 mapped, 509 flagged for review  
**Started:** Feb 18, 2026  
**Last updated:** Feb 19, 2026

## Objective
Map 2113 WISE transactions (2019-2026) to Xero account codes for Leif Oh Leif Distribution Pty Ltd.

## Work Completed (v1-v28)

### ✅ Mapping Rules Applied
1. **Sales receipts** → 200 Sales
   - Income from "LEIF OH LEIF DISTRIBUTION PTY LTD"
   
2. **Supplier payments** → 630 Inventory  
   - Marleen Fitterer, Iveta Lipina, Thorsten Albers, Terese Schoermer, etc.

3. **Currency conversions** → 850 Suspense  
   - All "Converted X to Y" transactions (184 transactions)

4. **ATM withdrawals** → 880 Owner A Drawings  
   - Volksbank, Deutsche Bank, Spk withdrawals (4 transactions)

5. **Various expense patterns:**
   - Office expenses → 453
   - Travel domestic → 493
   - Travel international → 494
   - Subscriptions → 485
   - Motor vehicle → 449
   - Freight → 425
   - And others per chart of accounts

### 🚨 Issues Identified (Accountant Review - Feb 19)

**Major finding:** ~350-400 of the 509 remaining transactions are **personal expenses** paid from the Wise business card, not legitimate business expenses.

**Categories needing reclassification:**
- Groceries (Coles, Carrefour, IGA) → should be 880 Drawings
- Most cafes/restaurants (McDonald's, KFC, casual dining) → should be 880 Drawings
- Personal entertainment (cinemas, sports) → should be 880 Drawings
- Medical/vet/grooming → should be 880 Drawings
- Personal subscriptions (YouTube, Prime Video) → should be 880 Drawings
- Personal shopping (clothes, outdoor gear) → should be 880 Drawings

**Large meals to verify:** Some may be legitimate business entertainment
- Walter's Steakhouse $368
- Bask Restaurant $779  
- Italian Street Kitchen $230

**Compliance gaps identified:**
1. **No motor vehicle logbook** → Cannot claim any car expenses without a valid 12-week logbook (ATO requirement)
2. **Travel diaries missing** → International trips >6 nights need written diary or claim is disallowed
3. **Personal/business separation** → Wise card is heavily used for personal spending

## Next Steps

### Option 1: Accept accountant recommendations (bulk recode)
Recode ~350 transactions to 880 Owner Drawings as recommended. This is the compliant approach but means re-doing significant work.

### Option 2: Morgan review first
Go through the accountant's report and decide which transactions are genuinely business vs personal before bulk changes.

### Option 3: Fresh start with better separation
- Archive current reconciliation as "needs review"
- Going forward: use Wise card ONLY for business
- Establish motor vehicle logbook
- Keep travel diaries for international trips

## Files

### Source Data
- `data/statement_*` — Original WISE bank statements (PDFs)

### Documentation
- `docs/xero-chart-of-accounts.txt` — Full Xero chart
- `docs/Leif Oh Leif Distribution - Chart of Accounts (1).pdf` — Original PDF

### Output
- `output/wise_reconciliation_v*.csv` — Progressive versions
- **Current:** `output/wise_reconciliation_v28.csv`

### CSV Format
- Date, Description, Amount, Currency, Balance, Direction
- XeroAccountCode, XeroAccountName
- NeedsReview (yes/no), ReviewNote
- SourceFile, RuleVersion

## Account Codes Reference (Commonly Used)

| Code | Account Name | Type |
|------|-------------|------|
| 200 | Sales | Revenue |
| 420 | Entertainment | Expense (50% deductible, no GST) |
| 425 | Freight & Courier | Expense |
| 449 | Motor Vehicle Expenses | Expense |
| 453 | Office Expenses | Expense |
| 485 | Subscriptions | Expense |
| 489 | Telephone & Internet | Expense |
| 493 | Travel - National | Expense |
| 494 | Travel - International | Expense |
| 630 | Inventory | Direct Costs |
| 850 | Suspense | Current Liabilities (clearing) |
| 880 | Owner A Drawings | Current Liabilities |
| 881 | Owner A Funds Introduced | Current Liabilities |

## Accountant Agent

An on-demand accounting specialist is available for tax/compliance advice:
- Location: `/Users/userclaw/.openclaw/workspace/agents/accountant`
- Spawn via Choncho when needed
- Has access to this project workspace and Xero chart
- Provides AU tax/ATO guidance

## Decision Required from Morgan

Before proceeding, need to decide:

1. **Motor vehicle logbook** — Do you have one? If not, all car expenses must go to 880 Drawings until established.

2. **Which big meals were business?** — Flag specific transactions that were genuine client/supplier entertainment

3. **Travel classification** — Which trips were business vs personal?
   - Berlin (Supreme buying) = business ✅
   - Hong Kong / Japan / Italy / Sunshine Coast = ?

4. **Approach going forward:**
   - Bulk recode to comply with accountant recommendations?
   - Manual review of each flagged item?
   - Accept current state and improve separation going forward?
