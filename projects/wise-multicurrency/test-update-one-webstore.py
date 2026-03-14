#!/usr/bin/env python3
"""Test updating ONE webstore sales transaction to see full error"""
import sys
import json
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
from xero_api_update import api_post

print("Fetching one webstore sales transaction...\n")

# Get one transaction
response = api_get('BankTransactions?page=16')
txns = response.get('BankTransactions', [])
webstore_txns = [t for t in txns if 'webstore' in t.get('Contact', {}).get('Name', '').lower()]

if not webstore_txns:
    print("No webstore sales found on page 16")
    sys.exit(1)

txn = webstore_txns[0]
print(f"Testing transaction:")
print(f"  ID: {txn.get('BankTransactionID')}")
print(f"  Date: {txn.get('Date','')[:10]}")
print(f"  Amount: ${txn.get('Total', 0)}")
print(f"  Contact: {txn.get('Contact', {}).get('Name', '')}")
print(f"  IsReconciled: {txn.get('IsReconciled', False)}")
print()

# Try to just update the contact name (don't un-reconcile yet)
try:
    update_data = {
        'BankTransactionID': txn.get('BankTransactionID'),
        'Contact': {'Name': 'Shopify'}
    }
    
    print(f"Attempting update with minimal data...")
    print(json.dumps(update_data, indent=2))
    print()
    
    result = api_post('BankTransactions', {'BankTransactions': [update_data]})
    print(f"✅ Success!")
    print(json.dumps(result, indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
