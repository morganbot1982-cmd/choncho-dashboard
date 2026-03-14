#!/usr/bin/env python3
import json, os, urllib.request, base64

CONFIG_DIR = os.path.join(os.path.dirname(__file__), 'config')
CREDS_PATH = os.path.join(CONFIG_DIR, 'xero_credentials.json')
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

def api_put(endpoint, data_dict, tenant_id):
    tokens = load_tokens()
    url = f"https://api.xero.com/api.xro/2.0/{endpoint}"
    data = json.dumps(data_dict).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PUT', headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
    })
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode())

account = {"Code": "206", "Name": "Consulting Revenue", "Type": "REVENUE", "TaxType": "OUTPUT"}
tenant_id = get_tenant_id()
response = api_put('Accounts', account, tenant_id)

if 'Accounts' in response:
    acc = response['Accounts'][0]
    print(f"✅ Created: {acc['Code']} - {acc['Name']}")
else:
    print(f"❌ Failed: {response}")
