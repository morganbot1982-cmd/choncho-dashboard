# Dashboard Sync Cron Job - FINAL Task Message

**Job ID:** 4e9c6d59-ae93-471d-821c-5df06189065c
**Schedule:** Every 1 hour
**Session:** isolated
**Agent:** main
**Model:** claude-sonnet-4-5

---

## Task Message (Complete)

```
You are the dashboard-sync cron job. Run hourly to keep the OpenClaw Project Dashboard in sync with actual work and auto-commit documentation.

**GOAL:** Safety net for abandoned sessions. Update dashboard + auto-commit docs even if Morgan didn't run Session End Protocol.

---

## RULES

1. Only sync sessions where Morgan was actively chatting (skip cron/heartbeat/hook sessions)
2. Check existing checklist before adding subtasks to avoid duplicates
3. Summaries must be concise (~200 words max): what is this, what's done, what's next, what's blocking
4. Subtasks must be specific and actionable ("Add token refresh to receipt handler" not "fix auth stuff")
5. Only update projects with actual activity in the last 2 hours
6. Dashboard must be running on http://localhost:3004
7. Auto-commit docs only (NOT code)

---

## STEPS

### 1. Verify Dashboard Running

Check: `curl -s http://localhost:3004 -o /dev/null -w '%{http_code}'`

If NOT 200:
- Start dashboard: `cd ~/.openclaw/workspace/openclaw-project-dashboard/apps/web && npx next dev --port 3004 &`
- Wait 10 seconds
- Verify again
- If still fails: abort with error message

### 2. List Active Sessions

Command: `sessions_list` with filter for last 2 hours

Skip these session types:
- cron sessions (key contains "cron:")
- heartbeat sessions (label = "heartbeat")
- hook sessions (key contains "hook:")
- This current dashboard-sync session

Keep only: chat sessions where Morgan was actively working

### 3. Read Session History

For each active session:
- `sessions_history` with limit 30 messages
- Look for work indicators:
  - Project names mentioned ("Clarat", "Tradies", "Dashboard")
  - File paths (clarat/, tradies-bookkeeping/, openclaw-project-dashboard/)
  - Git commands
  - Code edits
  - Feature discussions

### 4. Match Work to Dashboard Projects

**Known projects:**
- "Clarat" or path contains "clarat/" → proj-11adb2ec
- "Tradies" or "bookkeeping" or path contains "tradies-bookkeeping/" → proj-4b3ad803
- "Dashboard" or "project dashboard" or path contains "openclaw-project-dashboard/" → proj-1
- "Session" or "continuity" → proj-52e7dfad

For each project with detected work:
- GET `/api/projects/{projectId}` to check current state
- Store current rolling summary for comparison

### 5. Update Dashboard for Each Project

**Rolling Summary:**
- POST `/api/projects/{projectId}/notes` with `kind=summary`
- Format: What is this, what's done, what's next, what's blocking (~200 words)
- Include recent work from session
- Be specific about what changed

**Memory Notes:**
- POST `/api/projects/{projectId}/notes` with `kind=decision` for key decisions
- POST `/api/projects/{projectId}/notes` with `kind=fact` for discoveries/insights
- Only add if session revealed something worth remembering

**Subtasks:**
- GET current checklist first
- Check for duplicates (similar text or intent)
- POST `/api/projects/{projectId}/checklist` for NEW actionable items only
- Format: Specific and actionable ("Add error handling to receipt parser" not "fix bugs")
- Check off completed items if work in session finished them

### 6. Auto-Commit Documentation (NEW)

For each project with work detected:

**Check for uncommitted docs:**
```bash
cd {repo_path}
git status --porcelain | grep -E '\.(md|MD)$|^docs/'
```

**If uncommitted docs exist:**
```bash
git add *.md docs/ README.md CHANGELOG.md PR-SUMMARY.md CONTRIBUTING.md
git diff --cached --stat
git commit -m "Auto-save: documentation updates from {session_time}"
git push origin main
```

**What to commit:**
- ✅ All .md files (*.md, **/*.md)
- ✅ docs/ folder
- ✅ README.md, CHANGELOG.md, PR-SUMMARY.md, CONTRIBUTING.md

**What NOT to commit:**
- ❌ Code files (*.ts, *.tsx, *.js, *.jsx, *.py, etc.)
- ❌ Config files (.env, package.json, tsconfig.json)
- ❌ Database files (*.db, *.sqlite)
- ❌ node_modules, .next, dist, build folders

**Error handling:**
- If git commit fails (nothing staged): skip silently
- If git push fails (network/auth): note in summary but continue
- If repo doesn't exist: skip git steps gracefully

### 7. Reply with Summary

Format:
```
Dashboard sync complete:

✅ **{Project Title} ({projectId})** updated:
- Rolling summary refreshed
- {N} subtasks added
- Memory note: {brief description}
- Docs committed + pushed (commit: {hash})

✅ **{Project 2}** updated:
- Rolling summary refreshed
- Docs committed + pushed (commit: {hash})

No other projects had meaningful activity in the last 2 hours.
```

If no work detected:
```
Dashboard sync: no meaningful project work in the last 2 hours.
```

---

## EDGE CASES

**No repo exists:**
- Skip git commands gracefully
- Dashboard updates still work
- Note in summary: "No repo found, skipped git operations"

**Wrong/missing port:**
- Try port from MEMORY.md handoff first
- If fails, scan: 3000, 3001, 3002, 8080
- Report which port worked
- Update memory note with correct port

**Dashboard down:**
- Already handled in step 1 (auto-start)
- If auto-start fails, abort entire run

**Multi-project sessions:**
- Detect work on multiple projects in same session
- Update each project separately
- Commit docs separately per repo
- All point to same session key (acceptable)

**Duplicate subtasks:**
- Always GET current checklist first
- Compare new subtask text with existing
- Skip if similar intent already exists
- Better to miss one than create duplicates

---

## WHAT THIS JOB DOES NOT DO

- ❌ Does NOT commit code (only docs)
- ❌ Does NOT update MEMORY.md handoff (only Session End Protocol does that)
- ❌ Does NOT replace Session End Protocol (this is safety net only)
- ❌ Does NOT send notifications (delivery mode = none)
- ❌ Does NOT process personal/non-project chat
```

---

## Implementation

To update the cron job:
```bash
openclaw cron update \
  --job-id 4e9c6d59-ae93-471d-821c-5df06189065c \
  --patch '{"payload": {"message": "... paste task message above ..."}}'
```
