#!/usr/bin/env python3
"""Delete duplicate Wise transactions (backup CSV already created)"""

import json
import os
import urllib.request
import base64
import time
import csv

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'xero_tokens.json')
CREDS_PATH = os.path.join(CONFIG_DIR, 'xero_credentials.json')

def load_creds():
    with open(CREDS_PATH) as f:
        return json.load(f)

def load_tokens():
    with open(TOKEN_PATH) as f:
        return json.load(f)

def save_tokens(tokens):
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tokens, f, indent=2)

def refresh_access_token():
    creds = load_creds()
    tokens = load_tokens()
    auth_header = base64.b64encode(f"{creds['client_id']}:{creds['client_secret']}".encode()).decode()
    data = urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
    }).encode()
    req = urllib.request.Request("https://identity.xero.com/connect/token", data=data, headers={
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded',
    })
    resp = urllib.request.urlopen(req)
    new_tokens = json.loads(resp.read().decode())
    save_tokens(new_tokens)
    return new_tokens

def get_tenant_id():
    tokens = load_tokens()
    req = urllib.request.Request("https://api.xero.com/connections", headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/json',
    })
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            tokens = refresh_access_token()
            req = urllib.request.Request("https://api.xero.com/connections", headers={
                'Authorization': f'Bearer {tokens["access_token"]}',
                'Content-Type': 'application/json',
            })
            resp = urllib.request.urlopen(req)
        else:
            raise
    connections = json.loads(resp.read().decode())
    return connections[0]['tenantId'] if connections else None

def delete_bank_transaction(txn_id, tenant_id):
    """Delete a single bank transaction"""
    tokens = load_tokens()
    
    url = f"https://api.xero.com/api.xro/2.0/BankTransactions/{txn_id}"
    
    req = urllib.request.Request(url, method='DELETE', headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Accept': 'application/json',
    })
    
    try:
        resp = urllib.request.urlopen(req)
        return True, None
    except urllib.error.HTTPError as e:
        if e.code == 401:
            tokens = refresh_access_token()
            req = urllib.request.Request(url, method='DELETE', headers={
                'Authorization': f'Bearer {tokens["access_token"]}',
                'Xero-Tenant-Id': tenant_id,
                'Accept': 'application/json',
            })
            resp = urllib.request.urlopen(req)
            return True, None
        else:
            error_body = e.read().decode() if e.fp else str(e)
            return False, f"HTTP {e.code}: {error_body}"

# Load transaction IDs from backup CSV
csv_path = '/Users/userclaw/.openclaw/workspace/agents/accountant/wise-duplicates-voided-2026-02-23.csv'

print("Loading duplicate transaction IDs from backup CSV...\n")
print(f"Backup: {csv_path}\n")

to_delete = []
with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        to_delete.append(row['BankTransactionID'])

print(f"Found {len(to_delete)} transactions to DELETE\n")
print("⚠️  These will be permanently removed from Xero")
print("✅ Backup CSV contains full record of all deleted transactions\n")

tenant_id = get_tenant_id()
deleted_count = 0
error_count = 0
errors = []

print("Deleting transactions...\n")

for i, txn_id in enumerate(to_delete):
    success, error = delete_bank_transaction(txn_id, tenant_id)
    
    if error:
        error_count += 1
        if error_count <= 10:
            print(f"  ❌ {txn_id[:8]}: {error}")
        errors.append((txn_id, error))
    else:
        deleted_count += 1
    
    if (i + 1) % 50 == 0:
        print(f"  Progress: {i + 1}/{len(to_delete)} ({deleted_count} deleted, {error_count} errors)")
    
    # Rate limiting - be gentle with API
    if (i + 1) % 60 == 0:
        time.sleep(1)

print(f"\n{'='*80}")
print(f"DONE:")
print(f"  ✅ Deleted: {deleted_count} transactions")
print(f"  ❌ Errors: {error_count}")
print(f"  📄 Backup CSV: {csv_path}")
print(f"{'='*80}")
print(f"\nWise - Full Import: 1900 → {1900 - deleted_count} transactions")

if error_count > 0:
    print(f"\nFirst 10 errors:")
    for txn_id, err in errors[:10]:
        print(f"  {txn_id}: {err[:100]}")

