#!/usr/bin/env python3
"""Check tax types on all Rent Received transactions"""
import sys
from collections import Counter
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

print("Scanning all Rent Received transactions...\n")

all_rent_txns = []
for page in range(1, 50):
    response = api_get(f'BankTransactions?page={page}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    for txn in txns:
        for line_item in txn.get('LineItems', []):
            if line_item.get('AccountCode') == '255':
                all_rent_txns.append({
                    'txn_id': txn.get('BankTransactionID'),
                    'date': txn.get('Date', '')[:10],
                    'amount': txn.get('Total', 0),
                    'contact': txn.get('Contact', {}).get('Name', ''),
                    'tax_type': line_item.get('TaxType', 'NONE'),
                    'is_reconciled': txn.get('IsReconciled', False)
                })
                break

print(f"✅ Found {len(all_rent_txns)} Rent Received transactions\n")

# Count by tax type
tax_types = Counter(t['tax_type'] for t in all_rent_txns)
print("Tax Types:")
for tax_type, count in tax_types.items():
    print(f"  {tax_type}: {count}")

# Check reconciliation status
reconciled_count = sum(1 for t in all_rent_txns if t['is_reconciled'])
print(f"\nReconciled: {reconciled_count}/{len(all_rent_txns)}")

# Show non-EXEMPTOUTPUT ones
non_exempt = [t for t in all_rent_txns if t['tax_type'] != 'EXEMPTOUTPUT']
if non_exempt:
    print(f"\n⚠️ {len(non_exempt)} transactions NOT GST Free:")
    for t in non_exempt[:10]:
        print(f"  {t['date']} | ${t['amount']} | {t['contact']} | TaxType: {t['tax_type']}")
    if len(non_exempt) > 10:
        print(f"  ... and {len(non_exempt) - 10} more")
else:
    print(f"\n✅ All {len(all_rent_txns)} Rent Received transactions are already EXEMPTOUTPUT (GST Free)")
