# Google APIs Integration Reference

## Overview

**Services:** Gmail, Calendar, Drive, Sheets  
**Auth:** OAuth 2.0 (web app flow)  
**Scopes:** Per-API, must be enabled individually  
**Console:** https://console.cloud.google.com  
**Credential Storage:** `~/.openclaw/credentials/google/` (for main Choncho) or `agents/accountant/config/` (for accountant)

## OAuth 2.0 Setup

### One-Time Setup (Google Cloud Console)

1. **Create Project**: https://console.cloud.google.com/projectcreate
2. **Enable APIs**: Search for and enable:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Sheets API
3. **Create OAuth Credentials**:
   - APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:3000/oauth/callback` (or your callback)
   - Download JSON (client_secret_*.json)

4. **Add Test Users** (during development):
   - OAuth consent screen → Add test users
   - Add: morganbot1982@gmail.com
   - Test mode allows only listed users to authorize

5. **Store Credentials**:
   - Rename downloaded file to `client_secret.json`
   - Place in credential storage location

### Authorization Flow

```
1. Generate auth URL with required scopes
2. User clicks link → redirected to Google consent screen
3. User approves requested permissions
4. Google redirects back with authorization code
5. Exchange code for access + refresh tokens
6. Store tokens securely
```

### Required Scopes

**Gmail (read/send):**
```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.modify
```

**Calendar (read/write):**
```
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

**Drive (read/write):**
```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/drive.file
```

**Sheets (read/write):**
```
https://www.googleapis.com/auth/spreadsheets
```

**General (user info):**
```
openid
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
```

## Token Refresh

**Access tokens expire after 1 hour.** Refresh tokens last indefinitely (until revoked).

```http
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

client_id={{CLIENT_ID}}&
client_secret={{CLIENT_SECRET}}&
refresh_token={{REFRESH_TOKEN}}&
grant_type=refresh_token
```

**Response:**
```json
{
  "access_token": "ya29.new_token_here",
  "expires_in": 3600,
  "scope": "...",
  "token_type": "Bearer"
}
```

**Unlike Xero:** Refresh token does NOT rotate. You can reuse the same refresh token.

## Common API Operations

### Gmail: List Messages

```http
GET https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=10
Authorization: Bearer {{ACCESS_TOKEN}}
```

### Gmail: Send Message

```http
POST https://gmail.googleapis.com/gmail/v1/users/me/messages/send
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json

{
  "raw": "{{base64url_encoded_mime_message}}"
}
```

**MIME message format:**
```
From: sender@example.com
To: recipient@example.com
Subject: Test Subject

Body content here
```

Base64url encode the entire MIME string.

### Calendar: List Events

```http
GET https://www.googleapis.com/calendar/v3/calendars/primary/events?
  timeMin=2026-02-27T00:00:00Z&
  timeMax=2026-02-28T00:00:00Z&
  singleEvents=true&
  orderBy=startTime
Authorization: Bearer {{ACCESS_TOKEN}}
```

### Calendar: Create Event

```http
POST https://www.googleapis.com/calendar/v3/calendars/primary/events
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json

{
  "summary": "Event Title",
  "description": "Event details",
  "start": {
    "dateTime": "2026-03-01T10:00:00+10:00",
    "timeZone": "Australia/Brisbane"
  },
  "end": {
    "dateTime": "2026-03-01T11:00:00+10:00",
    "timeZone": "Australia/Brisbane"
  }
}
```

### Sheets: Read Range

```http
GET https://sheets.googleapis.com/v4/spreadsheets/{{SPREADSHEET_ID}}/values/Sheet1!A1:Z1000
Authorization: Bearer {{ACCESS_TOKEN}}
```

### Sheets: Write Range

```http
PUT https://sheets.googleapis.com/v4/spreadsheets/{{SPREADSHEET_ID}}/values/Sheet1!A1
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json

{
  "range": "Sheet1!A1",
  "majorDimension": "ROWS",
  "values": [
    ["Header1", "Header2", "Header3"],
    ["Row1Col1", "Row1Col2", "Row1Col3"],
    ["Row2Col1", "Row2Col2", "Row2Col3"]
  ]
}
```

### Sheets: Create Spreadsheet

```http
POST https://sheets.googleapis.com/v4/spreadsheets
Authorization: Bearer {{ACCESS_TOKEN}}
Content-Type: application/json

{
  "properties": {
    "title": "New Spreadsheet"
  }
}
```

**Response includes `spreadsheetId` for future operations.**

## Known Issues & Gotchas

### 1. OAuth Consent Screen Verification

**Problem:** Unverified apps show a scary warning screen.

**During Development:** Add users to test user list. They won't see warning.

**For Production:** Submit app for verification (takes days/weeks).

**Morgan's Setup:** Test mode, morganbot1982@gmail.com added as test user.

### 2. Quota Limits

**Gmail:**
- 1 billion quota units per day
- Sending emails: 100-500 per day (depending on account age)

**Sheets:**
- 300 read requests per minute per project
- 60 write requests per minute per project

**Calendar:**
- 1 million requests per day

**If hit:** HTTP 429 with `Retry-After` header. Implement backoff.

### 3. Token Storage

**Security:** Tokens grant access to Gmail, Calendar, Drive. Treat as passwords.

**Best Practice:**
- Store in `~/.openclaw/credentials/google/tokens.json`
- Permissions: `chmod 600` (read/write for owner only)
- Never log or commit tokens

### 4. Scopes Are Sticky

**Problem:** Changing scopes after initial auth doesn't automatically re-prompt user.

**Fix:** Delete tokens file and re-authorize to request new scopes.

### 5. Calendar Timezone Confusion

**Best Practice:** Always include explicit timezone in dateTime fields.

**Morgan's timezone:** `Australia/Brisbane` (GMT+10, no DST)

**Example:**
```json
"start": {
  "dateTime": "2026-03-01T10:00:00+10:00",
  "timeZone": "Australia/Brisbane"
}
```

## Debugging Checklist

When Google API isn't working:

```
□ Access token expired? (refresh if >1 hour old)
□ API enabled in Google Cloud Console?
□ Scopes match what's needed? (check consent screen + token response)
□ User added to test users? (if app unverified)
□ Quota exceeded? (check error message for quota details)
□ Timezone correct? (use Australia/Brisbane for Morgan)
□ Spreadsheet ID correct? (from URL: /d/{ID}/edit)
```

## Common Error Codes

| Code | Error | Cause | Fix |
|------|-------|-------|-----|
| 401 | Invalid Credentials | Token expired or wrong | Refresh access token |
| 403 | Forbidden / Quota Exceeded | API not enabled or quota hit | Enable API or wait for quota reset |
| 404 | Not Found | Wrong resource ID | Check spreadsheet ID, calendar ID, etc. |
| 400 | Bad Request | Invalid payload | Check required fields, types |
| 429 | Rate Limit Exceeded | Too many requests | Implement exponential backoff |

## Credential Storage

**Main Choncho Location:** `~/.openclaw/credentials/google/`
- `client_secret.json` (OAuth app credentials)
- `tokens.json` (access + refresh tokens)

**Accountant Location:** `agents/accountant/config/`
- `google_credentials.json`
- `google_tokens.json`

**Permissions:** `chmod 700` on directory, `chmod 600` on files.

## Rollback / Re-auth

**If tokens are corrupted:**
1. Delete `tokens.json`
2. Re-run OAuth authorization flow
3. User re-approves in browser (consent screen)
4. New tokens saved

**If credentials are wrong:**
1. Download new `client_secret.json` from Google Cloud Console
2. Replace old file
3. Delete `tokens.json`
4. Re-authorize

## Migration Notes (Feb 26, 2026)

**OAuth Setup Completed:**
- Created OAuth app in Google Cloud Console
- Enabled Gmail, Calendar, Drive, Sheets APIs
- Added morganbot1982@gmail.com as test user
- Completed authorization flow successfully
- Tested: Wise duplicates spreadsheet import (✅ working)

**Result:** Full API access operational. No more bot detection blocks in browser.
