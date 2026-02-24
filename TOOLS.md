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

Add whatever helps you do your job. This is your cheat sheet.
