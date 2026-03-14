#!/usr/bin/env python3
"""Reclassify company transfers and top-ups from 881 to inter-account transfers"""

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
    print("Reclassifying company transfers from 881 Owner Funds Introduced...\n")
    
    # Total to reclassify: 33 company transfers + 2 top-ups
    company_transfers = 22865.11
    top_ups = 406.00
    total = company_transfers + top_ups
    
    print(f"Company transfers (LOLD → Wise): 33 txns, ${company_transfers:,.2f}")
    print(f"Account top-ups: 2 txns, ${top_ups:,.2f}")
    print(f"Total to reclassify: 35 txns, ${total:,.2f}\n")
    
    tenant_id = get_tenant_id()
    
    # Create journal entry
    # Debit 881 (reduce owner funds liability)
    # Credit 877 Tracking Transfers (inter-account clearing)
    journal = {
        "Narration": "Reclassify LOLD company transfers and top-ups from Owner Funds Introduced to inter-account transfers",
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "JournalLines": [
            {
                "AccountCode": "881",  # Debit Owner Funds Introduced (reduce liability)
                "LineAmount": total,
                "Description": "Reclassify company transfers - not owner funds"
            },
            {
                "AccountCode": "877",  # Credit Tracking Transfers
                "LineAmount": -total,
                "Description": "Inter-account transfers from LOLD to Wise"
            }
        ]
    }
    
    try:
        response = api_put('ManualJournals', journal, tenant_id)
        if 'ManualJournals' in response and response['ManualJournals']:
            mj = response['ManualJournals'][0]
            journal_id = mj.get('ManualJournalID', '?')
            print(f"✅ Journal entry created: {journal_id}")
            print(f"   Debit: 881 Owner A Funds Introduced ${total:,.2f}")
            print(f"   Credit: 877 Tracking Transfers ${total:,.2f}")
        else:
            print(f"❌ Unexpected response: {response}")
    except Exception as e:
        print(f"❌ Error creating journal: {str(e)}")
    
    print(f"\n{'='*80}")
    print("SUMMARY:")
    print(f"  Before: 881 Owner Funds Introduced = 82 txns, $55,302.82")
    print(f"  Reclassified: 35 txns, ${total:,.2f}")
    print(f"  After: 881 Owner Funds Introduced = 47 txns, $32,031.71 (Morgan personal transfers only)")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
