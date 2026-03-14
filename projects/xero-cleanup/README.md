# Xero Tax Rate Cleanup

Systematic audit and fix workflow for incorrect tax rates on Xero transactions.

## Overview

This workflow:
1. **Audits** all transactions against expected tax rates for each account
2. **Reports** mismatches for review
3. **Fixes** unreconciled transactions (safely skips reconciled ones)

## Setup

### 1. Customize Tax Rules

Edit `audit-tax-rates.py` and update the `TAX_RULES` dictionary with your chart of accounts:

```python
TAX_RULES = {
    '200': 'OUTPUT',           # Sales (GST on Income)
    '255': 'EXEMPTOUTPUT',     # Rent Received (GST Free)
    '400': 'INPUT',            # Advertising (GST on Expenses)
    '404': 'BASEXCLUDED',      # Bank Fees (often GST-free)
    # Add all your accounts...
}
```

**Tax types:**
- `OUTPUT` = GST on Income (10%)
- `EXEMPTOUTPUT` = GST Free Income
- `INPUT` = GST on Expenses (claimable)
- `EXEMPTEXPENSES` = GST Free Expenses
- `BASEXCLUDED` = BAS Excluded (non-GST items like depreciation)
- `NONE` = No GST

### 2. Reference Your Chart of Accounts

Check `/Users/userclaw/.openclaw/workspace/chart-of-accounts.pdf` or:

```bash
cd /Users/userclaw/.openclaw/workspace/projects/xero-cleanup
python3 -c "
import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
accounts = api_get('Accounts')
for acc in accounts['Accounts']:
    print(f\"{acc['Code']}: {acc['Name']} (Type: {acc['Type']})\")
" > chart-of-accounts.txt
```

## Usage

### Step 1: Run Audit

```bash
cd /Users/userclaw/.openclaw/workspace/projects/xero-cleanup
chmod +x audit-tax-rates.py
./audit-tax-rates.py
```

This will:
- Scan all bank transactions
- Compare actual vs expected tax rates
- Generate `tax-audit-report.json` with all mismatches
- Show summary grouped by account

### Step 2: Review Report

Check the output - it shows:
- Total mismatches found
- Breakdown by account code
- Examples of each mismatch type
- Which ones are reconciled (unfixable via API)

### Step 3: Fix (Tier 2 - Requires Approval)

**⚠️ This modifies Xero data - review audit first!**

```bash
./fix-tax-rates.py
```

Prompts for `YES` confirmation, then:
- Updates unreconciled transactions
- Skips reconciled ones (can't be changed via API)
- Shows progress every 10 transactions
- Rate-limited to avoid API throttling

### Step 4: Verify

Re-run audit to confirm fixes:

```bash
./audit-tax-rates.py
```

Should show "All checked transactions have correct tax rates!"

## Safety Features

- ✅ Only touches **unreconciled** transactions
- ✅ Skips bank-statement reconciled items (can't be changed)
- ✅ Requires explicit `YES` confirmation before fixing
- ✅ Generates audit report before any changes
- ✅ Rate-limited API calls (0.3s delay between updates)
- ✅ Shows progress + errors during fix process

## Common Tax Rules Patterns

**Income accounts:**
- Taxable sales → `OUTPUT`
- Residential rent → `EXEMPTOUTPUT`
- Interest (if taxable) → `OUTPUT`

**Expense accounts:**
- Most business expenses → `INPUT`
- Bank fees → Often `BASEXCLUDED` (check with accountant)
- Depreciation → `BASEXCLUDED`
- Entertainment (non-deductible) → `BASEXCLUDED`

**When unsure:** Check with your accountant or existing correct transactions in that account.

## Troubleshooting

**"No such file or directory" for xero_api:**
- Ensure `/Users/userclaw/.openclaw/workspace/agents/accountant/xero_api.py` exists
- Check Xero auth tokens are valid

**"Reconciled transactions can't be updated":**
- These must be manually fixed in Xero UI
- Unreconcile → fix tax → re-reconcile

**"Rate limit exceeded":**
- Increase `time.sleep()` delay in fix script
- Run in smaller batches

## Files

- `audit-tax-rates.py` - Scan transactions, generate report
- `fix-tax-rates.py` - Apply fixes to unreconciled transactions
- `tax-audit-report.json` - Generated audit results
- `README.md` - This file

## Next Steps

After fixing:
1. Re-run audit to verify
2. Check BAS calculations in Xero
3. Consider adding more account codes to TAX_RULES for comprehensive coverage
4. Set up periodic audits (monthly?) to catch new incorrect entries

---

**Tier 2 Operation:** Write operations on Xero require explicit approval per TOOLS.md rules. Always review audit report before running fix script.
