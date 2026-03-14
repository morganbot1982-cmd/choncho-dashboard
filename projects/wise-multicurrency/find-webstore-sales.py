#!/usr/bin/env python3
"""Find all 'webstore sales' transactions and check which accounts they're in"""
import sys
from collections import defaultdict
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

print("Searching for 'webstore sales' transactions...\n")

# Get all bank transactions with 'webstore sales' contact
all_webstore = []
for page in range(1, 50):
    response = api_get(f'BankTransactions?page={page}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    # Filter for webstore sales
    webstore_txns = [t for t in txns if 'webstore' in t.get('Contact', {}).get('Name', '').lower()]
    all_webstore.extend(webstore_txns)
    print(f"Page {page}: {len(webstore_txns)} webstore sales transactions")

print(f"\n✅ Total 'webstore sales' transactions: {len(all_webstore)}\n")

# Group by account
by_account = defaultdict(list)
for txn in all_webstore:
    line_items = txn.get('LineItems', [])
    for item in line_items:
        account_code = item.get('AccountCode', 'UNKNOWN')
        by_account[account_code].append(txn)

# Display by account
print("Transactions by Account Code:")
for account_code, txns in sorted(by_account.items()):
    print(f"  {account_code}: {len(txns)} transactions")
    
    # Show sample
    if txns:
        sample = txns[0]
        print(f"    Sample: {sample.get('Date', '')[:10]} | ${sample.get('Total', 0)} | Reconciled: {sample.get('IsReconciled', False)}")

# Get Sales account details
print("\n📊 Looking for Sales account (200)...")
try:
    sales_account = api_get('Accounts/200')
    print(f"   Sales Account: {sales_account.get('Name', 'Not found')}")
except:
    print("   Could not find account 200")

print("\n🎯 Next steps:")
print("   1. Identify which account code is 'Sales' (usually 200)")
print("   2. Rename all webstore sales in Sales account to 'Shopify'")
print("   3. Flag any webstore sales in wrong accounts for manual review")
