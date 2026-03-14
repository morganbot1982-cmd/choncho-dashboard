# Xero Tax Fix - Start Here

## What's the situation?

**Found:** 2,228 incorrect tax rates in Xero  
**Fixable:** 698 unreconciled transactions  
**Can't fix:** 1,530 reconciled (locked by bank statements)

## Manual Fix Workflow (Recommended)

You've got **3 files** to work with:

### 1. **QUICK-REF.md** ← Keep this open while working
- Priority list
- Quick navigation steps
- Tax rate translations
- Session flow

### 2. **MANUAL-FIX-WORKFLOW.md** ← Your roadmap
- 7 priority accounts (biggest BAS impact first)
- Batch progress trackers with checkboxes
- Detailed instructions for each account
- Completion tracking

### 3. **progress-log.md** ← Track your sessions
- Log each work session
- Running total
- Dopamine hits from progress

## Quick Start

1. **Open Xero** in browser
2. **Open QUICK-REF.md** in second screen/window
3. **Pick Priority 1** (Travel International - biggest impact)
4. **Set 30-45 min timer**
5. **Fix one batch** (50 transactions)
6. **Check box** in MANUAL-FIX-WORKFLOW.md
7. **Log session** in progress-log.md
8. **Break** (5-10 min)
9. **Repeat** or stop for day

## Why This Approach?

✅ **ADHD-friendly** - Small batches, clear checkboxes, frequent wins  
✅ **Prioritized** - High-impact first (Travel = biggest BAS correction)  
✅ **Tracked** - See progress, stay motivated  
✅ **Flexible** - Do 1 batch or 10, your call  

## Don't Try to Do All 698 at Once

**Realistic pace:**
- 1 session = ~50 transactions (30-45 min)
- 1 account = 2-8 sessions
- Full cleanup = ~14 sessions total

**Spread over:**
- 1 week intensive = 2-3 sessions/day
- 2 weeks relaxed = 1-2 sessions/day
- 1 month casual = 1 session every 2 days

## Files Reference

- `tax-audit-report.json` - Full audit data (698 transactions)
- `audit-tax-rates.py` - Automated audit script (re-run to verify progress)
- `MANUAL-FIX-WORKFLOW.md` - Your main roadmap
- `QUICK-REF.md` - Quick reference card
- `progress-log.md` - Session tracker
- `README.md` - Technical documentation

## Next Steps

**Option A (Systematic):**  
Start with Priority 1 → work through list

**Option B (Quick Win):**  
Start with Priority 7 (Rent Received, 98 txns) for fast completion

**Option C (Check First):**  
Run `./audit-tax-rates.py` again to see current state

---

**Location:** `/Users/userclaw/.openclaw/workspace/projects/xero-cleanup/`

**Questions?** Ask Choncho anytime.

**Ready?** Open QUICK-REF.md and pick your first account.
