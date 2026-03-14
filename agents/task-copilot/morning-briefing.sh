#!/bin/bash
# Task Copilot - Morning Briefing
# Runs daily at 8 AM via OpenClaw cron

WORKSPACE="/Users/userclaw/.openclaw/workspace"
NOW_FILE="$WORKSPACE/NOW.md"
STATE_FILE="$WORKSPACE/agents/task-copilot/state.json"

# Read NOW.md and extract Next Actions (top 3)
NEXT_ACTIONS=$(grep -A 10 "## Next Actions" "$NOW_FILE" | grep "^[0-9]" | head -3 | sed 's/^[0-9]*\. //')

# Check for blockers
BLOCKERS=$(grep -A 5 "## Blockers" "$NOW_FILE" | grep "^-" | sed 's/^- //')

# Build message
if [ -z "$BLOCKERS" ] || echo "$BLOCKERS" | grep -qi "none"; then
  MESSAGE="Good morning! 🦬

Top 3 priorities today:
$NEXT_ACTIONS

No blockers - clear path ahead!"
else
  MESSAGE="Good morning! 🦬

Top 3 priorities today:
$NEXT_ACTIONS

⚠️ Blockers:
$BLOCKERS"
fi

# Send via WhatsApp using OpenClaw message tool
# (This would be called by OpenClaw's cron system which has access to the message tool)
echo "$MESSAGE"

# Update state
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq ".lastMorningBriefing = \"$DATE\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
