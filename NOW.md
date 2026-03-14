# NOW - Current Focus (Updated: 26 Feb 2026, 3:59 PM)

## 🎯 Top Priority: OAuth & Automation Setup

**Why:** Multiple projects blocked by missing OAuth integrations. Gmail/Sheets automation hitting bot detection. Need to fix foundation before scaling up.

**Critical blockers:**
1. Gmail OAuth (no API access - browser automation unreliable)
2. Google Sheets OAuth (same issue)
3. Google Calendar (working via AppleScript, but OAuth would be cleaner)

**Impact:**
- Can't reliably create email drafts
- Can't automate spreadsheet imports/exports
- Health tracking, Xero workflows, task management all affected

---

## 📋 Active Projects

### Health & Fitness Agent (Phase 0 - Baseline)
**Status:** GP completed, 2 appointments booked, 2 pending

**Done today:**
- ✅ GP appointment completed (11:15 AM)
- ✅ 3 specialist referrals received
- ✅ Cardiology booked (9 Mar, 1:55 PM, Milton)
- ✅ ENT booked (17 Mar, 11:10 AM, One Health Albion)
- ✅ All materials organized in project folder

**Pending:**
- ⚠️ Complete gastro email form (urgent)
- Book blood work (4Cyte walk-in, fasting)

**Next:** After OAuth fixed, automate appointment reminders

---

### Xero Accounting Cleanup
**Status:** 67% coded, awaiting Morgan's categorization

**Done:**
- ✅ Money IN: 436 transactions fully categorized
- ✅ Money OUT: 1,090 of 1,634 coded (67%)
- ✅ Exported 395 unmatched for manual review

**Blocked by:**
- Morgan needs to categorize 395 transactions in spreadsheet
- **OAuth blocker:** Can't auto-import to Google Sheets without OAuth

**Next:** Merge CREDITS + DEBITS → validate → import to Xero

---

### Task Management Migration (Dashboard → Leantime)
**Status:** Need to populate Leantime with current work

**Current:**
- ✅ Dashboard running (localhost:3333)
- ✅ Leantime deployed (localhost:8080)
- Tracking 7 active projects in dashboard

**Next:**
- Migrate projects from dashboard to Leantime
- Set up Leantime API integration for auto-updates
- **OAuth blocker:** Leantime may need API tokens for automation

---

### OpenClaw Setup & Security
**Done today:**
- ✅ Browser automation fixed (defaultProfile="openclaw")
- ✅ Security audit: All critical warnings resolved
- ✅ Telegram DMs closed (allowlist)
- ✅ Credentials directory permissions fixed
- ✅ DM session isolation enabled

**Remaining:**
- OAuth setup (Gmail, Sheets, Calendar)
- Create Matt Roach OpenClaw setup guide

---

## 🚧 Blockers

**Critical:**
1. **OAuth not set up** - Gmail, Sheets, Calendar all need OAuth
   - Impact: Can't automate emails, spreadsheets, calendar entries reliably
   - Browser automation hits bot detection after 1-2 actions
   
**High:**
2. **Wise categorization** - 395 transactions waiting for Morgan
   - Impact: Can't complete Xero import until done
   
3. **Leantime migration** - Need to populate from dashboard
   - Impact: Harder to track tasks, losing visibility

---

## 📅 Upcoming

**This week:**
- Set up OAuth (Gmail, Sheets) - **PRIORITY**
- Morgan: Categorize 395 Wise transactions
- Populate Leantime with current projects
- Create workflow for morning/evening briefings → Leantime tasks

**Next week:**
- Monday 9 Mar, 1:55 PM - Cardiology appointment
- Friday 17 Mar, 11:10 AM - ENT appointment

---

## 💡 Workflow Improvement Ideas

**What's working:**
- Morning/evening prompts (keep this!)
- WhatsApp reminders
- Dashboard visibility

**What needs fixing:**
- Too many tracking systems (dashboard, NOW.md, memory files, Leantime)
- No automated task creation from conversations
- Can't sync calendar/tasks bidirectionally

**Proposed:**
- OAuth → enables automated email, sheets, calendar
- Leantime as single source of truth for tasks
- Morning briefing pulls from Leantime
- Conversations auto-create Leantime tasks via API
- Dashboard becomes read-only view of Leantime data
