#!/usr/bin/env python3
"""
Automatically reconcile Wise AUD → CNY transfers via Xero API
Finds unreconciled AUD→CNY transactions and creates matching transfers to Wise CNY
"""
import sys
import re
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get
from xero_api_update import api_post

print("=" * 80)
print("WISE CNY TRANSFER RECONCILIATION")
print("=" * 80)

# Get Wise AUD account ID
accounts_response = api_get('Accounts?where=Type=="BANK"')
accounts = accounts_response.get('Accounts', [])
wise_aud = next((acc for acc in accounts if 'Wise AUD' in acc.get('Name', '')), None)
wise_cny = next((acc for acc in accounts if acc.get('Name') == 'Wise CNY'), None)

if not wise_aud or not wise_cny:
    print("❌ Error: Could not find Wise AUD or Wise CNY accounts")
    sys.exit(1)

wise_aud_id = wise_aud.get('AccountID')
wise_cny_id = wise_cny.get('AccountID')

print(f"✅ Found Wise AUD (ID: {wise_aud_id})")
print(f"✅ Found Wise CNY (ID: {wise_cny_id})")

# Fetch unreconciled bank statements for Wise AUD
print(f"\n📥 Fetching unreconciled Wise AUD transactions...")

statements_response = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_aud_id}")%20AND%20Status=="AUTHORISED"')
all_statements = statements_response.get('BankTransactions', [])

# Filter for AUD → CNY conversions
cny_transfers = []
for stmt in all_statements:
    # Skip reconciled
    if stmt.get('IsReconciled', False):
        continue
    
    # Look for CNY in description
    line_items = stmt.get('LineItems', [])
    if not line_items:
        continue
    
    description = line_items[0].get('Description', '')
    
    # Match pattern: "Converted X AUD to Y CNY"
    match = re.search(r'Converted.*?(\d+(?:,\d+)?(?:\.\d+)?)\s+AUD\s+to\s+(\d+(?:,\d+)?(?:\.\d+)?)\s+CNY', description)
    
    if match:
        aud_amount = float(match.group(1).replace(',', ''))
        cny_amount = float(match.group(2).replace(',', ''))
        
        cny_transfers.append({
            'statement': stmt,
            'aud_amount': aud_amount,
            'cny_amount': cny_amount,
            'date': stmt.get('Date', ''),
            'description': description
        })

print(f"\n✅ Found {len(cny_transfers)} unreconciled AUD → CNY transfers")

if len(cny_transfers) == 0:
    print("Nothing to reconcile!")
    sys.exit(0)

# Show what will be reconciled
print(f"\n📋 TRANSFERS TO RECONCILE:")
print("=" * 80)
for i, txn in enumerate(cny_transfers, 1):
    date = txn['date'][:10] if txn['date'] else 'Unknown'
    print(f"{i}. {date} | AUD {txn['aud_amount']:>10.2f} → CNY {txn['cny_amount']:>10.2f}")

# Confirm
print(f"\n⚠️  This will create {len(cny_transfers)} transfer transactions in Xero")
response = input("Type 'YES' to proceed: ")
if response != 'YES':
    print("Aborted.")
    sys.exit(0)

# Process transfers
success = 0
failed = 0

for i, txn in enumerate(cny_transfers, 1):
    stmt = txn['statement']
    stmt_id = stmt.get('BankTransactionID')
    date = stmt.get('Date')
    aud_amount = txn['aud_amount']
    cny_amount = txn['cny_amount']
    
    try:
        # Create transfer from Wise AUD to Wise CNY
        # This is a bank transfer transaction
        transfer_data = {
            'BankTransfers': [{
                'FromBankAccount': {
                    'AccountID': wise_aud_id
                },
                'ToBankAccount': {
                    'AccountID': wise_cny_id
                },
                'Amount': aud_amount,
                'Date': date,
                'CurrencyRate': cny_amount / aud_amount if aud_amount > 0 else 1,
                'FromBankTransactionID': stmt_id
            }]
        }
        
        # Create the bank transfer
        api_post('BankTransfers', transfer_data)
        
        success += 1
        print(f"✅ {i}/{len(cny_transfers)}: Reconciled {date[:10]} AUD {aud_amount:.2f} → CNY {cny_amount:.2f}")
        
    except Exception as e:
        failed += 1
        error_msg = str(e)[:100]
        print(f"❌ {i}/{len(cny_transfers)}: Failed - {error_msg}")

print(f"\n" + "=" * 80)
print(f"✅ COMPLETE!")
print(f"   Success: {success}")
print(f"   Failed: {failed}")
print(f"\n🎯 {success} CNY transfers reconciled")
