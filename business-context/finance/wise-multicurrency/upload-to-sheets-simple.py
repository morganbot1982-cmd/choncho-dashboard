#!/usr/bin/env python3
"""Upload duplicates CSV to Google Sheets using Google Sheets API"""
import csv
import json
import subprocess

# Read CSV
csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-duplicates-wrong-account-review.csv'
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

print(f"Read {len(rows)} rows from CSV")

# Use gog CLI to create spreadsheet
print("\nCreating spreadsheet via gog...")
result = subprocess.run(
    ['gog', 'sheets', 'create', '--title', 'Wise Duplicates - Review & Delete'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"Error creating spreadsheet: {result.stderr}")
    exit(1)

# Extract spreadsheet ID from output
output = result.stdout.strip()
print(f"gog output: {output}")

# Parse the ID (assuming format like: "Created spreadsheet: <ID>")
if 'spreadsheets/d/' in output:
    sheet_id = output.split('spreadsheets/d/')[1].split('/')[0]
elif output.startswith('1'):  # Direct ID output
    sheet_id = output.split()[0]
else:
    print(f"Could not parse sheet ID from: {output}")
    exit(1)

print(f"Spreadsheet ID: {sheet_id}")
print(f"URL: https://docs.google.com/spreadsheets/d/{sheet_id}")

# Now write data using gog sheets write
print(f"\nWriting {len(rows)} rows...")

# Convert rows to JSON format for gog
data_json = json.dumps(rows)

result = subprocess.run(
    ['gog', 'sheets', 'write', sheet_id, 'Sheet1!A1', '--values', data_json],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"Error writing data: {result.stderr}")
    print(f"Stdout: {result.stdout}")
    exit(1)

print("✅ Data written successfully!")
print(f"\n📊 Open here: https://docs.google.com/spreadsheets/d/{sheet_id}")
print(f"\n🎯 Next: Review duplicate groups, update 'Action' column (KEEP/DELETE)")
