# OpenClaw Installation Guide

**For:** New users setting up OpenClaw from scratch  
**Platform:** macOS  
**Last updated:** Feb 26, 2026

---

## TL;DR - The 10-Minute Version

**Critical success factors:**
1. 🔐 **Create dedicated Google account** (yourusername.openclaw@gmail.com)
2. 💻 **Single admin user** (fresh macOS recommended)
3. 🔑 **Do OAuth FIRST** (Phase 2) before any automation
4. ✅ **Version check** when anything breaks
5. 🚀 **Start with calendar** automation (low-risk, high-value)

**Installation order:**
Pre-Flight (10m) → Install (10m) → **OAuth (20m)** → Channels (10m) → Models (5m) → Calendar (15m) → Customize (10m) → Security Audit (5m)

**Total time:** 60-90 minutes

**Biggest mistakes to avoid:**
- ❌ Multi-user setup (use one admin account)
- ❌ Skipping OAuth (causes bot detection hell)
- ❌ Using personal Google account (create dedicated one)
- ❌ Not checking versions first when troubleshooting
- ❌ Automating sensitive stuff without testing

**Read the full guide below for details!**

---

## Prerequisites

### System Requirements
- **macOS** (tested on macOS 14+)
- **Admin account** - Install OpenClaw on your primary admin user
- **Clean system recommended** - Fresh macOS install avoids permission/path issues
- **Terminal access** - Basic command-line comfort helpful
- **Node.js** - Will be installed via Homebrew if needed

### What You'll Need
- **Dedicated Google account** (create NEW account for OpenClaw - see Security section)
- WhatsApp or Telegram account (for messaging)
- Anthropic Claude account (claude.ai)
- Phone for 2FA codes (you'll handle these manually)

---

## Security Architecture (READ THIS FIRST!)

### The Sandbox Philosophy

**Core principle:** OpenClaw should operate in an isolated environment, separate from your personal data.

### 1. Dedicated Google Account (CRITICAL)

**DO NOT use your personal Google account!**

**Create a NEW Google account specifically for OpenClaw:**
- Example: `yourusername.openclaw@gmail.com`
- Separate inbox, calendar, drive
- Share/delegate access to this account where needed

**Why this matters:**
- **Isolation:** If something goes wrong, your personal data is protected
- **Delegation:** OpenClaw acts on behalf of this account, not you directly
- **Clean testing:** Fresh environment without your personal clutter
- **Revocable:** Can disable/delete without affecting your personal Google account

**What this account should have access to:**
- ✅ Calendar (read/write for appointments, reminders)
- ✅ Gmail (read for notifications, drafts for review)
- ✅ Sheets (data manipulation, imports, categorization)
- ✅ Drive (file storage, document access)

**What it should NOT have:**
- ❌ Your bank accounts
- ❌ Financial services (Xero, QuickBooks - use manual review)
- ❌ Sensitive personal data
- ❌ Direct posting access to public social media

### 2. Two-Factor Authentication (2FA)

**YOU handle ALL 2FA codes. Always.**

OpenClaw should **NEVER** attempt to automate 2FA. This is a security boundary.

**How it works:**
1. OpenClaw starts an auth flow (OAuth, login, etc.)
2. Service requests 2FA code
3. **You enter the code manually** (from phone, authenticator app, SMS)
4. OpenClaw continues once authenticated

**Services that need 2FA:**
- Google account (the dedicated OpenClaw one)
- Anthropic Claude
- Banking/financial services (if you grant access)
- Any service with sensitive data

**Background work & 2FA:**
When OpenClaw needs a code during background tasks (cron jobs, overnight work):
- It sends you a WhatsApp/Telegram notification: "Need 2FA code - [description]"
- You enter the code when available
- This allows async work without compromising security

### 3. Access Boundaries

**Safe to automate freely:**
- ✅ Reading files, calendars, emails
- ✅ Creating drafts (you review before sending)
- ✅ Organizing data (spreadsheets, documents)
- ✅ Internal notes, reminders, task lists
- ✅ Web research, searching
- ✅ Code generation, file operations

**Requires explicit approval every time:**
- ⚠️ Sending emails to external people
- ⚠️ Posting to public channels (Twitter, Discord, etc.)
- ⚠️ Making purchases or financial transactions
- ⚠️ Deleting data (use `trash` commands, not `rm`)
- ⚠️ Accessing production systems

**Never automate (manual only):**
- 🚫 Banking transactions
- 🚫 Paying bills
- 🚫 Signing contracts
- 🚫 Anything with legal implications
- 🚫 2FA codes
- 🚫 Password management

### 4. Gateway Safety

**The gateway is OpenClaw's brain. Protect it.**

- Gateway runs on your local machine only
- No external access by default
- Token-based authentication (rotate if compromised)
- Logs all actions (check `~/.openclaw/logs/` for audit trail)

**Never share:**
- Gateway token
- OAuth credentials JSON files
- OpenClaw workspace files containing sensitive data

---

## Installation Phases (Follow This Order!)

**Total time:** 45-90 minutes depending on experience

### Phase 0: Pre-Flight (10 mins)
- ✅ Create dedicated Google account for OpenClaw
- ✅ Confirm you're on clean macOS (or accept permission complexity)
- ✅ Logged in as admin user (the one you'll use daily)
- ✅ Have 60+ minutes available
- ✅ Phone ready for WhatsApp QR scan

### Phase 1: Core Installation (10 mins)
1. Install OpenClaw (Homebrew or npm)
2. Run initial configuration
3. Start gateway (keep it running!)
4. Verify version

### Phase 2: OAuth Setup (20 mins) ⚠️ DO THIS BEFORE AUTOMATION
1. Create OAuth credentials in Google Cloud Console
2. Add yourself as test user
3. Enable APIs (Gmail, Calendar, Sheets, Drive)
4. Authenticate with `gog auth add`
5. **Why first:** Prevents bot detection hell

### Phase 3: Channel Setup (10 mins)
1. WhatsApp QR scan
2. Security settings (DM policy, session isolation)
3. Restart gateway
4. Test messaging

### Phase 4: Model Configuration (5 mins)
1. Configure Claude Max (OAuth, not API)
2. Set Sonnet as primary
3. Set Opus as backup/thinking model
4. Test with simple query

### Phase 5: First Automations (15 mins)
1. Connect Google Calendar
2. Test calendar queries
3. Set up email draft assistance
4. Configure reminders (optional)

### Phase 6: Workspace Customization (10 mins)
1. Edit SOUL.md (personality)
2. Edit USER.md (your preferences)
3. Edit TOOLS.md (your specific setup)
4. Review AGENTS.md (operating rules)

### Phase 7: Security Audit (5 mins)
1. Run `openclaw status`
2. Fix any CRITICAL warnings
3. Verify credentials directory permissions
4. Review access boundaries

---

## Installation Steps

### 1. Install OpenClaw

**Via Homebrew (recommended):**
```bash
brew install openclaw
```

**Or via npm:**
```bash
npm install -g openclaw
```

### 2. Initial Configuration

Run the configuration wizard:
```bash
openclaw configure
```

This will set up:
- Gateway token (for secure communication)
- Model selection (see Model Setup below)
- Channel configuration (WhatsApp, Telegram, etc.)

### 3. Start the Gateway

**IMPORTANT:** Run the gateway manually in a dedicated Terminal window/tab:

```bash
openclaw gateway
```

**Keep this Terminal window open.** The gateway needs to run continuously for OpenClaw to work.

**Tip:** Create a dedicated Terminal tab/window for the gateway so you can leave it running in the background.

---

## Model Setup (Claude Max via OAuth)

**Recommended configuration (what we use):**

### Primary Model: Claude Sonnet 4
- Fast, efficient, handles 95% of tasks
- Good balance of speed + capability

### Backup Model: Claude Opus
- For complex reasoning, long documents, hard problems
- Automatically used when Sonnet can't handle it

### Authentication: OAuth (NOT API keys)
1. Go to claude.ai
2. Log in with your Anthropic account
3. OpenClaw will use OAuth to authenticate
4. **Benefits:**
   - No API key management
   - Uses your Claude Pro/Max subscription
   - Seamless model switching

**During `openclaw configure`:**
- Choose "Claude Max (OAuth)"
- NOT "Claude API"
- Set Sonnet as default, Opus as thinking model

---

## Channel Setup

### WhatsApp (Recommended)

1. Run:
   ```bash
   openclaw whatsapp login
   ```

2. Scan QR code with WhatsApp on your phone

3. Configure security settings:
   ```bash
   openclaw config set channels.whatsapp.dmPolicy "allowlist"
   openclaw config set session.dmScope "per-channel-peer"
   ```

4. Restart gateway:
   ```bash
   openclaw gateway restart
   ```

### Telegram (Optional)

Similar process - follow on-screen instructions during `openclaw configure`.

---

## OAuth & API Integration (Google)

For Gmail, Calendar, Sheets, Drive automation:

### 1. Get OAuth Credentials

1. Go to: https://console.cloud.google.com/apis/credentials
2. Create new project (or select existing)
3. Click "Create Credentials" → "OAuth client ID"
4. Application type: **"Desktop app"**
5. Name it: "OpenClaw"
6. Download the JSON file

### 2. Add Yourself as Test User

1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Click "Audience" in sidebar
3. Under "Test users" click "+ ADD USERS"
4. Add your Gmail address
5. Click "Save"

### 3. Enable APIs

Visit these URLs and click "Enable" on each:

1. Gmail API: https://console.developers.google.com/apis/api/gmail.googleapis.com/overview
2. Calendar API: https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview
3. Sheets API: https://console.developers.google.com/apis/api/sheets.googleapis.com/overview
4. Drive API: https://console.developers.google.com/apis/api/drive.googleapis.com/overview

### 4. Configure OpenClaw

Place the OAuth JSON file in OpenClaw's shared intake folder, then run:

```bash
gog auth add --client-file /path/to/client_secret_xxx.json
```

Browser will open - log in and grant permissions.

**Done!** OpenClaw can now automate Gmail, Calendar, Sheets, Drive.

---

## Lessons from Real Setup Experience

**These are mistakes we made during our first install. Learn from them!**

### Mistake #1: Multi-User Setup ❌

**What we did wrong:**
- Installed OpenClaw under one macOS user (`morgan`)
- Tried to run it from another user (`userclaw`)
- Created permission chaos, file ownership issues, gateway confusion

**The fix:**
- ✅ Install under your PRIMARY admin user
- ✅ Always run gateway as that same user
- ✅ Don't switch users mid-session
- ✅ Fresh macOS = single user = zero problems

**Time wasted:** 4+ hours over multiple days

### Mistake #2: Skipping Version Checks ❌

**What we did wrong:**
- Telegram stopped working
- Spent 2+ hours troubleshooting configs, tokens, settings
- Turns out: gateway was just outdated

**The fix:**
- ✅ ALWAYS check versions FIRST when anything breaks
- ✅ `openclaw --version` before debugging
- ✅ Update immediately if behind
- ✅ Restart gateway after updates

**Time wasted:** 2+ hours

### Mistake #3: OAuth Setup Last ❌

**What we did wrong:**
- Tried Google Sheets automation immediately
- Hit bot detection repeatedly
- Tried manual workarounds (browser relay, etc.)
- All broke or were clunky

**The fix:**
- ✅ Do OAuth setup in Phase 2 (BEFORE any automation)
- ✅ OAuth = no bot detection = smooth automation
- ✅ Saves hours of fighting with manual workarounds

**Time wasted:** 3+ hours

### Mistake #4: Not Understanding Browser Architecture ❌

**What we did wrong:**
- Didn't know OpenClaw has built-in browser
- Installed Chrome extension relay (optional)
- Got confused about which mode to use
- Extension kept auto-installing even after deletion

**The fix:**
- ✅ Use built-in browser (`profile="openclaw"`) by default
- ✅ Chrome extension is OPTIONAL for visual debugging
- ✅ Set `browser.defaultProfile` to "openclaw" in config
- ✅ Restart gateway after changing browser config

**Time wasted:** 2 hours

### Mistake #5: Gateway Running as Wrong User ❌

**What we did wrong:**
- Started gateway from wrong user account
- Token mismatches
- Gateway crashes
- Confusing error messages

**The fix:**
- ✅ Always `whoami` before starting gateway
- ✅ If wrong user: switch with `su [admin-user]`
- ✅ Keep gateway running in dedicated Terminal tab
- ✅ Don't close that tab!

**Time wasted:** 1 hour

### Mistake #6: Using Personal Google Account ❌

**What we ALMOST did wrong:**
- Nearly gave OpenClaw access to personal Gmail/Calendar
- Would've mixed automation with personal data
- Hard to revoke access later

**The fix:**
- ✅ Create dedicated Google account for OpenClaw
- ✅ Keep personal data separate
- ✅ Easier to sandbox and test
- ✅ Can disable without affecting personal stuff

**Time saved by catching this early:** Potentially many hours + data safety

---

**Total time wasted on avoidable issues: 12+ hours**

**Follow this guide properly and you'll skip all of that!**

---

## 🚨 Red Flags - Stop Immediately

**If you see any of these, STOP and fix before continuing:**

### ❌ "Permission denied" errors
**What it means:** Wrong user or file ownership issue  
**Fix:** Confirm you're the admin user who installed OpenClaw
```bash
whoami  # Should match the user you installed as
ls -la ~/.openclaw  # Should show your username
```

### ❌ Gateway crashes on startup
**What it means:** Token mismatch or port conflict  
**Fix:**
```bash
# Kill any existing gateway
pkill openclaw-gateway

# Rotate token
openclaw configure  # Go through Gateway section

# Try again
openclaw gateway
```

### ❌ "Authentication failed" or "Invalid token"
**What it means:** OAuth not set up or expired  
**Fix:** Complete Phase 2 (OAuth Setup) before trying automation

### ❌ Google blocks with "bot detection"
**What it means:** You skipped OAuth setup!  
**Fix:** Go back to Phase 2, set up OAuth properly

### ❌ Can't find `openclaw` command
**What it means:** Not in PATH or installation failed  
**Fix:**
```bash
# Check installation
which openclaw

# If empty, reinstall:
brew install openclaw
# or
npm install -g openclaw
```

### ❌ Multiple OpenClaw processes running
**What it means:** Old gateway didn't shut down properly  
**Fix:**
```bash
ps aux | grep openclaw
# Kill all PIDs shown:
kill [PID]

# Start fresh:
openclaw gateway
```

### ❌ CRITICAL warnings in `openclaw status`
**What it means:** Security or config issue  
**Fix:** Address every CRITICAL warning before daily use
- Follow the fix commands shown
- Restart gateway after changes

---

## Common Issues & Fixes

### Issue: Gateway won't start
**Cause:** Running as wrong user or port conflict  
**Fix:**
- Make sure you're logged into macOS as the admin user you installed OpenClaw under
- Check for existing gateway process: `ps aux | grep openclaw`
- Kill old processes: `pkill openclaw-gateway`
- Restart: `openclaw gateway`

### Issue: Version mismatches / mysterious failures
**Cause:** Outdated OpenClaw or extension  
**Fix:**
1. Check version: `openclaw --version`
2. Update: `brew upgrade openclaw` or `npm update -g openclaw`
3. Restart gateway
4. **Always check versions FIRST when troubleshooting!**

### Issue: Browser automation not working
**Cause:** Wrong browser profile configured  
**Fix:**
```bash
openclaw config set browser.defaultProfile "openclaw"
openclaw gateway restart
```

### Issue: Permission errors with files
**Cause:** Multi-user setup or wrong directory ownership  
**Fix:**
- Stick to single admin user setup (avoid complexity)
- Check file ownership: `ls -la ~/.openclaw`
- Fix if needed: `chown -R $(whoami) ~/.openclaw`

### Issue: 2FA blocks automation
**Expected behavior:** OpenClaw should never automate 2FA  
**Solution:** You handle all 2FA codes manually - this is a security feature, not a bug!

---

## Post-Installation Setup

### 1. Workspace Files

Edit these files in `~/.openclaw/workspace/`:

- **SOUL.md** - Define your assistant's personality
- **USER.md** - Tell it about yourself (preferences, timezone, work style)
- **TOOLS.md** - Document your specific setup (camera names, SSH hosts, etc.)
- **AGENTS.md** - Operating instructions (already has good defaults)

### 2. Test Everything

1. Send a WhatsApp message to yourself
2. Ask OpenClaw to check your calendar
3. Have it create a test Google Sheet
4. Verify browser automation works

### 3. Security Audit

Run a security check:
```bash
openclaw status
```

Fix any CRITICAL warnings before daily use.

---

## First Automations to Set Up

**Start with low-risk, high-value automations that immediately improve your workflow.**

### 1. Google Calendar Integration (HIGHEST PRIORITY)

**Why this first:**
- ✅ Non-destructive (can't break anything)
- ✅ Immediate daily value
- ✅ Tests OAuth + API access
- ✅ Foundation for reminders/scheduling

**Set it up:**

1. **Connect your dedicated OpenClaw Google account:**
   - Share your personal calendar to openclaw account (read-only)
   - Or grant openclaw account edit access if you want it to create events

2. **Test it:**
   ```
   "What's on my calendar today?"
   "Add appointment: Dentist, Friday 2pm"
   "Remind me about the meeting in 30 minutes"
   ```

3. **Enable automatic reminders:**
   - OpenClaw can send WhatsApp reminders for upcoming appointments
   - Morning overview of today's schedule
   - Pre-meeting reminders (30 min before)
   - See HEARTBEAT.md for configuration

**What you get:**
- Voice/text appointment booking
- Natural language ("next Tuesday 3pm")
- Automatic WhatsApp reminders (mobile + desktop)
- Morning daily briefing with schedule
- No more forgotten appointments

### 2. Email Draft Assistance (Safe, Non-Posting)

**Why this works well:**
- ✅ OpenClaw creates drafts, YOU review & send
- ✅ Never posts automatically
- ✅ Saves time on repetitive emails

**Set it up:**

1. **Grant Gmail access** (via OAuth - already done if you followed this guide)

2. **Test it:**
   ```
   "Draft email to Matt about OpenClaw setup - keep it brief"
   "Create draft reply to [person] - acknowledge their question, say I'll respond tomorrow"
   ```

3. **OpenClaw will:**
   - Create the draft in Gmail
   - Notify you it's ready
   - You review, edit, and send manually

**Use cases:**
- Meeting follow-ups
- Quick acknowledgments
- Standard responses
- Email templates

### 3. Apple Reminders Integration (If on macOS)

**Why it's great:**
- ✅ Syncs to iPhone/Watch automatically
- ✅ Voice input via OpenClaw
- ✅ Location-based reminders possible
- ✅ Always with you (phone)

**Set it up:**

Install the apple-reminders skill:
```bash
# (Installation command - check clawhub.com for latest)
```

**Test it:**
```
"Remind me to bring cash when I go to Corey's place"
"Add to shopping list: milk, eggs, bread"
"Show my reminders for this week"
```

### 4. Document & File Organization

**Why it helps:**
- ✅ No risk of data loss (reading/organizing only)
- ✅ Massive time saver
- ✅ Great for ADHD/task management

**Examples:**
```
"Organize these receipts by month and category"
"Find all PDFs in Downloads from last week and move to ~/Documents/Archive"
"Create a project folder for [project name] with standard subfolders"
```

**Works with:**
- Local files (Mac filesystem)
- Google Drive (via API)
- Dropbox, iCloud (with some setup)

### 5. Spreadsheet Data Manipulation

**Why it's powerful:**
- ✅ Automates tedious data work
- ✅ CSV imports, categorization, cleanup
- ✅ Can review output before finalizing

**Use cases:**
- Bank statement categorization
- Expense tracking
- Data imports to accounting software
- List processing

**Example workflow:**
```
"Import this CSV to Google Sheets and categorize the transactions"
"Review for errors" (you check)
"Export final version for Xero import"
```

### 6. Web Research & Summarization

**Zero-risk, high-value:**

```
"Summarize this article: [URL]"
"Find the top 3 plumbers in Brisbane with good reviews"
"What's the weather this weekend?"
"Compare prices for [product] across major retailers"
```

### What NOT to Set Up Yet

**Save these for later (after you're comfortable):**

- ❌ Social media posting (high risk, public-facing)
- ❌ Direct Xero/financial writes (test thoroughly first)
- ❌ Automated outbound messaging (easy to spam accidentally)
- ❌ Code deployment (wait until you trust the workflow)
- ❌ Production system access (sandbox first!)

**Start small, build trust, expand gradually.**

---

## Understanding OpenClaw's Browser

**Critical concept:** OpenClaw has TWO ways to interact with the web.

### 1. Built-in Browser (`openclaw` profile)

**What it is:**
- Headless/invisible browser for automation
- Fast, reliable, API-friendly
- Used by default for most tasks

**When it's used:**
- OAuth flows
- Google Sheets/Gmail automation
- Web scraping
- Form filling
- Multi-step workflows

**Key point:** This runs in the background - you won't see windows opening.

### 2. Chrome Extension Relay (Optional)

**What it is:**
- Takes over your existing Chrome tabs
- Visible automation (you see it happening)
- Useful for debugging

**When to use:**
- Visual confirmation needed
- Debugging automation
- Learning what OpenClaw is doing
- Complex UI interactions

**Default:** Use the built-in browser (profile="openclaw"). Only use Chrome relay when explicitly needed.

### Bot Detection & OAuth

**Problem:** Services like Gmail detect automated access and block it.

**Solution:** OAuth authentication (we set this up in Phase 2).

**Before OAuth:**
```
"Create a Google Sheet" → ❌ Blocked as bot
```

**After OAuth:**
```
"Create a Google Sheet" → ✅ Works smoothly
```

**That's why OAuth is Phase 2 of this guide - it unblocks automation.**

---

## Best Practices

### 1. Keep Gateway Running
- Dedicated Terminal tab/window
- Don't close it accidentally
- If it crashes, check logs: `~/.openclaw/logs/`

### 2. Version Check First
**When troubleshooting ANY issue:**
1. Check OpenClaw version
2. Check browser extension version (if using)
3. Check related tool versions
4. Update if outdated
5. THEN troubleshoot

**This saves hours of debugging!**

### 3. API > Browser
- Use APIs when available (faster, more reliable)
- Browser automation only when:
  - No API exists
  - OAuth/auth flows
  - Visual tasks

### 4. Backup Your Workspace
```bash
cp -r ~/.openclaw/workspace ~/Dropbox/openclaw-backup/
```

Run this weekly or after major changes.

---

## Getting Help

- **Docs:** https://docs.openclaw.ai
- **Discord:** https://discord.com/invite/clawd
- **GitHub:** https://github.com/openclaw/openclaw
- **Skills Hub:** https://clawhub.com

---

## Quick Reference Commands

```bash
# Start gateway
openclaw gateway

# Restart gateway
openclaw gateway restart

# Check status
openclaw status

# Check version
openclaw --version

# Update OpenClaw
brew upgrade openclaw
# or
npm update -g openclaw

# View config
openclaw config get

# Edit config
openclaw config set <key> <value>

# WhatsApp login
openclaw whatsapp login

# Google OAuth setup
gog auth add --client-file /path/to/credentials.json
```

---

## What's Next?

Once installed and running:

1. **Customize workspace files** (SOUL.md, USER.md, etc.)
2. **Set up skills** - Install from clawhub.com
3. **Configure heartbeats** - Proactive monitoring
4. **Create cron jobs** - Scheduled tasks
5. **Explore agents** - Spawn sub-agents for complex work

**Most important:** Start small, learn the basics, then expand!

---

*This guide is based on real-world setup experience. Your mileage may vary slightly depending on your system configuration.*
