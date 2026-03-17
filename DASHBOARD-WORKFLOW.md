# 🦬 Dashboard-Centered Workflow

**Status:** DRAFT - Working document to align understanding
**Last updated:** 2026-03-17 3:45 PM

---

## 🔄 The Complete Loop (VALIDATED)

### 📝 Scenario 1: Work on Existing Project

**GOAL:** Complete seamless continuity. Zero context loss. Know EVERYTHING about the project as if previous session never ended.

#### 🎬 1. TRIGGER
- 💬 Morgan says "work on Clarat" (or any project name)
- Works the same if Morgan says dashboard ID ("work on proj-11adb2ec")
- Dashboard is rarely opened directly — chat is where work happens

#### 🧠 2. RECALL PROCESS (Session Startup Protocol)

**What agent checks:**
- ✅ MEMORY.md handoff (dashboard ID, repo, port, GitHub)
- ✅ Dashboard API (`curl http://localhost:3004/api/projects/{id}`)
  - Rolling summary (what/done/next/blocking)
  - Unchecked subtasks
  - Memory notes (decisions, facts)
  - Activity log
  - Deliverables (specs, reports)
- ✅ Git status + recent commits
- ✅ Dev server health check
- ✅ Project README.md (quick reference)

**What agent SKIPS (to avoid token bloat):**
- ❌ Session transcript (cron already compressed it)
- ❌ memory/*.md daily logs (cron already compressed it)
- ❌ progress-log.md (cron already compressed it)
- ❌ todo.md (project subtasks in dashboard)

**Agent presents briefing:**
- Summary from dashboard
- Unchecked subtasks
- Git state
- Server status
- Asks: "Which subtask?"

#### 🛠️ 3. DURING WORK

**Cron job runs hourly (safety net):**
- Reads session history (last 2 hours)
- Updates dashboard API (summary, subtasks, memory notes)
- Auto-commits docs only: `git add *.md docs/` → commit → push
- Does NOT commit code (code commits are deliberate)

**Milestone Protocol (when big task complete):**
- Agent reminds: 🎯 "Milestone reached! Ready to lock this in?"
- Morgan decides whether to commit
- If yes: commit + push code + update dashboard

#### 🏁 4. SESSION END

**Manual trigger (ideal):**
- Morgan says "wrap up" / "done" / "end session"
- Agent executes Session End Protocol:
  1. Commit + push code (if uncommitted changes)
  2. Update dashboard (summary, subtasks, memory notes, commit hash)
  3. Update MEMORY.md handoff (timestamp + session key)
  4. Confirm completion

**Abrupt end (fallback):**
- Morgan walks away / closes window / loses connection
- Cron job catches it within 1 hour
- Updates dashboard (but NOT handoff — timestamp stays stale until next proper end)

#### 🔄 5. HANDOFF vs MILESTONE

**Handoff = bridge between sessions**
- Only updated at session end (when session key changes)
- Contains: last worked timestamp + session key
- Purpose: next session knows where to look

**Milestone = checkpoint within session**
- No handoff update needed (session key unchanged)
- Just: commit + dashboard update + continue working

#### 🔄 6. PROJECT SWITCH (mid-session)

When Morgan says "let's work on Tradies instead":

**Project Switch Protocol:**
1. 🎯 Checkpoint current project (mini session-end):
   - Update dashboard (summary, subtasks, memory notes)
   - Update handoff (timestamp + session key)
   - Commit + push if uncommitted changes
2. 📖 Load new project (full recall):
   - Read handoff + dashboard + git status + README
   - Present briefing
3. ✅ Continue in SAME session

**Why same session:**
- Typical: max 2 projects per session, < 16 hours
- Can reference both if needed
- Cron + switch protocol keep things clean

**Trade-off:** Both projects point to same session key in handoff (acceptable)

---

## 🤔 What Dashboard Contains

- ✅ Rolling summary (current state)
- ✅ Subtasks (what's next)
- ✅ Memory notes (decisions, key facts)
- ✅ Activity log (what changed when)
- ✅ Deliverables, files
- ✅ Git info (can be noted in memory)

---

## ❓ What MEMORY.md Handoff Adds

- 🔗 Session key (for pulling old chat transcripts)
- ⏱️ Last worked timestamp (staleness indicator)

**Question:** Is this redundant if dashboard rolling summary is good?

---

## 🚧 MISSING SCENARIOS TO DOCUMENT

### Scenario 2: New Idea (No Project Created Yet)
- ❓ What happens?
- ❓ Where does the idea get captured?
- ❓ When does it become a dashboard project?
- ❓ Who creates it (you or agent)?

### Scenario 3: Work NOT on a Project
- ❓ General assistant tasks (not project-specific)
- ❓ Where does this get tracked?
- ❓ Does it need tracking?

### Scenario 4: Multiple Projects in One Session
- ❓ How does cron know which project gets which work?
- ❓ What if you switch mid-conversation?

### Scenario 5: Work Outside Sessions
- ❓ You code/commit directly without talking to agent
- ❓ How does dashboard know?
- ❓ Manual sync needed?

### Scenario 6: Session Ends Badly (crash/disconnect)
- ❓ Cron is safety net, but what if cron misses it?
- ❓ Recovery process?

---

## 📋 TO DO: Complete This Document

1. Fill in missing scenarios with Morgan
2. Identify gaps in current workflow
3. Decide what ACTUALLY needs to be tracked where
4. Align cron job, handoff protocol, project creation to match
5. Move final version to proper location (AGENTS.md? Separate WORKFLOW.md?)

---

## 💭 Open Questions

1. Is session transcript history actually needed if dashboard summary is good?
2. Should cron auto-create dashboard projects when it detects new work?
3. What's the canonical source of truth: MEMORY.md handoff or dashboard API?
4. Should handoff section exist at all or is it duplicate data?

