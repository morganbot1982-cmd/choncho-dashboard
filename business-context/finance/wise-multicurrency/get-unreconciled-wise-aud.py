#!/usr/bin/env python3
"""Get all unreconciled transactions from Wise AUD account"""
import sys
import csv
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# Correct Wise AUD account ID
wise_aud_id = "10142dd5-d7b0-4f95-9ab0-7e5e5a1baa7e"

print("Fetching unreconciled transactions from Wise AUD...\n")

all_txns = []
for page_num in range(1, 50):
    # Get unreconciled transactions only
    response = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_aud_id}")%20AND%20Status=="AUTHORISED"&page={page_num}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    # Filter for unreconciled only
    unreconciled = [t for t in txns if not t.get('IsReconciled', False)]
    all_txns.extend(unreconciled)
    print(f"Page {page_num}: {len(unreconciled)} unreconciled (of {len(txns)} total)")

print(f"\n✅ Total unreconciled: {len(all_txns)}")

# Export to CSV
csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-aud-unreconciled.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'TransactionID', 'Date', 'Type', 'Contact', 'Amount', 'Reference', 
        'Description', 'AccountCode', 'AccountName', 'SuggestedCode'
    ])
    writer.writeheader()
    
    for txn in all_txns:
        # Get line item details
        line_items = txn.get('LineItems', [])
        for item in line_items:
            writer.writerow({
                'TransactionID': txn.get('BankTransactionID', ''),
                'Date': txn.get('Date', '')[:10],
                'Type': txn.get('Type', ''),
                'Contact': txn.get('Contact', {}).get('Name', ''),
                'Amount': txn.get('Total', 0),
                'Reference': txn.get('Reference', ''),
                'Description': item.get('Description', ''),
                'AccountCode': item.get('AccountCode', ''),
                'AccountName': item.get('AccountCode', ''),  # Will fill in later
                'SuggestedCode': ''  # For AI suggestions
            })

print(f"\n📊 Exported to: {csv_file}")
print(f"\nNext: Review transactions and I'll help batch-code them")
