#!/usr/bin/env python3
"""Get FRESH duplicate list and delete them"""

import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
import json
import os
import urllib.request
import base64
import time
import csv
from collections import defaultdict

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'xero_tokens.json')
CREDS_PATH = os.path.join(CONFIG_DIR, 'xero_credentials.json')

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

def delete_bank_transaction(txn_id, tenant_id):
    tokens = load_tokens()
    url = f"https://api.xero.com/api.xro/2.0/BankTransactions/{txn_id}"
    req = urllib.request.Request(url, method='DELETE', headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
    })
    try:
        urllib.request.urlopen(req)
        return True, None
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"

wise_import_id = "01aab634-157c-4992-8c11-2f14724d7191"

print("Step 1: Fetching CURRENT Wise transactions...\n")

total_txns = []
for page_num in range(1, 20):
    page = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_import_id}")&page={page_num}')
    txns = page.get('BankTransactions', [])
    if not txns:
        break
    total_txns.extend(txns)

print(f"Current total: {len(total_txns)} transactions\n")

print("Step 2: Finding duplicates (same date + amount)...\n")

by_date_amount = defaultdict(list)
for txn in total_txns:
    date = txn.get('Date', '?')[:10]
    total = txn.get('Total', 0)
    key = f"{date}_{total}"
    by_date_amount[key].append(txn)

duplicates = {k: v for k, v in by_date_amount.items() if len(v) > 1}

# Keep first, delete rest
to_delete = []
for key, txns in duplicates.items():
    sorted_txns = sorted(txns, key=lambda x: x.get('BankTransactionID', ''))
    to_delete.extend(sorted_txns[1:])  # All except first

print(f"Duplicate groups: {len(duplicates)}")
print(f"Transactions to delete: {len(to_delete)}\n")

# Export fresh CSV
csv_path = '/Users/userclaw/.openclaw/workspace/agents/accountant/wise-duplicates-deleted-2026-02-23-fresh.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['BankTransactionID', 'Date', 'Amount', 'Description', 'ContactName'])
    writer.writeheader()
    for txn in to_delete:
        writer.writerow({
            'BankTransactionID': txn.get('BankTransactionID', ''),
            'Date': txn.get('Date', '?')[:10],
            'Amount': txn.get('Total', 0),
            'Description': txn.get('Reference', ''),
            'ContactName': txn.get('Contact', {}).get('Name', '')
        })

print(f"✅ Exported to: {csv_path}\n")

print("Step 3: Deleting duplicates...\n")

tenant_id = get_tenant_id()
deleted = 0
errors = 0

for i, txn in enumerate(to_delete):
    txn_id = txn.get('BankTransactionID')
    success, error = delete_bank_transaction(txn_id, tenant_id)
    
    if success:
        deleted += 1
    else:
        errors += 1
        if errors <= 5:
            print(f"  ❌ {txn_id[:8]}: {error}")
    
    if (i + 1) % 50 == 0:
        print(f"  Progress: {i + 1}/{len(to_delete)} ({deleted} deleted, {errors} errors)")
    
    if (i + 1) % 60 == 0:
        time.sleep(1)

print(f"\n{'='*80}")
print(f"✅ Deleted: {deleted}")
print(f"❌ Errors: {errors}")
print(f"📄 Backup: {csv_path}")
print(f"Wise - Full Import: {len(total_txns)} → {len(total_txns) - deleted}")
print(f"{'='*80}")

