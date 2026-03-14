#!/usr/bin/env python3
"""Export and void duplicate Wise transactions"""

import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
import json
import os
import urllib.request
import base64
import csv
from collections import defaultdict

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'xero_tokens.json')

def load_tokens():
    with open(TOKEN_PATH) as f:
        return json.load(f)

def get_tenant_id():
    tokens = load_tokens()
    req = urllib.request.Request("https://api.xero.com/connections", headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/json',
    })
    resp = urllib.request.urlopen(req)
    connections = json.loads(resp.read().decode())
    return connections[0]['tenantId'] if connections else None

def api_post(endpoint, data_dict, tenant_id):
    tokens = load_tokens()
    url = f"https://api.xero.com/api.xro/2.0/{endpoint}"
    data = json.dumps(data_dict).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())

wise_import_id = "01aab634-157c-4992-8c11-2f14724d7191"

print("Step 1: Fetching all Wise - Full Import transactions...\n")

total_txns = []
for page_num in range(1, 20):
    page = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_import_id}")&page={page_num}')
    txns = page.get('BankTransactions', [])
    if not txns:
        break
    total_txns.extend(txns)
    print(f"  Page {page_num}: {len(txns)} transactions (total: {len(total_txns)})")

print(f"\nTotal transactions: {len(total_txns)}")

print("\nStep 2: Identifying duplicates (same date + amount)...\n")

by_date_amount = defaultdict(list)

for txn in total_txns:
    date = txn.get('Date', '?')[:10]
    total = txn.get('Total', 0)
    key = f"{date}_{total}"
    by_date_amount[key].append(txn)

duplicates = {k: v for k, v in by_date_amount.items() if len(v) > 1}

print(f"Duplicate groups: {len(duplicates)}")
print(f"Total duplicate transactions: {sum(len(v) for v in duplicates.values())}")

# For each duplicate group, keep the first, void the rest
to_void = []
for key, txns in duplicates.items():
    # Sort by BankTransactionID to have consistent "first"
    sorted_txns = sorted(txns, key=lambda x: x.get('BankTransactionID', ''))
    keep = sorted_txns[0]
    void_these = sorted_txns[1:]
    to_void.extend(void_these)

print(f"Transactions to void: {len(to_void)}")

print("\nStep 3: Exporting to CSV...\n")

csv_path = '/Users/userclaw/.openclaw/workspace/agents/accountant/wise-duplicates-voided-2026-02-23.csv'

with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'BankTransactionID', 'Date', 'Amount', 'Description', 'ContactName', 
        'Status', 'DuplicateGroup', 'AccountCode', 'AccountName'
    ])
    writer.writeheader()
    
    for txn in to_void:
        date = txn.get('Date', '?')[:10]
        total = txn.get('Total', 0)
        dup_key = f"{date}_{total}"
        
        writer.writerow({
            'BankTransactionID': txn.get('BankTransactionID', ''),
            'Date': date,
            'Amount': total,
            'Description': txn.get('Reference', ''),
            'ContactName': txn.get('Contact', {}).get('Name', ''),
            'Status': txn.get('Status', ''),
            'DuplicateGroup': dup_key,
            'AccountCode': txn.get('LineItems', [{}])[0].get('AccountCode', '') if txn.get('LineItems') else '',
            'AccountName': txn.get('LineItems', [{}])[0].get('Description', '') if txn.get('LineItems') else ''
        })

print(f"✅ Exported {len(to_void)} transactions to:")
print(f"   {csv_path}")

print("\nStep 4: Voiding transactions in Xero...\n")

tenant_id = get_tenant_id()
voided_count = 0
error_count = 0

for i, txn in enumerate(to_void):
    txn_id = txn.get('BankTransactionID')
    
    # Update transaction status to VOIDED
    try:
        void_data = {
            "BankTransactionID": txn_id,
            "Status": "VOIDED"
        }
        response = api_post('BankTransactions', void_data, tenant_id)
        voided_count += 1
        if (i + 1) % 50 == 0:
            print(f"  Voided {i + 1}/{len(to_void)}...")
    except Exception as e:
        error_count += 1
        if error_count <= 5:
            print(f"  ❌ Error voiding {txn_id[:8]}: {str(e)}")

print(f"\n{'='*80}")
print(f"DONE:")
print(f"  ✅ Voided: {voided_count} transactions")
print(f"  ❌ Errors: {error_count}")
print(f"  📄 Backup CSV: {csv_path}")
print(f"{'='*80}")
print(f"\nWise - Full Import: {len(total_txns)} → {len(total_txns) - voided_count} active transactions")

