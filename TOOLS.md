# TOOLS.md - Local Notes

Environment-specific notes only. Keep under 2KB.
Routing logic, command handling, and multi-step workflows belong in skills.

---

## File Sharing SOP

- **Intake folder:** `/Users/Shared/OpenClaw Inbox`
- Download from Drive first (avoid cloud-only placeholders)
- Copy into shared inbox, then tell assistant "files are in OpenClaw Inbox"

## OpenClaw Gateway

- Installed under `morgan` user account
- Gateway must be started as `morgan`, not `userclaw`
- Started manually with `openclaw gateway` in dedicated Terminal tab
- If restarting needed, remind Morgan to switch to `morgan` first

## Xero API Access Rules

**Nothing outbound without Morgan's explicit approval.**

- Tier 1 (free): Read data, analyse locally, draft documents
- Tier 2 (needs Morgan's "go"): Write transactions, create draft invoices
- Tier 3 (NEVER): Send invoices, submit to ATO, delete, change settings, make payments

See `agents/accountant/AGENT.md` for full details.
