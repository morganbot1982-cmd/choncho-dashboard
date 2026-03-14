# How to Get a Separate Desktop Session

## The Problem
Your current URL: `http://127.0.0.1:18789/chat?session=agent%3Amain%3Adirect%3A%2B61402666843`

This is EXPLICITLY connecting to the WhatsApp session (notice `+61402666843` = your WhatsApp number).

## The Fix

**Option 1: Use the default chat (no session parameter)**
Open: `http://127.0.0.1:18789/chat`

This will create a NEW session that's NOT tied to WhatsApp.

**Option 2: Force a webchat session**
Open: `http://127.0.0.1:18789/chat?session=agent:main:webchat`

This explicitly creates a webchat session separate from WhatsApp.

## Test It
1. Open one of the URLs above in a NEW browser tab
2. Send a test message
3. Check if it appears on WhatsApp (it shouldn't!)
4. If it works, bookmark that URL for desktop work

## Status Files Still Work
Regardless of which session you're in, I'll read the STATUS files at session start, so context carries over between WhatsApp and desktop.

---

**Try Option 1 first:** http://127.0.0.1:18789/chat

Let me know if it works!
