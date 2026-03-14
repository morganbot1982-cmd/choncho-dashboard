#!/usr/bin/env python3
"""Analyze money coming INTO Wise AUD account by Australian financial year"""
import csv
from datetime import datetime
from collections import defaultdict

csv_file = '/Users/Shared/OpenClaw Inbox/statement_2019-07-01_2026-02-14_pdf (1) copy/statement_2017-04-28_2026-02-26_csv/statement_16108725_AUD_2017-04-28_2026-02-26.csv'

# Read CSV
income_by_fy = defaultdict(float)
transaction_count_by_fy = defaultdict(int)

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            # Parse date
            date_str = row['Date']
            dt = datetime.strptime(date_str, '%d-%m-%Y')
            
            # Parse amount (positive = money IN, negative = money OUT)
            amount = float(row['Amount'])
            
            # Only count money coming IN (positive amounts)
            if amount > 0:
                # Determine financial year (AU: July 1 - June 30)
                if dt.month >= 7:
                    fy = f"FY{dt.year}-{dt.year+1}"
                else:
                    fy = f"FY{dt.year-1}-{dt.year}"
                
                income_by_fy[fy] += amount
                transaction_count_by_fy[fy] += 1
        except (ValueError, KeyError) as e:
            continue

# Sort by financial year
sorted_fys = sorted(income_by_fy.keys())

print("=" * 70)
print("WISE AUD ACCOUNT - MONEY IN BY FINANCIAL YEAR")
print("=" * 70)
print(f"{'Financial Year':<20} {'Income (AUD)':<20} {'Transactions':<15}")
print("-" * 70)

total_income = 0
total_txns = 0

for fy in sorted_fys:
    income = income_by_fy[fy]
    txns = transaction_count_by_fy[fy]
    total_income += income
    total_txns += txns
    print(f"{fy:<20} ${income:>18,.2f} {txns:>14,}")

print("-" * 70)
print(f"{'TOTAL':<20} ${total_income:>18,.2f} {total_txns:>14,}")
print("=" * 70)
