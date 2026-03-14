#!/usr/bin/env python3
"""Find all 'Rent Received' transactions"""
import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

print("Searching for 'Rent Received' account...\n")

# First, find the account code for Rent Received
accounts = api_get('Accounts')
rent_account = None
for acc in accounts.get('Accounts', []):
    if 'rent' in acc.get('Name', '').lower() and 'receiv' in acc.get('Name', '').lower():
        rent_account = acc
        print(f"Found account: {acc.get('Code')} - {acc.get('Name')}")
        break

if not rent_account:
    print("Could not find 'Rent Received' account")
    print("\nSearching by contact name instead...")
    # Try searching by contact
    for page in range(1, 10):
        response = api_get(f'BankTransactions?page={page}')
        txns = response.get('BankTransactions', [])
        if not txns:
            break
        rent_txns = [t for t in txns if 'rent' in t.get('Contact', {}).get('Name', '').lower()]
        if rent_txns:
            print(f"Page {page}: Found {len(rent_txns)} transactions with 'rent' in contact name")
            sample = rent_txns[0]
            print(f"  Sample: {sample.get('Contact', {}).get('Name', '')} | Account: {sample.get('LineItems', [{}])[0].get('AccountCode', '?')}")
else:
    # Search for transactions with this account code
    account_code = rent_account.get('Code')
    print(f"\nSearching for transactions with account code {account_code}...\n")
    
    all_rent_txns = []
    for page in range(1, 50):
        response = api_get(f'BankTransactions?page={page}')
        txns = response.get('BankTransactions', [])
        if not txns:
            break
        
        for txn in txns:
            for line_item in txn.get('LineItems', []):
                if line_item.get('AccountCode') == account_code:
                    all_rent_txns.append({
                        'txn': txn,
                        'line_item': line_item
                    })
                    break
    
    print(f"✅ Found {len(all_rent_txns)} Rent Received transactions\n")
    
    if all_rent_txns:
        # Sample data
        sample = all_rent_txns[0]
        txn = sample['txn']
        line = sample['line_item']
        
        print(f"Sample transaction:")
        print(f"  Date: {txn.get('Date', '')[:10]}")
        print(f"  Amount: ${txn.get('Total', 0)}")
        print(f"  Contact: {txn.get('Contact', {}).get('Name', '')}")
        print(f"  Account: {line.get('AccountCode')} - {rent_account.get('Name')}")
        print(f"  Current Tax Type: {line.get('TaxType', 'NONE')}")
        print(f"  IsReconciled: {txn.get('IsReconciled', False)}")
