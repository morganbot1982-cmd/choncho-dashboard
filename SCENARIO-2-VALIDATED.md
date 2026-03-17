# 📋 Scenario 2: New Idea (No Project Yet) - VALIDATED

**Status:** Ready for implementation
**Date:** 2026-03-17 5:45 PM

---

## 🎯 GOAL

Capture new ideas and convert them into tracked projects with proper setup, seamlessly bridging from conversation to structured work.

---

## 🔄 THE COMPLETE WORKFLOW

### 🎬 STEP 1: IDEA CAPTURE

**When:** Morgan mentions a new idea

**Typical triggers:**
- "I've got an idea I'd like us to work on..."
- "What if we built..."
- "I'm thinking about..."
- (Often happens via WhatsApp, before bed or in car)

**Agent response:**
- Listen and engage
- Ask clarifying questions
- Don't create anything yet

---

### 💭 STEP 2: DISCUSSION & BRAINSTORMING

**What happens:**
- Discuss the idea
- Refine the concept
- **Agent identifies logical next steps** (becomes initial checklist items)

**Example:**
```
Morgan: "I want to build a receipt scanner for tradies"
Agent: "Interesting. So we'd need:
1. OCR integration (Claude vision vs Mindee?)
2. WhatsApp webhook to receive photos
3. Xero API connection for posting transactions
Want to make this a tracked project?"
```

**Key:** Agent proposes checklist items during discussion, not after project creation

---

### ✅ STEP 3: PROJECT CREATION (When Morgan confirms)

**Agent asks:**
```
Ready to create project "Receipt Scanner"?

**Initial checklist:**
1. Research OCR libraries (Claude vision vs Mindee)
2. Set up WhatsApp webhook handler
3. Design receipt data structure
4. Connect Xero API for transaction posting

**Is this a code-based project?** (will create git repo + README)
**Priority:** low | medium | high | critical
```

**Morgan provides:**
- Confirmation
- Code-based: yes/no
- Priority level

---

### 🛠️ STEP 4: CREATION EXECUTION

**What agent creates (in order):**

#### 1. Dashboard Project
`POST http://localhost:3004/api/projects`

```json
{
  "title": "Receipt Scanner",
  "summary": "AI-powered OCR for tradies receipts. WhatsApp photo → Claude vision → Xero posting.",
  "stage": "active",
  "priority": "high",
  "tags": ["ocr", "whatsapp", "ai", "bookkeeping", "tradies"]
}
```

**Tags auto-generated** from discussion keywords

#### 2. Checklist Items
`POST http://localhost:3004/api/projects/{projectId}/checklist` (for each)

```json
{"text": "Research OCR libraries (Claude vision vs Mindee)"}
{"text": "Set up WhatsApp webhook handler"}
{"text": "Design receipt data structure"}
{"text": "Connect Xero API for transaction posting"}
```

**REQUIRED:** text field must be present

#### 3. Rolling Summary Note
`POST http://localhost:3004/api/projects/{projectId}/notes`

```json
{
  "kind": "summary",
  "title": "Project summary",
  "content": "Receipt Scanner - AI-powered OCR for tradies receipts. WhatsApp photo → Claude vision → Xero posting. Initial discussion identified 4 key components: OCR integration, WhatsApp webhook, receipt data structure, and Xero API connection.",
  "pinned": true
}
```

**REQUIRED:** kind, content
**MUST BE:** kind="summary", pinned=true

#### 4. MEMORY.md Handoff Entry
Add to `## Project Handoff` section:

```markdown
### Receipt Scanner
- **Last worked:** 2026-03-17 5:45 PM
- **Session key:** agent:main:whatsapp:direct:+61402666843
- **Dashboard:** proj-abc123 → `curl -s http://localhost:3004/api/projects/proj-abc123`
- **Repo:** ~/.openclaw/workspace/receipt-scanner
- **GitHub:** (to be added)
```

#### 5. Git Repo (if code-based project)
```bash
mkdir ~/.openclaw/workspace/receipt-scanner
cd ~/.openclaw/workspace/receipt-scanner
git init
echo "# Receipt Scanner

AI-powered OCR for tradies receipts.

## Overview
WhatsApp photo → Claude vision → Xero posting

## Components
- OCR integration
- WhatsApp webhook
- Receipt data structure
- Xero API connection
" > README.md
git add README.md
git commit -m "Initial commit: project setup"
```

#### 6. Confirmation
```
✅ Project "Receipt Scanner" created:
- Dashboard: proj-abc123
- 4 checklist items added
- Rolling summary created
- Git repo initialized at ~/.openclaw/workspace/receipt-scanner

Ready to work. Which checklist item first?
```

Then immediately transition to Scenario 1 workflow (working on existing project)

---

## 🎯 WHAT GETS POPULATED

### Kanban View:
- ✅ Project card with title + summary
- ✅ Stage: "active"
- ✅ Priority badge (color)
- ✅ Tag pills (auto-generated)

### Project Workspace View:

**Chat tab:**
- Empty (no messages yet)

**Memory tab:**
- ✅ Rolling summary note (pinned)

**Deliverables tab:**
- Empty initially

**Files tab:**
- Empty initially

**Checklist tab:**
- ✅ All initial checklist items from discussion (unchecked)

**Activity tab:**
- Auto-populated:
  - "Project created"
  - "Checklist item added" (x{N})
  - "Memory note saved"

---

## 🔄 CRON JOB DISCOVERY (Dynamic)

**Problem:** Hardcoded project mappings break when new projects are created

**Solution:** Dynamic discovery using BOTH dashboard + MEMORY.md

### Cron Job Project Discovery Flow:

**1. Get all projects from dashboard:**
```bash
curl -s http://localhost:3004/api/projects | jq -r '.projects[] | "\(.id)|\(.title)"'
```
Returns: proj-abc123|Receipt Scanner, proj-11adb2ec|Clarat, etc.

**2. Read MEMORY.md for technical metadata:**
- Parse `## Project Handoff` section
- Extract repo paths, ports, GitHub URLs for each project

**3. Match work to projects:**
- For each session with work:
  - Check if messages mention project title
  - Check if file paths match repo path
  - Match to dashboard project

**4. For matched projects:**
- Update dashboard (summary, subtasks, notes)
- If repo path exists in MEMORY.md → check git + auto-commit docs
- If port exists → check dev server
- If no MEMORY.md entry → dashboard-only updates (graceful degradation)

**Benefits:**
- ✅ Dashboard = authoritative list of active projects
- ✅ MEMORY.md = technical metadata (repo, port, etc.)
- ✅ New projects auto-discovered
- ✅ Graceful handling of missing metadata
- ✅ No hardcoded mappings to maintain

---

## 🚧 EDGE CASES

### Idea mentioned but not ready to track
- Morgan describes idea
- Agent asks clarifying questions
- Morgan says "not yet, just thinking"
- Agent: don't create project, conversation ends

### Discussion doesn't identify clear subtasks
- Can't create project without at least 1-2 subtasks
- Agent: "I'm not sure what the first steps are. Can you help me break this down?"
- Continue discussion until subtasks emerge

### Non-code project
- Morgan confirms NOT code-based
- Skip git repo creation
- Dashboard + handoff still created
- Handoff has repo path but notes "(non-code project, no repo)"

### Project created but work never starts
- Dashboard has project in "active" stage
- No work detected by cron
- Project stays there until Morgan archives it or work begins
- No harm, just sits in kanban

---

## ✅ VALIDATION CHECKLIST

- [x] Workflow makes sense to Morgan
- [x] All dashboard fields populated correctly
- [x] MEMORY.md handoff structure defined
- [x] Git repo creation optional based on project type
- [x] Cron job can discover new projects dynamically
- [x] Edge cases handled
- [x] Smooth transition to Scenario 1 after creation

---

## 📋 IMPLEMENTATION TASKS

1. Add "New Project Creation Protocol" to AGENTS.md
2. Update cron job for dynamic project discovery (both sources)
3. Test end-to-end: idea → discussion → creation → work
4. Verify dashboard populated correctly (all tabs)
5. Verify MEMORY.md handoff entry created
6. Verify git repo created (if code project)
7. Verify cron discovers new project on next run
8. Document in MEMORY.md that Scenario 2 is live

