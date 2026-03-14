#!/usr/bin/env python3
"""Convert CSV to JSON 2D array for gog"""
import csv
import json

csv_file = '/Users/userclaw/.openclaw/workspace/projects/wise-multicurrency/wise-duplicates-wrong-account-review.csv'
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

print(json.dumps(rows))
