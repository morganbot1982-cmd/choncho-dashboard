# Leantime Integration Reference

## Overview

**Service:** Leantime (open-source project management)  
**Version:** Latest (Docker)  
**Setup:** Docker Compose with MySQL backend  
**Base URL:** http://localhost:8080  
**Auth:** Session-based (login form) + API key for programmatic access

## Known Issues & Gotchas

### ⚠️ CRITICAL: User Assignment

**Problem:** Creating projects via API does NOT automatically assign the creator as a project member.

**Symptom:** Projects exist in database but user can't see them in UI (empty dashboard).

**Root cause:** Leantime API creates project record but skips `zp_relationuserproject` table insertion.

**Fix:** Manually insert user-to-project relationship via database:
```sql
INSERT INTO zp_relationuserproject (userId, projectId, projectRole)
VALUES ({{USER_ID}}, {{PROJECT_ID}}, 'owner');
```

**Prevention:** After creating project via API, ALWAYS verify user can see it in UI before proceeding.

### Ghost Users ("Peak Workshop")

**Problem:** Easy to accidentally create multiple clients/users during setup testing.

**Prevention:**
- Use morganbot1982@gmail.com as the ONLY user
- Use "Leif Oh Leif Distribution" (or Morgan's business name) as the ONLY client
- Check for ghosts: `SELECT * FROM zp_user;` and `SELECT * FROM zp_clients;`
- Delete ghosts immediately if found

## Docker Setup

### docker-compose.yml Structure

```yaml
services:
  leantime:
    image: leantime/leantime:latest
    ports:
      - "8080:80"
    environment:
      LEAN_DB_HOST: leantime-db
      LEAN_DB_USER: leantime
      LEAN_DB_PASSWORD: leantime
      LEAN_DB_DATABASE: leantime
      LEAN_SESSION_PASSWORD: changeme
      LEAN_SESSION_SALT: changemetoo
    depends_on:
      - leantime-db

  leantime-db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: leantime
      MYSQL_USER: leantime
      MYSQL_PASSWORD: leantime
    volumes:
      - leantime-db-data:/var/lib/mysql

volumes:
  leantime-db-data:
```

### Common Commands

```bash
# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f leantime
docker compose logs -f leantime-db

# Access MySQL directly
docker compose exec -T leantime-db mysql -uleantime -pleantime leantime

# Restart after config change
docker compose restart leantime

# Full reset (⚠️ DESTROYS DATA)
docker compose down -v
```

## Database Schema (Key Tables)

### zp_user
```sql
CREATE TABLE zp_user (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255),
  firstname VARCHAR(255),
  lastname VARCHAR(255),
  user VARCHAR(255), -- This is the EMAIL
  password VARCHAR(255),
  clientId INT,
  ...
);
```

### zp_clients
```sql
CREATE TABLE zp_clients (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  ...
);
```

### zp_projects
```sql
CREATE TABLE zp_projects (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255),
  clientId INT,
  details TEXT,
  state INT,
  ...
);
```

### zp_relationuserproject (THE CRITICAL ONE)
```sql
CREATE TABLE zp_relationuserproject (
  id INT PRIMARY KEY AUTO_INCREMENT,
  userId INT,
  projectId INT,
  projectRole VARCHAR(50) -- 'owner', 'member', etc.
);
```

**This table controls who can see which projects.** Missing entry = invisible project.

## API Reference

### Authentication

**Method:** API Key (preferred for automation)

Generate key in UI: User Settings → API Key

**Header:** `Authorization: Bearer {{API_KEY}}`

OR session-based (login form, cookies).

### Common Endpoints

**Create Project:**
```http
POST /api/jsonrpc
Content-Type: application/json

{
  "method": "leantime.rpc.Projects.addProject",
  "params": {
    "project": {
      "name": "Project Name",
      "details": "Description",
      "clientId": 1,
      "state": 0
    }
  },
  "id": 1,
  "jsonrpc": "2.0"
}
```

**⚠️ Remember:** After creating, you MUST assign user to project via database.

**Create Task:**
```http
POST /api/jsonrpc

{
  "method": "leantime.rpc.Tickets.addTicket",
  "params": {
    "ticket": {
      "headline": "Task Name",
      "description": "Details",
      "projectId": 3,
      "status": 3,
      "userId": 1
    }
  },
  "id": 1,
  "jsonrpc": "2.0"
}
```

**List Projects:**
```http
POST /api/jsonrpc

{
  "method": "leantime.rpc.Projects.getUserProjects",
  "params": {
    "userId": 1
  },
  "id": 1,
  "jsonrpc": "2.0"
}
```

## Debugging Checklist

When Leantime isn't working:

```
□ Is Docker container running? (docker compose ps)
□ Can you reach http://localhost:8080? (curl or browser)
□ Can Leantime reach MySQL? (check logs for connection errors)
□ Are environment variables set? (docker compose exec leantime env | grep LEAN_)
□ Can you login? (test in browser first)
□ After creating project, did you assign user? (check zp_relationuserproject)
□ Are there ghost users/clients? (SELECT from zp_user and zp_clients)
```

## Validation Queries

```sql
-- Check users (should be ONLY Morgan)
SELECT id, username, firstname, lastname, user FROM zp_user;

-- Check clients (should be ONLY Morgan's business)
SELECT id, name FROM zp_clients;

-- Check projects
SELECT id, name, clientId, state FROM zp_projects;

-- Check user-project assignments (critical!)
SELECT u.user, p.name, r.projectRole 
FROM zp_relationuserproject r
JOIN zp_user u ON r.userId = u.id
JOIN zp_projects p ON r.projectId = p.id;

-- Delete ghost user
DELETE FROM zp_user WHERE user != 'morganbot1982@gmail.com';

-- Delete ghost client
DELETE FROM zp_clients WHERE id != 1; -- Assuming Morgan's business is ID 1
```

## Rollback / Clean Start

```bash
# Full nuke (⚠️ DESTROYS ALL DATA)
docker compose down -v
docker compose up -d

# Then recreate single user setup from scratch
```

## Expected State (Clean Setup)

After proper setup, queries should show:

```
zp_user: 1 row (morganbot1982@gmail.com)
zp_clients: 1 row (Leif Oh Leif Distribution)
zp_projects: N rows (Morgan's actual projects)
zp_relationuserproject: N rows (one per project, all assigned to Morgan)
```

## Migration Notes (Feb 26, 2026)

**Previous setup had:**
- Ghost client "Peak Workshop"
- Projects assigned to Peak Workshop
- Morgan couldn't see projects in dashboard

**Fix applied:**
- Direct database INSERT into zp_relationuserproject
- Projects became visible

**Lesson:** API project creation is incomplete. Always verify user assignment.
