# 📋 Scenario 2: New Idea (No Project Created Yet)

**Status:** DRAFT - Working through questions
**Date:** 2026-03-17 5:00 PM

---

## 🎯 GOAL

Define the workflow from "Morgan has an idea" → "Tracked project in dashboard with proper setup"

---

## ❓ KEY QUESTIONS TO ANSWER

### Q1: Who creates the dashboard project?

Options:
- A) Morgan tells agent "create a project called X" → agent creates via API
- B) Agent detects new work and auto-creates project
- C) Morgan creates manually in dashboard UI
- D) Any of these should work

**Morgan's answer:**

---

### Q2: When does the idea become a dashboard project?

- When Morgan first mentions it?
- When Morgan explicitly says "make this a project"?
- When code/work starts?
- When git repo is created?
- Some other trigger?

**Morgan's answer:**

---

### Q3: Where does the initial context go?

- Morgan describes idea in chat → agent populates dashboard summary?
- Morgan creates dashboard project with notes first?
- Agent captures chat context automatically?

**Morgan's answer:**

---

### Q4: When does git repo get created?

- Same time as dashboard project?
- Only when code work starts?
- Morgan decides manually?
- Agent auto-creates when needed?

**Morgan's answer:**

---

### Q5: What gets created in what order?

Typical sequence:
1. Idea mentioned in chat
2. Dashboard project created (?)
3. MEMORY.md handoff entry added (?)
4. Git repo initialized (?)
5. Initial files created (README, etc.) (?)

**What's the right sequence?**

---

### Q6: How does cron job discover new projects?

Current problem: cron has hardcoded mappings.

Options:
- A) Cron queries `/api/projects` to get ALL projects dynamically
- B) Agent tells cron about new projects somehow
- C) Cron scans MEMORY.md handoff section for new entries

**Which approach?**

---

## 🔄 POTENTIAL WORKFLOWS

### Option A: Agent-Driven
1. Morgan: "I have an idea for a receipt scanner app"
2. Agent: "Want to create a dashboard project for this?"
3. Morgan: "yes"
4. Agent:
   - Creates dashboard project via API
   - Adds MEMORY.md handoff entry
   - Creates git repo (mkdir + git init)
   - Creates README.md with initial context
   - Commits + pushes
5. Agent: "✅ Project created. Ready to work on it."

### Option B: Manual Dashboard First
1. Morgan opens dashboard UI
2. Creates new project: "Receipt Scanner"
3. Fills in initial notes
4. Closes dashboard
5. Morgan in chat: "work on receipt scanner"
6. Agent:
   - Finds project in dashboard by name
   - Adds MEMORY.md handoff entry if missing
   - Asks: "Need a git repo?"
   - If yes: creates repo + README + commit

### Option C: Auto-Detect
1. Morgan: "Let's build a receipt scanner"
2. Agent detects this is new work (not matching existing projects)
3. Agent: "This looks new. Create a dashboard project?"
4. Morgan: "yes"
5. Agent: same as Option A step 4

---

## 🚧 EDGE CASES TO HANDLE

- Idea mentioned but not ready to be tracked yet (just brainstorming)
- Dashboard project created but work never starts
- Git repo exists but no dashboard project
- Dashboard project exists but no git repo (non-code projects)
- Multiple ideas discussed in one session

---

## 📋 TO DO

1. Morgan answers Q1-Q6
2. Pick workflow option (A, B, or C)
3. Define step-by-step protocol
4. Update AGENTS.md with "New Project Protocol"
5. Update cron job to handle project discovery
6. Test end-to-end

