# Task Copilot Setup Instructions

## Phase 1 Components

### ✅ Created
- `AGENT.md` - Agent personality and instructions
- `state.json` - Task tracking state
- `morning-briefing.sh` - 8 AM daily briefing script
- `evening-recap.sh` - 6 PM daily recap script

### ⏳ To Schedule (OpenClaw Cron)

**Morning Briefing (8 AM daily):**
```bash
# Command to run: bash /Users/userclaw/.openclaw/workspace/agents/task-copilot/morning-briefing.sh
# Schedule: 0 8 * * * (every day at 8 AM Brisbane time)
# Send output to WhatsApp via message tool
```

**Evening Recap (6 PM daily):**
```bash
# Command to run: bash /Users/userclaw/.openclaw/workspace/agents/task-copilot/evening-recap.sh  
# Schedule: 0 18 * * * (every day at 6 PM Brisbane time)
# Send output to WhatsApp via message tool
```

### Task Capture (Already Works)
Just message me:
- "task: order packaging tape" → I'll add to NOW.md
- "todo: call supplier" → Added to Next Actions
- Any format with task/todo/reminder keywords

### Nudge System (To Build)
- Check every 3 days for stale tasks
- Send reminder via WhatsApp
- Accept "done", "skip", or "later [date]"

## Testing

**Test morning briefing now:**
```bash
bash /Users/userclaw/.openclaw/workspace/agents/task-copilot/morning-briefing.sh
```

**Test evening recap now:**
```bash
bash /Users/userclaw/.openclaw/workspace/agents/task-copilot/evening-recap.sh
```

## Next Steps
1. Schedule cron jobs via OpenClaw
2. Test for a few days
3. Adjust timing/format based on feedback
4. Build nudge system
5. Add voice message support
