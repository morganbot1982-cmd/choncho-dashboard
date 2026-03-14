# Integration Examples

Full walkthroughs showing the Plan → Validate → Execute → Document → Clean Failures workflow in action.

---

## Example 1: Clean Leantime Setup from Scratch

**Goal:** Install Leantime with single user (morganbot1982@gmail.com), no ghost data.

### PLAN

**What we're doing:**
1. Stop existing Leantime (if running)
2. Nuke volumes to ensure clean start
3. Start fresh Leantime + MySQL
4. Create ONLY Morgan as user
5. Create ONLY Morgan's business as client
6. Create projects assigned to Morgan
7. Verify Morgan can login and see everything

**Destructive operations:** `docker compose down -v` (destroys all existing data)

**Confirm with Morgan:** "This will delete all current Leantime data. OK to proceed?"

### VALIDATE (Pre-flight)

**Check current state:**
```bash
# Is Leantime running?
docker compose ps | grep leantime

# Any volumes to destroy?
docker volume ls | grep leantime
```

**Expected:** Existing container + volume present.

### EXECUTE

**Step 1: Stop and nuke**
```bash
cd /Users/userclaw/.openclaw/workspace/projects/leantime
docker compose down -v
```

**Validation:** `docker compose ps` shows nothing.

**Step 2: Start fresh**
```bash
docker compose up -d
```

**Validation:**
```bash
docker compose ps  # Both containers running?
docker compose logs leantime | tail -20  # No errors?
curl http://localhost:8080  # Returns HTML?
```

**Step 3: Create single user via UI (first-run setup)**

*This step requires browser interaction - Leantime's first-run wizard.*

Open http://localhost:8080 in browser, complete setup:
- Email: morganbot1982@gmail.com
- Password: {{SECURE_PASSWORD}}
- Company: Leif Oh Leif Distribution
- Role: Owner

**Validation:** Can login successfully.

**Step 4: Create projects via API**

*Now that base user exists, use API for projects.*

```python
import requests

API_KEY = "get_from_ui_settings"
BASE_URL = "http://localhost:8080/api/jsonrpc"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

projects = [
    {"name": "Xero Accounting Cleanup", "details": "HIGH priority", "clientId": 1},
    {"name": "Health & Fitness Agent", "details": "Personal health tracking", "clientId": 1},
    {"name": "Ecommerce JV", "details": "Joint venture setup", "clientId": 1},
    {"name": "Task Copilot", "details": "AI task management", "clientId": 1},
    {"name": "Headwear Sample Range", "details": "Product samples", "clientId": 1}
]

for project in projects:
    payload = {
        "method": "leantime.rpc.Projects.addProject",
        "params": {"project": project},
        "id": 1,
        "jsonrpc": "2.0"
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    print(f"Created: {project['name']} - Status: {response.status_code}")
```

**Validation after each:** Check response.status_code == 200.

**Step 5: ⚠️ CRITICAL - Assign user to projects**

*API project creation does NOT auto-assign. Must do manually via database.*

```bash
# Get user ID
docker compose exec -T leantime-db mysql -uleantime -pleantime leantime -e \
  "SELECT id FROM zp_user WHERE user='morganbot1982@gmail.com';"

# Get project IDs
docker compose exec -T leantime-db mysql -uleantime -pleantime leantime -e \
  "SELECT id, name FROM zp_projects ORDER BY id;"

# Assign Morgan to all projects (assuming user ID = 1, project IDs = 1-5)
for project_id in {1..5}; do
  docker compose exec -T leantime-db mysql -uleantime -pleantime leantime -e \
    "INSERT INTO zp_relationuserproject (userId, projectId, projectRole) VALUES (1, $project_id, 'owner');"
done
```

**Validation:** Query back:
```bash
docker compose exec -T leantime-db mysql -uleantime -pleantime leantime -e \
  "SELECT u.user, p.name, r.projectRole FROM zp_relationuserproject r
   JOIN zp_user u ON r.userId = u.id
   JOIN zp_projects p ON r.projectId = p.id;"
```

**Expected:** 5 rows showing Morgan assigned to all projects.

**Step 6: Real test - Morgan can see projects**

Open http://localhost:8080 in browser, login as Morgan.

**Expected:** Dashboard shows all 5 projects. Tasks view is empty (normal). No "Peak Workshop" or ghost users visible.

### DOCUMENT

**Create SETUP.md:**
```markdown
# Leantime Setup

## Prerequisites
- Docker & Docker Compose installed
- Port 8080 available

## Installation
1. `cd /Users/userclaw/.openclaw/workspace/projects/leantime`
2. `docker compose up -d`
3. Open http://localhost:8080
4. Complete first-run wizard:
   - Email: morganbot1982@gmail.com
   - Company: Leif Oh Leif Distribution
5. After project creation via API, ALWAYS assign user via database:
   ```sql
   INSERT INTO zp_relationuserproject (userId, projectId, projectRole)
   VALUES (1, {{PROJECT_ID}}, 'owner');
   ```

## Access
- URL: http://localhost:8080
- User: morganbot1982@gmail.com
```

**Create TROUBLESHOOTING.md:**
```markdown
# Leantime Troubleshooting

## Projects not visible in dashboard

**Symptom:** Projects exist in database but don't show in UI.

**Cause:** User not assigned to project in `zp_relationuserproject` table.

**Fix:**
```sql
INSERT INTO zp_relationuserproject (userId, projectId, projectRole)
VALUES ({{USER_ID}}, {{PROJECT_ID}}, 'owner');
```

## Ghost users/clients present

**Check:**
```sql
SELECT * FROM zp_user;
SELECT * FROM zp_clients;
```

**Fix:** Delete any that aren't Morgan's:
```sql
DELETE FROM zp_user WHERE user != 'morganbot1982@gmail.com';
DELETE FROM zp_clients WHERE id != 1;
```
```

**Create ROLLBACK.md:**
```markdown
# Leantime Rollback

## Full reset (destroys all data)
```bash
cd /Users/userclaw/.openclaw/workspace/projects/leantime
docker compose down -v
```

## Restart without data loss
```bash
docker compose restart leantime
```
```

### CLEAN FAILURES

*(None in this case - setup succeeded.)*

If setup had failed at Step 5, rollback would be:
1. `docker compose down -v`
2. Document the failure in TROUBLESHOOTING.md
3. Provide Morgan with exact error + proposed fix

### COMPLETION CHECKLIST

```
✅ Morgan can login
✅ Morgan can see all 5 projects
✅ No ghost users (only morganbot1982@gmail.com)
✅ No ghost clients (only Leif Oh Leif Distribution)
✅ SETUP.md created
✅ TROUBLESHOOTING.md created
✅ ROLLBACK.md created
```

**Done.**

---

## Example 2: Debugging OAuth 401 Error

**Problem:** Xero API returning 401 Unauthorized.

### PLAN

**Hypothesis:** Access token expired (they only last 30 minutes).

**Steps:**
1. Check token file modification time
2. Attempt token refresh
3. Test API call with new token
4. If still fails, check tenant ID

**No destructive operations.**

### VALIDATE (Pre-flight)

**Check current state:**
```bash
# When was token last refreshed?
ls -l agents/accountant/config/xero_tokens.json

# What's in it? (don't log the actual tokens!)
cat agents/accountant/config/xero_tokens.json | jq '{expires_in, token_type}'
```

**Expected:** File is >30 minutes old → likely expired.

### EXECUTE

**Step 1: Attempt token refresh**

```python
import json
import urllib.request
import base64

# Load credentials
with open('agents/accountant/config/xero_credentials.json') as f:
    creds = json.load(f)

with open('agents/accountant/config/xero_tokens.json') as f:
    tokens = json.load(f)

# Prepare refresh request
auth_header = base64.b64encode(
    f"{creds['client_id']}:{creds['client_secret']}".encode()
).decode()

data = urllib.parse.urlencode({
    'grant_type': 'refresh_token',
    'refresh_token': tokens['refresh_token']
}).encode()

req = urllib.request.Request(
    "https://identity.xero.com/connect/token",
    data=data,
    headers={
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
)

try:
    resp = urllib.request.urlopen(req)
    new_tokens = json.loads(resp.read().decode())
    
    # Save new tokens
    with open('agents/accountant/config/xero_tokens.json', 'w') as f:
        json.dump(new_tokens, f, indent=2)
    
    print("✅ Token refreshed successfully")
except urllib.error.HTTPError as e:
    print(f"❌ Refresh failed: {e.code} {e.read().decode()}")
```

**Validation:** New tokens file created, `access_token` value changed.

**Step 2: Test API call**

```python
# Get tenant ID
req = urllib.request.Request(
    "https://api.xero.com/connections",
    headers={'Authorization': f"Bearer {new_tokens['access_token']}"}
)
resp = urllib.request.urlopen(req)
connections = json.loads(resp.read().decode())
tenant_id = connections[0]['tenantId']

print(f"✅ Tenant ID: {tenant_id}")

# Test actual API call (get accounts)
req = urllib.request.Request(
    "https://api.xero.com/api.xro/2.0/Accounts",
    headers={
        'Authorization': f"Bearer {new_tokens['access_token']}",
        'Xero-Tenant-Id': tenant_id,
        'Accept': 'application/json'
    }
)
resp = urllib.request.urlopen(req)
accounts = json.loads(resp.read().decode())

print(f"✅ Retrieved {len(accounts['Accounts'])} accounts")
```

**Validation:** Accounts retrieved successfully → OAuth working.

### DOCUMENT

**Update TROUBLESHOOTING.md:**
```markdown
## 401 Unauthorized from Xero API

**Cause:** Access token expired (30 minute lifespan).

**Fix:** Refresh token using refresh_token grant.

**Prevention:** Implement automatic refresh in API wrapper.
```

### CLEAN FAILURES

*(None - fix succeeded.)*

### COMPLETION CHECKLIST

```
✅ API calls working again
✅ New tokens saved
✅ TROUBLESHOOTING.md updated
```

**Done.**

---

## Example 3: Docker Container Won't Start

**Problem:** `docker compose up` fails, leantime container exits immediately.

### PLAN

**Hypothesis:** Missing environment variable or MySQL not ready.

**Steps:**
1. Check container logs
2. Check environment variables
3. Verify MySQL is accessible
4. Check docker-compose.yml for typos

### VALIDATE (Pre-flight)

```bash
# Container status
docker compose ps -a

# Recent logs
docker compose logs leantime --tail 50
```

**Expected:** Container in "Exit 1" state, logs show error.

### EXECUTE

**Step 1: Read logs**

```
leantime_1 | Fatal error: Uncaught PDOException: SQLSTATE[HY000] [2002] Connection refused
```

**Interpretation:** Leantime can't connect to MySQL.

**Step 2: Check MySQL status**

```bash
docker compose ps | grep leantime-db
```

**Result:** MySQL container also exited.

**Step 3: Check MySQL logs**

```bash
docker compose logs leantime-db --tail 50
```

**Result:**
```
[ERROR] --initialize specified but the data directory has files in it. Aborting.
```

**Diagnosis:** Volume has corrupted/partial data from previous failed start.

**Step 4: Fix - nuke volumes and restart**

```bash
docker compose down -v  # Destroys volumes
docker compose up -d
```

**Validation:**
```bash
docker compose ps  # Both running?
docker compose logs leantime | grep -i error  # No errors?
curl http://localhost:8080  # Returns HTML?
```

**Result:** ✅ Both containers running, Leantime accessible.

### DOCUMENT

**Update TROUBLESHOOTING.md:**
```markdown
## Container exits immediately with database connection error

**Symptom:** `docker compose up` fails, leantime exits with "Connection refused".

**Cause:** MySQL data directory corrupted or partially initialized.

**Fix:**
```bash
docker compose down -v  # ⚠️ Destroys all data
docker compose up -d
```

**Prevention:** Always use `docker compose down` (not `docker stop`) to stop services cleanly.
```

### CLEAN FAILURES

*(None - rollback successfully recovered.)*

### COMPLETION CHECKLIST

```
✅ Containers running
✅ Leantime accessible
✅ TROUBLESHOOTING.md updated
⚠️ Data lost (expected - clean start)
```

**Done.**

---

## Key Patterns from These Examples

1. **Always validate before and after each step** - Don't assume success
2. **Document failures immediately** - While debugging, capture exact errors in TROUBLESHOOTING.md
3. **Test with real usage** - "Morgan can see it" > "API returns 200"
4. **Clean up on failure** - Leave system in known state, not partial config
5. **Update docs while working** - Don't leave it for "later"
