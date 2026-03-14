# Wise Multi-Currency Import - Progress Status

**Session Date:** Feb 25-26, 2026 (11:00 PM - 1:30 AM)  
**Status:** Framework Complete, Ready for Full Processing

---

## ✅ COMPLETED

### 1. Control Totals Established
**Source:** `raw/statement_16108725_AUD_2017-04-28_2026-02-26.csv`

| Metric | Value |
|--------|-------|
| **Total Transactions** | 2,070 |
| **Money IN (Credits)** | 436 txns, $198,003.59 |
| **Money OUT (Debits)** | 1,634 txns, -$197,962.09 |
| **Net Balance** | $41.50 |

**⚠️ ALL processed CSVs MUST match these totals before Xero import!**

Saved: `processed/control-totals.json`

---

### 2. Money IN Fully Categorized (436 transactions)

**Files Created:**
- `categorization-rules.json` - Payer-to-account mapping
- `processed/wise-aud-xero-import-CREDITS.csv` - Ready for import (after new accounts created)

**Summary:**
- ✅ Coded & Ready: 325 transactions
  - 200 Sales: 80 txns, $39,659
  - 201 Sean Maxwell Ferguson: 29 txns, $25,928
  - 265 Refunds: 66 txns, $4,376
  - 204 Maxine Pemble: 1 txn, $1,661
  
- 📋 New Accounts to Create in Xero (6 accounts, 95 txns, $63,089):
  1. **Income - Robert Cleary** (Revenue, GST on Income) - 62 txns, $17,670
  2. **Income - Dan Smith** (Revenue, GST on Income) - 47 txns, $13,360
  3. **Income - Sky Point Roofing** (Revenue, GST on Income) - 10 txns, $9,799
  4. **Income - Car Loan** (Revenue, GST on Income) - 5 txns, $10,100
  5. **Income - Car Payment** (Revenue, GST on Income) - 10 txns, $2,080
  6. **Income - Morgan Williams** (Revenue, GST on Income) - 13 txns, $8,400
  
- 🔄 Special Handling:
  - Transfers to LOLD: 34 txns (marked, no code - manual matching)
  - Conversions: 9 txns (uncoded - Jason to advise)
  - Morgan Schoermer transfers: 32 txns (uncoded - Morgan to handle)

---

### 3. Money OUT Merchant Coding Rules Defined

**Files Created:**
- `merchant-coding-rules.json` - Merchant-to-account mapping
- `travel-categorization.json` - All travel expenses categorized

**Key Rules Established:**

| Merchant Pattern | Account | Tax Type | Notes |
|-----------------|---------|----------|-------|
| Sper QLD Treasury | TBD_FINES | BAS Excluded | Fines - not deductible |
| Rakutenpay Tokyo | 429 General Expenses | GST Free Imports | Japan purchases |
| Uber Eats | 421 (≤$35) / 880 (>$35) | Split | Meals vs Drawings |
| Apple.com/bill | 429 General Expenses | GST on Expenses | Subscriptions |
| Ikea | TBD_OFFICE_FURNITURE | GST on Expenses | Office furniture |
| Bunnings | TBD_OFFICE_EQUIPMENT | GST on Expenses | Office supplies |
| Clo3d | TBD_SOFTWARE | GST on Expenses | Design software |
| Post Office | TBD_POSTAGE | GST on Expenses | Shipping |
| Coles/Woolworths | 880 Owner Drawings | BAS Excluded | Groceries - personal |
| Uber Trips | 493 Travel - Local | GST on Expenses | Business rides |

**Travel Categorized:**
- International: 1 txn, $1,531 → 494 Travel - International
- Domestic flights: 5 txns, $1,122 → 492 Travel - National
- Domestic hotels: 2 txns, $789 → 492 Travel - National
- Car rentals: 4 txns, $1,744 → 492 Travel - National
- Refunds: 3 txns, +$409 → 265 Refunds
- **Net travel spend:** -$4,776

---

### 4. Xero Import Preparation

**Xero CSV Format Research:**
- Standard format: `*Date`, `*Amount`, `*Payee`, `*Description`, `*Reference`, `AccountCode`, `TaxType`, `Notes`
- Date format: DD/MM/YYYY
- Asterisk (*) = required field

**Current Status:**
- Money IN CSV generated with placeholder codes (NEW_IRC, NEW_IDS, etc.)
- Once new accounts created in Xero, need to:
  1. Get actual account codes (e.g., 207, 208, 209...)
  2. Update CSV replacing placeholders
  3. Generate Money OUT CSV
  4. Merge both files
  5. Validate totals = control totals
  6. Import to Xero Wise AUD account

---

## 🚧 TODO (Next Session)

### Immediate Priority: New Xero Accounts

**Morgan to create in Xero:**
1. Income - Robert Cleary (Revenue, GST on Income)
2. Income - Dan Smith (Revenue, GST on Income)
3. Income - Sky Point Roofing (Revenue, GST on Income)
4. Income - Car Loan (Revenue, GST on Income)
5. Income - Car Payment (Revenue, GST on Income)
6. Income - Morgan Williams (Revenue, GST on Income)
7. Fines (Expense, BAS Excluded)
8. Office Furniture (Fixed Asset or Expense - confirm with Jason)
9. Office Equipment/Supplies (Expense, GST on Expenses)
10. Software/Subscriptions (if not using 429 General)
11. Postage & Shipping (Expense, GST on Expenses)

**Then provide Choncho with account codes.**

---

### Phase 2: Process Money OUT (1,634 transactions)

**Apply merchant coding rules to:**
- Card transactions (1,204 txns, -$76,514)
- Transfers out (278 txns, -$82,799)
- Conversions (148 txns, -$38,580) - leave uncoded for Jason

**Major categories to process:**
- Groceries (Coles, Woolworths) → 880 Owner Drawings
- Utilities/bills → Various expense accounts
- Software/subscriptions → TBD account
- Hardware stores → TBD Office Equipment
- Meals/restaurants → 421 Meals / 880 Drawings (split by $35)
- Uber trips → 493 Travel - Local
- Personal transfers → 880 Owner Drawings

**Generate:** `processed/wise-aud-xero-import-DEBITS.csv`

---

### Phase 3: Merge & Validate

1. **Merge Credits + Debits** → `processed/wise-aud-xero-import-FINAL-v1.csv`
2. **Validate totals:**
   - Transaction count = 2,070 ✓
   - Credits sum = $198,003.59 ✓
   - Debits sum = -$197,962.09 ✓
   - Net = $41.50 ✓
3. **Manual review of uncoded/flagged transactions**
4. **Generate v2, v3... as needed**
5. **Final validation before import**

---

### Phase 4: Xero Import

1. **Backup current Wise account** (if any data exists)
2. **Import CSV to Wise AUD account**
3. **Verify import success:**
   - Check transaction count
   - Spot-check account codes
   - Verify running balance matches
4. **Handle special cases:**
   - Company transfers (mark as transfer to LOLD manually)
   - Conversions (Jason's advice)
   - Morgan Schoermer transfers (Morgan's decision)

---

## 📂 FILES CREATED

```
projects/wise-multicurrency/
├── README.md
├── ChartOfAccounts.csv (from Morgan)
├── PROGRESS-STATUS.md (this file)
├── categorization-rules.json
├── merchant-coding-rules.json
├── travel-categorization.json
├── raw/
│   └── statement_16108725_AUD_2017-04-28_2026-02-26.csv (2070 txns)
├── processed/
│   ├── control-totals.json (validation baseline)
│   └── wise-aud-xero-import-CREDITS.csv (436 txns, needs account codes)
└── analysis/ (empty, for reports)
```

---

## 🎯 SUCCESS CRITERIA

Before importing to Xero:
- ✅ All 2,070 transactions categorized (coded or marked for special handling)
- ✅ Control totals match exactly
- ✅ New accounts created in Xero with codes updated in CSV
- ✅ Manual review of ambiguous/high-value transactions complete
- ✅ Company transfers flagged for manual matching
- ✅ Conversions left uncoded with notes for Jason
- ✅ CSV format validated (Xero will accept it)

---

## 💡 LESSONS LEARNED

1. **Control totals first** - Established baseline before any processing
2. **Version everything** - Each change = new CSV version, track progress
3. **Don't import until complete** - All txns categorized, totals validated
4. **Cross-reference original** - Always compare back to source data
5. **Document decisions** - Save merchant rules, payer mappings for future use
6. **Handle special cases separately** - Company transfers, conversions, personal = manual

---

## ⏰ TIME TRACKING

- **Session 1:** Feb 25, 11:00 PM - Feb 26, 1:30 AM (2.5 hours)
  - Framework setup
  - Money IN categorization complete
  - Merchant rules defined
  - Travel expenses categorized
  
- **Estimated remaining:** 2-3 hours
  - Process Money OUT: 1.5 hours
  - Validate & merge: 0.5 hours
  - Final review: 0.5 hours
  - Xero import & verification: 0.5 hours

---

**Next session start here:** Phase 2 - Process Money OUT (1,634 transactions)

**Resume command:** "Continue Wise AUD processing - Money OUT phase"
