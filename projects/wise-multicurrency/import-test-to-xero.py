#!/usr/bin/env python3
"""Import TEST batch of Wise transactions to Xero"""

import csv
import json
import os
import sys
import urllib.request
import urllib.error

# Add accountant agent path for xero_api
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import load_tokens, get_tenant_id, refresh_access_token

WISE_ACCOUNT_ID = '01aab634-157c-4992-8c11-2f14724d7191'
TEST_CSV = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/WISE-AUD-XERO-IMPORT-TEST.csv'

def api_post(endpoint, payload, tenant_id):
    tokens = load_tokens()
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f'https://api.xero.com/api.xro/2.0/{endpoint}',
        data=data,
        headers={
            'Authorization': f'Bearer {tokens["access_token"]}',
            'Xero-Tenant-Id': tenant_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        method='PUT'
    )
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        if e.code == 401:
            tokens = refresh_access_token()
            req.add_header('Authorization', f'Bearer {tokens["access_token"]}')
            try:
                resp = urllib.request.urlopen(req)
                return json.loads(resp.read().decode()), None
            except urllib.error.HTTPError as e2:
                return None, f'HTTP {e2.code}: {e2.read().decode()[:200]}'
        else:
            body = e.read().decode()
            return None, f'HTTP {e.code}: {body}'

def parse_date(date_str):
    """Convert DD/MM/YYYY to YYYY-MM-DD"""
    parts = date_str.split('/')
    return f'{parts[2]}-{parts[1]}-{parts[0]}'

def build_xero_transaction(row, idx):
    """Convert CSV row to Xero BankTransaction"""
    date = parse_date(row['*Date'])
    amount = float(row['*Amount'])
    payee = row['*Payee']
    desc = row['*Description']
    account_code = row['AccountCode']
    tax_type = row['TaxType'] or 'GST on Expenses'
    
    # Determine type: SPEND (negative) or RECEIVE (positive)
    if amount < 0:
        txn_type = 'SPEND'
        line_amount = abs(amount)
    else:
        txn_type = 'RECEIVE'
        line_amount = abs(amount)
    
    txn = {
        'Type': txn_type,
        'Contact': {
            'Name': payee[:255] if payee else 'Wise Transaction',
        },
        'Date': date,
        'LineItems': [{
            'Description': desc[:4000] if desc else payee,
            'Quantity': 1,
            'UnitAmount': round(line_amount, 2),
            'AccountCode': account_code if account_code else '429',  # Uncoded = General Expenses (fix later)
            # Note: TaxType omitted - Xero uses the account's default tax setting
        }],
        'BankAccount': {
            'AccountID': WISE_ACCOUNT_ID,
        },
        'Reference': f'TEST-{idx:03d}',
    }
    
    return txn

def main():
    print('🦬 Importing TEST batch to Xero...\n')
    
    # Load test CSV
    with open(TEST_CSV) as f:
        rows = list(csv.DictReader(f))
    
    print(f'Found {len(rows)} test transactions')
    
    tid, tname = get_tenant_id()
    print(f'Connected to Xero: {tname}\n')
    
    # Build transactions
    transactions = []
    for idx, row in enumerate(rows, 1):
        txn = build_xero_transaction(row, idx)
        transactions.append(txn)
        print(f'  {idx}. {row["*Date"]} | {row["*Amount"]:>8} | {row["*Payee"][:40]}')
    
    print(f'\n📤 Importing {len(transactions)} transactions to Wise AUD account...')
    
    # Import to Xero
    result, err = api_post('BankTransactions', {'BankTransactions': transactions}, tid)
    
    if err:
        print(f'\n❌ Import failed: {err}')
        return 1
    else:
        imported = len(result.get('BankTransactions', []))
        print(f'\n✅ SUCCESS! Imported {imported} transactions to Xero')
        print(f'   Check Wise AUD account in Xero to see them (unreconciled)')
        return 0

if __name__ == '__main__':
    sys.exit(main())
