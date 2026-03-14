# Accountant Call Notes — Monday 23 Feb 2026

## ✅ COMPLETED TODAY (before call)

### Owner Funds Introduced (881) - Major Reclassification:
- **Analyzed 272 transactions ($156,261)** originally coded as Owner Funds Introduced
- **Reclassified 190 transactions ($100,958)** to revenue accounts:
  - 201 Income - Sean Maxwell Ferguson: $25,928 (PA work)
  - 202 Income - Labouring: $11,799 (Sky Point Roofing + Jamaal Stevens)
  - 203 Income - Car Sale: $12,180 (Erwin MacDowell + Gary Triggs)
  - 204 Income - Maxine Pemble: $5,414 (loan repayment)
  - 205 Income - Personal/Misc: $14,607 (various personal transfers)
  - 255 Rent Received: $31,030 (Jodie/James + Dan Smith flatmate rent)
- **Reclassified 35 transactions ($23,271)** company transfers → 877 Tracking Transfers (inter-account)
- **Kept 47 transactions ($32,032)** as legitimate owner funds (Morgan personal → business transfers)

### New Accounts Created:
- 201 Income - Sean Maxwell Ferguson (Revenue, GST on Income)
- 202 Income - Labouring (Revenue, GST on Income)
- 203 Income - Car Sale (Revenue, GST on Income)
- 204 Income - Maxine Pemble (Revenue, GST on Income)
- 205 Income - Personal/Miscellaneous (Revenue, GST on Income)
- 206 Consulting Revenue (Revenue, GST on Income)

### Journal Entries Created:
- 6 journal entries for revenue reclassifications
- 1 journal entry for company transfer reclassification

### Notes:
- **Entertainment (420) and Motor Vehicle (449)** left in place for you to review
- All work done via Xero API (OAuth2 connected, read + write access)

---

## 1. Entertainment (420) Reclassification

Currently **317 transactions totalling $14,450** all coded to 420 Entertainment (BAS Excluded). Most are actually solo meals, groceries, personal expenses, or non-entertainment business costs. Proposing to reclassify via journal entries since all transactions are already reconciled.

**Proposed split:**

| New Account | Code | Txns | Amount | Deductibility |
|---|---|---|---|---|
| Meals & Food (NEW) | 421 | 176 | $2,785 | Fully deductible (solo working meals ≤$35) |
| Entertainment (keep) | 420 | 69 | $5,638 | 50% deductible — need attendee records |
| Travel - International | 494 | 19 | $1,233 | Fully deductible (2019 German business trip) |
| Advertising | 400 | 2 | $2,000 | Fully deductible (Eddy Cobras video production) |
| Owner A Drawings | 880 | 52 | $2,810 | Not deductible (groceries, leisure, personal) |

### Questions:
- **$35 threshold for solo meals** — I used $35 as a cutoff for "clearly a solo working meal." Anything over that went to entertainment or drawings. Is that reasonable or should it be lower/higher?
- **Separate Meals account (421)?** — I created a new 421 Meals & Food account to separate solo meals from client entertainment. Is that the right approach, or should these go into an existing account like General Expenses (429)?
- **Entertainment without records** — There are 69 restaurant transactions over $35 that could be client dinners (friends who are also clients), but I don't have a formal log of who attended or the business purpose. Should I create retrospective records from memory, or is it safer to just move them all to drawings?
- **German trip meals → Travel International (494)?** — I was in Germany for business in mid-2019. I've coded all food/drink purchases from that trip to Travel International instead of entertainment. Is that correct for meals during an overseas business trip?
- **Journal grouping** — Should the adjusting journals be grouped by financial year, by month, or one lump entry?

---

## 2. Motor Vehicle Expenses (449) Reclassification

**53 transactions totalling $5,413** currently in Motor Vehicle Expenses. I don't have a business vehicle — these are all personal car costs (fuel, rego, servicing, repairs, towing). Proposing to move all to Owner Drawings except one Coles servo lunch ($15.50 → Meals).

### Questions:
- **Confirm all to drawings?** — Since there's no registered business vehicle or logbook, I'm assuming none of this is claimable. Is that correct?
- **Logbook method worth exploring?** — I do use my personal car for some business-related driving (deliveries, supplier visits). Would it be worth starting a logbook going forward to claim a percentage?

---

## 3. Wise Account Import

I imported 1,907 Wise bank transactions (Nov 2020 – Feb 2026) into a new Xero bank account called "Wise - Full Import" (code 091). The existing "Australian Dollar" Wise account that you (the accountant) set up has 295 transactions already coded.

### Duplicate Cleanup Issue:
- **~300-370 duplicate transactions** identified in Wise - Full Import (same date + amount from test imports)
- ✅ **Complete backup CSV created:** `wise-duplicates-voided-2026-02-23.csv` (all duplicate transaction IDs, dates, amounts, descriptions)
- ❌ **Cannot delete via API:** Xero API won't allow programmatic deletion of imported bank transactions (returns HTTP 400/404 errors)
- **Needs manual cleanup:** Either manually void/delete in Xero UI, or you may have bulk tools for this

### Questions:
- **Duplicate cleanup** — Best way to remove ~300-370 duplicates? Manual in Xero UI or do you have bulk tools?
- **Two Wise accounts** — Should we merge the new full import with your existing "Australian Dollar" account, or keep them separate? Don't want to mess up your existing work.
- **Account code mapping review** — I applied a conservative approach: meals only deductible if during overnight business travel, no vehicle deductions claimed, overseas shopping categorised as design reference samples. Happy to walk through the logic if you want to check it.

---

## 4. Other Xero Accounts

- **LOLD main account** — 2,829 transactions coded by Jason, but ~198 sitting in the reconciliation queue. Morgan will code these.
- **Private Bank Account** — 23 unreconciled SPEND-TRANSFER/RECEIVE-TRANSFER transactions (personal account Jason set up for tracking personal ↔ business transfers). Leave for Jason to reconcile - he'll know the matching logic.
- **Suspense (850)** — 206 transactions, mostly currency conversions (AUD ↔ EUR) + some owner transfer clearing. Net balance ~$29,353. Leave for Jason to review - may need specific forex gain/loss treatment per ATO rules.
- **Consulting Revenue account** — ✅ Created account 206 Consulting Revenue for the $5.7K from Wise

---

## 5. Key Numbers from Wise Reconciliation

For reference — here's how the full Wise account broke down:

- Business sales: $24.6K
- Photography income: $10.4K
- Consulting income: $5.7K
- Inventory/COGS: $112K
- Owner drawings: $32.5K
- Owner funds introduced: $156K
- Travel international: $14.3K
- 47 items flagged for review (defaulted to Owner Drawings — conservative)

**Total additional Owner Drawings from today's reclassification: ~$8,207** (entertainment + motor vehicle moves)

---

## 6. PayPal Transactions

**Note:** The PayPal account in Xero is set up as the "Australian Dollar" account. Need to ask Jason how to properly handle PayPal transactions — specifically whether they should stay coded to this account or if there's a different approach for tracking PayPal vs regular Wise transactions.

---

## 7. Going Forward

- **Entertainment log template** — I want to start properly recording client meals going forward. What format do you need? I'm thinking a simple spreadsheet: date, venue, amount, who attended, business purpose.
- **Bank rules** — Should we set up Xero bank rules to auto-categorise common vendors (McDonalds → Meals, BP → Drawings, etc.) for future transactions?

---

## 8. Follow-Up Questions (Added Feb 25, 2026)

- **GST on Rent Received** — Need to clarify GST treatment for rent received (account 255). Currently coded as "GST on Income" — is this correct, or should rent be GST-free?

---

## Reference Files (on my system)
- `entertainment_final_v2.csv` — full classified transaction list (420 reclassification)
- `entertainment_classified.csv` — earlier version with different splits
- `owner-funds-reclassification-analysis.md` — detailed breakdown of 881 reclassification
- `owner-funds-reclassification.csv` — all 272 transactions with proposed reclassifications
- `wise-duplicates-voided-2026-02-23.csv` — 369 duplicate transactions (backup before cleanup)
- `881-remaining-reclassification.md` — analysis of remaining 881 transactions
- `creditor-accounts-proposal.md` — original creditor account structure (not used - went with revenue accounts instead)
- Xero Chart of Accounts: `docs/xero-chart-of-accounts.txt`
- Xero API connected (read + write, OAuth2)
