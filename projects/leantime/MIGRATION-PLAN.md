# Leantime Migration Plan

**Date:** 26 February 2026  
**Goal:** Migrate all dashboard projects into Leantime for better task management

---

## Projects to Migrate (7 total)

### 1. OAuth & Automation Setup (NEW - Priority 1)
**Status:** In progress  
**Priority:** CRITICAL

**Tasks:**
- [x] Analyze OAuth blockers
- [x] Create workflow proposal
- [ ] Set up Gmail OAuth (in progress with Morgan)
- [ ] Set up Sheets OAuth
- [ ] Set up Calendar OAuth
- [ ] Set up Drive OAuth
- [ ] Test all OAuth flows
- [ ] Update workflows to use OAuth APIs

**Blockers:** Waiting for Morgan to download Google Cloud credentials

**Due date:** Today (26 Feb)

---

### 2. Health & Fitness Agent
**Status:** Phase 0 - Baseline Assessment  
**Priority:** HIGH

**Milestones:**
- [x] GP appointment booked
- [x] GP appointment completed (26 Feb, 11:15 AM)
- [x] Specialist referrals received (3)
- [x] Cardiology booked (9 Mar, 1:55 PM)
- [x] ENT booked (17 Mar, 11:10 AM)
- [ ] Complete gastro email form (URGENT)
- [ ] Book blood work (4Cyte, fasting)
- [ ] Baseline measurements
- [ ] Create baseline.json

**Tasks (Phase 1 - after baseline):**
- [ ] Set up food tracking (photo → calorie analysis)
- [ ] Set up spending tracker
- [ ] Set up movement reminders (pushups, water, walks)
- [ ] Build check-in system
- [ ] Weekly progress reports

**Upcoming appointments:**
- 9 Mar, 1:55 PM - Cardiology (Advara HeartCare, Milton)
- 17 Mar, 11:10 AM - ENT Specialist (One Health Albion)

**Dependencies:** OAuth (for automated reminders)

---

### 3. Xero Accounting Cleanup
**Status:** 67% complete, awaiting categorization  
**Priority:** HIGH

**Done:**
- [x] Owner Funds reclassified (272 txns, $156K)
- [x] LOLD main reconciliation (34 txns processed)
- [x] Wise account imported (1,907 txns)
- [x] Entertainment classified (317 txns)
- [x] Motor Vehicle classified (53 txns)
- [x] Accountant notes prepared
- [x] Receipt workflow built
- [x] Money IN categorized (436 txns, $198K)
- [x] Money OUT coded (1,090 of 1,634 txns)
- [x] Exported 395 unmatched for review

**Pending:**
- [ ] Morgan: Categorize 395 unmatched transactions
- [ ] Merge CREDITS + DEBITS CSVs
- [ ] Validate totals against control baseline
- [ ] Import to Xero
- [ ] Wise duplicate cleanup (~370 duplicates)
- [ ] LOLD main: 62 transfers remaining
- [ ] PayPal handling (Jason to advise)

**Blockers:**
- OAuth (can't auto-import CSV to Sheets)
- Morgan's categorization work (395 txns)

**Dependencies:** OAuth (Sheets)

---

### 4. Ecommerce JV
**Status:** Early planning  
**Priority:** MEDIUM

**Done:**
- [x] Blueprint drafted
- [x] Partnership identified (ex-colleague)
- [x] Business model defined (China → AU → 3PL → Shopify)
- [x] Budget set ($20K AUD, accessories first)

**Next:**
- [ ] Partnership agreement draft
- [ ] First product selection
- [ ] Supplier research (China)
- [ ] 3PL evaluation (AU warehouses)
- [ ] Shopify store setup
- [ ] Automation stack planning

**Dependencies:** None (can progress independently)

---

### 5. Project Dashboard / PM Tool
**Status:** Phase 1 live, migrating to Leantime  
**Priority:** MEDIUM

**Done:**
- [x] Local dashboard built (localhost:3333)
- [x] Auto-refresh (30s)
- [x] GitHub repo created
- [x] Docker installed
- [x] Leantime deployed (localhost:8080)

**Next:**
- [ ] Get Leantime admin credentials
- [ ] Set up API token
- [ ] Migrate projects to Leantime (this plan!)
- [ ] Build API integration (conversation → tasks)
- [ ] Convert dashboard to read-only view (pulls from Leantime)

**Dependencies:** OAuth (optional, for Calendar sync)

---

### 6. Task Copilot (Voice + Mobile Assistant)
**Status:** Phase 1 LIVE  
**Priority:** MEDIUM

**Done:**
- [x] Full project brief created
- [x] Phase 1 launched (24 Feb)
- [x] Morning briefings (8 AM daily)
- [x] Evening recaps (6 PM daily)
- [x] Task capture ("task: [description]")

**Next:**
- [ ] Integrate with Leantime (pull priorities)
- [ ] Build sub-agent
- [ ] Voice interface (Phase 3)
- [ ] Smart scheduling (Phase 4)

**Dependencies:** Leantime API

---

### 7. Headwear Sample Range
**Status:** Planning  
**Priority:** LOW

**Done:**
- [x] Range plan template created

**Next:**
- [ ] Define shapes (4-5 styles)
- [ ] Define colorways (2-4 per shape)
- [ ] Source materials
- [ ] Production schedule
- [ ] Set deadline

**Dependencies:** None

---

## Migration Execution Steps

**Once we have Leantime access:**

1. **Create Projects** (7 total)
   - OAuth & Automation Setup
   - Health & Fitness Agent
   - Xero Accounting Cleanup
   - Ecommerce JV
   - Project Dashboard / PM Tool
   - Task Copilot
   - Headwear Sample Range

2. **Add Tasks** (from above lists)
   - Mark completed tasks as done
   - Set priorities (CRITICAL, HIGH, MEDIUM, LOW)
   - Set due dates where known
   - Add dependencies/blockers

3. **Set Up Views**
   - Today view (due today)
   - This week view
   - Priority view (all CRITICAL/HIGH tasks)
   - Blocked view (tasks with blockers)

4. **Test API Integration**
   - Create task via API
   - Update task status
   - Read tasks for morning briefing

5. **Update Dashboard**
   - Convert to read from Leantime API
   - Remove manual update code
   - Keep 30s auto-refresh

---

## API Integration Requirements

**Morning Briefing (8 AM):**
```
GET /api/v1/tasks?status=open&priority=high,critical&due<=today+2days
→ Pull top 3 priorities
→ Format into WhatsApp message
```

**Task Creation (conversational):**
```
POST /api/v1/tasks
{
  "title": "Call ENT clinic",
  "project": "Health & Fitness Agent",
  "due_date": "2026-02-27",
  "priority": "high"
}
```

**Evening Recap (6 PM):**
```
GET /api/v1/tasks?status=completed&updated>=today
→ Pull completed tasks
→ Celebrate wins
```

---

## Next Steps

1. ✅ Create this migration plan
2. ⏳ Wait for OAuth setup to complete
3. ⏳ Access Leantime, get API token
4. ⏳ Execute migration (create projects + tasks)
5. ⏳ Test API integration
6. ⏳ Update morning briefing to pull from Leantime

**Estimated time:** 30-45 minutes after OAuth is done

---

*Ready to execute once Morgan completes OAuth setup!*
