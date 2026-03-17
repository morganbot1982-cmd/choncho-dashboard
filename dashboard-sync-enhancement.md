# Dashboard Sync Cron Enhancement

## Current Behavior

The dashboard-sync cron job (ID: `4e9c6d59-ae93-471d-821c-5df06189065c`) runs hourly and:

1. Lists active sessions (last 2 hours)
2. Reads session history
3. Matches work to dashboard projects
4. Updates rolling summaries, memory notes, subtasks via dashboard API

## Required Extension

**Add:** Update MEMORY.md Project Handoff section after updating each dashboard project.

### Implementation

After updating a dashboard project (e.g., `proj-1`, `proj-11adb2ec`), the job should:

1. Read `~/.openclaw/workspace/MEMORY.md`
2. Find the project in the "## Project Handoff" section
3. Update the `**Last worked:**` line with current timestamp (format: `YYYY-MM-DD HH:MM AM/PM`)
4. Update the `**Session key:**` line with the most recent session key that touched that project
5. Write MEMORY.md back using the `Edit` tool

### Example Edit

**Before:**
```markdown
### Clarat
- **Last worked:** 2026-03-16 11:30 PM
- **Session key:** agent:main:hook:a64fc6a4-def2-4a20-aefe-75a04df8f4ee
```

**After** (if work detected in `agent:main:whatsapp:direct:+61402666843` session):
```markdown
###Clarat
- **Last worked:** 2026-03-17 2:30 PM
- **Session key:** agent:main:whatsapp:direct:+61402666843
```

### Updated Instructions for Cron Job

The job's `payload.message` should include:

```
... existing dashboard sync instructions ...

**ALSO: Update MEMORY.md Project Handoff**

After updating each dashboard project:
1. Map dashboardId to MEMORY.md handoff entry:
   - proj-11adb2ec → "### Clarat"
   - proj-4b3ad803 → "### Tradies Bookkeeping"
   - proj-1 → "### OpenClaw Project Dashboard"
   - proj-52e7dfad → "### Session & Continuity Improvements"
2. Read MEMORY.md
3. Use Edit tool to update the two lines:
   - Last worked: [current timestamp in format "YYYY-MM-DD H:MM AM/PM"]
   - Session key: [most recent session that worked on this project]
4. Only update if you actually synced work for that project (don't update unchanged projects)
```

## Next Steps

1. Update the cron job definition with `cron update` tool
2. Test by manually triggering a run with `cron run`
3. Verify MEMORY.md gets updated correctly
4. Mark subtask `item-8e01300a` complete
