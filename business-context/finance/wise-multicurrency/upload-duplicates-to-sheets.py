#!/usr/bin/env python3
"""Upload duplicates CSV to Google Sheets"""
import sys
import csv
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from google_sheets_api import create_spreadsheet, write_to_sheet

# Read CSV
csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-duplicates-wrong-account-review.csv'
rows = []
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

print(f"Read {len(rows)} rows from CSV (including header)")

# Create spreadsheet
title = "Wise Duplicates - Review & Delete"
print(f"\nCreating spreadsheet: {title}")
sheet_id = create_spreadsheet(title)
print(f"✅ Created: https://docs.google.com/spreadsheets/d/{sheet_id}")

# Write data
print(f"\nWriting {len(rows)} rows...")
write_to_sheet(sheet_id, 'Sheet1', rows, start_cell='A1')
print(f"✅ Data written")

print(f"\n🎯 Next Steps:")
print(f"1. Open: https://docs.google.com/spreadsheets/d/{sheet_id}")
print(f"2. Review duplicate groups")
print(f"3. Change 'Action' column: KEEP or DELETE")
print(f"4. Tell Choncho when ready → delete via API")
