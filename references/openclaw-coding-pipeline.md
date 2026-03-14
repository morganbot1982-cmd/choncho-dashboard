# OpenClaw Coding Pipeline
**Source:** https://github.com/Clintos11/openclaw-coding-pipeline  
**Saved:** 2026-03-02  
**Status:** Will go private soon

---

# openclaw-coding-pipeline

A multi-agent coding pipeline for OpenClaw that orchestrates feature builds through 7 staged sub-agents with retry loops, structured context passing, and durable progress tracking.

## Pipeline Flow

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

Each stage runs as a separate sub-agent with its own persona, model assignment, and fresh context window. A durable progress file passes context between stages and enables recovery from stalls.

## How It Works

- You write a spec for the feature you want to build
- An orchestrator agent spawns, reading the spec
- The orchestrator runs 7 stages sequentially, spawning one child sub-agent per stage
- Each child reads a shared progress file for context from prior stages
- If a stage fails, the orchestrator retries by spawning a fix → re-verify cycle
- When all stages pass, you get a PR ready for merge

**Typical runtime:** 15–25 minutes for a medium feature.

## Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and running
- GitHub CLI (gh) authenticated (for PR creation)
- Git configured with push access to your repo
- At least 2 model providers configured (recommended: one strong reasoning model + one fast coding model)

## Installation

### 1. Create agent directories

```bash
# Create agent directories
for agent in planner setup developer verifier tester reviewer; do
  mkdir -p ~/.openclaw/agents/feature-dev-$agent/agent
  cp agents/$agent/SOUL.md ~/.openclaw/agents/feature-dev-$agent/agent/
  cp agents/$agent/IDENTITY.md ~/.openclaw/agents/feature-dev-$agent/agent/
  cp agents/$agent/AGENTS.md ~/.openclaw/agents/feature-dev-$agent/agent/
done

mkdir -p ~/.openclaw/agents/coding-orchestrator/agent
```

### 2. Create orchestrator AGENTS.md

Create `~/.openclaw/agents/coding-orchestrator/agent/AGENTS.md`:

```markdown
# Coding Orchestrator
You orchestrate multi-stage coding pipelines. You spawn child sub-agents for each stage, track progress via a durable progress file, and handle retries. You NEVER write code yourself.
```

### 3. Configure model assignments

Add per-agent model overrides under `agents.overrides`:

**Model rationale:** Strong reasoning models (Opus) for stages requiring architectural judgment (Plan, Verify, Review). Fast coding models (Codex) for mechanical implementation (Setup, Implement, Test, PR).

Substitute with whatever models you have access to — the pipeline is model-agnostic. Just ensure reasoning stages get your best model.

### 4. Update subagent allowlist

Ensure these agent IDs are in your subagent allowlist (if you use one):

```
coding-orchestrator
feature-dev-planner
feature-dev-setup
feature-dev-developer
feature-dev-verifier
feature-dev-tester
feature-dev-reviewer
```

### 5. Install skill

Copy SKILL.md to your skills directory:

```bash
mkdir -p ~/.openclaw/skills/coding-pipeline
cp SKILL.md ~/.openclaw/skills/coding-pipeline/
```

This lets your main agent auto-detect and use the pipeline when coding tasks come up.

## Usage

### Via Skill (Auto-detect)

Tell your OpenClaw agent:

> "Build [feature X] on [repo]. Here's the spec: [paste spec or path to spec file]."

If you have the skill installed, the agent will recognise it as a coding task and follow the pipeline automatically.

### Manual Spawn

```javascript
sessions_spawn({
  agentId: "coding-orchestrator",
  label: "my-feature",
  mode: "session", // CRITICAL: must be "session", not "run"
  task: `You are a coding pipeline orchestrator...` // See templates/orchestrator-prompt.md
})
```

⚠️ **Critical:** always use `mode: "session"`. `mode: "run"` is one-shot — the session closes after the first stage completes and the orchestrator can't receive results from subsequent stages.

### Recovery from Stalls

If the orchestrator stalls (no progress file update in 10+ minutes), send it:

> "Resume from progress file."

It reads the progress file, finds the next pending stage, and continues.

## Pipeline Stages

| # | Stage | Agent | Model | Purpose |
|---|-------|-------|-------|---------|
| 1 | Plan | feature-dev-planner | Reasoning | Decompose spec into ordered user stories |
| 2 | Setup | feature-dev-setup | Coding | Create branch, establish build/test baseline |
| 3 | Implement | feature-dev-developer | Coding | Build each story, write tests, commit |
| 4 | Verify | feature-dev-verifier | Reasoning | Quality gate: diff review, security, tests |
| 5 | Test | feature-dev-tester | Coding | Integration/E2E testing |
| 6 | PR | feature-dev-developer | Coding | Push branch, create GitHub PR |
| 7 | Review | feature-dev-reviewer | Reasoning | Final code review, merge readiness |

## Retry Logic

- Verify fail → Implement fix (max 2 retries) → re-Verify
- Test fail (branch-caused) → Implement fix (max 1 retry) → re-Test
- Review changes requested → Implement fix (max 1 retry) → re-Review
- Exceeds retry limit → escalate to parent with full context

## Progress File

The durable contract between stages. Located at `<repo>/progress-<branch-name>.md`.

Every stage reads it before starting and writes to it after completing. Contains:

- Stage statuses (pass/fail)
- Key decisions and context
- Files changed
- Codebase patterns discovered
- Blockers and issues

This is the recovery mechanism — not session memory. If the orchestrator restarts, it rebuilds state entirely from this file.

## Repository Structure

```
├── README.md # This file
├── SKILL.md # OpenClaw skill definition
├── LICENSE # MIT
├── agents/
│ ├── planner/
│ │ ├── SOUL.md # Persona: methodical architect
│ │ ├── IDENTITY.md # Name + role
│ │ └── AGENTS.md # Detailed instructions
│ ├── setup/ # Environment prep agent
│ ├── developer/ # Implementation agent
│ ├── verifier/ # Quality gate agent
│ ├── tester/ # Integration test agent
│ └── reviewer/ # Code review agent
├── templates/
│ └── orchestrator-prompt.md # Full orchestrator spawn template
└── examples/
 └── spawn-example.md # Copy-paste spawn example
```

## Hard-Won Lessons

These are hard-won from real pipeline runs:

- `mode: "session"` is non-negotiable for orchestrators. `mode: "run"` dies mid-pipeline.
- Progress file is the source of truth, not session memory. Always read it first.
- One stage per turn, then yield. Never sleep, poll, or spawn multiple stages at once.
- Never implement code as the orchestrator. Only orchestrate.
- Security checks are non-negotiable gates — .gitignore, no secrets, input validation.
- Don't mix concerns in PRs — separate backend/frontend when scope is large.
- Fresh context per child is a feature — the progress file is the handoff contract.
- Monitor for staleness — no progress file update in 10 min likely means a stall.
- Always push to feature branches and create PRs — never merge to main locally.
- Let automated review bots check PRs before force-merging — adds a valuable safety layer.

## Repo-Agnostic Design

This pipeline is repo-agnostic. To use it on any project:

- Write a spec for what you want built
- Update the orchestrator prompt template with your repo path, branch name, and spec path
- Spawn the orchestrator

The agents discover build commands, test commands, and code conventions from the repo itself. No project-specific configuration needed beyond the spec.

## License

MIT
