#!/usr/bin/env python3
"""Check status of ALL Wise AUD transactions"""
import sys
from collections import Counter
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# Correct Wise AUD account ID
wise_aud_id = "10142dd5-d7b0-4f95-9ab0-7e5e5a1baa7e"

print("Fetching ALL transactions from Wise AUD...\n")

all_txns = []
for page_num in range(1, 50):
    response = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_aud_id}")&page={page_num}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    all_txns.extend(txns)
    print(f"Page {page_num}: {len(txns)} transactions")

print(f"\n✅ Total transactions: {len(all_txns)}\n")

# Count by status
statuses = Counter(t.get('Status') for t in all_txns)
print("By Status:")
for status, count in statuses.items():
    print(f"  {status}: {count}")

# Count by reconciled
reconciled_count = sum(1 for t in all_txns if t.get('IsReconciled', False))
unreconciled_count = len(all_txns) - reconciled_count
print(f"\nBy Reconciliation:")
print(f"  Reconciled: {reconciled_count}")
print(f"  Unreconciled: {unreconciled_count}")

# Show a sample unreconciled
if unreconciled_count > 0:
    print(f"\nSample unreconciled transaction:")
    for txn in all_txns:
        if not txn.get('IsReconciled', False):
            print(f"  Date: {txn.get('Date','')[:10]}")
            print(f"  Contact: {txn.get('Contact',{}).get('Name','')}")
            print(f"  Amount: ${txn.get('Total', 0)}")
            print(f"  Reference: {txn.get('Reference', '')}")
            print(f"  Status: {txn.get('Status', '')}")
            print(f"  IsReconciled: {txn.get('IsReconciled', False)}")
            break
