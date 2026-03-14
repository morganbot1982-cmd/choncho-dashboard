#!/usr/bin/env python3
"""Xero API helper — read-only queries"""

import json
import os
import urllib.request
import urllib.parse
import base64
import sys
import time

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
        return connections[0]['tenantId'], connections[0].get('tenantName', '?')
    return None, None

def api_get(endpoint, tenant_id=None):
    tokens = load_tokens()
    if not tenant_id:
        tenant_id, _ = get_tenant_id()
    url = f"https://api.xero.com/api.xro/2.0/{endpoint}"
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Accept': 'application/json',
    })
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            tokens = refresh_access_token()
            req = urllib.request.Request(url, headers={
                'Authorization': f'Bearer {tokens["access_token"]}',
                'Xero-Tenant-Id': tenant_id,
                'Accept': 'application/json',
            })
            resp = urllib.request.urlopen(req)
        else:
            raise
    return json.loads(resp.read().decode())

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'connections'
    
    if cmd == 'connections':
        tid, tname = get_tenant_id()
        print(f"Connected org: {tname} (tenant: {tid})")
    
    elif cmd == 'accounts':
        data = api_get('Accounts')
        for a in sorted(data.get('Accounts', []), key=lambda x: x.get('Code', '')):
            code = a.get('Code', '-')
            name = a.get('Name', '?')
            atype = a.get('Type', '?')
            status = a.get('Status', '?')
            print(f"{code:>6}  {name:<50} {atype:<15} {status}")
    
    elif cmd == 'bankaccounts':
        data = api_get('Accounts?where=Type=="BANK"')
        for a in data.get('Accounts', []):
            print(f"{a.get('Code','-'):>6}  {a.get('Name','?'):<50} {a.get('BankAccountNumber','?')}")
    
    elif cmd.startswith('transactions'):
        # Usage: transactions [page] [bank_account_id]
        page = sys.argv[2] if len(sys.argv) > 2 else '1'
        data = api_get(f'BankTransactions?page={page}')
        txns = data.get('BankTransactions', [])
        print(f"Page {page}: {len(txns)} transactions")
        for t in txns[:5]:
            print(f"  {t.get('Date','?')[:10]}  {t.get('Contact',{}).get('Name','?'):<30}  {t.get('Total',0):>10.2f}  {t.get('Status','?')}")
    
    else:
        data = api_get(cmd)
        print(json.dumps(data, indent=2)[:5000])
