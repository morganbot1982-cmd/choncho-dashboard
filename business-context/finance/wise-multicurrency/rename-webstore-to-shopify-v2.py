#!/usr/bin/env python3
"""Rename 'webstore sales' to 'Shopify' in Sales account (200)"""
import sys
import time
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
from xero_api_update import api_post

print("Fetching 'webstore sales' transactions in Account 200...\n")

# Get all webstore sales transactions
all_webstore = []
for page in range(1, 50):
    response = api_get(f'BankTransactions?page={page}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    webstore_txns = [t for t in txns if 'webstore' in t.get('Contact', {}).get('Name', '').lower()]
    all_webstore.extend(webstore_txns)

# Filter for Account 200 only
sales_txns = []
for txn in all_webstore:
    line_items = txn.get('LineItems', [])
    for item in line_items:
        if item.get('AccountCode') == '200':
            sales_txns.append(txn)
            break

print(f"Found {len(sales_txns)} transactions in Sales (200) to rename\n")

# Process transactions
success_count = 0
error_count = 0

for i, txn in enumerate(sales_txns, 1):
    txn_id = txn.get('BankTransactionID')
    is_reconciled = txn.get('IsReconciled', False)
    date = txn.get('Date', '')[:10]
    amount = txn.get('Total', 0)
    
    try:
        # Step 1: Un-reconcile if needed
        if is_reconciled:
            txn_copy = txn.copy()
            txn_copy['IsReconciled'] = False
            api_post('BankTransactions', {'BankTransactions': [txn_copy]})
            time.sleep(0.3)
        
        # Step 2: Update contact name to Shopify
        txn_update = txn.copy()
        txn_update['Contact'] = {'Name': 'Shopify'}
        api_post('BankTransactions', {'BankTransactions': [txn_update]})
        time.sleep(0.3)
        
        # Step 3: Re-reconcile if it was reconciled
        if is_reconciled:
            txn_update['IsReconciled'] = True
            api_post('BankTransactions', {'BankTransactions': [txn_update]})
            time.sleep(0.3)
        
        success_count += 1
        if i % 10 == 0:
            print(f"Progress: {i}/{len(sales_txns)} ({success_count} success, {error_count} errors)")
    
    except Exception as e:
        error_count += 1
        print(f"❌ Error on {date} ${amount}: {str(e)[:100]}")
        continue

print(f"\n✅ Complete!")
print(f"   Success: {success_count}")
print(f"   Errors: {error_count}")
print(f"\n🎯 'webstore sales' → 'Shopify' in Sales account")
