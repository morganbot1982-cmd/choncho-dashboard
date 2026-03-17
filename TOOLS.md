# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## File Sharing SOP (Morgan)

Use this as the default handoff path for documents to OpenClaw.

### Primary intake folder (canonical)

- `/Users/Shared/OpenClaw Inbox`
- Workspace link (for agent reads): `/Users/morgan/.openclaw/workspace/inbox/wise`

### Fastest reliable workflow

1. Download files locally first (if coming from Google Drive, avoid cloud-only placeholders).
2. Copy/move files into `/Users/Shared/OpenClaw Inbox`.
3. Tell assistant: "files are in OpenClaw Inbox".

### Known gotchas (from 2026-02-18)

- Cross-user paths caused permission failures; shared path avoids this.
- `Library/CloudStorage` items may require **Download now / Available offline** before they can be copied.
- Finder automation/open commands may fail; direct copy into shared inbox is more reliable.
- For now, prefer local handoff over direct Drive path access.
- Revisit permanent Google Drive sync permissions tomorrow.

## OpenClaw Gateway (Critical)

- **OpenClaw is installed under the `morgan` user account**
- Gateway must always be started as `morgan`, not `userclaw`
- To switch: `su morgan`
- Gateway is started manually with `openclaw gateway` in a dedicated Terminal tab
- If gateway needs restarting, remind Morgan to switch to `morgan` first

## Xero API Access Rules

**HARD RULE — Nothing outbound without Morgan's explicit approval.**

- Tier 1 (free): Read data, analyse locally, draft documents
- Tier 2 (needs Morgan's "go"): Write transactions, create draft invoices, modify records
- Tier 3 (NEVER): Send invoices to clients, submit to ATO, delete, change settings, make payments

See `agents/accountant/AGENT.md` for full details.

---

## Personal Command Center (WhatsApp)

Morgan's personal task/life management assistant. When a WhatsApp message arrives from Morgan that isn't a tradies bookkeeping command (receipt, "who owes me", "chase", "monthly summary"), route it through the Command Center.

### How to process

**Step 1: Send the message to the command API**
```bash
curl -s -X POST http://localhost:3005/api/command \
  -H "Content-Type: application/json" \
  -d '{"text":"<user message>"}'
```

**Step 2: Check the response**

The API returns JSON with these possible shapes:

```json
// Direct reply — send back via WhatsApp
{"reply": "formatted message", "intent": {...}}

// Needs Claude classification — ambiguous input
{"needsClassification": true, "classificationPrompt": "...", "originalText": "..."}

// Task created with nuclear flag — set up persistent reminders
{"reply": "...", "intent": {...}, "nuclear": true, "taskId": "..."}

// Reminder requested — create an OpenClaw cron job
{"reply": "...", "intent": {...}, "createReminder": true}
```

**Step 3: Handle each case**

- **Direct reply:** Send `reply` field back via WhatsApp as-is
- **Needs classification:** Use the `classificationPrompt` as a system prompt, get Claude's JSON response, then POST it back to `/api/command` with the classified intent as `{"text":"<original>"}` — or just handle the intent directly
- **Nuclear flag:** Create an OpenClaw cron job that sends WhatsApp reminders every 3 min until Morgan replies "ok"/"done"/"stop". Use escalating messages from the API.
- **Create reminder:** Parse the `when` field from the intent and create an OpenClaw cron job for that time

### Auto-scheduling reminders for tasks with due dates

When a task is created with a due date/time (either from `add_task` or `createReminder`):

1. **Get the reminder schedule:**
```bash
curl -s http://localhost:3005/api/tasks/<taskId>/schedule
```
This returns pre-calculated reminders based on the task's tier:
- **Gentle** (normal): 30 min before
- **Persistent** (high priority): 1 hour + 30 min before
- **Nuclear** (appointments/calls): 1 hour + 30 min + 15 min before + repeating at event time

2. **Create each cron job** from the `cronJobs` array in the response. Each entry is ready to pass directly to the OpenClaw `cron` tool's `job` parameter.

3. **Update each reminder** with the cron job ID:
```bash
curl -s -X PATCH http://localhost:3005/api/reminders/<dbReminderId> \
  -H "Content-Type: application/json" \
  -d '{"cronJobId":"<cron job id>"}'
```

### Handling `createReminder` responses (standalone reminders)

When the command API returns `"createReminder": true` (e.g., "remind me to call mum Thursday"):

1. **Parse the time** from `intent.when` (e.g., "thursday", "tomorrow 3pm", "in 2 hours")
2. **Create a task** with the parsed due date via `/api/tasks` POST
3. **Then call** `/api/tasks/<id>/schedule` to auto-schedule the reminders
4. **Create the cron jobs** from the response

### Handling `nuclear` task responses

When the command API returns `"nuclear": true`:

1. Call `/api/tasks/<taskId>/schedule` — it auto-detects nuclear tier
2. Create all cron jobs from the response (includes escalating pre-reminders + repeating nuclear at event time)
3. **On acknowledgment** ("ok"/"done"/"stop"): remove the nuclear cron jobs and mark reminders as sent

### Handling acknowledgments ("ok", "done", "stop")

When the command API returns `intent.type === "acknowledge"`:
1. Check for any active nuclear cron jobs (query `/api/reminders?status=pending`)
2. Remove/disable the cron jobs
3. Mark reminders as sent
4. Send the acknowledgment reply

### Priority routing

1. Check if message matches tradies bookkeeping triggers FIRST (receipt photo with "test receipt", "who owes me", "chase", "monthly summary")
2. If no tradies match → route to Command Center (`/api/command`)
3. If Command Center returns `needsClassification` → use your own judgment to classify and act

### Command Center must be running

Dashboard runs on port 3005. If it's down:
```bash
cd ~/.openclaw/workspace/personal-command-center && npx next dev --port 3005 &>/tmp/pcc-dev.log &
```

---

## Receipt Processing (Tradies Bookkeeping)

When Morgan or a client sends a **receipt photo via WhatsApp**, process it as follows:

### Step 1: Extract receipt data
Use the `image` tool to analyse the photo with this prompt:
```
Extract all data from this receipt. Return ONLY a JSON object:
{"vendor":"store name","date":"YYYY-MM-DD","total":number,"gst":number,"items":[{"description":"item","quantity":number,"amount":number}],"category":"materials|tools|fuel|vehicle|subcontractor|office|safety|other","payment_method":"cash/card/eftpos","abn":"ABN or null","reference":"receipt number or null"}
Category guide: materials (timber,concrete,pipe,fittings,paint), tools (power tools,hand tools,blades,PPE), fuel (petrol,diesel), vehicle (rego,service,parts), subcontractor (labour hire), office (phone,internet,stationery), safety (first aid,signs).
Return ONLY JSON.
```

### Step 2: Post to Xero
Run the receipt handler script:
```bash
cd ~/.openclaw/workspace/tradies-bookkeeping && node receipt-handler.mjs <image-path> '<receipt-json>'
```

### Step 3: Reply
Send the confirmation from the script output back via WhatsApp.

### Command: "menu" / "help" / "commands"
When the user asks for help, menu, or what commands are available, reply with:

```
📋 *What I can do:*

1️⃣ *Snap a receipt* — Send a photo next
2️⃣ *Who owes me* — See outstanding & overdue invoices
3️⃣ *Chase [name]* — Resend an invoice to chase payment
4️⃣ *Monthly summary* — How's business going this month
5️⃣ *Job costs [job name]* — Spending on a specific job (coming soon)
6️⃣ *Help* — Show this menu

💡 _Voice notes work too — just say any command._
```

### Number shortcuts after menu
If the user sends a number (1-6) right after seeing the menu, treat it as selecting that option:
- **1** → Reply "📸 Send me the receipt photo now" then process the next image as a receipt (no caption needed)
- **2** → Run "who owes me"
- **3** → Reply "Who do you want to chase?" then run chase-invoice with their next reply
- **4** → Run monthly summary
- **5** → Reply "Which job?" then run job costs with their next reply (coming soon)
- **6** → Show menu again

When the user selects option 1, the NEXT image they send should be processed as a receipt regardless of caption.

### Trigger
ONLY process a WhatsApp image as a receipt if the message caption contains **"test receipt"** (case insensitive). This is a dev/testing trigger — Morgan's personal WhatsApp is the bot for now.

If an image arrives WITHOUT "test receipt" in the caption, treat it as a normal message. Do not process it as a receipt.

### Command: "who owes me" / "overdue invoices"
When the user asks who owes them money, overdue invoices, or outstanding payments:
```bash
cd ~/.openclaw/workspace/tradies-bookkeeping && node who-owes-me.mjs
```
For overdue only:
```bash
cd ~/.openclaw/workspace/tradies-bookkeeping && node who-owes-me.mjs --overdue-only
```
Parse the JSON output and send the `reply` field back to the user.

### Command: "chase [name]" / "send invoice to [name]"
When the user wants to resend an invoice to chase payment:
```bash
# Step 1: DRY RUN (always do this first — shows what would be sent)
cd ~/.openclaw/workspace/tradies-bookkeeping && node chase-invoice.mjs "<contact name>"

# Step 2: ONLY if user confirms, add --send flag
cd ~/.openclaw/workspace/tradies-bookkeeping && node chase-invoice.mjs "<contact name>" --send
```
**NEVER run with --send without the user explicitly confirming.** This sends a real email to a real client. Show the dry run first, ask "want me to send it?", then send only if they say yes.

### Command: "monthly summary" / "how am I going" / option 4
When the user asks for a monthly summary or how business is going:
```bash
cd ~/.openclaw/workspace/tradies-bookkeeping && node monthly-summary.mjs
```
For a specific month:
```bash
cd ~/.openclaw/workspace/tradies-bookkeeping && node monthly-summary.mjs 2026-02
```
Parse the JSON output and send the `reply` field back.

### When NOT to process
- No "test receipt" in caption — ignore as receipt, respond normally
- If the image is clearly not a receipt even with the trigger — tell Morgan
- If Morgan says "don't process this" or similar

---

Add whatever helps you do your job. This is your cheat sheet.
