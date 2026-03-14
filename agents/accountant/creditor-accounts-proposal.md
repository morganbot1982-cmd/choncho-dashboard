# Creditor Accounts - Chart of Accounts Proposal
**Date:** 2026-02-23  
**Total Creditors:** 19  
**Total Amount:** $100,957.77

## Available Code Ranges

**Current chart shows:**
- Current Liabilities: 800-877, 880-881
- Non-Current Liabilities: 900+ (currently only 900 Loan - Morgan exists)

**Available codes:** 882-899 (18 codes in Current Liabilities) OR 901+ (unlimited in Non-Current Liabilities)

**Recommendation:** Use **901-920 range** (Non-Current Liabilities) to keep these separate from operational current liabilities and group them with the existing "900 Loan - Morgan" account.

---

## Proposed Creditor Accounts (sorted by amount)

| Code | Account Name | Account Type | Tax Rate | Txns | Amount | Category |
|------|-------------|--------------|----------|------|---------|----------|
| **901** | Creditor - Sean Maxwell Ferguson | NonCurrentLiabilities | BAS Excluded | 29 | $25,928.00 | PA Work |
| **902** | Creditor - Jodie Ehmer / James Cleary | NonCurrentLiabilities | BAS Excluded | 61 | $17,370.00 | Rent/Bills |
| **903** | Creditor - Daniel Thomas Smith | NonCurrentLiabilities | BAS Excluded | 47 | $13,360.00 | Flatmate Rent |
| **904** | Creditor - Erwin MacDowell | NonCurrentLiabilities | BAS Excluded | 5 | $10,100.00 | Car Sale |
| **905** | Creditor - Sky Point Roofing | NonCurrentLiabilities | BAS Excluded | 10 | $9,799.00 | Labouring Income |
| **906** | Creditor - Maxine Pemble | NonCurrentLiabilities | BAS Excluded | 2 | $5,414.00 | Loan Repayment |
| **907** | Creditor - Craig Wah Day | NonCurrentLiabilities | BAS Excluded | 5 | $2,724.20 | Personal |
| **908** | Creditor - Gary Lee Triggs | NonCurrentLiabilities | BAS Excluded | 10 | $2,080.00 | Car Sale |
| **909** | Creditor - Jamaal Max Stevens | NonCurrentLiabilities | BAS Excluded | 2 | $2,000.00 | Labouring Income |
| **910** | Creditor - Cory Gene Eaton | NonCurrentLiabilities | BAS Excluded | 3 | $1,500.00 | Personal |
| **911** | Creditor - Matilda Rose Cotton | NonCurrentLiabilities | BAS Excluded | 2 | $1,500.00 | Personal |
| **912** | Creditor - Uzziah Leslie Woods | NonCurrentLiabilities | BAS Excluded | 2 | $1,050.00 | Personal |
| **913** | Creditor - Jonathan Ritzmann | NonCurrentLiabilities | BAS Excluded | 1 | $1,048.82 | Personal |
| **914** | Creditor - Corey Reed Schoermer | NonCurrentLiabilities | BAS Excluded | 1 | $1,000.00 | Family |
| **915** | Creditor - Ewan Jomain | NonCurrentLiabilities | BAS Excluded | 3 | $680.00 | Personal |
| **916** | Creditor - Alexandra Dominic | NonCurrentLiabilities | BAS Excluded | 1 | $350.00 | Personal |
| **917** | Creditor - Joseph Matthew Power | NonCurrentLiabilities | BAS Excluded | 2 | $350.00 | Personal |
| **918** | Creditor - Other/Miscellaneous | NonCurrentLiabilities | BAS Excluded | 3 | $4,403.75 | Needs Review |

**Note:** "J Cleary" (1 txn, $300) appears to be same person as James Cleary — merged into account 902.

**Total:** 18 creditor accounts proposed (codes 901-918)

---

## Alternative: Current Liabilities Range

If accountant prefers Current Liabilities instead of Non-Current:

Use codes **882-899** (same account names, change AccountType to "CurrentLiabilities")

---

## Next Steps

1. **Confirm with accountant:** Should these be CurrentLiabilities or NonCurrentLiabilities?
2. **Create accounts in Xero** via API or manual entry
3. **Journal entries:** Reclassify 190 transactions from "881 Owner A Funds Introduced" to respective creditor accounts
4. **Review "Other/Miscellaneous" (account 918):** 3 transactions totaling $4,403.75 need individual review before final classification

---

## Implementation Notes

**Account naming convention:**
- "Creditor - [Full Name]" for individuals
- "Creditor - [Company Name]" for entities (Sky Point Roofing)

**Why "Creditor" prefix?**
- Clearly identifies these as amounts owed to third parties
- Distinguishes from "Owner" accounts (880, 881, 900)
- Groups them logically in reports

**Tax treatment:** All BAS Excluded (these are personal income/loan accounts, not business transactions)

---

## Summary by Category

| Category | Accounts | Total Amount | Notes |
|----------|----------|--------------|-------|
| PA Work | 1 | $25,928.00 | Sean Ferguson — clarify if business revenue |
| Rent/Bills | 2 | $30,730.00 | Jodie/James + Dan Smith — taxable? |
| Labouring Income | 2 | $11,799.00 | Sky Point + Jamaal — personal income |
| Car Sale | 2 | $12,180.00 | Erwin + Gary — personal asset sale |
| Loan Repayment | 1 | $5,414.00 | Maxine — not taxable |
| Personal/Family | 9 | $10,903.02 | Various personal transfers |
| Other | 1 | $4,403.75 | Needs review |
| **TOTAL** | **18** | **$100,957.77** | |

---

**Ready to create these accounts?** Let me know if you want me to:
1. Create them via Xero API
2. Generate a CSV import file for Xero
3. Adjust the code range or naming convention
