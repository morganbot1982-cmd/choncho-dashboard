#!/usr/bin/env python3
"""Find duplicate transactions in correct Wise AUD account"""
import sys
import csv
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# CORRECT Wise AUD account from yesterday's discovery
wise_aud_id = "10142dd5-d7b0-4f95-9ab0-7e5e5a1baa7e"

print("Fetching Wise AUD transactions...\n")

# Get all pages
all_txns = []
for page_num in range(1, 50):
    page = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_aud_id}")&page={page_num}')
    txns = page.get('BankTransactions', [])
    if not txns:
        break
    all_txns.extend(txns)
    print(f"Page {page_num}: {len(txns)} transactions (total: {len(all_txns)})")

print(f"\nTotal transactions in Wise AUD: {len(all_txns)}")

# Find potential duplicates (same date + same amount)
from collections import defaultdict
by_date_amount = defaultdict(list)

for txn in all_txns:
    date = txn.get('Date', '?')[:10]
    total = txn.get('Total', 0)
    key = f"{date}_{total}"
    by_date_amount[key].append(txn)

duplicates = {k: v for k, v in by_date_amount.items() if len(v) > 1}

print(f"\nPotential duplicates (same date + amount): {len(duplicates)} groups")
print(f"Total duplicate transactions: {sum(len(v) for v in duplicates.values())}\n")

# Export to CSV for Google Sheets review
csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-aud-duplicates-review.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'DuplicateGroup', 'TransactionID', 'Date', 'Contact', 'Amount', 
        'Status', 'IsReconciled', 'Reference', 'DELETE'
    ])
    writer.writeheader()
    
    for group_key, txns in duplicates.items():
        for txn in txns:
            writer.writerow({
                'DuplicateGroup': group_key,
                'TransactionID': txn.get('BankTransactionID', ''),
                'Date': txn.get('Date', '')[:10],
                'Contact': txn.get('Contact', {}).get('Name', ''),
                'Amount': txn.get('Total', 0),
                'Status': txn.get('Status', ''),
                'IsReconciled': txn.get('IsReconciled', False),
                'Reference': txn.get('Reference', ''),
                'DELETE': ''  # Morgan fills this in
            })

print(f"\n✅ Exported to: {csv_file}")
print(f"Total rows: {sum(len(v) for v in duplicates.values())}")
print("\nNext: Upload to Google Sheets for Morgan to review")
