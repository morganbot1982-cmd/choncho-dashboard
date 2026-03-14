# Xero Integration Reference

## Overview

**Service:** Xero Accounting API  
**Version:** api.xro/2.0  
**Auth:** OAuth 2.0 (authorization_code grant)  
**Base URL:** https://api.xero.com/api.xro/2.0/  
**Rate Limits:** 60 calls/minute per app  
**Credential Storage:** `agents/accountant/config/xero_credentials.json` and `xero_tokens.json`

## OAuth 2.0 Flow

### Setup (One-time)

1. Create app at https://developer.xero.com/app/manage
2. Set redirect URI: `http://localhost:3000/callback` (or your callback URL)
3. Note Client ID and Client Secret
4. Store in `xero_credentials.json`:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "redirect_uri": "http://localhost:3000/callback"
}
```

### Authorization Flow

```
1. User clicks authorize → redirected to Xero login
2. User approves scopes
3. Xero redirects back with authorization code
4. Exchange code for access + refresh tokens
5. Store tokens in xero_tokens.json
```

### Token Refresh (Every 30 Minutes)

**Access tokens expire after 30 minutes.** You MUST refresh them.

```http
POST https://identity.xero.com/connect/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {{base64(client_id:client_secret)}}

grant_type=refresh_token&refresh_token={{REFRESH_TOKEN}}
```

**Response:**
```json
{
  "access_token": "new_token",
  "expires_in": 1800,
  "token_type": "Bearer",
  "refresh_token": "new_refresh_token"
}
```

**⚠️ Important:** Refresh token also rotates! Always save the new one.

### Tenant ID

Xero uses "tenants" (organizations). After getting access token, fetch tenant ID:

```http
GET https://api.xero.com/connections
Authorization: Bearer {{ACCESS_TOKEN}}
```

**Response:**
```json
[
  {
    "id": "tenant-uuid-here",
    "tenantId": "tenant-uuid-here",
    "tenantType": "ORGANISATION",
    "tenantName": "Leif Oh Leif Distribution Pty Ltd",
    ...
  }
]
```

**Every API call requires:**
- `Authorization: Bearer {{ACCESS_TOKEN}}`
- `Xero-Tenant-Id: {{TENANT_ID}}`

## Common API Operations

### Get Chart of Accounts

```http
GET /api.xro/2.0/Accounts
Headers:
  Authorization: Bearer {{TOKEN}}
  Xero-Tenant-Id: {{TENANT_ID}}
  Accept: application/json
```

### Get Bank Transactions

```http
GET /api.xro/2.0/BankTransactions?page=1
Headers:
  Authorization: Bearer {{TOKEN}}
  Xero-Tenant-Id: {{TENANT_ID}}
```

**Pagination:** Xero returns 100 records per page. Use `?page=2`, `?page=3`, etc.

### Create Bank Transaction

```http
POST /api.xro/2.0/BankTransactions
Headers:
  Authorization: Bearer {{TOKEN}}
  Xero-Tenant-Id: {{TENANT_ID}}
  Content-Type: application/json

{
  "BankTransactions": [
    {
      "Type": "RECEIVE",
      "Contact": {
        "Name": "Customer Name"
      },
      "LineItems": [
        {
          "Description": "Payment received",
          "Quantity": 1,
          "UnitAmount": 100.00,
          "AccountCode": "200",
          "TaxType": "OUTPUT"
        }
      ],
      "BankAccount": {
        "AccountID": "bank-account-uuid"
      },
      "Date": "2026-02-27"
    }
  ]
}
```

### Update Bank Transaction

```http
POST /api.xro/2.0/BankTransactions
Headers: (same as above)

{
  "BankTransactions": [
    {
      "BankTransactionID": "existing-uuid",
      "Contact": {
        "Name": "Updated Name"
      }
    }
  ]
}
```

**⚠️ Critical Constraint:** You **cannot** modify reconciled transactions via API.

## Known Issues & Gotchas

### 1. Reconciled Transactions Are Protected

**Error:**
```
"This Bank Transaction cannot be edited as it has been reconciled with a Bank Statement."
```

**Cause:** Transaction is bank-statement-reconciled (matched against imported CSV statement).

**Fix:** Transactions must be un-reconciled in UI first, then you can modify via API.

**Workaround:** For bulk changes, consider creating new transactions instead of modifying existing.

### 2. Tax Types Depend on Account Defaults

**Problem:** Bank transactions don't always accept explicit `TaxType` in API.

**Solution:** Omit `TaxType` from bank transaction payloads. Xero uses the account's default tax setting.

### 3. Multiple Accounts with Similar Names

**Problem:** Easy to import to wrong account if you search by name.

**Example:** "Wise AUD" vs "Wise - Full Import" (both exist, different IDs).

**Fix:** Always use `AccountID` (UUID), not account name. Verify ID before bulk operations.

### 4. Deleted Transactions Still Appear in API

**Status:** `"Status": "DELETED"`

**Problem:** Can't modify deleted transactions, but they still return in API queries.

**Filter:** Check `Status != "DELETED"` when processing.

### 5. Rate Limiting

**Limit:** 60 calls per minute per app.

**Headers on rate limit:**
```
X-Rate-Limit-Problem: minute
Retry-After: 60
```

**Fix:** Implement exponential backoff. Sleep for `Retry-After` seconds.

## Account Structure (Leif Oh Leif Distribution)

### Key Accounts (from Chart)

| Code | Name | Type | Tax Default |
|------|------|------|-------------|
| 200 | Sales | Revenue | OUTPUT (GST on Income) |
| 255 | Rent Received | Revenue | EXEMPTOUTPUT (GST Free) |
| 265 | Other Revenue | Revenue | OUTPUT |
| 310 | Owner Drawings | Equity | NONE |
| 404 | General Expenses | Expense | INPUT (GST on Expenses) |
| 420 | Entertainment | Expense | NONE (Non-deductible) |
| 421 | Freight & Courier | Expense | INPUT |
| 429 | General Expenses | Expense | INPUT |
| 880 | Cost of Sales | Expense | INPUT |

### Bank Accounts

| Name | AccountID | Notes |
|------|-----------|-------|
| Wise AUD | `10142dd5-d7b0-4f95-9ab0-7e5e5a1baa7e` | ✅ CORRECT account |
| Wise - Full Import | `01aab634-157c-4992-8c11-2f14724d7191` | ❌ OLD/WRONG account |
| LOLD Bank Account | `4b9e4922-84d1-4d4b-9c69-b7909a43de4a` | Current account |

**Always use the correct Wise AUD ID for new imports.**

## Debugging Checklist

When Xero API isn't working:

```
□ Access token expired? (refresh every 30 min)
□ Refresh token rotated? (save new one after each refresh)
□ Tenant ID correct? (fetch from /connections)
□ Rate limit hit? (check X-Rate-Limit headers)
□ Transaction reconciled? (can't modify if reconciled)
□ Account ID correct? (not name - use UUID)
□ TaxType causing issues? (try omitting it for bank transactions)
```

## Validation Queries

**Check account exists:**
```http
GET /api.xro/2.0/Accounts/{{ACCOUNT_ID}}
```

**Check transaction count in account:**
```http
GET /api.xro/2.0/BankTransactions?where=BankAccount.AccountID==Guid("{{ACCOUNT_ID}}")&page=1
```

**Check for reconciled transactions:**
```http
GET /api.xro/2.0/BankTransactions?where=IsReconciled==true&page=1
```

## Common Error Codes

| Code | Error | Cause | Fix |
|------|-------|-------|-----|
| 401 | Unauthorized | Token expired | Refresh access token |
| 403 | Forbidden | Wrong tenant or permissions | Check Xero-Tenant-Id header |
| 404 | Not Found | Wrong endpoint or resource ID | Verify URL and IDs |
| 400 | Validation Exception | Bad payload or constraint violation | Check error `Elements[].ValidationErrors` |
| 429 | Too Many Requests | Rate limited | Wait for Retry-After seconds |

## Token Storage

**Location:** `agents/accountant/config/xero_tokens.json`

**Structure:**
```json
{
  "access_token": "eyJh...",
  "expires_in": 1800,
  "token_type": "Bearer",
  "refresh_token": "abc123...",
  "id_token": "...",
  "scope": "openid profile email accounting.transactions ..."
}
```

**Security:** This file contains live credentials. Never log or commit it.

## Rollback / Re-auth

**If tokens are corrupted:**
1. Delete `xero_tokens.json`
2. Re-run OAuth authorization flow
3. User re-approves in browser
4. New tokens saved

**If credentials are wrong:**
1. Regenerate Client Secret in Xero developer portal
2. Update `xero_credentials.json`
3. Delete `xero_tokens.json`
4. Re-authorize

## Migration Notes (Feb 26-27, 2026)

**Wise Import:**
- 2,070 transactions imported to Wise AUD account
- 80% coded with account codes
- 20% defaulted to General Expenses (429)
- Duplicates identified in old "Wise - Full Import" account (to be cleaned later)

**Tax Fixes:**
- Attempted to change "webstore sales" contact → blocked (reconciled)
- Attempted to fix Rent Received tax types → blocked (reconciled + deleted status)
