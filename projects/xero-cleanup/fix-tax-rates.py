#!/usr/bin/env python3
"""
Fix incorrect tax rates on unreconciled transactions
Run audit-tax-rates.py first to generate the report
"""
import sys
import json
import time
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
from xero_api_update import api_post

# Import same rules from audit script
from audit_tax_rates import TAX_RULES

print("=" * 80)
print("XERO TAX RATE FIXER")
print("=" * 80)

# Load audit report
report_file = '/Users/userclaw/.openclaw/workspace/projects/xero-cleanup/tax-audit-report.json'
try:
    with open(report_file, 'r') as f:
        report = json.load(f)
except FileNotFoundError:
    print(f"\n❌ Error: Run audit-tax-rates.py first to generate report")
    sys.exit(1)

mismatches = report['mismatches']
fixable = [m for m in mismatches if not m['is_reconciled']]

print(f"\nFound {len(fixable)} unreconciled transactions to fix")
print(f"(Skipping {len(mismatches) - len(fixable)} reconciled transactions)")

if not fixable:
    print(f"\n✅ Nothing to fix!")
    sys.exit(0)

# Confirm before proceeding
print(f"\n⚠️  This will update {len(fixable)} transactions in Xero")
response = input(f"Type 'YES' to proceed: ")
if response != 'YES':
    print("Aborted.")
    sys.exit(0)

# Process fixes
success = 0
failed = 0
skipped = 0

for i, mismatch in enumerate(fixable, 1):
    txn_id = mismatch['txn_id']
    date = mismatch['date']
    amount = mismatch['amount']
    contact = mismatch['contact']
    account_code = mismatch['account_code']
    expected_tax = mismatch['expected_tax']
    actual_tax = mismatch['actual_tax']
    
    try:
        # Fetch current transaction
        response = api_get(f'BankTransactions/{txn_id}')
        txn = response.get('BankTransactions', [{}])[0]
        
        if not txn:
            print(f"❌ Transaction {txn_id} not found")
            failed += 1
            continue
        
        # Double-check it's still unreconciled
        if txn.get('IsReconciled', False):
            print(f"⏭️  Skipped (now reconciled): {date} | ${amount} | {contact}")
            skipped += 1
            continue
        
        # Update tax type on matching line items
        updated = False
        for line in txn.get('LineItems', []):
            if line.get('AccountCode') == account_code and line.get('TaxType') == actual_tax:
                line['TaxType'] = expected_tax
                updated = True
        
        if not updated:
            print(f"⏭️  Skipped (no matching line): {date} | ${amount}")
            skipped += 1
            continue
        
        # Send update
        api_post('BankTransactions', {'BankTransactions': [txn]})
        success += 1
        
        if i % 10 == 0:
            print(f"Progress: {i}/{len(fixable)} ({success} success, {failed} failed, {skipped} skipped)")
        
        time.sleep(0.3)  # Rate limiting
        
    except Exception as e:
        failed += 1
        error_msg = str(e)[:100]
        print(f"❌ Error on {date} ${amount}: {error_msg}")

print(f"\n" + "=" * 80)
print(f"✅ COMPLETE!")
print(f"   Success: {success}")
print(f"   Failed: {failed}")
print(f"   Skipped: {skipped}")
print(f"\n🎯 Tax rates corrected on {success} transactions")
print(f"\nRe-run audit-tax-rates.py to verify fixes")
