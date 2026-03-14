#!/usr/bin/env python3
"""
Audit all Xero transactions for incorrect tax rates based on chart of accounts
Generates report of mismatches for review before fixing
"""
import sys
import json
from collections import defaultdict, Counter
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# Tax rate rules by account code
# Format: 'AccountCode': 'EXPECTED_TAX_TYPE'
TAX_RULES = {
    # Income accounts (OUTPUT = GST on Income 10%)
    '200': 'OUTPUT',  # Sales
    '201': 'OUTPUT',  # Income - Sean Maxwell Ferguson
    '204': 'OUTPUT',  # Income - Maxine Pemble
    '206': 'OUTPUT',  # Consulting Revenue
    '212': 'OUTPUT',  # Income - Robert Cleary
    '213': 'OUTPUT',  # Income - Dan Smith
    '214': 'OUTPUT',  # Income - Sky Point Roofing
    '215': 'OUTPUT',  # Income - Win Mc Dowell Car Loan
    '216': 'OUTPUT',  # Income - Morgan Williams
    '258': 'OUTPUT',  # Photography Income
    '260': 'OUTPUT',  # Abyss Income
    
    # Exempt income (EXEMPTOUTPUT = GST Free)
    '255': 'EXEMPTOUTPUT',  # Rent Received (residential rent is GST-free in AU)
    '270': 'EXEMPTOUTPUT',  # Interest Income (financial supplies GST-free)
    '265': 'EXEMPTOUTPUT',  # Refunds (typically GST-free)
    
    # Expenses - GST on Expenses (INPUT = claimable)
    '400': 'INPUT',  # Advertising
    '408': 'INPUT',  # Cleaning
    '412': 'INPUT',  # Consulting & Accounting
    '425': 'INPUT',  # Freight & Courier
    '429': 'INPUT',  # General Expenses
    '433': 'INPUT',  # Insurance
    '441': 'INPUT',  # Legal expenses
    '445': 'INPUT',  # Light, Power, Heating
    '449': 'INPUT',  # Motor Vehicle Expenses
    '453': 'INPUT',  # Office Expenses
    '461': 'INPUT',  # Printing & Stationery
    '469': 'INPUT',  # Rent (commercial rent has GST)
    '473': 'INPUT',  # Repairs and Maintenance
    '485': 'INPUT',  # Subscriptions
    '489': 'INPUT',  # Telephone & Internet
    '493': 'INPUT',  # Travel - National
    '494': 'INPUT',  # Travel - International
    '421': 'INPUT',  # Meals & Food (if business-related)
    '310': 'INPUT',  # Cost of Goods Sold
    '315': 'INPUT',  # Cost Of Goods Chinese Suppliers
    
    # BAS Excluded (BASEXCLUDED = no GST)
    '416': 'BASEXCLUDED',  # Depreciation
    '420': 'BASEXCLUDED',  # Entertainment (non-deductible)
    '404': 'BASEXCLUDED',  # Bank Fees (financial services GST-free)
    '405': 'BASEXCLUDED',  # Merchant Fee (financial services)
    '508': 'BASEXCLUDED',  # Stripe Fees (financial services)
    '437': 'BASEXCLUDED',  # Interest Expense (financial services)
    '314': 'BASEXCLUDED',  # Currency Exchange Charge
    '504': 'BASEXCLUDED',  # Fines (no GST)
    '505': 'BASEXCLUDED',  # Income Tax Expense
    '477': 'BASEXCLUDED',  # Wages and Salaries (no GST on wages)
    '478': 'BASEXCLUDED',  # Superannuation (no GST)
}

print("=" * 80)
print("XERO TAX RATE AUDIT")
print("=" * 80)
print(f"\nChecking {len(TAX_RULES)} account codes with defined tax rules\n")

# Collect all transactions
print("📥 Fetching bank transactions...")
all_mismatches = []
stats = {
    'total_txns': 0,
    'total_lines': 0,
    'mismatches': 0,
    'reconciled_mismatches': 0
}

for page in range(1, 100):  # Max 100 pages
    response = api_get(f'BankTransactions?page={page}')
    txns = response.get('BankTransactions', [])
    if not txns:
        break
    
    stats['total_txns'] += len(txns)
    
    for txn in txns:
        txn_id = txn.get('BankTransactionID')
        date = txn.get('Date', '')[:10]
        total = txn.get('Total', 0)
        contact = txn.get('Contact', {}).get('Name', 'No Contact')
        is_reconciled = txn.get('IsReconciled', False)
        
        for line in txn.get('LineItems', []):
            stats['total_lines'] += 1
            account_code = line.get('AccountCode')
            actual_tax = line.get('TaxType', 'NONE')
            
            # Check if this account has a tax rule
            if account_code in TAX_RULES:
                expected_tax = TAX_RULES[account_code]
                
                if actual_tax != expected_tax:
                    stats['mismatches'] += 1
                    if is_reconciled:
                        stats['reconciled_mismatches'] += 1
                    
                    all_mismatches.append({
                        'txn_id': txn_id,
                        'date': date,
                        'amount': total,
                        'contact': contact,
                        'account_code': account_code,
                        'expected_tax': expected_tax,
                        'actual_tax': actual_tax,
                        'is_reconciled': is_reconciled
                    })

print(f"✅ Scanned {stats['total_txns']} transactions ({stats['total_lines']} line items)")
print(f"\n📊 AUDIT RESULTS")
print("=" * 80)
print(f"Total mismatches: {stats['mismatches']}")
print(f"  - Unreconciled (fixable): {stats['mismatches'] - stats['reconciled_mismatches']}")
print(f"  - Reconciled (skip): {stats['reconciled_mismatches']}")

if all_mismatches:
    print(f"\n🔍 MISMATCH DETAILS\n")
    
    # Group by account code
    by_account = defaultdict(list)
    for m in all_mismatches:
        by_account[m['account_code']].append(m)
    
    for account_code in sorted(by_account.keys()):
        matches = by_account[account_code]
        expected = matches[0]['expected_tax']
        tax_types = Counter(m['actual_tax'] for m in matches)
        
        print(f"\nAccount {account_code} (Expected: {expected})")
        print(f"  Found {len(matches)} mismatches:")
        for tax_type, count in tax_types.items():
            print(f"    - {tax_type}: {count} transactions")
        
        # Show first 5 examples
        print(f"  Examples:")
        for m in matches[:5]:
            reconciled = " [RECONCILED]" if m['is_reconciled'] else ""
            print(f"    {m['date']} | ${m['amount']:>8.2f} | {m['contact'][:30]} | {m['actual_tax']}{reconciled}")
        if len(matches) > 5:
            print(f"    ... and {len(matches) - 5} more")
    
    # Save to file for review
    report_file = '/Users/userclaw/.openclaw/workspace/projects/xero-cleanup/tax-audit-report.json'
    with open(report_file, 'w') as f:
        json.dump({
            'stats': stats,
            'mismatches': all_mismatches,
            'by_account': {k: len(v) for k, v in by_account.items()}
        }, f, indent=2)
    
    print(f"\n📄 Full report saved to: {report_file}")
    print(f"\n✅ Next step: Review report, then run fix-tax-rates.py to correct unreconciled transactions")
else:
    print(f"\n✅ All checked transactions have correct tax rates!")
