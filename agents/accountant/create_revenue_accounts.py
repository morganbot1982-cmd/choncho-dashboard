#!/usr/bin/env python3
"""Create new revenue accounts in Xero"""

import json
import os
import urllib.request
import urllib.parse
import base64

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
    accounts_to_create = [
        {"Code": "201", "Name": "Income - Sean Maxwell Ferguson", "Type": "REVENUE", "TaxType": "OUTPUT"},
        {"Code": "202", "Name": "Income - Labouring", "Type": "REVENUE", "TaxType": "OUTPUT"},
        {"Code": "203", "Name": "Income - Car Sale", "Type": "REVENUE", "TaxType": "OUTPUT"},
        {"Code": "204", "Name": "Income - Maxine Pemble", "Type": "REVENUE", "TaxType": "OUTPUT"},
        {"Code": "205", "Name": "Income - Personal/Miscellaneous", "Type": "REVENUE", "TaxType": "OUTPUT"},
    ]
    
    print("Creating 5 new revenue accounts in Xero...\n")
    
    tenant_id = get_tenant_id()
    created = []
    errors = []
    
    for account_data in accounts_to_create:
        try:
            response = api_put('Accounts', account_data, tenant_id)
            if 'Accounts' in response and response['Accounts']:
                account = response['Accounts'][0]
                created.append(account)
                print(f"✅ {account['Code']} - {account['Name']}")
            else:
                errors.append(f"❌ {account_data['Code']} - Unexpected response: {response}")
                print(errors[-1])
        except Exception as e:
            errors.append(f"❌ {account_data['Code']} - {account_data['Name']}: {str(e)}")
            print(errors[-1])
    
    print(f"\n{'='*70}")
    print(f"DONE: {len(created)} accounts created, {len(errors)} errors")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
