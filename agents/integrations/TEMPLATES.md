# Documentation Templates

Standard structures for integration documentation. Copy and customize for each integration.

---

## SETUP.md Template

```markdown
# {{INTEGRATION_NAME}} Setup

## Prerequisites

List what must be installed/configured before starting:
- Software dependencies (Docker, Node.js, Python, etc.)
- Accounts needed (developer accounts, API keys)
- Ports that must be available
- Other services that must be running first

## Installation

Step-by-step installation instructions:

1. **Step 1 name**
   ```bash
   command here
   ```
   
   Expected result: what should happen
   
2. **Step 2 name**
   ```bash
   another command
   ```
   
   Expected result: ...

## Configuration

Environment variables / config files:

```bash
# .env file or config location
VARIABLE_NAME=value_here
ANOTHER_VAR=another_value
```

Explanation of each variable:
- `VARIABLE_NAME`: What it controls, acceptable values
- `ANOTHER_VAR`: What it controls, acceptable values

## First-Time Setup

Special steps only needed once (account creation, OAuth, etc.):

1. Create account at {{PROVIDER_URL}}
2. Generate API credentials
3. Store credentials in {{LOCATION}}
4. Run authorization flow: {{COMMAND}}

## Verification

How to confirm it's working:

```bash
# Test command
curl http://localhost:{{PORT}}/health
```

Expected: `{"status": "ok"}`

## Access

- **URL**: http://localhost:{{PORT}}
- **User**: {{EMAIL}}
- **Password**: {{STORED_WHERE}}

## Next Steps

After initial setup:
- Read CONFIG.md for detailed configuration options
- Read TROUBLESHOOTING.md if you encounter issues
```

---

## CONFIG.md Template

```markdown
# {{INTEGRATION_NAME}} Configuration Reference

## Environment Variables

### Required

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `VAR_NAME` | What it does | none | `value` |
| `ANOTHER` | What it does | `default` | `example` |

### Optional

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `OPTIONAL_VAR` | What it does | `default` | `value` |

## Configuration Files

### File: {{PATH_TO_CONFIG}}

```json
{
  "setting1": "value",
  "setting2": 123
}
```

**Settings:**
- `setting1`: (string) What it controls
- `setting2`: (number) What it controls

## Docker Compose

Key sections explained:

```yaml
services:
  service-name:
    image: image:tag
    ports:
      - "8080:80"  # Host:Container
    environment:
      VAR: value   # Explanation
    volumes:
      - data:/path # Explanation
```

## Credential Storage

**Location**: {{WHERE_CREDS_STORED}}

**Structure**:
```json
{
  "key1": "value",
  "key2": "value"
}
```

**Security**: Permissions should be `chmod 600` (owner read/write only).

## Default Values

When not specified:
- Setting A defaults to: {{VALUE}}
- Setting B defaults to: {{VALUE}}

## Advanced Configuration

Optional/power-user settings:

### Feature X
Enable with: `FEATURE_X=true`

What it does: ...

### Feature Y
Configure via: {{CONFIG_FILE}}

Options: ...
```

---

## TROUBLESHOOTING.md Template

```markdown
# {{INTEGRATION_NAME}} Troubleshooting

## Quick Diagnostics

Run these commands to check status:

```bash
# Check if service is running
docker compose ps

# View recent logs
docker compose logs --tail 50 {{SERVICE_NAME}}

# Test connectivity
curl http://localhost:{{PORT}}/health
```

## Common Issues

### Issue: {{SYMPTOM_DESCRIPTION}}

**Symptom**: What the user sees/experiences

**Cause**: Why this happens

**Fix**:
```bash
commands to fix it
```

**Prevention**: How to avoid this in the future

**Related**: Links to similar issues or documentation

---

### Issue: {{ANOTHER_SYMPTOM}}

**Symptom**: ...

**Cause**: ...

**Fix**:
```bash
...
```

## Error Messages

### Error: "{{EXACT_ERROR_TEXT}}"

**Meaning**: Plain English explanation

**Check**:
1. First thing to verify
2. Second thing to verify
3. Third thing to verify

**Fix**: Command or procedure to resolve

---

### Error: "{{ANOTHER_ERROR}}"

**Meaning**: ...

**Check**: ...

**Fix**: ...

## Validation Queries

Useful commands to check state:

```bash
# Check database
docker compose exec db-service psql -U user -c "SELECT * FROM table;"

# Check files
ls -la /path/to/files

# Check environment
docker compose exec service env | grep VAR_NAME
```

## Getting Help

If none of the above solves your issue:

1. Capture full error: `docker compose logs {{SERVICE}} > error.log`
2. Check {{PROVIDER_DOCS_URL}} for known issues
3. Search GitHub issues: {{GITHUB_ISSUES_URL}}
4. Ask in {{COMMUNITY_CHANNEL}}

Include:
- Exact error message
- Steps to reproduce
- Output of diagnostic commands above
```

---

## ROLLBACK.md Template

```markdown
# {{INTEGRATION_NAME}} Rollback Procedures

## Restart Without Data Loss

```bash
docker compose restart {{SERVICE_NAME}}
```

Use when: Service crashed or needs config reload without losing data.

---

## Stop Service (Keeps Data)

```bash
docker compose stop {{SERVICE_NAME}}
```

Use when: Need to temporarily stop service but preserve all data.

To start again: `docker compose start {{SERVICE_NAME}}`

---

## Full Reset (⚠️ DESTROYS DATA)

```bash
docker compose down -v
```

Use when: Starting fresh, corrupted data, or testing clean install.

**Warning**: This deletes all volumes (database, uploads, etc.).

**Before running**:
1. Backup any important data
2. Confirm with user
3. Document what will be lost

To set up again: Follow SETUP.md from the beginning.

---

## Rollback Configuration Change

If a config change broke things:

1. Restore previous config:
   ```bash
   cp {{CONFIG_FILE}}.backup {{CONFIG_FILE}}
   ```

2. Restart service:
   ```bash
   docker compose restart {{SERVICE_NAME}}
   ```

3. Verify it's working:
   ```bash
   curl http://localhost:{{PORT}}/health
   ```

---

## Rollback Database Migration

If database schema change failed:

1. Restore from backup:
   ```bash
   docker compose exec db-service psql -U user db_name < backup.sql
   ```

2. Restart service:
   ```bash
   docker compose restart {{SERVICE_NAME}}
   ```

---

## Rollback OAuth/Credentials

If credentials are corrupted:

1. Delete current tokens:
   ```bash
   rm {{PATH_TO_TOKENS}}
   ```

2. Re-run authorization flow:
   ```bash
   {{AUTH_COMMAND}}
   ```

3. User approves in browser

4. New tokens saved automatically

---

## Emergency Stop All

If everything is broken and you need to stop immediately:

```bash
docker compose down
```

This stops all services but keeps data (volumes remain).

To start again: `docker compose up -d`

---

## Recovery Checklist

After any rollback:

```
□ Service is running (docker compose ps)
□ No errors in logs (docker compose logs --tail 20)
□ Health check passes (curl endpoint)
□ User can access UI/API
□ Data is intact (spot check critical records)
□ Document what went wrong in TROUBLESHOOTING.md
```
```

---

## Quick Reference

**When creating docs for a new integration:**

1. Copy these templates to `integrations/{{NAME}}/`
2. Replace `{{PLACEHOLDERS}}` with actual values
3. Fill in integration-specific details
4. Delete sections that don't apply
5. Add sections for integration-specific concerns

**Minimum viable documentation:**
- SETUP.md (how to install)
- ROLLBACK.md (how to undo)

**Nice to have:**
- CONFIG.md (what settings mean)
- TROUBLESHOOTING.md (common issues)

**Build as you go:** Update docs WHILE working, not after.
