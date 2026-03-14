# Note for Accountant - Wise Duplicates

## Issue
- Wise - Full Import account has **~300-370 duplicate transactions** (from test import attempts)
- Same date + same amount = duplicate groups
- Currently 1,900 total transactions in the account

## What We Tried
- ✅ Exported complete backup CSV with all duplicate transaction IDs
- ❌ Cannot delete via Xero API (returns HTTP 400/404 errors)
- Xero doesn't allow programmatic deletion of imported bank transactions

## Backup File
**Location:** `agents/accountant/wise-duplicates-voided-2026-02-23.csv`

**Contains:**
- BankTransactionID
- Date
- Amount
- Description
- Contact Name
- Duplicate Group identifier

## Recommendation
**Manual cleanup needed:**
- Either manually void/delete in Xero UI using the CSV as reference
- Or accountant may have bulk cleanup tools for imported duplicates

## Status
- All other Owner Funds reclassification completed successfully
- Entertainment (420) and Motor Vehicle (449) left for accountant review
- Duplicates are the only outstanding cleanup item
