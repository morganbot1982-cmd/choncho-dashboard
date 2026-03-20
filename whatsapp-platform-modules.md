# WhatsApp AI Platform — Module Reference

Complete record of all features, ideas, and decisions from the original projects (Tradies Bookkeeping, WhatsApp Modular Systems, Booking Agent, Personal Command Center). Nothing lost.

---

## Core Layer (Shared Infrastructure)

**Status:** ✅ Built and working

- **WhatsApp routing** — priority-based message router (now a skill: `whatsapp-router`)
- **Voice notes** — Whisper transcription → command pipeline. Zero extra dev needed. Huge UX win for tradies on job sites with dirty hands.
- **Cron reminders** — OpenClaw cron → WhatsApp delivery. 4-tier ADHD-optimised: gentle (30 min before), persistent (1 hr + 30 min), blocker buster (stale task detection), nuclear (every 3 min until acknowledged)
- **Dashboard framework** — Next.js, touch-optimised, mobile-first. PWA manifest for install-to-homescreen.
- **WhatsApp sandboxing rule** — CRITICAL for client-facing apps: the WhatsApp number is an APP INTERFACE, not a chatbot. Users outside the app's scope get redirected to menu. No freeform chat for client-facing products.
- **Dual menu system** — bookkeeping commands (1-6), command center (10-16). Dynamic based on active modules.
- **Dev/test setup** — Morgan's personal WhatsApp (+61402666843) as dev bot. "test receipt" trigger prevents accidental processing. Production requires WhatsApp Business API + Meta business verification.

---

## Module: Command Center (Personal Assistant)

**Status:** ✅ Built, tested, working  
**Repo:** `~/.openclaw/workspace/personal-command-center`  
**Port:** 3005  
**GitHub:** https://github.com/morganbot1982-cmd/personal-command-center

### Features
- **Task management** — add, list, complete tasks organised by life areas
- **Shopping list** — separate from tasks, "done with X" checks both tasks and shopping
- **Daily briefing** — morning cron (9 AM) pulls calendar + tasks + reminders
- **Blocker buster** — evening cron (6 PM) detects stale tasks (3+ days)
- **Reminder scheduling** — natural language ("remind me to call mum Thursday") → auto-creates cron jobs based on task tier
- **Nuclear alerts** — appointments/calls get escalating reminders: 1 hr → 30 min → 15 min → every 3 min at event time until "ok"/"done"/"stop"
- **Google Calendar sync** — via `gog` CLI
- **Dashboard UI** — touch-optimised cards, 44px min touch targets, 24px checkboxes, undo support for completed tasks
- **Natural language input** — routes through `/api/command`, falls back to Claude classification for ambiguous input

### Menu (10-16)
10. Dashboard link | 11. Add task | 12. My tasks | 13. Shopping list | 14. Briefing | 15. Reminders | 16. Help

### Decisions
- Shopping completion checks tasks AND shopping items (falls back)
- Mobile UX: whole row tappable, enlarged checkboxes, undo via strikethrough
- PWA: manifest.json + meta tags for homescreen install

---

## Module: Bookkeeper (Tradies)

**Status:** ✅ Pipeline working, needs beta client  
**Repo:** `~/.openclaw/workspace/tradies-bookkeeping`  
**GitHub:** https://github.com/morganbot1982-cmd/tradies-bookkeeping

### Features — Built ✅
- **Receipt capture** — photo via WhatsApp → Claude vision OCR → JSON extraction → Xero draft bill
- **"Who owes me"** — queries Xero for outstanding/overdue invoices
- **"Chase invoice"** — resend overdue invoice (dry run first, NEVER auto-send)
- **Monthly summary** — P&L snapshot from Xero (income, expenses, profit, margin %, top 5 categories)
- **WhatsApp menu** (1-6) — snap receipt, who owes me, chase, monthly summary, job costs, help
- **Voice commands** — all text commands work via voice notes

### Features — Planned ⬜
- **Job tagging** — file receipts under job names ("Smith reno") for per-job cost tracking
- **Job budget query** — "how much spent on Smith job" totals all tagged receipts
- **Invoice creation via WhatsApp** — tradie dictates invoice details by text (needs investigation — complex)
- **Missing receipt reminders** — weekly WhatsApp nudge
- **Human review queue dashboard** — for accountant oversight
- **Keyword trigger update** — change from "test receipt" to "receipt" or "r" for production

### Decisions
- **Claude vision over Mindee OCR** — no extra API, no extra cost, better at messy handwritten receipts, one less dependency
- **WhatsApp as FULL business interface** — not just receipts. Everything tradies need accessible via chat commands
- **Service scope = full bookkeeping**, not just receipt capture:
  - Xero setup for new clients (onboarding revenue)
  - Backlog cleanup (shoebox-to-Xero, $80/hr)
  - Ongoing monthly bookwork (reconciliation, BAS prep)
- **Business model** — 3 monthly tiers undercutting traditional bookkeepers. Docs created 2026-03-18.
- **Testing done** — 3 real receipts (Bunnings Stafford, Coles, Bunnings Newstead) all posted as drafts to Xero correctly

### Xero Integration
- Dev app: "openclaw accountant" on developer.xero.com
- Connected org: Leif Oh Leif Distribution (AU, AUD)
- Auth: `xero-auth.mjs`, tokens in `.env`, refresh on 401
- Scopes: accounting.transactions, contacts, settings, offline_access

---

## Module: Booking Agent

**Status:** ⬜ Designed, zero code  
**Repo:** `~/.openclaw/workspace/whatsapp-booking-agent` (empty/minimal)

### Features — Planned
- **Client-side booking** — text WhatsApp to book/reschedule/cancel. Zero friction, no app download
- **Calendar/availability engine** — time slots, duration, breaks, blocked time
- **Client intent parser** — natural language: "book a cut for Friday 2pm" → parsed intent
- **Owner-side management** — block time, view bookings, manage schedule via WhatsApp
- **Confirmation + reminders** — reuse existing cron infrastructure
- **Dashboard** — bookings overview, calendar view, client list
- **Multi-tenant** — one system, many operators (barbers, tattooists, trades, cleaners, PT)

### Decisions
- WhatsApp sandboxing applies (rule-bound, no freeform chat)
- Revenue model + pricing strategy needed
- Landing page / marketing site needed

---

## Module: Invoicing / Payments (Future)

**Status:** ⬜ Idea only
- Create + send invoices via WhatsApp
- Payment tracking
- Ties into Xero integration from bookkeeper module

---

## Module: CRM / Client Comms (Future)

**Status:** ⬜ Idea only
- Shared contact/client layer across modules
- Client communication history
- Follow-ups and relationship management

---

## Platform Architecture (from Modular Systems project)

### Design Principles
- One WhatsApp number per business
- Modular: pay for what you need
- Shared core (routing, cron, dashboard, voice)
- Module registry (enable/disable per customer)
- Unified menu system (dynamic based on active modules)
- Shared dashboard framework (tabs per module)

### Multi-Tenant Requirements
- Auth + tenant isolation
- Per-customer module config
- Shared contact layer
- One system, many operators

### Go-to-Market
- Pricing model + tier structure needed
- Landing page / marketing site needed
- Target market: tradies and solo operators in Brisbane
- Beta client: tradie doing $300K+/year, ideally existing Xero user

---

## Production Requirements (All Modules)

- [ ] WhatsApp Business API number (Meta business verification)
- [ ] Dedicated WhatsApp number (not Morgan's personal)
- [ ] Production Next.js build (not dev server)
- [ ] Remove batphone (+61435084682) from allowlist
- [ ] Error handling docs (Xero fail, OCR fail, wrong format)
- [ ] Conversation flow design for each command
- [ ] Beta testing with 2-3 real users (not just Morgan)
