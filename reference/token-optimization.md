# Token Optimization — Key Learnings
*Source: Twitter thread by @legendaryy, Feb 2026*

## Model Tiering (biggest cost saver)
- **Daily driver:** `anthropic/claude-sonnet-4-5-20250929` — $3/$15 per 1M tokens, nearly Opus-level (72.5% vs 72.7% OSWorld)
- **Deep reasoning:** `anthropic/claude-opus-4-6` — $15/$75 per 1M tokens, use only when needed
- **Budget fallback:** Kimi K2.5 via OpenRouter — ~$0.60/$2 per 1M tokens
- **Ultra budget:** MiniMax M2.5 — $0.30/$1.20 per 1M tokens, MIT licensed
- Can swap models mid-session when needed
- **⚠️ Use exact model identifiers** — "Sonnet 4.6" in articles ≠ actual API model name

## Persistence (prevent re-deriving context)
- Write everything important to markdown files
- Long sessions get compacted — agent loses context silently
- Files are onboarding docs for an employee with amnesia
- Key files: USER.md, AGENTS.md, MEMORY.md, SOUL.md, todo.md, progress-log.md

## Async Work Pattern
- Build → Test → Log → Decide → Loop
- todo.md = live task list, self-expanding
- progress-log.md = morning briefing, what happened overnight
- Cron jobs wake agent on schedule (e.g. 2am, 4am, 6am for overnight work)

## Escalation Rules
- After 3 failed attempts on same issue: STOP and re-plan
- Escalate immediately for: missing credentials, external outages, ambiguous requirements

## General Principles
- Start with one workflow, make it perfect, then add the next
- Separate dev (coding) from ops (monitoring, scheduling, comms)
- The setup IS the work — writing rules is product work
- Run `openclaw doctor --fix` when things break
- Security: run `openclaw security audit` regularly

## Model Comparison (Feb 2026)
| Model | Model ID | Agent Quality | Tool Calls | Cost (in/out per 1M) |
|---|---|---|---|---|
| Claude Sonnet 4.5 | `anthropic/claude-sonnet-4-5-20250929` | Excellent | Reliable | $3 / $15 |
| Claude Opus 4.6 | `anthropic/claude-opus-4-6` | Excellent | Reliable | $15 / $75 |
| Kimi K2.5 | `openrouter/moonshotai/kimi-k2.5` | Great | Reliable | ~$0.60 / $2 |
| MiniMax M2.5 | (check OpenRouter) | Great | Reliable | $0.30 / $1.20 |
| GLM-5 | (check OpenRouter) | Good | Solid | $0.75 / $2.55 |
