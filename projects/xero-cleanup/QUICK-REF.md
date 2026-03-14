# Quick Reference Card

Keep this open while fixing transactions in Xero.

## Priority Order (Start Here)

1. **Travel International (494)** - 396 txns - Change BASEXCLUDED → INPUT
2. **Merchant Fees (405)** - 217 txns - Change INPUT → BASEXCLUDED
3. **Travel National (493)** - 73 txns - Change to INPUT
4. **Rent Expenses (469)** - 65 txns - Change to INPUT
5. **Entertainment (420)** - 115 txns - Change INPUT → BASEXCLUDED
6. **Refunds (265)** - 104 txns - Change OUTPUT → EXEMPTOUTPUT
7. **Rent Received (255)** - 98 txns - Change OUTPUT → EXEMPTOUTPUT

## Xero Navigation

**Get to transactions:**
1. Reports → Account Transactions
2. Select account code
3. Filter: "Unreconciled" only
4. Click Edit on each transaction
5. Change Tax Rate
6. Save

## Tax Rate Translations

**Xero labels:**
- "GST on Income" = OUTPUT
- "GST Free Income" = EXEMPTOUTPUT
- "GST on Expenses" = INPUT
- "GST Free Expenses" = EXEMPTEXPENSES
- "BAS Excluded" = BASEXCLUDED

## Common Fixes

**Most operating expenses** → "GST on Expenses" (INPUT)  
**Financial services** (bank/merchant fees) → "BAS Excluded"  
**Residential rent received** → "GST Free Income"  
**Entertainment** → "BAS Excluded"  
**Fines/penalties** → "BAS Excluded"  

## Session Flow

1. Pick one priority account
2. Set 30-45 min timer
3. Fix one batch (50 transactions or less)
4. Check box in MANUAL-FIX-WORKFLOW.md
5. Log in progress-log.md
6. Take 5-10 min break
7. Repeat or stop for day

## Track Progress

Open in split screen:
- This card (Quick Ref)
- MANUAL-FIX-WORKFLOW.md (checkboxes)
- Xero in browser

---

**Current session:** Account _____ | Batch _____ | Fixed: _____
