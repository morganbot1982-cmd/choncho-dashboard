# OAuth & Automation Blockers Analysis

**Date:** 26 February 2026  
**Purpose:** Identify and resolve all OAuth/automation blockers across projects

---

## 🚨 Critical Blockers (Blocking Multiple Projects)

### 1. Gmail OAuth - NOT SET UP ❌

**Impact:** HIGH - Affects 4 projects

**Current state:**
- Using browser automation (hits bot detection after 1-2 actions)
- Can't reliably create email drafts
- Failed to create 2nd/3rd GP referral emails today (bot detection)

**Affected projects:**
- Health & Fitness (appointment booking emails, reminders)
- Xero Accounting (receipt forwarding, accountant communication)
- Task Copilot (email-based task capture)
- OpenClaw Setup (Matt Roach guide delivery)

**What we need:**
- Google Cloud Console OAuth credentials
- `gog` CLI authenticated with Gmail API scopes
- Service: `gmail` (read, send, drafts, labels)

**Fix steps:**
1. Download OAuth credentials from Google Cloud Console
2. Run: `gog auth credentials <credentials.json>`
3. Run: `gog auth add morganbot1982@gmail.com --services gmail`
4. Test: Create draft email via API
5. Update workflows to use `gog gmail draft create` instead of browser

**Time estimate:** 10-15 minutes

---

### 2. Google Sheets OAuth - NOT SET UP ❌

**Impact:** HIGH - Affects 3 projects

**Current state:**
- Can't auto-import CSV to Sheets
- Manual drag/drop required (friction)
- Today: Asked Morgan to manually import Wise categorization CSV

**Affected projects:**
- Xero Accounting (categorization spreadsheets, reconciliation tracking)
- Health & Fitness (food tracking, spending logs, health data)
- Task Copilot (task tracking, project dashboard data)

**What we need:**
- Same OAuth credentials as Gmail (Google Workspace)
- `gog` authenticated with Sheets API scopes
- Service: `sheets` (read, write, create)

**Fix steps:**
1. Use same OAuth credentials from Gmail setup
2. Run: `gog auth add morganbot1982@gmail.com --services sheets` (if not already done)
3. Test: Create new sheet, import CSV
4. Update workflows to use `gog sheets import` instead of browser

**Time estimate:** 5 minutes (if Gmail OAuth already done)

---

### 3. Google Calendar OAuth - WORKING VIA APPLESCRIPT ⚠️

**Impact:** MEDIUM - Works but suboptimal

**Current state:**
- Using AppleScript to add events to Calendar.app
- Works reliably but limited (can't read events, check conflicts, etc.)
- Can add events but can't query calendar for briefings

**Affected projects:**
- Health & Fitness (appointment reminders)
- Task Copilot (morning briefings with today's schedule)
- All projects (event scheduling)

**What we need:**
- Same OAuth as above
- Service: `calendar` (read, write, events)

**Fix steps:**
1. Run: `gog auth add morganbot1982@gmail.com --services calendar`
2. Test: Read today's events
3. Test: Create event via API
4. Update morning briefing to include calendar events

**Time estimate:** 5 minutes (if Gmail OAuth already done)

**Benefits:**
- Read calendar for morning briefings
- Check for conflicts before booking
- Update/delete events (not just create)
- Set reminders programmatically

---

## 🟡 Medium Priority (Project-Specific)

### 4. Google Drive OAuth - NOT SET UP ⚠️

**Impact:** MEDIUM - Nice to have

**Current state:**
- No access to Google Drive via API
- Can't auto-upload files, create folders, share documents

**Potential use cases:**
- Health & Fitness: Store baseline photos, blood work results
- Xero Accounting: Backup receipts, financial documents
- All projects: Automated backups, file organization

**Fix steps:**
1. Run: `gog auth add morganbot1982@gmail.com --services drive`
2. Test: Upload file, create folder

**Time estimate:** 5 minutes (if Gmail OAuth already done)

---

### 5. Xero OAuth - ✅ WORKING

**Status:** DONE - No blocker

**Current state:**
- OAuth2 authenticated
- Read/write access to accounts, transactions, contacts
- Used successfully for Xero cleanup work

**No action needed.**

---

### 6. Leantime API Access - NOT CONFIGURED ❌

**Impact:** MEDIUM - Blocks task automation

**Current state:**
- Leantime deployed (localhost:8080)
- No API integration yet
- Can't auto-create/update tasks from conversations

**What we need:**
- Leantime API token/credentials
- Test API endpoints (create task, update task, get projects)
- Build integration: conversation → Leantime task

**Fix steps:**
1. Log into Leantime, generate API token
2. Test API with curl/Postman
3. Build integration script
4. Test: Create task from chat message

**Time estimate:** 30-45 minutes

---

## 🟢 Working / No Blocker

### 7. WhatsApp - ✅ WORKING
- Two-way messaging
- Photo upload (receipt workflow)
- Reliable delivery

### 8. Browser Automation (openclaw profile) - ✅ WORKING
- Fixed today (defaultProfile="openclaw")
- Direct CDP control
- Limited use (bot detection for Gmail/Sheets)

---

## 📋 Recommended Fix Order

**Priority 1: Core Google Services (30 mins total)**
1. Gmail OAuth (15 min) - Unblocks email automation
2. Sheets OAuth (5 min) - Unblocks data workflows
3. Calendar OAuth (5 min) - Enhances briefings
4. Drive OAuth (5 min) - Nice to have

**Priority 2: Task Management (45 mins)**
5. Leantime API setup (45 min) - Unblocks task automation

**Priority 3: Testing & Integration (1-2 hours)**
6. Test all OAuth flows end-to-end
7. Update existing workflows to use OAuth instead of browser
8. Document for future reference

---

## 🎯 Master OAuth Setup Checklist

**Prerequisites:**
- [ ] Google Cloud Console project exists
- [ ] OAuth credentials downloaded (credentials.json)
- [ ] `gog` CLI installed (should already be via Homebrew)

**Setup:**
- [ ] Run: `gog auth credentials <path-to-credentials.json>`
- [ ] Run: `gog auth add morganbot1982@gmail.com --services gmail,calendar,sheets,drive`
- [ ] Complete OAuth flow in browser (Morgan logs in, grants permissions)
- [ ] Verify: `gog auth status` shows all services authenticated

**Test:**
- [ ] Gmail: Create draft email via `gog gmail draft create`
- [ ] Calendar: Read today's events via `gog calendar events today`
- [ ] Sheets: Create new sheet via `gog sheets create`
- [ ] Drive: List files via `gog drive list`

**Integration:**
- [ ] Update AGENTS.md with OAuth workflow instructions
- [ ] Update email draft creation to use Gmail API
- [ ] Update calendar entries to use Calendar API (optional, AppleScript works)
- [ ] Update CSV imports to use Sheets API

---

## 💡 Workflow Improvements After OAuth

**Current pain points:**
1. Can't create reliable email drafts (browser bot detection)
2. Manual CSV imports (Morgan has to drag/drop)
3. Can't read calendar for briefings
4. No automated file backups

**After OAuth:**
1. ✅ Create email drafts via API (reliable, fast)
2. ✅ Auto-import CSVs to Sheets (one command)
3. ✅ Morning briefings include today's calendar
4. ✅ Auto-backup important files to Drive
5. ✅ Leantime tasks auto-created from conversations

---

## ⏱️ Total Time Estimate

**Minimum (Gmail + Sheets only):** 20 minutes  
**Recommended (Gmail + Sheets + Calendar + Drive):** 35 minutes  
**Full setup (+ Leantime API):** 80 minutes (1hr 20min)

**Benefit:** Unblocks 4 major projects, enables reliable automation

---

## 🚀 Next Steps

**Morgan's decision:**
1. Quick fix (Gmail + Sheets only) - 20 minutes
2. Full Google OAuth (Gmail + Sheets + Calendar + Drive) - 35 minutes
3. Complete setup (Google + Leantime) - 80 minutes

**My recommendation:** Option 2 (Full Google OAuth, 35 mins)  
**Why:** Unblocks most work, sets foundation for all future automation, worth the investment now vs. piecemeal later.

After OAuth is set up, we can:
- Reliably automate emails (GP bookings, Matt guide)
- Import Wise categorization to Sheets with one command
- Include calendar in morning briefings
- Build Leantime integration at our own pace
