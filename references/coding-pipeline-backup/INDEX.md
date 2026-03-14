# OpenClaw Coding Pipeline - Backup Archive

**Source:** https://github.com/Clintos11/openclaw-coding-pipeline  
**Saved:** 2026-03-02 13:51  
**Reason:** Repo going private soon

---

## Contents

### Core Documentation
- `SKILL.md` - OpenClaw skill definition (auto-detect coding tasks)
- `templates/orchestrator-prompt.md` - Full spawn template with placeholders

### Agent Definitions (7 specialized sub-agents)

Each agent has 3 files: SOUL.md (persona), IDENTITY.md (name/role), AGENTS.md (detailed instructions)

#### 1. Planner (feature-dev-planner)
- **Role:** Methodical architect  
- **Model:** Reasoning (Opus/high-thinking)
- **Job:** Decompose spec into ordered user stories
- Files: `agents/planner/`

#### 2. Setup (feature-dev-setup)
- **Role:** Environment prep specialist
- **Model:** Coding (Codex/fast)
- **Job:** Create branch, establish build/test baseline
- Files: `agents/setup/`

#### 3. Developer (feature-dev-developer)
- **Role:** Implementation specialist
- **Model:** Coding (Codex/fast)
- **Job:** Build features, write tests, commit
- Files: `agents/developer/`

#### 4. Verifier (feature-dev-verifier)
- **Role:** Quality gate enforcer
- **Model:** Reasoning (Opus/high-thinking)
- **Job:** Security checks, diff review, test validation
- Files: `agents/verifier/`

#### 5. Tester (feature-dev-tester)
- **Role:** Integration test specialist
- **Model:** Coding (Codex/fast)
- **Job:** E2E testing, cross-cutting concerns
- Files: `agents/tester/`

#### 6. PR Creator (feature-dev-developer, reused)
- **Role:** Git/GitHub specialist
- **Model:** Coding (Codex/fast)
- **Job:** Push branch, create GitHub PR
- Files: `agents/developer/` (same as #3)

#### 7. Reviewer (feature-dev-reviewer)
- **Role:** Final code reviewer
- **Model:** Reasoning (Opus/high-thinking)
- **Job:** Security, performance, merge readiness
- Files: `agents/reviewer/`

### Pipeline Flow

```
PLAN → SETUP → IMPLEMENT → VERIFY → TEST → PR → REVIEW
 ↑ | | |
 └───────────┘ | |
 (max 2 retries) | |
 ↑ | |
 └───────────────────┘ |
 (max 1 retry) |
 ↑ |
 └──────────────────────────────┘
 (max 1 retry)
```

### Key Features

- **Durable progress file** - Survives restarts, enables recovery
- **Retry loops** - Automatic fix → re-verify cycles
- **Model assignment** - Reasoning for architecture, coding for implementation
- **Repo-agnostic** - Discovers build/test commands from any project
- **15-25 min runtime** - For medium features

### Installation Summary

```bash
# 1. Create agent directories
for agent in planner setup developer verifier tester reviewer; do
  mkdir -p ~/.openclaw/agents/feature-dev-$agent/agent
  cp agents/$agent/*.md ~/.openclaw/agents/feature-dev-$agent/agent/
done

mkdir -p ~/.openclaw/agents/coding-orchestrator/agent

# 2. Create orchestrator AGENTS.md
echo "# Coding Orchestrator\nYou orchestrate multi-stage coding pipelines..." > \
  ~/.openclaw/agents/coding-orchestrator/agent/AGENTS.md

# 3. Install skill
mkdir -p ~/.openclaw/skills/coding-pipeline
cp SKILL.md ~/.openclaw/skills/coding-pipeline/

# 4. Update openclaw.json with agent allowlist + model overrides
```

### Usage Example

```javascript
sessions_spawn({
  agentId: "coding-orchestrator",
  label: "feature/user-dashboard",
  mode: "session",  // CRITICAL: persistent, not "run"
  task: `<filled orchestrator template from templates/orchestrator-prompt.md>`
})
```

### Hard-Won Lessons

- `mode: "session"` is non-negotiable (not "run")
- Progress file is source of truth (not session memory)
- One stage per turn, then yield
- Never implement code as orchestrator
- Security checks are gates, not optional
- Monitor for staleness (10+ min no progress = stall)

### Files Archived

- **Total:** 21 markdown files, 108KB
- **Agent files:** 18 (6 agents × 3 files each)
- **Templates:** 1 orchestrator prompt
- **Documentation:** README + SKILL + this INDEX
- **Examples:** spawn examples

---

## To Use This Archive

1. Copy agent files to `~/.openclaw/agents/`
2. Copy SKILL.md to `~/.openclaw/skills/coding-pipeline/`
3. Update your `openclaw.json` with agent IDs and model assignments
4. Use the orchestrator template to spawn pipelines

**Repo will go private soon - this is your permanent backup!**
