# Continuity Solution — Designed 2026-03-17

## The Problem
Every morning Morgan loses 30-60 min reconciling context. Sessions are messy (mixed topics, multiple tabs → same session key). Memory files are scattered. Dashboard exists but agent doesn't read it at startup. No protocol connects everything.

## The Solution: 3 Pieces

### 1. HANDOFF.md (workspace file, per-project state)
Auto-maintained. Read at every session start alongside AGENTS.md/SOUL.md/USER.md.

```markdown
## Clarat
Last session: 2026-03-16 11:30 PM
Done: Showcase HTML, UI polish, repo private, Clintos11 added
Next: 10 styling fixes in docs/STYLING-FIXES-NEEDED.md
Blockers: None
Git: main, clean, pushed
Server: localhost:3000
Dashboard: proj-11adb2ec

## Tradies Bookkeeping
Last session: 2026-03-16 10:48 PM
Done: Pipeline unblocked — WhatsApp, Claude vision, AI categorisation, Xero OAuth all working
Next: Build receipt processing prototype
Blockers: None
Dashboard: proj-4b3ad803
```

### 2. Project Registry (projects.json)
Maps natural language → structured data. "Clarat", "tradies", "dashboard" → repo, port, dashboard ID, github URL.

### 3. Protocols (added to AGENTS.md)

**Session start (every session):**
1. Read HANDOFF.md → instant context
2. If project mentioned: query dashboard API, check session history, git status, dev server
3. Present briefing

**Project switch (mid-session):**
1. Update HANDOFF.md for current project before switching
2. Load new project context

**Session end / goodnight:**
1. Update HANDOFF.md with what was done + next steps
2. Update dashboard
3. Commit + push if applicable

**Cron safety net:**
- Hourly sync already exists — extend to also update HANDOFF.md if agent didn't

## Key Design Decisions
- No strict naming/commands needed — agent matches intent to project registry
- Sessions stay messy — that's fine. HANDOFF.md is the structured layer on top
- Works regardless of how many tabs/sessions are open
- HANDOFF.md is a workspace file → auto-loaded every session

## Status
- [ ] Create HANDOFF.md with current project state
- [ ] Create projects.json registry
- [ ] Add protocols to AGENTS.md
- [ ] Update cron sync to maintain HANDOFF.md
- [ ] Test end-to-end across session boundary
