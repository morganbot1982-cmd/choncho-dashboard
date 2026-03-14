#!/usr/bin/env python3
"""Write duplicates CSV to existing Google Sheet"""
import csv
import json
import subprocess

# Spreadsheet ID from gog create
sheet_id = "1CS0Ki23_jr_5KOsGSQ6FWd2RqF2fLS5hZUhYXwEmklA"

# Read CSV
csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-duplicates-wrong-account-review.csv'
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

print(f"Read {len(rows)} rows from CSV")

# Write to sheet using gog sheets update
# Format: pass rows as JSON array
values_json = json.dumps(rows)

print(f"\nWriting to Sheet1!A1...")
result = subprocess.run(
    ['gog', 'sheets', 'update', sheet_id, 'Sheet1!A1', '--values', values_json],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"❌ Error: {result.stderr}")
    print(f"Stdout: {result.stdout}")
    exit(1)

print(f"✅ {len(rows)} rows written successfully!")
print(f"\n📊 Open: https://docs.google.com/spreadsheets/d/{sheet_id}")
print(f"\n🎯 Review duplicates:")
print(f"   - 274 duplicate groups")
print(f"   - 674 transactions total")
print(f"   - Suggested: KEEP first, DELETE rest")
print(f"   - Update 'Action' column as needed")
