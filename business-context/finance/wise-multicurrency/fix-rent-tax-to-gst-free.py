#!/usr/bin/env python3
"""Change OUTPUT tax to EXEMPTOUTPUT on Rent Received transactions"""
import sys
import time
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
from xero_api_update import api_post

print("Finding Rent Received transactions with OUTPUT tax...\n")

# Get all Rent Received with OUTPUT tax
targets = []
for page in range(1, 50):
    response = api_get(f'BankTransactions?page={page}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    for txn in txns:
        for line_item in txn.get('LineItems', []):
            if line_item.get('AccountCode') == '255' and line_item.get('TaxType') == 'OUTPUT':
                targets.append(txn)
                break

print(f"Found {len(targets)} Rent Received transactions with OUTPUT (GST)\n")

# Update them
success = 0
failed = 0
skipped_reconciled = 0

for i, txn in enumerate(targets, 1):
    txn_id = txn.get('BankTransactionID')
    is_reconciled = txn.get('IsReconciled', False)
    date = txn.get('Date', '')[:10]
    amount = txn.get('Total', 0)
    contact = txn.get('Contact', {}).get('Name', '')
    
    # Skip bank-statement reconciled ones
    if is_reconciled:
        skipped_reconciled += 1
        print(f"⏭️  Skipped (reconciled): {date} | ${amount} | {contact}")
        continue
    
    try:
        # Update line items to EXEMPTOUTPUT
        for line in txn.get('LineItems', []):
            if line.get('AccountCode') == '255':
                line['TaxType'] = 'EXEMPTOUTPUT'
        
        # Send update
        api_post('BankTransactions', {'BankTransactions': [txn]})
        success += 1
        
        if i % 5 == 0:
            print(f"Progress: {i}/{len(targets)} ({success} success, {failed} failed, {skipped_reconciled} skipped)")
        
        time.sleep(0.3)  # Rate limiting
        
    except Exception as e:
        failed += 1
        error_msg = str(e)[:100]
        print(f"❌ Error on {date} ${amount}: {error_msg}")

print(f"\n✅ Complete!")
print(f"   Success: {success}")
print(f"   Failed: {failed}")
print(f"   Skipped (reconciled): {skipped_reconciled}")
print(f"\n🎯 Rent Received transactions changed: OUTPUT → EXEMPTOUTPUT (GST Free)")
