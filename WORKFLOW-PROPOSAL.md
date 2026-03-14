# Workflow Improvement Proposal

**Date:** 26 February 2026  
**Goal:** Build on what's working (prompting system), reduce friction, keep you moving forward

---

## ✅ What's Working Now

**Morning/Evening Prompts (Task Copilot):**
- 8 AM: Top 3 priorities + blockers
- 6 PM: Wins recap + what's blocking tomorrow
- **You like this!** It keeps you on track without overwhelming you

**WhatsApp Communication:**
- Two-way messaging works great
- Immediate, mobile-friendly
- Background work notifications

**Dashboard Visibility:**
- See all projects at a glance
- Track progress over time
- Quick status checks

---

## ❌ What's Not Working

**Too many systems:**
- Dashboard (localhost:3333)
- NOW.md
- Memory files (daily notes)
- Leantime (not populated yet)
- **Result:** Hard to know "what's the source of truth?"

**Manual tracking:**
- You have to remember to update files
- I can't auto-create tasks from our conversations
- No bidirectional sync (calendar ↔ tasks ↔ briefings)

**OAuth blockers:**
- Can't reliably automate emails, sheets, calendar
- Hitting bot detection constantly
- Adds friction to every workflow

---

## 🎯 Proposed Workflow (Builds on What Works)

### Core Principle
**"You talk, I track. I prompt, you act."**

- You focus on the work
- I handle the tracking, organizing, reminding
- Morning/evening prompts guide your day
- Leantime becomes single source of truth

---

### Morning Routine (Automated - 8 AM)

**WhatsApp message from Choncho:**

```
🦬 Good morning Morgan!

📅 Today: Thursday, 27 Feb 2026

🎯 Top 3 Priorities:
1. Complete gastro email form (urgent)
2. Categorize 395 Wise transactions in spreadsheet
3. Set up Gmail OAuth (20 mins - unblocks email automation)

📆 Calendar:
- No appointments today

🚧 Blockers from yesterday:
- OAuth not set up (affects 4 projects)

Choose a number (1-3) or say "something else"
```

**How it works:**
- Pulls from Leantime tasks (priority order)
- Includes today's calendar (after OAuth setup)
- Highlights blockers
- Conversational, not overwhelming

---

### During the Day (Conversational Task Capture)

**You say (in chat):**
> "Remind me to call ENT clinic tomorrow"

**I automatically:**
1. Create Leantime task: "Call ENT clinic"
2. Set due date: Tomorrow
3. Add to calendar reminder (after OAuth)
4. Confirm: "✅ Added to tomorrow's tasks"

**You say:**
> "I finished categorizing the Wise transactions"

**I automatically:**
1. Mark Leantime task as complete
2. Update dashboard
3. Check if anything was blocking on this
4. Prompt next action: "Great! Ready to merge and import to Xero?"

**No manual tracking needed.** Just talk naturally.

---

### Evening Recap (Automated - 6 PM)

**WhatsApp message from Choncho:**

```
🦬 Evening recap!

✅ Today's wins:
- Completed gastro email form
- Categorized 395 Wise transactions
- 2/3 priorities done

⏳ Still pending:
- Gmail OAuth setup (20 mins)

📋 Tomorrow's top 3:
1. Set up Gmail OAuth (carry-over)
2. Merge Wise CREDITS + DEBITS
3. Import to Xero

🌟 Momentum: 2-day streak of hitting 2+ priorities!

Anything blocking tomorrow?
```

**How it works:**
- Summarizes completed tasks from Leantime
- Celebrates progress (no shame for incomplete)
- Sets up tomorrow
- Encourages check-in on blockers

---

### Workflow Components

#### 1. Leantime = Single Source of Truth

**Why Leantime:**
- Proper task management (due dates, priorities, projects)
- Can access from anywhere (web UI)
- API for automation
- Better than scattered markdown files

**How we populate it:**
- I migrate current dashboard projects → Leantime projects
- Each project gets tasks from its README checklist
- Ongoing: Conversations auto-create tasks

**You can:**
- View in Leantime UI when you want
- Or just rely on my morning/evening prompts
- Both stay in sync via API

#### 2. Dashboard = Read-Only View

**Current dashboard (localhost:3333) becomes:**
- Read-only summary of Leantime data
- High-level project status
- No manual updates needed
- Auto-refreshes from Leantime API

**Benefit:** You get visibility without maintenance burden

#### 3. Conversational Task Management

**Keywords I listen for:**
- "Remind me to [X]" → Create task
- "I finished [X]" → Mark complete
- "Block this on [X]" → Add blocker dependency
- "Priority: [X]" → Adjust priority

**I handle:**
- Creating tasks in Leantime
- Setting due dates
- Tracking blockers
- Updating status

**You just talk naturally.**

#### 4. OAuth-Powered Automation

**After OAuth setup:**
- Calendar ↔ Leantime sync (tasks with due dates → calendar events)
- Email drafts created via API (no bot detection)
- Spreadsheets auto-populated (no manual CSV imports)
- Morning briefing includes calendar + tasks

**Everything flows seamlessly.**

---

## 🚀 Migration Plan (Dashboard → Leantime)

### Phase 1: Initial Population (30 mins)

**I do this once:**

For each project on dashboard:
1. Create Leantime project
2. Migrate tasks from project README checklists
3. Set priorities based on current status
4. Link blockers (e.g., "Xero import" blocked by "Wise categorization")

**Projects to migrate:**
1. Xero Accounting Cleanup
2. Health & Fitness Agent
3. Ecommerce JV
4. Task Copilot
5. Headwear Sample Range
6. OpenClaw Setup
7. OAuth Setup (new project!)

### Phase 2: Daily Sync (Automated)

**Every morning/evening:**
- I query Leantime API for tasks
- Generate morning briefing from task list
- Update dashboard from Leantime data
- No manual work needed

### Phase 3: Conversational Integration (Ongoing)

**As we work:**
- You mention tasks → I add to Leantime
- You complete work → I update status
- Blockers arise → I track dependencies

**Seamless, no friction.**

---

## 📊 Example: How It Flows

**Morning (8 AM):**
```
🦬 Good morning!

🎯 Top 3 today:
1. Gmail OAuth setup (20 mins)
2. Categorize Wise transactions
3. Call ENT clinic

Choose 1-3 or "something else"
```

**You say:** "Let's do #1"

**I respond:**
```
✅ Starting OAuth setup

I'll guide you through:
1. Download credentials from Google Cloud Console
2. Run gog auth commands (I'll provide exact commands)
3. Test Gmail/Sheets/Calendar

Ready? I'll share the first step.
```

**During work (you say):** "Remind me to review accountant notes tomorrow"

**I respond:**
```
✅ Added to tomorrow:
- Review accountant notes (Xero project)

Anything else?
```

**Evening (6 PM):**
```
🦬 Evening recap!

✅ Today:
- Gmail OAuth setup complete! 🎉
- Can now automate emails, sheets, calendar

📋 Tomorrow:
1. Review accountant notes
2. Categorize Wise transactions
3. Call ENT clinic

2-day streak of hitting priorities! 🔥
```

---

## 🎯 What You Need to Do

**One-time setup (this week):**
1. **Gmail OAuth** (20 mins) - I guide you through it
2. **Leantime population** (I do this, 30 mins) - You just review/approve

**Ongoing (zero effort):**
- Talk to me naturally about tasks
- Respond to morning prompts (pick 1-3)
- Optional: Check Leantime UI when you want full view

**That's it.** I handle the rest.

---

## 💡 Key Benefits

**For you:**
- ✅ Clear daily priorities (no decision fatigue)
- ✅ No manual tracking (I handle it all)
- ✅ Mobile-friendly (WhatsApp prompts)
- ✅ Flexible (Leantime UI available when needed)
- ✅ Momentum tracking (streaks, wins, progress)

**For projects:**
- ✅ Single source of truth (Leantime)
- ✅ Automatic updates (no stale data)
- ✅ Blocker visibility (know what's stuck)
- ✅ Progress tracking (dashboard shows trends)

**For automation:**
- ✅ Reliable email/sheets/calendar (OAuth)
- ✅ Conversational task creation
- ✅ Seamless workflows (talk → I execute)

---

## ⏱️ Timeline

**Today (remaining time):**
- Update dashboard with today's progress ✅ (done)
- Create OAuth blocker analysis ✅ (done)
- Create this workflow proposal ✅ (done)

**Tomorrow (or next session):**
- Set up Gmail OAuth (20 mins) - **Priority 1**
- Populate Leantime from dashboard (30 mins) - I do this
- Test morning briefing with Leantime integration

**Next week:**
- Refine prompts based on what works
- Add calendar sync
- Build out conversational task capture

---

## 🤔 Your Decision

**Option 1: Go all-in (Recommended)**
- Set up OAuth today (20 mins)
- I populate Leantime this evening
- Start fresh tomorrow with new workflow

**Option 2: OAuth first, Leantime later**
- Set up OAuth today (20 mins)
- Keep using dashboard for now
- Migrate to Leantime next week

**Option 3: Leantime first, OAuth later**
- I populate Leantime now
- Manual workflows for now
- OAuth when we hit friction

**My recommendation:** Option 1  
**Why:** Fixes foundation (OAuth) + sets up better tracking (Leantime) in one shot. Then we're unblocked and can move fast.

---

What do you want to tackle first? 🦬
