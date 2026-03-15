# HEARTBEAT.md

## Purpose
Lightweight proactive checks with low noise. If nothing needs attention, reply exactly `HEARTBEAT_OK`.

## Quiet Hours
- 23:00-08:00 (Australia/Brisbane): only alert for urgent issues.

## Health Checks (rotating)
- OpenClaw/gateway status basics
- Node connectivity (paired devices reachable)
- Pipeline/project status checks (if configured)
- Optional Moltbook check
- Calendar upcoming events (for WhatsApp reminders)
- **Leantime blocker check** (urgent items only - see protocol below)

## Cadence
- Run a small subset per heartbeat (avoid heavy full sweeps every time).
- Memory recap every few hours.

## Alert Threshold
Alert only when one of these is true:
- service down/unhealthy
- pipeline error/stall
- node disconnected unexpectedly
- urgent item requiring Morgan's attention

Otherwise: `HEARTBEAT_OK`.

## Memory Hygiene Loop
Every few hours during heartbeats:
1. Update `todo.md` (current tasks, blockers)
2. Append completed work to `progress-log.md`
3. Promote durable facts to `MEMORY.md` (curated only)

## Calendar Reminders (WhatsApp)
Check calendar during heartbeats and send WhatsApp reminders:
- **Morning (first heartbeat after 8 AM):** Today's schedule overview
- **30 min before events:** Heads-up reminder (skip if Morgan is likely aware)
- **Evening prep (around 6 PM):** Tomorrow's early appointments
- **Smart timing:** Don't spam; skip obvious reminders (e.g., all-day events)

Track last reminder time in heartbeat-state.json to avoid duplicates.

## Active Task Reminders (WhatsApp)
Check `heartbeat-state.json` for active task reminders and send to WhatsApp:
- Blood test reminder: Every 2-3 hours during day (8 AM - 8 PM)
- Skip if sent within last 2 hours
- Track `lastSent` timestamp to avoid spam

## Leantime Monitoring Protocol (Hybrid)

**During heartbeats (urgent only):**
- Query for blocked tasks or high-priority overdue items
- SQL: `SELECT id, headline, status, priority FROM zp_tickets WHERE (status = 1 OR (priority = 3 AND dateToFinish < NOW())) AND type = 'task';`
- Alert Morgan immediately if any found
- Stay quiet for routine completions

**Evening briefing (6 PM):**
- Full daily summary of completed tasks
- Blocked or at-risk items
- Tomorrow's top priorities from Leantime
- Include in daily recap

**On-demand:**
- Respond to "what's done?" or "status check" with live query

**Don't spam:** Only alert during heartbeats for actual blockers/urgent issues.

## State Tracking
Use `memory/heartbeat-state.json` with at least:
- `lastChecks`
- `lastMemoryRecap`
- `lastMoltbookCheck`
- `lastCalendarReminder` (timestamp of last WhatsApp reminder sent)
- `lastLeantimeCheck` (timestamp of last blocker check)
last WhatsApp reminder sent)
- `lastLeantimeCheck` (timestamp of last blocker check)
