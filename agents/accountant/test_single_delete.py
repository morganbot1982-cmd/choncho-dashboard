import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
import json
import os
import urllib.request
import base64

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
    return connections[0]['tenantId']

# Get one transaction from Wise - Full Import
wise_import_id = "01aab634-157c-4992-8c11-2f14724d7191"
page = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_import_id}")&page=1')
txn = page.get('BankTransactions', [])[0] if page.get('BankTransactions') else None

if txn:
    txn_id = txn.get('BankTransactionID')
    print(f"Test transaction: {txn_id}")
    print(f"Status: {txn.get('Status')}")
    print(f"Date: {txn.get('Date')[:10]}")
    print(f"Amount: {txn.get('Total')}\n")
    
    tenant_id = get_tenant_id()
    tokens = load_tokens()
    
    # Try method 1: POST with Status=DELETED
    print("Method 1: POST with Status=DELETED")
    url = f"https://api.xero.com/api.xro/2.0/BankTransactions/{txn_id}"
    data = json.dumps({"Status": "DELETED"}).encode()
    req = urllib.request.Request(url, data=data, method='POST', headers={
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Xero-Tenant-Id': tenant_id,
        'Content-Type': 'application/json',
    })
    try:
        resp = urllib.request.urlopen(req)
        print(f"✅ Success: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: HTTP {e.code} - {e.read().decode()[:200]}")

