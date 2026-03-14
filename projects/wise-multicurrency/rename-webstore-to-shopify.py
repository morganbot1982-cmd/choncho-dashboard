#!/usr/bin/env python3
"""Rename 'webstore sales' to 'Shopify' in Sales account (200)"""
import sys
import time
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get, api_post

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
            break  # Only add once per transaction

print(f"Found {len(sales_txns)} transactions in Sales (200) to rename\n")

# Process in batches
success_count = 0
error_count = 0

for i, txn in enumerate(sales_txns, 1):
    txn_id = txn.get('BankTransactionID')
    is_reconciled = txn.get('IsReconciled', False)
    
    try:
        # Step 1: Un-reconcile if needed
        if is_reconciled:
            txn['IsReconciled'] = False
            api_post('BankTransactions', {'BankTransactions': [txn]})
            time.sleep(0.5)  # Rate limiting
        
        # Step 2: Update contact name
        txn['Contact'] = {'Name': 'Shopify'}
        api_post('BankTransactions', {'BankTransactions': [txn]})
        time.sleep(0.5)
        
        # Step 3: Re-reconcile if it was reconciled
        if is_reconciled:
            txn['IsReconciled'] = True
            api_post('BankTransactions', {'BankTransactions': [txn]})
            time.sleep(0.5)
        
        success_count += 1
        if i % 10 == 0:
            print(f"Progress: {i}/{len(sales_txns)} ({success_count} success, {error_count} errors)")
    
    except Exception as e:
        error_count += 1
        print(f"❌ Error on transaction {txn_id}: {e}")

print(f"\n✅ Complete!")
print(f"   Success: {success_count}")
print(f"   Errors: {error_count}")
print(f"\n🎯 All 'webstore sales' in Sales account renamed to 'Shopify'")
