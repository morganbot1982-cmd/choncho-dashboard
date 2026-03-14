#!/bin/bash
# Task Copilot - Evening Recap
# Runs daily at 6 PM via OpenClaw cron

WORKSPACE="/Users/userclaw/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
STATE_FILE="$WORKSPACE/agents/task-copilot/state.json"

# Get today's date
TODAY=$(date +%Y-%m-%d)
MEMORY_FILE="$MEMORY_DIR/$TODAY.md"

# Extract wins from today's memory file (look for checkmarks and "done" items)
if [ -f "$MEMORY_FILE" ]; then
  WINS=$(grep -E "✅|completed|done|finished" "$MEMORY_FILE" | head -5)
else
  WINS="No memory file for today yet."
fi

# Build message
if [ -n "$WINS" ] && [ "$WINS" != "No memory file for today yet." ]; then
  MESSAGE="End of day recap 🦬

Today's wins:
$WINS

What's blocking tomorrow? Reply to update."
else
  MESSAGE="End of day recap 🦬

No wins logged today - rough day or just didn't document?

What's blocking tomorrow? Reply to update."
fi

# Send via WhatsApp
echo "$MESSAGE"

# Update state
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq ".lastEveningRecap = \"$DATE\"" "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"
