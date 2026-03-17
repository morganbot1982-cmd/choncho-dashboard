# 🦬 Handoff System — Design Doc

## 🔴 The Problem

Every time a new session starts (morning, reset, different channel), the agent starts blank. It only knows what's in the auto-injected workspace files (AGENTS.md, SOUL.md, USER.md, MEMORY.md, etc).

Everything else — what Morgan worked on last night, where he stopped, what subtasks are next — is gone. The agent has to reconstruct context from scattered files and usually does a bad job because there's no protocol.

**This costs Morgan 30-60 min every morning.** He's been trying to fix it for weeks. He built an entire project dashboard (ClawBoard) with hourly cron sync, rolling summaries, subtasks, decision notes. The infrastructure exists but the agent doesn't use it at startup.

**Secondary problem:** Multiple webchat tabs all route to `agent:main:main`. Topics get mixed. Sessions become noise.

---

## 🟢 The Solution: Handoff Protocol

### 📌 What it is

A per-project pointer stored in **MEMORY.md** (guaranteed auto-loaded every session). It tells a fresh session exactly where to look — not the detail itself, just the index card.

**The dashboard is the source of truth.** The handoff just says "look here."

### 📋 What the handoff contains (per project)

```
### Clarat
- Last worked: 2026-03-16 11:30 PM
- Session key: agent:main:hook:a64fc6a4...
- Dashboard: proj-11adb2ec → curl command
- Repo: ~/.openclaw/workspace/clarat
- GitHub: https://github.com/morganbot1982-cmd/clarat
- Port: 3000
```

Only fields that exist for that project. No port? Don't include it. No GitHub? Skip it.

### 📊 What the dashboard already provides (no duplication needed)

- ✅ Rolling summaries (what it is, what's done, what's next)
- ✅ Subtasks (the actual next jobs — specific and actionable)
- ✅ Decision notes (why things were done a certain way)
- ✅ Activity log (what happened and when)
- ✅ Cron sync maintains all of this automatically every hour

**The handoff does NOT duplicate any of this.** No "blockers", no "todos", no "what was done". That's all in the dashboard already.

---

## ⚡ What happens at session start

1. **MEMORY.md is already loaded** — agent sees all handoff pointers immediately
2. **If Morgan mentions a project** ("work on Clarat", "back to tradies", "where were we"):
   - Match words to handoff entry
   - Hit dashboard API → get rolling summary + unchecked subtasks + notes
   - Read last 10-15 messages from previous session key → exact stopping point
   - Check git status + dev server health
   - Present briefing: summary + subtasks as "here's what's next, which one?"
3. **If Morgan just says "morning"**: show all handoff entries with summaries, ask which project

---

## 🔄 When the handoff gets updated

1. **Session end** — update handoff for every project touched (last worked + session key)
2. **Project switch** — update handoff for project being left before loading new one
3. **Cron safety net** — hourly dashboard-sync also updates handoff, so crashes don't break tomorrow

---

## 🏗️ Where it lives

- **Handoff pointers** → MEMORY.md (auto-loaded every session)
- **Startup protocol** → AGENTS.md (auto-loaded every session, mandatory rules)
- **Project detail** → Dashboard API at localhost:3004 (source of truth)
- **Session history** → `sessions_history` tool with session key from handoff

No new files to discover. Everything in guaranteed-loaded locations.

---

## ✅ What it solves

- Morning context loading — instant, no hunting
- Subtasks as next jobs — pulled from dashboard, not invented
- Session messiness accepted — handoff is structured layer on top
- Multiple tabs don't matter — handoff is per-project, not per-tab
- Cron as safety net — you don't rely on agent remembering

## ❌ What it doesn't solve

- Parallel interactive webchat sessions (webchat UI limitation)
- Real-time cross-session awareness
- Dashboard chat quality (separate problem — context compilation)

---

## 📝 Status

- [x] Design agreed ← WE ARE HERE, STILL REVIEWING
- [ ] Morgan's changes incorporated (in progress)
- [ ] Write handoff pointers to MEMORY.md
- [ ] Write startup/end/switch protocols to AGENTS.md
- [ ] Test via WhatsApp session (webchat = control room)
- [ ] Verify end-to-end across session boundary
