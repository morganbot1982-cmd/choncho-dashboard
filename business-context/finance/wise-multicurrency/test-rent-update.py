#!/usr/bin/env python3
"""Test updating ONE rent transaction to see full error"""
import sys
import json
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
from xero_api_update import api_post

# Get the first unreconciled rent with OUTPUT tax
print("Finding one unreconciled Rent Received with OUTPUT tax...\n")

target_txn = None
for page in range(1, 50):
    response = api_get(f'BankTransactions?page={page}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    for txn in txns:
        if txn.get('IsReconciled', False):
            continue
        for line_item in txn.get('LineItems', []):
            if line_item.get('AccountCode') == '255' and line_item.get('TaxType') == 'OUTPUT':
                target_txn = txn
                break
        if target_txn:
            break
    if target_txn:
        break

if not target_txn:
    print("No unreconciled Rent with OUTPUT tax found")
    sys.exit(1)

print(f"Testing transaction:")
print(f"  ID: {target_txn.get('BankTransactionID')}")
print(f"  Date: {target_txn.get('Date')}")
print(f"  Amount: ${target_txn.get('Total')}")
print(f"  Contact: {target_txn.get('Contact', {}).get('Name')}")
print(f"  IsReconciled: {target_txn.get('IsReconciled')}")
print(f"  Status: {target_txn.get('Status')}")
print(f"  Type: {target_txn.get('Type')}")
print()

# Show current line item
for line in target_txn.get('LineItems', []):
    if line.get('AccountCode') == '255':
        print(f"Current line item:")
        print(f"  Account: {line.get('AccountCode')}")
        print(f"  TaxType: {line.get('TaxType')}")
        print(f"  TaxAmount: {line.get('TaxAmount')}")
        print()

# Try updating
try:
    # Modify the tax type
    for line in target_txn.get('LineItems', []):
        if line.get('AccountCode') == '255':
            line['TaxType'] = 'EXEMPTOUTPUT'
    
    print("Attempting to update tax type to EXEMPTOUTPUT...")
    result = api_post('BankTransactions', {'BankTransactions': [target_txn]})
    print("✅ Success!")
    print(json.dumps(result, indent=2)[:500])
    
except Exception as e:
    print(f"❌ Full error:")
    print(str(e))
