#!/usr/bin/env python3
"""Check bank statement lines in Wise AUD (what shows in reconciliation)"""
import sys
import csv
sys.path.insert(0, '/Users/userclaw/.openclaw/workspace/agents/accountant')
from xero_api import api_get

# Correct Wise AUD account ID
wise_aud_id = "10142dd5-d7b0-4f95-9ab0-7e5e5a1baa7e"

print("Fetching bank statement lines from Wise AUD...\n")

# Get bank account details first
account = api_get(f'BankTransactions?where=BankAccount.AccountID==Guid("{wise_aud_id}")')
print(f"Account response: {account}")

# Try getting statements
statements_url = f'Statements/{wise_aud_id}'
try:
    statements = api_get(statements_url)
    print(f"Statements: {statements}")
except Exception as e:
    print(f"Error getting statements: {e}")

# Alternative: Get account and check balance
accounts_url = f'Accounts/{wise_aud_id}'
try:
    account_detail = api_get(accounts_url)
    print(f"\nAccount details: {account_detail}")
except Exception as e:
    print(f"Error: {e}")
