# Xero Tax Rate Manual Fix Workflow

**Total to fix:** 698 unreconciled transactions with incorrect tax rates

## Priority Order (Biggest Impact First)

### ✅ **PRIORITY 1: Travel International (Account 494)**
**Impact:** 405 transactions marked BASEXCLUDED, should be INPUT (claimable GST)
**BAS impact:** HIGH - missing claimable expenses
**Fixable:** ~396 unreconciled

**How to fix in Xero:**
1. Reports → Account Transactions → Account 494 (Travel - International)
2. Filter: Status = Draft/Awaiting Payment (unreconciled)
3. For each transaction:
   - Click Edit
   - Change Tax Rate from "BAS Excluded" to "GST on Expenses"
   - Save
4. Track progress below

**Progress tracker:**
```
[ ] Batch 1: 0-50 transactions
[ ] Batch 2: 51-100
[ ] Batch 3: 101-150
[ ] Batch 4: 151-200
[ ] Batch 5: 201-250
[ ] Batch 6: 251-300
[ ] Batch 7: 301-350
[ ] Batch 8: 351-396 ✓
```

---

### ✅ **PRIORITY 2: Merchant Fees (Account 405)**
**Impact:** 217 transactions marked INPUT, should be BASEXCLUDED
**BAS impact:** HIGH - incorrectly claiming GST on financial services
**Fixable:** ~217 unreconciled

**How to fix in Xero:**
1. Reports → Account Transactions → Account 405 (Merchant Fee)
2. Filter: Unreconciled only
3. For each transaction:
   - Click Edit
   - Change Tax Rate from "GST on Expenses" to "BAS Excluded"
   - Save

**Progress tracker:**
```
[ ] Batch 1: 0-50 transactions
[ ] Batch 2: 51-100
[ ] Batch 3: 101-150
[ ] Batch 4: 151-200
[ ] Batch 5: 201-217 ✓
```

---

### ✅ **PRIORITY 3: Travel National (Account 493)**
**Impact:** 159 mismatches (mix of EXEMPTEXPENSES/BASEXCLUDED, should be INPUT)
**BAS impact:** HIGH - missing claimable travel expenses
**Fixable:** ~73 unreconciled

**How to fix in Xero:**
1. Reports → Account Transactions → Account 493 (Travel - National)
2. Filter: Unreconciled only
3. Change all to "GST on Expenses"

**Progress tracker:**
```
[ ] Batch 1: 0-40 transactions
[ ] Batch 2: 41-73 ✓
```

---

### ✅ **PRIORITY 4: Rent Expenses (Account 469)**
**Impact:** 145 mismatches (should be INPUT for commercial rent)
**BAS impact:** MEDIUM-HIGH
**Fixable:** ~65 unreconciled

**How to fix in Xero:**
1. Reports → Account Transactions → Account 469 (Rent)
2. Filter: Unreconciled only
3. Change to "GST on Expenses"

**Progress tracker:**
```
[ ] Batch 1: 0-35 transactions
[ ] Batch 2: 36-65 ✓
```

---

### ✅ **PRIORITY 5: Entertainment (Account 420)**
**Impact:** 125 marked INPUT, should be BASEXCLUDED (non-deductible)
**BAS impact:** MEDIUM - incorrectly claiming entertainment
**Fixable:** ~115 unreconciled

**How to fix in Xero:**
1. Reports → Account Transactions → Account 420 (Entertainment)
2. Filter: Unreconciled only
3. Change from "GST on Expenses" to "BAS Excluded"

**Progress tracker:**
```
[ ] Batch 1: 0-50 transactions
[ ] Batch 2: 51-100
[ ] Batch 3: 101-115 ✓
```

---

### ✅ **PRIORITY 6: Refunds (Account 265)**
**Impact:** 110 marked OUTPUT, should be EXEMPTOUTPUT
**BAS impact:** MEDIUM
**Fixable:** ~104 unreconciled

**How to fix in Xero:**
1. Reports → Account Transactions → Account 265 (Refunds)
2. Filter: Unreconciled only
3. Change from "GST on Income" to "GST Free Income"

**Progress tracker:**
```
[ ] Batch 1: 0-50 transactions
[ ] Batch 2: 51-100
[ ] Batch 3: 101-104 ✓
```

---

### ✅ **PRIORITY 7: Rent Received (Account 255)**
**Impact:** 98 marked OUTPUT, should be EXEMPTOUTPUT
**BAS impact:** HIGH - residential rent is GST-free
**Fixable:** ALL 98 unreconciled ✓

**How to fix in Xero:**
1. Reports → Account Transactions → Account 255 (Rent Received)
2. Filter: Unreconciled only
3. Change from "GST on Income" to "GST Free Income"

**Progress tracker:**
```
[ ] Batch 1: 0-50 transactions
[ ] Batch 2: 51-98 ✓
```

---

### ⚠️ **PRIORITY 8: Lower Volume / Less Critical**

**Cost of Goods (Account 310):** 146 mismatches → ~65 fixable  
**Subscriptions (Account 485):** 92 mismatches → ~85 fixable  
**Bank Fees (Account 404):** 59 mismatches → ~49 fixable  
**Advertising (Account 400):** 52 mismatches → ~28 fixable  
**Office Expenses (Account 453):** 44 mismatches → ~44 fixable  
**Motor Vehicle (Account 449):** 43 mismatches → ~37 fixable  
**Fines (Account 504):** 37 marked INPUT, should be BASEXCLUDED → ~6 fixable  

*(Continue with remaining accounts as time permits)*

---

## Daily Workflow Template

**Session goal:** Fix 1-2 priority accounts per session (30-60 min work blocks)

### Before you start:
1. [ ] Open Xero in browser
2. [ ] Have this checklist visible
3. [ ] Set timer for 30-45 min (pomodoro)
4. [ ] Pick ONE priority account to tackle

### During fix session:
1. [ ] Navigate to account in Xero
2. [ ] Filter for unreconciled transactions
3. [ ] Work through batch (track with checkboxes above)
4. [ ] Take 5 min break between batches

### After session:
1. [ ] Update progress tracker (check boxes)
2. [ ] Note completion in memory/YYYY-MM-DD.md
3. [ ] If account complete, move to next priority

---

## Quick Reference: Tax Rate Changes

**Income:**
- OUTPUT → EXEMPTOUTPUT (Rent, Refunds, Interest)

**Expenses:**
- BASEXCLUDED → INPUT (Travel, Subscriptions, most operating expenses)
- INPUT → BASEXCLUDED (Merchant fees, Bank fees, Fines, Depreciation, Entertainment)
- EXEMPTEXPENSES → INPUT (most operating expenses)

**When unsure:** Check existing correct transactions in that account for pattern.

---

## Completion Tracking

**Started:** ________________  
**Target completion:** ________________

**Accounts completed:**
- [ ] Priority 1: Travel International (396 txns)
- [ ] Priority 2: Merchant Fees (217 txns)
- [ ] Priority 3: Travel National (73 txns)
- [ ] Priority 4: Rent Expenses (65 txns)
- [ ] Priority 5: Entertainment (115 txns)
- [ ] Priority 6: Refunds (104 txns)
- [ ] Priority 7: Rent Received (98 txns)
- [ ] Priority 8: Remaining accounts (as time permits)

**Total fixed:** _______ / 698

---

## Tips

✅ **Work in batches** - Don't try to do all 698 at once  
✅ **Start with high-impact** - Travel/Merchant fees affect BAS most  
✅ **Use Xero filters** - "Unreconciled" filter is your friend  
✅ **Take breaks** - 30-45 min sessions with 5-10 min breaks  
✅ **Track progress** - Check boxes = dopamine hits = momentum  

⚠️ **Skip reconciled transactions** - You can't change them (they're in the 1,530 skipped count)

---

**When you're done with a priority, update this file and commit progress to memory.**
