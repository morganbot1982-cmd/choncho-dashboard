# HEARTBEAT.md

## Purpose
Lightweight proactive checks with low noise. If nothing needs attention, reply exactly `HEARTBEAT_OK`.

## Quiet Hours
- 23:00–08:00 (Australia/Brisbane): only alert for urgent issues.

## Health Checks (rotating)
- OpenClaw/gateway status basics
- Node connectivity (paired devices reachable)
- Pipeline/project status checks (if configured)
- Optional Moltbook check

## Cadence
- Run a small subset per heartbeat (avoid heavy full sweeps every time).
- Memory recap every few hours.

## Alert Threshold
Alert only when one of these is true:
- service down/unhealthy
- pipeline error/stall
- node disconnected unexpectedly
- urgent item requiring Morgan’s attention

Otherwise: `HEARTBEAT_OK`.

## Memory Hygiene Loop
Every few hours during heartbeats:
1. Update `NOW.md` (current focus, blockers, top 3 next actions)
2. Append key bullets to today’s `memory/YYYY-MM-DD.md`
3. Promote durable facts to `MEMORY.md` (curated only)

## State Tracking
Use `memory/heartbeat-state.json` with at least:
- `lastChecks`
- `lastMemoryRecap`
- `lastMoltbookCheck`
