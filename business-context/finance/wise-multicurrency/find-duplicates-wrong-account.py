#!/usr/bin/env python3
"""Find duplicate transactions in WRONG Wise account (Full Import)"""
import sys
import csv
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# WRONG account (where old imports went)
wise_wrong_id = "01aab634-157c-4992-8c11-2f14724d7191"

print("Fetching Wise - Full Import transactions (WRONG ACCOUNT)...\n")

# Get all pages
all_txns = []
for page_num in range(1, 50):
    page = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_wrong_id}")&page={page_num}')
    txns = page.get('BankTransactions', [])
    if not txns:
        break
    all_txns.extend(txns)
    print(f"Page {page_num}: {len(txns)} transactions (total: {len(all_txns)})")

print(f"\nTotal transactions in Wise - Full Import: {len(all_txns)}")

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
csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-duplicates-wrong-account-review.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'DuplicateGroup', 'TransactionID', 'Date', 'Contact', 'Amount', 
        'Status', 'IsReconciled', 'Reference', 'Action'
    ])
    writer.writeheader()
    
    for group_key, txns in sorted(duplicates.items()):
        for i, txn in enumerate(txns):
            writer.writerow({
                'DuplicateGroup': group_key,
                'TransactionID': txn.get('BankTransactionID', ''),
                'Date': txn.get('Date', '')[:10],
                'Contact': txn.get('Contact', {}).get('Name', ''),
                'Amount': txn.get('Total', 0),
                'Status': txn.get('Status', ''),
                'IsReconciled': txn.get('IsReconciled', False),
                'Reference': txn.get('Reference', ''),
                'Action': 'KEEP' if i == 0 else 'DELETE'  # Suggest keeping first, delete rest
            })

print(f"\n✅ Exported to: {csv_file}")
print(f"Total rows: {sum(len(v) for v in duplicates.values())}")
print("\nNext: Upload to Google Sheets for Morgan to review")
