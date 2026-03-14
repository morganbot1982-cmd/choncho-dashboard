# LEANTIME-PROTOCOL.md

## Overview

Leantime is a project management system designed around two core workflows:
- **🚀 MAKE** (execution): To-Dos, Milestones, Goals
- **🧠 THINK** (ideation): Ideas, Blueprints, Retrospectives

This protocol defines how Choncho should interact with Leantime to support Morgan's work.

---

## Core Concepts

### Tasks vs. Ideas vs. Subtasks

**TASKS (To-Dos)**
- Live in: 🚀 MAKE → To-Dos
- Purpose: Actionable work items with clear completion criteria
- Characteristics:
  - Have specific owners, due dates, and statuses
  - Move through workflow stages (New → In Progress → Done)
  - Can be organized into Milestones and Sprints
  - Support rich formatting and attachments
  - Can have subtasks (child tasks)

**IDEAS**
- Live in: 🧠 THINK → Ideas
- Purpose: Brainstorming, discussion, concept exploration
- Characteristics:
  - Less structured than tasks
  - Can evolve into tasks/milestones
  - Focus on collaboration and iteration
  - Not bound to strict timelines initially

**SUBTASKS**
- Live in: Parent task's "Subtasks" section
- Purpose: Break down complex tasks into smaller steps
- Characteristics:
  - Inherit project from parent
  - Can have own status, assignee, due date
  - Not meant to be standalone work items

---

## Task Anatomy

### Required Fields
1. **Headline**: Short, descriptive title (use emoji for visual scanning)
2. **Type**: Task (default), Milestone, Bug, Feature, etc.
3. **Status**: New, Blocked, In Progress, Waiting for Approval, Done
4. **Priority**: Low (1), Medium (2), High (3)

### Optional But Recommended
- **Description**: Rich HTML content (use `<br/>` for line breaks, `<strong>` for labels)
- **Due Date**: Target completion date/time
- **Assigned to**: Who owns this task
- **Milestone**: Which project phase this belongs to
- **Sprint**: Which sprint (for agile workflows)
- **Tags**: Keywords for filtering
- **Effort**: Size/complexity estimate

### Organization Fields
- **Project**: Which project this task belongs to
- **Related To**: Link to parent/related tasks
- **Collaborators**: Additional team members

### Schedule Fields
- **Work Start/End**: Planned work window
- **Planned Hours / Hours Left**: Time tracking

---

## What Makes a Task "Actionable"?

A well-formed Leantime task should have:

1. **Clear headline** with context
   - ✅ Good: "✅ STEP 7: Test MVP with Sample Data"
   - ❌ Bad: "Testing"

2. **Structured description** with:
   - Brief summary at top
   - Numbered steps or sections
   - Specific acceptance criteria ("✅ Done when:")
   - HTML formatting for readability

3. **Completion criteria** that's unambiguous
   - Not: "Make it work"
   - Yes: "All calculations are correct, drivers changes recalculate history, mobile works, no bugs found"

4. **Appropriate scope**
   - Small enough to complete in 1-2 work sessions
   - Large tasks should be broken into subtasks
   - Each task addresses ONE deliverable

5. **Proper metadata**
   - Status reflects reality (don't leave everything as "New")
   - Due date is realistic
   - Priority matches actual urgency

---

## Description Formatting Best Practices

Leantime uses a rich text editor that needs **HTML formatting** (not markdown).

### Template Structure
```html
Brief one-sentence summary of what this task does.<br/><br/>

<strong>Section 1: Context/Setup</strong><br/>
- Bullet point 1<br/>
- Bullet point 2<br/>
<br/>

<strong>Section 2: Steps</strong><br/>
1. First step<br/>
2. Second step<br/>
   • Sub-item (use bullet symbol)<br/>
   • Sub-item<br/>
<br/>

<strong>✅ Done when:</strong><br/>
Clear completion criteria
```

### Formatting Rules
- **Line breaks**: Use `<br/>` (NOT `\n`)
- **Bold labels**: Use `<strong>Label:</strong>` 
- **Paragraph breaks**: Use `<br/><br/>`
- **Bullets**: Use `•` or `-` manually (not `<ul>/<li>`)
- **Emoji**: Work perfectly (✅ → ⚠️ 📊 🎯 etc.)

### Example (Observed Pattern)
```html
Build the monthly calendar view showing daily profit data.<br/><br/>

<strong>Go to:</strong> Design tab<br/>
<br/>

<strong>1. Create new page:</strong><br/>
- Add new page, name it "Monthly"<br/>
- Update navigation tabs: [Today] [Monthly] [Drivers]<br/>
<br/>

<strong>2. Add month selector at top:</strong><br/>
- Dropdown element showing current month/year<br/>
- Previous/Next arrow buttons: [← February] [April →]<br/>
<br/>

<strong>✅ Done when:</strong><br/>
Calendar shows all days with profit amounts, colors work, monthly totals are correct, can click days for details
```

---

## Headline Best Practices

### Use Emoji for Visual Scanning
Common patterns observed:
- ✅ Completion/testing tasks
- 📅 Calendar/date-related
- 🎛️ Dashboard/UI building
- 🧮 Calculations/logic
- 🔧 Configuration/setup
- 🎯 Core features
- 🗄️ Database/data structure
- 📋 Documentation/lists
- 🚀 Launch/deploy tasks
- ⚠️ Blockers/warnings

### Use STEP Numbering for Sequential Work
When tasks must be done in order:
- "🗄️ STEP 1: Set Up Database Structure"
- "🎯 STEP 2: Build the TODAY Dashboard Page"
- "🔧 STEP 3: Make the Popup Form"
- etc.

This makes it clear:
- Tasks are part of a sequence
- The order matters
- Progress through phases

---

## Parent/Child Task Structure

### When to Use Subtasks
- A task has 3+ discrete steps that could be done separately
- Different people might own different parts
- You want to track progress within a larger task
- Steps might have different completion dates

### When NOT to Use Subtasks
- Task is already small/focused
- Steps must be done atomically
- Description with numbered steps is sufficient

### Creating Subtasks
1. Open parent task
2. Scroll to "Subtasks" section
3. Click "Add Task"
4. Subtasks inherit the parent's project but can have own:
   - Status
   - Assignee
   - Due date
   - Priority

---

## Kanban vs. Table vs. List Views

**Kanban (default)**: Best for visual workflow management
- Columns: New → Blocked → In Progress → Waiting for Approval → Done
- Drag tasks between columns to update status
- See task cards with description preview, due date, priority
- Filter and group by milestone, assignee, tags

**Table**: Best for bulk editing and data entry
- Spreadsheet-like view
- Quick inline editing
- Sort and filter by any field
- Export to CSV

**List**: Best for focused work lists
- Simple vertical list
- Shows more detail per task
- Good for daily planning

---

## Calendar Integration

Leantime has calendar functionality:
- Tasks with due dates appear on the calendar
- Can view by day/week/month
- Useful for deadline visibility
- Not a replacement for To-Do list (calendar is read-only view)

---

## Project Setup Template

### 1. Create Project (SQL)
```sql
INSERT INTO zp_projects (name, details, clientId, state) VALUES (
  '🎯 Project Name',
  'Brief description.<br/><br/><strong>Field:</strong> Details<br/><strong>Field:</strong> Details',
  1, 0
);
SET @projectId = LAST_INSERT_ID();
INSERT INTO zp_relationuserproject (userId, projectId, projectRole) VALUES (1, @projectId, 'owner');
```

### 2. Define Project Background
Use HTML formatting in `details` field:
```html
Brief project summary sentence.<br/><br/>

<strong>Target Market:</strong> Who is this for?<br/>
<strong>Key Features:</strong><br/>
- Feature 1<br/>
- Feature 2<br/>
<br/>

<strong>Tech Stack:</strong> Technologies used<br/>
<strong>Status:</strong> Current state
```

### 3. Create Initial Milestones (Optional)
- Phase 1: Discovery
- Phase 2: Build
- Phase 3: Launch
- (Or use sprints for agile workflows)

### 4. Populate Initial Tasks
Use the task creation SQL pattern (see next section)

---

## Task Creation Rules

### Via SQL (Bulk Operations)
```sql
INSERT INTO zp_tickets (projectId, headline, description, status, priority, userId, type, date, dateToFinish) VALUES
(@projectId, '✅ Task Headline', 
 'Summary.<br/><br/><strong>Field:</strong> Detail<br/><strong>Field:</strong> Detail', 
 3, 2, 1, 'task', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY));
```

**Critical field values:**
- `status = 3` (New/Open)
- `priority = 1` (Low), `2` (Medium), `3` (High)
- `userId = 1` (Morgan)
- `type = 'task'` (REQUIRED - without this, tasks won't show in UI)
- `date` and `dateToFinish` must be set (use NOW() + interval)

### Via UI (Individual Tasks)
1. Navigate to project → To-Dos
2. Click "+ New"
3. Fill in:
   - Headline
   - Description (use rich text editor)
   - Status, Priority, Due Date
   - Type = Task
4. Save

### Verification Checklist
After creating tasks (especially via SQL):
1. ✅ MySQL command includes `--default-character-set=utf8mb4`
2. ✅ Emoji in task headlines render correctly
3. ✅ HTML formatting in descriptions (`<br/>` and `<strong>`)
4. ✅ All required fields present
5. ✅ **Open browser and verify tasks show in UI**
6. ✅ Check at least one task description renders properly
7. ✅ Only then claim "done"

**Never claim completion without browser verification.**

---

## Integration Protocol: How Choncho Reads/Updates Leantime

### Session Start Workflow

**Every time Choncho starts a session with Morgan:**

1. **Read today's + yesterday's memory** (`memory/YYYY-MM-DD.md`)
2. **Check Leantime for active work**:
   ```sql
   SELECT id, headline, status, priority, dateToFinish
   FROM zp_tickets 
   WHERE userId = 1 
     AND status IN (3, 4, 5) -- New, In Progress, Blocked
   ORDER BY priority DESC, dateToFinish ASC
   LIMIT 10;
   ```

3. **Greet Morgan with context**:
   ```
   "Here's where we left off:
   - 🎨 Clarity: 7 tasks in progress (STEP 7 due tomorrow)
   - 🔧 AI Bookkeeping: 2 blockers need attention
   - 🖼️ Icon Press: 5 tasks ready to start
   
   Which project do you want to work on?"
   ```

4. **Don't just sit idle** - be proactive with status

### During Session: Task Updates

**When Morgan completes work:**
1. Update task status via SQL:
   ```sql
   UPDATE zp_tickets 
   SET status = 7, -- Done
       dateFinish = NOW()
   WHERE id = [TASK_ID];
   ```

2. Log to memory:
   ```
   DONE: ✅ STEP 7 testing completed (Clarity project)
   ```

**When blockers arise:**
1. Update status to Blocked (6):
   ```sql
   UPDATE zp_tickets 
   SET status = 6 
   WHERE id = [TASK_ID];
   ```

2. Add comment explaining blocker (if using UI)

### Session End Workflow

**Before ending a session:**

1. **Verify all task updates were saved**
   - Run query to check status changes applied
   - Confirm no orphaned work

2. **Update memory with session summary**:
   ```
   ## 2026-03-11 Session Summary
   
   ### Completed
   - ✅ STEP 7: MVP testing (Clarity)
   
   ### In Progress
   - 🔧 Setup database migration (AI Bookkeeping)
   
   ### Blocked
   - 📊 Dashboard widget - waiting on API access
   
   ### Next Session
   - Continue AI Bookkeeping migration
   - Review Icon Press backlog
   ```

3. **No loose ends** - every started task has a status update

---

## Reading Tasks for Context

### Query Patterns

**Get all open tasks for Morgan:**
```sql
SELECT t.id, t.headline, t.description, t.status, t.priority, 
       t.dateToFinish, p.name as project_name
FROM zp_tickets t
JOIN zp_projects p ON t.projectId = p.id
WHERE t.userId = 1 
  AND t.status < 7 -- Not done
ORDER BY t.priority DESC, t.dateToFinish ASC;
```

**Get tasks by project:**
```sql
SELECT id, headline, status, dateToFinish
FROM zp_tickets
WHERE projectId = [PROJECT_ID]
  AND status < 7
ORDER BY dateToFinish ASC;
```

**Get overdue tasks:**
```sql
SELECT id, headline, dateToFinish
FROM zp_tickets
WHERE userId = 1
  AND dateToFinish < NOW()
  AND status < 7
ORDER BY priority DESC;
```

### Parsing Task Descriptions

When reading a task to understand what needs doing:
1. Extract the summary (first sentence/paragraph)
2. Look for numbered steps or sections
3. Find the "✅ Done when:" criteria
4. Note any prerequisites or blockers
5. Check for related tasks (via description or Related To field)

---

## Common Pitfalls & How to Avoid Them

### ❌ Mistake: Creating tasks without `type = 'task'`
**Why it fails**: Tasks won't appear in UI  
**Fix**: Always set `type = 'task'` in SQL inserts

### ❌ Mistake: Using `\n` for line breaks in descriptions
**Why it fails**: Leantime renders HTML, not plain text  
**Fix**: Use `<br/>` instead

### ❌ Mistake: Forgetting to set `date` and `dateToFinish`
**Why it fails**: Tasks may not show in some views  
**Fix**: Always set both fields (use NOW() + interval)

### ❌ Mistake: Not verifying in browser after SQL inserts
**Why it fails**: Database success ≠ UI rendering success  
**Fix**: Always open browser and check tasks show correctly

### ❌ Mistake: Creating overly broad tasks
**Why it fails**: No clear completion criteria, hard to track progress  
**Fix**: Break into subtasks or use STEP numbering

### ❌ Mistake: Ignoring status updates
**Why it fails**: Kanban board doesn't reflect reality  
**Fix**: Update status as work progresses (In Progress → Done)

### ❌ Mistake: Using Ideas when you mean Tasks
**Why it fails**: Ideas don't have workflow/completion tracking  
**Fix**: Ideas = brainstorm, Tasks = actionable work

---

## When to Use Each Feature

### Use To-Dos (Tasks) when:
- Work is clearly defined
- You know who should do it
- It has a completion date
- Status tracking matters

### Use Ideas when:
- Exploring possibilities
- Brainstorming with team
- Concept isn't ready to execute
- Discussion needed before committing

### Use Milestones when:
- Organizing work into phases
- Setting major deadlines
- Grouping related tasks
- Tracking progress toward big goals

### Use Subtasks when:
- Parent task has 3+ distinct steps
- Steps could be done by different people
- You want granular progress tracking
- Parts have different due dates

### Use Sprints when:
- Following agile/scrum methodology
- Working in time-boxed iterations
- Want burndown charts
- Team velocity matters

---

## Example: Full Workflow

**Scenario**: Morgan asks Choncho to set up a new project for "Client Portal"

### Step 1: Create Project
```sql
INSERT INTO zp_projects (name, details, clientId, state) VALUES (
  '🔐 Client Portal',
  'Self-service portal for clients to view invoices, update details, and track projects.<br/><br/><strong>Target Users:</strong> Existing clients<br/><strong>Tech:</strong> Next.js + Supabase<br/><strong>Launch:</strong> Q2 2026',
  1, 0
);
SET @projectId = LAST_INSERT_ID();
INSERT INTO zp_relationuserproject (userId, projectId, projectRole) VALUES (1, @projectId, 'owner');
```

### Step 2: Create Initial Tasks
```sql
INSERT INTO zp_tickets (projectId, headline, description, status, priority, userId, type, date, dateToFinish) VALUES
(@projectId, '🗄️ STEP 1: Set up database schema', 
 'Define database structure for client data.<br/><br/><strong>Tables needed:</strong><br/>- clients<br/>- invoices<br/>- projects<br/><br/><strong>✅ Done when:</strong> Schema created, migrations run, can insert test data',
 3, 3, 1, 'task', NOW(), DATE_ADD(NOW(), INTERVAL 3 DAY)),

(@projectId, '🔐 STEP 2: Build authentication', 
 'Set up Supabase auth with email/password.<br/><br/><strong>Requirements:</strong><br/>- Login page<br/>- Password reset<br/>- Session management<br/><br/><strong>✅ Done when:</strong> Clients can log in, stay logged in, reset password',
 3, 3, 1, 'task', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY)),

(@projectId, '📊 STEP 3: Build invoice viewer', 
 'Display invoices in clean, printable format.<br/><br/><strong>UI needs:</strong><br/>- List of all invoices<br/>- Filter by date/status<br/>- View/download PDF<br/><br/><strong>✅ Done when:</strong> Clients can see invoices, filter, and download PDFs',
 3, 2, 1, 'task', NOW(), DATE_ADD(NOW(), INTERVAL 10 DAY));
```

### Step 3: Verify in Browser
```
Open http://localhost:8080/tickets/showKanban
Switch to Client Portal project
Confirm 3 tasks show in "New" column
Click one task to verify description renders correctly
```

### Step 4: Update Memory
```
## 2026-03-11 Work Log

### Created
- 🔐 Client Portal project with 3 initial tasks (STEP 1-3)

### Next
- Start STEP 1 database work tomorrow
```

### Step 5: During Work Session
```sql
-- When Morgan starts STEP 1
UPDATE zp_tickets SET status = 5 WHERE id = [STEP_1_ID]; -- In Progress

-- When completed
UPDATE zp_tickets SET status = 7, dateFinish = NOW() WHERE id = [STEP_1_ID]; -- Done
```

---

## Choncho's Leantime Responsibilities

### ✅ Always Do
- Verify tasks in browser after SQL operations
- Use HTML formatting in descriptions
- Set all required fields (type, status, dates)
- Update task status as work progresses
- Log task changes to memory
- Check for overdue/blocked tasks at session start
- Provide context on current work state

### ❌ Never Do
- Create tasks without completion criteria
- Leave tasks in "New" when work is in progress
- Forget to set due dates
- Use markdown instead of HTML
- Claim "done" without browser verification
- Create orphaned subtasks (always link to parent)
- Ignore status updates

---

## Quick Reference: SQL Commands

### Create Project
```sql
INSERT INTO zp_projects (name, details, clientId, state) VALUES 
('🎯 Project', 'Description with <br/> breaks', 1, 0);
SET @projectId = LAST_INSERT_ID();
INSERT INTO zp_relationuserproject (userId, projectId, projectRole) 
VALUES (1, @projectId, 'owner');
```

### Create Task
```sql
INSERT INTO zp_tickets (projectId, headline, description, status, priority, userId, type, date, dateToFinish) VALUES
([ID], '✅ Task', 'Desc<br/><br/><strong>Done:</strong> Criteria', 3, 2, 1, 'task', NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY));
```

### Update Task Status
```sql
-- In Progress
UPDATE zp_tickets SET status = 5 WHERE id = [ID];

-- Done
UPDATE zp_tickets SET status = 7, dateFinish = NOW() WHERE id = [ID];

-- Blocked
UPDATE zp_tickets SET status = 6 WHERE id = [ID];
```

### Query Tasks
```sql
-- Morgan's open tasks
SELECT id, headline, status, dateToFinish FROM zp_tickets 
WHERE userId = 1 AND status < 7 
ORDER BY priority DESC;

-- Project tasks
SELECT id, headline, status FROM zp_tickets 
WHERE projectId = [ID] AND status < 7;

-- Overdue
SELECT id, headline, dateToFinish FROM zp_tickets 
WHERE userId = 1 AND dateToFinish < NOW() AND status < 7;
```

---

## Final Notes

**This protocol is living documentation.** As Morgan and Choncho use Leantime more, patterns will emerge and this document should be updated to reflect what actually works.

Key principles:
1. **Actionable over aspirational** - tasks should have clear next steps
2. **Context over cryptic** - descriptions should be self-explanatory
3. **Status reflects reality** - Kanban should match actual work state
4. **Completion criteria matter** - "Done when:" is non-negotiable
5. **Verify before claiming done** - browser check every SQL operation

**When in doubt:** Look at working examples in existing projects (Clarity, AI Bookkeeping Service) and follow their patterns.

---

*Protocol created: 2026-03-11*  
*Last updated: 2026-03-11*  
*Author: Choncho (Leantime exploration subagent)*
