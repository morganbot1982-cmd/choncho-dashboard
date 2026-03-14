#!/usr/bin/env python3
"""Import reconciled Wise transactions into Xero 'Wise - Full Import' bank account"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from xero_api import load_tokens, load_creds, get_tenant_id, refresh_access_token, save_tokens

WISE_ACCOUNT_ID = '01aab634-157c-4992-8c11-2f14724d7191'
CSV_PATH = os.path.join(os.path.dirname(__file__), 'reconciliation_current.csv')
PROGRESS_PATH = os.path.join(os.path.dirname(__file__), 'config', 'wise_import_progress.json')

def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH) as f:
            return json.load(f)
    return {'imported': 0, 'last_index': -1, 'errors': []}

def save_progress(prog):
    with open(PROGRESS_PATH, 'w') as f:
        json.dump(prog, f, indent=2)

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
        elif e.code == 429:
            # Rate limited - wait and retry
            retry_after = int(e.headers.get('Retry-After', '60'))
            print(f'  ⏳ Rate limited, waiting {retry_after}s...')
            time.sleep(retry_after + 1)
            try:
                resp = urllib.request.urlopen(req)
                return json.loads(resp.read().decode()), None
            except urllib.error.HTTPError as e2:
                return None, f'HTTP {e2.code} after retry: {e2.read().decode()[:200]}'
        else:
            body = e.read().decode()[:300]
            return None, f'HTTP {e.code}: {body}'

def build_xero_transaction(row, idx):
    """Convert a CSV row to a Xero BankTransaction object"""
    date = row['Date']  # YYYY-MM-DD format
    desc = row['Description']
    amount = float(row['Amount'])
    account_code = row['XeroAccountCode']
    # Remap codes that Xero won't accept in bank transactions
    CODE_REMAP = {
        '630': '310',  # Inventory → COGS
        '877': '429',  # Tracking Transfers → General Expenses
    }
    account_code = CODE_REMAP.get(account_code, account_code)
    direction = row['Direction']
    
    # Determine type: SPEND (outgoing/negative) or RECEIVE (incoming/positive)
    if direction == 'outgoing' or amount < 0:
        txn_type = 'SPEND'
        line_amount = abs(amount)
    else:
        txn_type = 'RECEIVE'
        line_amount = abs(amount)
    
    txn = {
        'Type': txn_type,
        'Contact': {
            'Name': desc[:255],  # Use description as contact name
        },
        'Date': date,
        'LineItems': [{
            'Description': desc,
            'Quantity': 1,
            'UnitAmount': round(line_amount, 2),
            'AccountCode': account_code,
        }],
        'BankAccount': {
            'AccountID': WISE_ACCOUNT_ID,
        },
        'Reference': f'WISE-{idx:05d}',
    }
    
    return txn

def main():
    # Load CSV
    with open(CSV_PATH) as f:
        rows = list(csv.DictReader(f))
    
    # Filter out suspense/currency conversions
    real_rows = [(i, r) for i, r in enumerate(rows) if r['XeroAccountCode'] != '850']
    print(f'Total rows: {len(rows)} | Real transactions: {len(real_rows)}', flush=True)
    
    progress = load_progress()
    start_from = progress['last_index'] + 1
    
    tid, tname = get_tenant_id()
    print(f'Connected to: {tname}', flush=True)
    print(f'Resuming from index: {start_from}', flush=True)
    
    # Process in batches of 50
    BATCH_SIZE = 50
    batch = []
    batch_indices = []
    imported = progress['imported']
    
    for idx, (orig_idx, row) in enumerate(real_rows):
        if idx < start_from:
            continue
        
        txn = build_xero_transaction(row, orig_idx)
        batch.append(txn)
        batch_indices.append(idx)
        
        if len(batch) >= BATCH_SIZE:
            # Send batch
            result, err = api_post('BankTransactions', {'BankTransactions': batch}, tid)
            if err:
                print(f'  ❌ Batch error at index {batch_indices[0]}-{batch_indices[-1]}: {err}')
                progress['errors'].append({'indices': batch_indices, 'error': err})
                save_progress(progress)
                # Try individual items
                for bi, btxn in zip(batch_indices, batch):
                    r2, e2 = api_post('BankTransactions', {'BankTransactions': [btxn]}, tid)
                    if e2:
                        print(f'    ❌ Single #{bi}: {e2}')
                        progress['errors'].append({'index': bi, 'error': e2})
                    else:
                        imported += 1
                    progress['last_index'] = bi
                    progress['imported'] = imported
                    save_progress(progress)
                    time.sleep(0.5)
            else:
                imported += len(batch)
                progress['last_index'] = batch_indices[-1]
                progress['imported'] = imported
                save_progress(progress)
                print(f'  ✅ Batch {batch_indices[0]}-{batch_indices[-1]} done ({imported}/{len(real_rows)})', flush=True)
            
            batch = []
            batch_indices = []
            time.sleep(1)  # Rate limit buffer
    
    # Final partial batch
    if batch:
        result, err = api_post('BankTransactions', {'BankTransactions': batch}, tid)
        if err:
            print(f'  ❌ Final batch error: {err}')
            progress['errors'].append({'indices': batch_indices, 'error': err})
        else:
            imported += len(batch)
            progress['last_index'] = batch_indices[-1]
            progress['imported'] = imported
            print(f'  ✅ Final batch done ({imported}/{len(real_rows)})')
        save_progress(progress)
    
    print(f'\n🏁 Import complete: {imported}/{len(real_rows)} transactions imported')
    if progress['errors']:
        print(f'⚠️  {len(progress["errors"])} errors logged')

if __name__ == '__main__':
    main()
