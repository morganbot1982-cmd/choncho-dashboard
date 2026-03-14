# Session Routing Issue - March 11, 2026

## Problem
Web UI is connected to WhatsApp session instead of separate desktop session.
Every web response also goes to WhatsApp (duplication).

## Current Session Info
- Session Key: `agent:main:direct:+61402666843`
- Channel: whatsapp
- Session ID: e197bd56-33a8-425d-b3fd-08b4493536c1
- Source: openclaw-control-ui (web UI)

## Expected Behavior
- WhatsApp session: Separate (phone/bed work)
- Desktop session: Separate (web UI work)
- STATUS files: Bridge between them (no message duplication)

## Possible Causes
1. Web UI defaulted to most recent session (WhatsApp)
2. Session picker selected WhatsApp session
3. No separate web UI session exists yet

## Next Steps
1. Check how Morgan accessed web UI (direct URL? session picker?)
2. Create separate session for web UI
3. Ensure STATUS files work across both sessions
4. Test that web replies don't go to WhatsApp

## Temp Solution
Writing to this file instead of replying to avoid WhatsApp spam.

Morgan can read this and tell me how to proceed.
