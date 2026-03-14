# Example: Spawning a Pipeline Run

## Scenario

You want to add a user dashboard with an activity feed to your Next.js app at `/home/user/projects/my-app`.

## Step 1: Write a spec

Create `specs/user-dashboard.md` in your repo:

```markdown
# User Dashboard

## Overview
Add a user dashboard page at `/dashboard` showing recent activity and account settings.

## Requirements
- Activity feed showing last 20 actions (DB-backed)
- Settings panel for display name and email preferences
- Responsive layout (mobile-first)
- API routes: GET /api/activity, PATCH /api/settings

## Technical Notes
- Use existing auth middleware for route protection
- Activity stored in `activity` table (user_id, action, timestamp, metadata JSON)
- Settings stored in existing `users` table (add columns if needed)
```

## Step 2: Spawn the orchestrator

```javascript
sessions_spawn({
  agentId: "coding-orchestrator",
  label: "user-dashboard",
  mode: "session",
  task: `You are a coding pipeline orchestrator. Run the following task through staged child subagents.
Each stage MUST be a separate sessions_spawn child subagent — do not implement stages yourself.

### CRITICAL: Execution Model
- You are a PERSISTENT SESSION. You will receive auto-announce messages when children complete.
- Spawn ONE child subagent per turn, then yield (stop generating).
- When the child completes, you will receive its result as a new message. Read it, update progress file, spawn next stage.
- If you receive a "Resume from progress file" message, read the progress file and continue from the next pending stage.
- NEVER sleep, poll, or implement code yourself.

### Context
- Repo: /home/user/projects/my-app
- Branch: feature/user-dashboard (create from main)
- Spec: specs/user-dashboard.md
- Scope: Add user dashboard with activity feed and settings panel

### Progress File
Write progress to: /home/user/projects/my-app/progress-feature-user-dashboard.md
This is your source of truth. Update after EVERY stage. If you restart, rebuild state from this file.

### Stages
Run in order: PLAN → SETUP → IMPLEMENT → VERIFY → TEST → PR → REVIEW

Agent IDs per stage:
- PLAN: feature-dev-planner
- SETUP: feature-dev-setup
- IMPLEMENT: feature-dev-developer
- VERIFY: feature-dev-verifier
- TEST: feature-dev-tester
- PR: feature-dev-developer
- REVIEW: feature-dev-reviewer

### Retry Rules
- VERIFY fail → IMPLEMENT fix (max 2x) → re-VERIFY
- TEST fail (branch-caused) → IMPLEMENT fix (max 1x) → re-TEST
- REVIEW changes_requested → IMPLEMENT fix (max 1x) → re-REVIEW

After all stages pass, announce: summary, PR URL, merge readiness.`
})
```

## Step 3: Wait

The pipeline runs autonomously. Typical runtime: 15–25 minutes.

You'll receive an announcement when it completes with:
- Summary of what was built
- PR URL
- Merge readiness assessment

## Step 4: Recovery (if needed)

If the orchestrator goes quiet for 10+ minutes, send it:

```
Resume from progress file.
```

It reads `progress-feature-user-dashboard.md` and picks up from the next pending stage.
