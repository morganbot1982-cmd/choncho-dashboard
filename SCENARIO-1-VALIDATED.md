# 📋 Scenario 1: Work on Existing Project (VALIDATED)

**Status:** Ready for implementation
**Date:** 2026-03-17 4:30 PM

---

## 🎯 GOAL

**Complete seamless continuity across sessions.**

When Morgan says "work on Clarat", agent must know EVERYTHING about the project as if the previous session never ended:
- What was built (code, features, files)
- Why it was built (decisions, tradeoffs)
- What problems were hit (bugs, blockers, failed attempts)
- What was discovered (insights, patterns, gotchas)
- What's working now
- What's broken
- What files changed
- The full development story

**Zero context loss. Zero "where were we" questions.**

---

## 🔄 THE COMPLETE WORKFLOW

### 🎬 STEP 1: TRIGGER

**What Morgan does:**
- Says "work on Clarat" (or any project name)
- OR says "work on proj-11adb2ec" (dashboard ID works too)

**Notes:**
- Dashboard is rarely opened directly
- Chat is where work happens
- Dashboard = brain/status hub, not primary interface

---

### 🧠 STEP 2: RECALL PROCESS (Session Startup Protocol)

**Agent immediately checks these sources (in order):**

#### ✅ MEMORY.md Handoff (auto-loaded)
Location: `~/.openclaw/workspace/MEMORY.md` → `## Project Handoff` section

Reads:
- Dashboard project ID
- Last worked timestamp
- Session key
- Repo path
- Port (if applicable)
- GitHub URL

Example:
```markdown
### Clarat
- **Last worked:** 2026-03-16 11:30 PM
- **Session key:** agent:main:hook:a64fc6a4-def2-4a20-aefe-75a04df8f4ee
- **Dashboard:** proj-11adb2ec → `curl -s http://localhost:3004/api/projects/proj-11adb2ec`
- **Repo:** ~/.openclaw/workspace/clarat
- **GitHub:** https://github.com/morganbot1982-cmd/clarat
- **Port:** 3000
```

#### ✅ Dashboard API Query
Command: `curl -s http://localhost:3004/api/projects/{projectId}`

Gets:
- **Rolling summary** — Current state (what is this, what's done, what's next, what's blocking)
- **Unchecked subtasks** — Specific actionable next steps
- **Memory notes** — Decisions, facts, discoveries
- **Activity log** — Recent changes with timestamps
- **Deliverables** — Pinned specs, reports
- **Files** — Any uploaded documents

#### ✅ Git Status
Commands:
```bash
cd {repo_path}
git status
git log --oneline -5
```

Checks:
- Uncommitted changes?
- Current branch
- Recent commits (last 5)

#### ✅ Dev Server Health
Command: `curl -s http://localhost:{port} -o /dev/null -w '%{http_code}'`

Checks:
- Is server running?
- What port?
- Responds with 200?

#### ✅ Project README
File: `{repo_path}/README.md`

Purpose: Quick reference for "what is this project"

---

#### ❌ EXPLICITLY SKIP (to avoid token bloat)

**These are NOT checked:**
- Session transcript (cron already compressed it into dashboard summary)
- memory/*.md daily session logs (cron already compressed them)
- progress-log.md (cron already compressed it)
- todo.md (project subtasks should be in dashboard, not global todo)
- Project docs/ folder (only check on-demand when asked)

**Why skip:** These are narrative history. The cron job reads them every hour and compresses them into dashboard summary. Reading them again = duplicate work + token bloat.

**Exception:** If dashboard summary is unclear or missing context, agent can read session transcript on-demand.

---

**Agent presents briefing:**
```
📊 Clarat (e-commerce P&L dashboard)

**Current state:**
- 6 pages complete, ClawBoard design applied
- 170 days of real data seeded
- Showcase HTML ready to share

**Unchecked subtasks:**
1. Test showcase with users and gather feedback
2. Decide public demo vs private beta
3. Add export feature

**Git:** Clean working tree, 5 commits ahead
**Server:** Running on localhost:3000 ✅

Which subtask do you want to start on?
```

---

### 🛠️ STEP 3: DURING WORK

**Agent focuses on execution:**
- Does the work
- Uses tools
- Commits when appropriate (manual or when asked)

**Cron job runs hourly as safety net:**

#### What the cron job does:
1. **Lists active sessions** (last 2 hours) via `sessions_list`
2. **Filters** — skips cron/heartbeat/hook sessions, only reads chat sessions
3. **For each active session:**
   - Reads last 30 messages via `sessions_history`
   - Matches work to dashboard projects by:
     - Project names/keywords in messages
     - File paths mentioned
     - Context clues
4. **For each project with detected work:**
   - GET dashboard project to check current state
   - POST rolling summary update (what/done/next/blocking, ~200 words)
   - POST memory notes for key decisions/facts
   - POST new subtasks (checks for duplicates first, must be specific/actionable)
   - **Auto-commit docs only:**
     ```bash
     git add *.md docs/ README.md CHANGELOG.md
     git commit -m "Auto-save: documentation updates from session"
     git push
     ```
5. **Reports summary** (but delivery mode = none, so it doesn't spam Morgan)

#### What cron does NOT do:
- ❌ Does NOT commit code files (*.ts, *.tsx, *.js, etc.)
- ❌ Does NOT commit config files (.env, package.json)
- ❌ Does NOT commit database files
- ❌ Does NOT update MEMORY.md handoff (only at session end)

**Why this split:**
- Docs are safe to auto-commit (won't break anything)
- Code commits should be deliberate (Morgan or milestone protocol decides)
- Cron is safety net for abandoned sessions, not primary commit mechanism

---

### 🎯 MILESTONE PROTOCOL (mid-session checkpoint)

**When:** Big task complete, breakthrough achieved, logical stopping point

**What agent does:**
```
🎯 **Milestone reached!** 

Ready to lock this in?
✅ Commit + push code
📊 Update dashboard
🔄 Continue working
```

**Agent provides reminder but does NOT execute unless Morgan confirms.**

**If Morgan confirms:**
1. Commit + push code (with descriptive message)
2. Update dashboard:
   - Rolling summary (note what was just completed)
   - Check off completed subtasks
   - Add memory note if key decision was made
   - Note git commit hash in memory
3. Continue working in same session

**Handoff update:** NOT needed (session key unchanged, this is mid-session)

---

### 🔄 PROJECT SWITCH PROTOCOL (mid-session)

**Trigger:** Morgan says "let's work on Tradies instead" while working on Clarat

**What agent does:**

#### 1. Checkpoint Current Project (mini session-end)
```
🔄 Switching from Clarat → Tradies Bookkeeping

Checkpointing Clarat first...
```

Execute:
- Update dashboard (summary, subtasks, memory notes, commit hash)
- Update MEMORY.md handoff (timestamp + current session key)
- Commit + push if uncommitted changes exist
- Confirm: "✅ Clarat checkpointed"

#### 2. Load New Project (full recall)
- Read MEMORY.md handoff for Tradies
- Query dashboard API
- Check git status
- Check dev server
- Read README
- Present briefing

#### 3. Continue in SAME Session
- Both projects now point to same session key in handoff
- This is acceptable — cron can handle multi-project sessions
- Typical: max 2 projects per session, < 16 hours work

---

### 🏁 STEP 4: SESSION END PROTOCOL

#### **Ideal Case: Manual Trigger**

**Trigger:** Morgan says "wrap up" / "done" / "end session" / "closing up"

**What agent executes:**

1. **Commit + push code** (if uncommitted changes exist)
   ```bash
   cd {repo_path}
   git add .
   git commit -m "{descriptive message based on session work}"
   git push
   ```

2. **Update dashboard via API:**
   - POST rolling summary (final state: what was done, what's next, any blockers)
   - PATCH subtasks (check off completed, add newly discovered ones)
   - POST memory notes for key decisions/discoveries
   - Include git commit hash in memory note

3. **Update MEMORY.md handoff:**
   ```markdown
   ### Clarat
   - **Last worked:** 2026-03-17 4:30 PM
   - **Session key:** agent:main:whatsapp:direct:+61402666843
   ```
   Update ONLY these two lines (timestamp + session key)

4. **Verify and confirm:**
   ```
   ✅ Session end complete:
   - Code committed + pushed (commit: a1b2c3d)
   - Dashboard updated
   - Handoff updated
   
   See you next time! 🦬
   ```

---

#### **Fallback Case: Abrupt End**

**What happens:** Morgan walks away, closes window, loses connection, doesn't say "wrap up"

**Result:**
- Session transcript exists but no explicit end protocol ran
- Cron job runs within next hour
- Cron updates dashboard (summary, subtasks, memory notes)
- Cron auto-commits docs
- **BUT:** MEMORY.md handoff timestamp stays stale (last manual update)

**Implication:**
- Next session will still work (dashboard has current state)
- But handoff timestamp won't reflect latest work
- Handoff becomes "last time I properly ended a session" vs "last time I actually worked"

**This is acceptable** — dashboard is source of truth, handoff is just a pointer.

---

## 🔑 KEY DISTINCTIONS

### Handoff vs Milestone

**Handoff = bridge between sessions**
- Updated at session end (when session KEY changes)
- Contains: timestamp + session key
- Purpose: next session knows which session to reference
- Only matters when sessions CHANGE

**Milestone = checkpoint within session**
- Updated mid-session after big task
- No handoff update (session key unchanged)
- Just: commit + dashboard update + continue

---

### Dashboard vs MEMORY.md

**Dashboard = living project state**
- Rolling summary (current status)
- Subtasks (what's next)
- Memory notes (decisions, facts)
- Activity log (timeline)
- Updated constantly (hourly by cron, on-demand by agent)

**MEMORY.md Handoff = session pointer**
- Which session last worked on this
- When it was last worked
- Where to find the project (repo, dashboard ID, port)
- Updated only at session boundaries

---

### Cron Job vs Session End Protocol

**Cron Job = safety net**
- Runs automatically every hour
- Updates dashboard whether you ended properly or not
- Auto-commits docs
- Does NOT update handoff (can't know which session is "current")
- Catches abandoned work

**Session End Protocol = clean closure**
- Runs when you explicitly say "wrap up"
- Updates dashboard + handoff + commits all code
- Proper timestamp in handoff
- Preferred method, but cron catches it if you forget

---

## ✅ VALIDATION CHECKLIST

Before implementing, verify:
- [ ] Scenario 1 workflow makes sense to Morgan
- [ ] No missing steps or edge cases
- [ ] All data sources identified (what to read, what to skip)
- [ ] Token bloat avoided (no duplicate history reading)
- [ ] Auto-commit logic is safe (docs only, not code)
- [ ] Protocols are clear (milestone, switch, end)
- [ ] Cron job behavior understood (safety net, not primary)

---

## 📋 IMPLEMENTATION TASKS

Once validated:
1. Update AGENTS.md with Session Startup Protocol (step 2)
2. Update AGENTS.md with Milestone Protocol reminder
3. Update AGENTS.md with Project Switch Protocol
4. Update AGENTS.md with Session End Protocol (step 4)
5. Update cron job task message to include doc auto-commits
6. Test end-to-end with one project
7. Verify all protocols trigger correctly
8. Document in MEMORY.md that Scenario 1 is live

