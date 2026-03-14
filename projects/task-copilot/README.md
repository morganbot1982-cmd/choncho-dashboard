# Task Copilot — Project Brief

*Created: 2026-02-22*

## Vision
A dedicated AI task assistant that knows Morgan's full business context, keeps him on track across all work (digital and physical), and is accessible by voice or text from anywhere — including away from the computer.

## Why This Matters
- Morgan runs multiple business activities solo — distribution, headwear brand, photography, ecommerce JV, accounting, physical workshop tasks
- ADHD means great ideas but structure helps convert them into consistent execution
- Much of the work is labour-intensive and away from the computer — needs mobile/voice-first input
- Current system (asking Choncho) requires being at the computer and initiating conversation — too passive

## Core Principles
1. **Push, not pull** — the agent reaches out, Morgan doesn't have to remember to check
2. **Voice-first** — talk to it like a colleague, especially when hands are busy
3. **Context-aware** — knows the full business structure, current projects, priorities, and constraints
4. **One thing at a time** — ADHD-friendly: suggests the single most important next action
5. **Capture everything** — any thought, task, note can be captured instantly by voice or text
6. **Low friction** — if it takes more than 5 seconds to capture a task, it's too slow

## Agent Knowledge (must be trained on)

### Morgan's Business Structure
- **Leif Oh Leif Distribution Pty Ltd** — main company entity
  - Distribution/import business (15 years experience in AU clothing/distribution)
  - Handmade headwear brand with in-house sample workshop
  - Photography income stream
  - Consulting income stream
- **Ecommerce JV** (new) — joint venture with partner
  - Import from China → AU warehouse → 3PL → Shopify
  - Accessories first, $20K AUD budget
  - Partner: old colleague, ex-sales manager, same industry
- **Physical workspace** — workshop/studio for headwear production and samples
- **Accounting** — Xero, Wise bank account, accountant relationship

### Morgan's Work Patterns
- Solo operator — no employees, does everything from admin to physical production
- Splits time between computer work (admin, design, marketing, accounting) and hands-on work (workshop, shipping, photography)
- Often away from desk — needs to capture tasks and get updates without a screen
- Benefits from structure: clear next actions, time-boxing, progress tracking
- Values momentum — prefers steady progress over perfection

### Key Context the Agent Needs
- Current project status (reads from NOW.md / PM tool)
- Today's priorities and schedule
- Business calendar and deadlines (BAS, tax, supplier timelines)
- Which tasks are blocked and why
- What got done recently (to avoid repeating or forgetting)

## Phases

### Phase 1 — Morning Briefings + Nudges (NOW)
- Cron-based morning briefing pushed via messaging channel
- End of day recap
- Periodic nudges for stale tasks
- Uses Choncho's existing infrastructure
- **Requires:** Working messaging channel (Telegram or WhatsApp)

### Phase 2 — Dedicated Sub-Agent
- Separate OpenClaw agent with own personality and task-focused system prompt
- Integrated with PM tool (Plane/Leantime) via API
- Can create, update, complete tasks
- Communicates with Choncho for project context
- Has full business structure knowledge baked in
- **Requires:** PM tool running, agent configuration

### Phase 3 — Voice Interface
- Voice input for task capture ("Hey, add a task: order packaging tape")
- Voice output for briefings and updates (TTS)
- Could use:
  - Telegram voice messages (transcription → task)
  - WhatsApp voice notes
  - Custom voice interface (web or native)
  - Apple Shortcuts integration for Siri-like trigger
- Hands-free mode for workshop/physical work
- **Requires:** Working messaging channel with voice support, STT pipeline

### Phase 4 — Smart Scheduling
- Learns Morgan's work patterns over time
- Suggests optimal times for different task types
- "You usually do computer work in the morning — want to batch these admin tasks?"
- Integrates with calendar
- Auto-prioritisation based on deadlines, dependencies, energy levels
- **Requires:** Enough usage data to learn patterns

## Technical Stack (proposed)
- **Agent:** OpenClaw sub-agent with dedicated AGENT.md
- **Task storage:** PM tool API (Plane/Leantime)
- **Messaging:** Telegram or WhatsApp (voice + text)
- **Voice input:** Platform native (Telegram voice messages) or Whisper STT
- **Voice output:** ElevenLabs TTS (sag) or OpenClaw TTS
- **Briefings:** OpenClaw cron jobs
- **Context:** Reads workspace files + PM tool + calendar

## Personality
- Direct, encouraging, no-nonsense
- Knows when to push and when to back off
- Celebrates wins without being cheesy
- Understands physical work is real work — doesn't only track computer tasks
- Brief by default — expands only when asked

## Open Questions
- Which messaging platform first? (Telegram needs fixing, WhatsApp status unclear)
- Voice interface: native platform voice messages vs custom STT pipeline?
- How much autonomy? (auto-schedule tasks vs just suggest?)
- Should it have access to Xero/Shopify or just task management?
- Separate personality from Choncho or extension of Choncho?
