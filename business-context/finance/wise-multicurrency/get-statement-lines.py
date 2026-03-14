#!/usr/bin/env python3
"""Get bank statement lines (unreconciled imports) from Wise AUD"""
import sys
import csv
from datetime import datetime
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# Correct Wise AUD account ID
wise_aud_id = "10142dd5-d7b0-4f95-9ab0-7e5e5a1baa7e"

print("Fetching bank statement lines from Wise AUD...\n")

# Get statements - this shows imported transactions waiting to be reconciled
try:
    # Try the Statements endpoint with date range
    from_date = "2017-01-01"
    to_date = datetime.now().strftime("%Y-%m-%d")
    
    response = api_get(f'BankStatements/{wise_aud_id}?fromDate={from_date}&toDate={to_date}')
    print(f"Response: {response}")
    
    if 'Statements' in response:
        statements = response['Statements']
        print(f"\n✅ Found {len(statements)} statement periods")
        
        all_lines = []
        for stmt in statements:
            lines = stmt.get('StatementLines', [])
            print(f"  Statement {stmt.get('StatementID','?')}: {len(lines)} lines")
            all_lines.extend(lines)
        
        print(f"\n📊 Total statement lines: {len(all_lines)}")
        
        # Export to CSV
        if all_lines:
            csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-aud-statement-lines.csv'
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'Date', 'Amount', 'Payee', 'Description', 'Reference', 'IsReconciled', 'StatementLineID'
                ])
                writer.writeheader()
                
                for line in all_lines:
                    writer.writerow({
                        'Date': line.get('Date', '')[:10] if line.get('Date') else '',
                        'Amount': line.get('Amount', 0),
                        'Payee': line.get('Payee', ''),
                        'Description': line.get('Description', ''),
                        'Reference': line.get('Reference', ''),
                        'IsReconciled': line.get('IsReconciled', False),
                        'StatementLineID': line.get('StatementLineID', '')
                    })
            
            print(f"\n✅ Exported to: {csv_file}")
            
            # Count unreconciled
            unreconciled = [l for l in all_lines if not l.get('IsReconciled', False)]
            print(f"\n📋 Unreconciled: {len(unreconciled)}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
