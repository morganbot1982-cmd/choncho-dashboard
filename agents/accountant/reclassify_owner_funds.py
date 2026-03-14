#!/usr/bin/env python3
"""Create journal entries to reclassify Owner Funds Introduced to revenue accounts"""

import csv
import json
import os
import urllib.request
import urllib.parse
import base64
from datetime import datetime

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
CREDS_PATH = os.path.join(CONFIG_DIR, 'xero_credentials.json')
TOKEN_PATH = os.path.join(CONFIG_DIR, 'xero_tokens.json')

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
    if connections:
        return connections[0]['tenantId']
    return None

def categorize_to_account(desc):
    """Map transaction description to account code"""
    if 'JODIE ANN EHMER' in desc or 'JAMES ROBERT CLEARY' in desc or 'J CLEARY' in desc:
        return '255'  # Rent Received
    elif 'SMITH D T' in desc or 'DANIEL THOMAS SMITH' in desc:
        return '255'  # Rent Received
    elif 'SEAN MAXWELL FERGUSON' in desc:
        return '201'  # Income - Sean Maxwell Ferguson
    elif 'SKY POINT ROOFING' in desc or 'STEVENS JAMAAL MAX' in desc:
        return '202'  # Income - Labouring
    elif 'ERWIN EDWARD MACDOWELL' in desc:
        return '203'  # Income - Car Sale
    elif 'GARY LEE TRIGGS' in desc:
        return '203'  # Income - Car Sale
    elif 'Maxine Lucia Pemble' in desc:
        return '204'  # Income - Maxine Pemble
    else:
        return '205'  # Income - Personal/Miscellaneous

def api_put(endpoint, data_dict, tenant_id=None):
    tokens = load_tokens()
    if not tenant_id:
        tenant_id = get_tenant_id()
    
    url = f"https://api.xero.com/api.xro/2.0/{endpoint}"
    data = json.dumps(data_dict).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='PUT', headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })
    
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 401:
            tokens = refresh_access_token()
            req = urllib.request.Request(url, data=data, method='PUT', headers={
                'Authorization': f'Bearer {tokens["access_token"]}',
                'Xero-Tenant-Id': tenant_id,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read().decode())
        else:
            error_body = e.read().decode() if e.fp else str(e)
            raise Exception(f"HTTP {e.code}: {error_body}")

def main():
    print("Reclassifying Owner Funds Introduced transactions...\n")
    
    # Load the owner funds data
    owner_funds_file = '/tmp/owner_funds_intro.csv'
    
    # Group transactions by account code
    by_account = {}
    skip_count = 0
    
    with open(owner_funds_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row['Description']
            
            # Skip legitimate owner funds
            if any(x in desc for x in ['LEIF OH LEIF', 'MORGAN SCHOERMER', 'MORGAN K SCHOERMER', 
                                        'schoermer morgan', 'Topped up account']):
                skip_count += 1
                continue
            
            account_code = categorize_to_account(desc)
            
            if account_code not in by_account:
                by_account[account_code] = []
            
            by_account[account_code].append(row)
    
    print(f"Skipped {skip_count} legitimate owner funds transactions")
    print(f"Reclassifying {sum(len(txns) for txns in by_account.values())} transactions\n")
    
    tenant_id = get_tenant_id()
    
    # Create one journal entry per account
    for account_code, transactions in sorted(by_account.items()):
        total = sum(float(t['Amount']) for t in transactions)
        count = len(transactions)
        
        # Get account name for reference
        account_names = {
            '201': 'Sean Maxwell Ferguson',
            '202': 'Labouring',
            '203': 'Car Sale',
            '204': 'Maxine Pemble',
            '205': 'Personal/Misc',
            '255': 'Rent Received'
        }
        account_name = account_names.get(account_code, account_code)
        
        # Create journal entry
        journal = {
            "Narration": f"Reclassify {count} Owner Funds Introduced transactions to {account_name}",
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "JournalLines": [
                {
                    "AccountCode": "881",  # Debit Owner Funds Introduced (reduce liability)
                    "LineAmount": total,
                    "Description": f"Reclassify to {account_code} {account_name}"
                },
                {
                    "AccountCode": account_code,  # Credit revenue account
                    "LineAmount": -total,
                    "Description": f"Reclassified from Owner Funds Introduced"
                }
            ]
        }
        
        try:
            response = api_put('ManualJournals', journal, tenant_id)
            if 'ManualJournals' in response and response['ManualJournals']:
                mj = response['ManualJournals'][0]
                print(f"✅ {account_code} {account_name:<25} {count:>3} txns  ${total:>10,.2f}  (Journal {mj.get('ManualJournalID', '?')[:8]}...)")
            else:
                print(f"❌ {account_code} {account_name} - Unexpected response")
        except Exception as e:
            print(f"❌ {account_code} {account_name} - Error: {str(e)}")
    
    print(f"\n{'='*80}")
    print("DONE: Journal entries created")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
