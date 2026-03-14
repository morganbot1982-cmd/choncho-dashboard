#!/usr/bin/env python3
"""Export chart of accounts from Xero for tax rule mapping"""
import sys
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

print("Fetching chart of accounts from Xero...\n")

response = api_get('Accounts')
accounts = response.get('Accounts', [])

print(f"Found {len(accounts)} accounts\n")
print("=" * 100)
print(f"{'Code':<8} | {'Name':<50} | {'Type':<20}")
print("=" * 100)

# Sort by code
sorted_accounts = sorted(accounts, key=lambda a: a.get('Code', ''))

for acc in sorted_accounts:
    code = acc.get('Code', 'N/A')
    name = acc.get('Name', 'N/A')
    acc_type = acc.get('Type', 'N/A')
    status = acc.get('Status', 'ACTIVE')
    
    # Only show active accounts
    if status == 'ACTIVE':
        print(f"{code:<8} | {name[:50]:<50} | {acc_type:<20}")

print("=" * 100)
print(f"\n✅ Active accounts listed above")
print(f"\nUse these codes to build TAX_RULES in audit-tax-rates.py")
