# Integrations Agent

**Status:** Active  
**Purpose:** Handle complex API integrations, database operations, and system configurations

## Quick Start

```bash
# Spawn for a task
/subagents spawn integrations "Set up Leantime with single user"
```

## What It Does

- OAuth flows & API authentication
- Database operations & migrations  
- Docker service setup
- Multi-step integration workflows
- Validation at every step
- Clean rollback when things fail
- Comprehensive documentation

## Current Integrations

### To Be Set Up
- [ ] Leantime (clean restart needed - user assignment issue)

### Working
- [x] Xero API (OAuth configured)
- [x] Google APIs (Gmail, Calendar, Drive, Sheets)

## Documentation Structure

Each integration gets its own folder:

```
integrations/
├── leantime/
│   ├── SETUP.md
│   ├── CONFIG.md
│   ├── TROUBLESHOOTING.md
│   └── ROLLBACK.md
├── xero/
│   └── ... (similar)
└── google-apis/
    └── ... (similar)
```

## Key Principles

1. **Single source of truth** - One user (Morgan), one org (your business)
2. **Validate every step** - Test before proceeding
3. **Document everything** - Setup, config, rollback
4. **Clean failures** - Never leave partial state
5. **Real testing** - Morgan can actually use it

## Files

- `AGENT.md` - System prompt / role definition
- `SOUL.md` - Personality / approach
- `README.md` - This file
- `integrations/` - Per-integration documentation

---

**Agent ID:** `integrations`  
**Allowlist:** Added to main agent's subagents  
**Created:** 2026-02-28
