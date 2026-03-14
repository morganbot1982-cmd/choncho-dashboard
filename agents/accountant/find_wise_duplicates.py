#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

wise_import_id = "01aab634-157c-4992-8c11-2f14724d7191"

print("Fetching Wise - Full Import transactions...\n")

# Get first page to see total
page1 = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_import_id}")&page=1')
total_txns = page1.get('BankTransactions', [])
print(f"Page 1: {len(total_txns)} transactions")

# Get more pages if needed
for page_num in range(2, 20):
    page = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_import_id}")&page={page_num}')
    txns = page.get('BankTransactions', [])
    if not txns:
        break
    total_txns.extend(txns)
    print(f"Page {page_num}: {len(txns)} transactions (total: {len(total_txns)})")

print(f"\nTotal transactions in Wise - Full Import: {len(total_txns)}")

# Look for potential duplicates (same date + same amount)
from collections import defaultdict
by_date_amount = defaultdict(list)

for txn in total_txns:
    date = txn.get('Date', '?')[:10]
    total = txn.get('Total', 0)
    status = txn.get('Status', '?')
    key = f"{date}_{total}"
    by_date_amount[key].append(txn)

duplicates = {k: v for k, v in by_date_amount.items() if len(v) > 1}

print(f"\nPotential duplicates (same date + amount): {len(duplicates)} groups")
print(f"Total duplicate transactions: {sum(len(v) for v in duplicates.values())}\n")

# Show sample
print("Sample duplicates (first 10 groups):\n")
for i, (key, txns) in enumerate(list(duplicates.items())[:10]):
    print(f"{i+1}. {key} ({len(txns)} transactions)")
    for txn in txns[:3]:
        print(f"   {txn.get('Date','?')[:10]} {txn.get('Contact',{}).get('Name','?'):<30} ${txn.get('Total',0):>10.2f} {txn.get('Status','?')} {txn.get('BankTransactionID','?')[:8]}")

print(f"\n... {len(duplicates)} duplicate groups total")
