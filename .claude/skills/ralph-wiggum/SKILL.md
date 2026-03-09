# Ralph Wiggum Autonomous Loop

**Autonomous task execution system with safety features**

---

## Overview

Ralph Wiggum Loop is an autonomous task execution system that automatically processes tasks from the Needs_Action folder. It analyzes tasks, creates execution plans, executes steps, and moves completed tasks to Done - all with built-in safety features.

---

## Features

### Autonomous Execution
- Automatically detects new tasks
- Analyzes task requirements
- Creates execution plans
- Executes steps sequentially
- Moves completed tasks to Done

### Safety Features
- **Max 5 iterations** per task
- **Human approval** for risky operations
- **Risky keyword detection** (delete, remove, sudo, etc.)
- **Automatic approval requests** for sensitive actions
- **State persistence** across runs

### Task Analysis
- Automatic task type detection (email, social, accounting, etc.)
- Priority determination (high, medium, low)
- Risk assessment
- Step estimation

### Plan Generation
- Creates detailed execution plans
- Breaks tasks into steps
- Identifies approval requirements
- Logs execution progress

---

## Usage

### Manual Execution
```bash
# Process one task
python scripts/ralph_wiggum_loop.py

# Run continuously (checks every 60 seconds)
python scripts/ralph_wiggum_loop.py continuous
```

### Via Skill
```
/ralph-wiggum
```

### Automatic (Scheduled)
Ralph runs automatically via the scheduler every 15 minutes.

---

## How It Works

### Workflow

```
1. Check Needs_Action folder
   ↓
2. Get next task
   ↓
3. Analyze task
   - Determine type
   - Assess risk
   - Estimate steps
   ↓
4. Create Plan.md
   - Break into steps
   - Identify approvals needed
   ↓
5. Execute steps (max 5 iterations)
   ↓
   For each step:
   - Check if risky
   - Request approval if needed
   - Execute action
   - Log result
   ↓
6. Move to Done
   ↓
7. Update state
```

### Safety Checks

**Before Execution:**
- Check for risky keywords
- Assess operation type
- Determine if approval needed

**During Execution:**
- Max 5 iterations enforced
- Approval required for:
  - Risky operations (delete, remove, etc.)
  - Social media posts (always)
  - File operations with risky keywords
  - Any operation with admin/sudo

**After Execution:**
- State saved
- Logs updated
- Task moved to appropriate folder

---

## Task Types

Ralph automatically detects and handles:

### Email Tasks
- Extracts recipient, subject, body
- Validates email format
- Sends via Business MCP
- Logs activity

### Social Media Tasks
- Extracts content and platform
- Validates content length
- **Always requires approval**
- Posts via Social/Business MCP

### Accounting Tasks
- Extracts amount, type, description
- Validates transaction
- Records via accounting manager
- Updates Current_Month.md

### File Management Tasks
- Identifies files
- Performs operations
- Requires approval if risky
- Uses File MCP

### General Tasks
- Analyzes requirements
- Creates custom plan
- Executes with safety checks

---

## Risky Operations

Ralph automatically detects risky keywords and requests approval:

**Risky Keywords:**
- delete, remove, drop, truncate, destroy
- format, wipe, erase, reset, force
- sudo, admin, root, password, credential

**Approval Process:**
1. Ralph detects risky operation
2. Creates approval request in Needs_Approval/
3. Pauses task execution
4. Waits for human decision
5. Resumes based on approval status

---

## State Management

Ralph maintains state in `Logs/ralph_state.json`:

```json
{
  "current_task": "task_name.md",
  "iteration": 3,
  "started_at": "2026-02-25T15:00:00",
  "completed_tasks": [
    {
      "task": "send_email.md",
      "completed_at": "2026-02-25T15:05:00",
      "iterations": 3
    }
  ],
  "failed_tasks": []
}
```

---

## Generated Files

### Execution Plans
**Location:** `AI_Employee_Vault/Plans/Plan_<task_name>.md`

**Format:**
```markdown
# Execution Plan: Task Name

**Created:** 2026-02-25 15:00:00
**Task Type:** email
**Priority:** medium
**Risky:** No
**Estimated Steps:** 3

---

## Original Task
[Task content]

---

## Execution Steps

### Step 1: Extract Email Details
**Action:** Parse recipient, subject, and body
**Expected Result:** Email details extracted
**Status:** Pending

### Step 2: Validate Email
**Action:** Verify email format
**Expected Result:** Email validated
**Status:** Pending

### Step 3: Send Email
**Action:** Use Business MCP to send
**Expected Result:** Email sent successfully
**Status:** Pending

---

## Execution Log
[Updated during execution]
```

### Approval Requests
**Location:** `AI_Employee_Vault/Needs_Approval/APPROVAL_<timestamp>_<task>.md`

**Format:**
```markdown
---
action: Send email to all@company.com
task: send_announcement
created: 2026-02-25T15:00:00
status: pending
---

# Approval Required

## Task
send_announcement

## Action
Send email to all@company.com

## Reason
This operation requires human approval for safety

## Decision Required
Please update status to:
- `status: approved`
- `status: rejected`
```

---

## Configuration

### Max Iterations
Default: 5 iterations per task

Change in `ralph_wiggum_loop.py`:
```python
MAX_ITERATIONS = 5  # Adjust as needed
```

### Risky Keywords
Add/remove keywords in `ralph_wiggum_loop.py`:
```python
RISKY_KEYWORDS = [
    'delete', 'remove', 'drop',
    # Add more...
]
```

### Check Interval (Continuous Mode)
Default: 60 seconds

```bash
# Custom interval (in seconds)
python scripts/ralph_wiggum_loop.py continuous
```

---

## Integration

### With Scheduler
Ralph runs automatically every 15 minutes via `scripts/scheduler.py`.

### With Error Recovery
Ralph integrates with the error recovery system for automatic retry on failures.

### With MCP Servers
Ralph uses:
- Business MCP (email, LinkedIn, logging)
- Social MCP (social media posting)
- File MCP (file operations)
- Accounting Manager (financial transactions)

---

## Examples

### Example 1: Email Task

**Task File:** `Needs_Action/send_client_update.md`
```markdown
Send email to client@example.com

Subject: Project Update
Body: The project is on track and will be delivered next week.
```

**Ralph's Process:**
1. Analyzes: Type=email, Priority=medium, Risky=no
2. Creates Plan_send_client_update.md
3. Executes:
   - Step 1: Extract details ✓
   - Step 2: Validate email ✓
   - Step 3: Send email ✓
4. Moves to Done/
5. Logs success

**Result:** Email sent, task completed in 3 iterations

---

### Example 2: Social Media Task (Requires Approval)

**Task File:** `Needs_Action/linkedin_announcement.md`
```markdown
Post to LinkedIn:

Excited to announce our new product launch! 🚀
```

**Ralph's Process:**
1. Analyzes: Type=social_media, Priority=medium, Risky=no
2. Creates Plan_linkedin_announcement.md
3. Executes:
   - Step 1: Extract content ✓
   - Step 2: Validate content ✓
   - Step 3: Post to LinkedIn → **Requires Approval**
4. Creates APPROVAL_<timestamp>_linkedin_announcement.md
5. Pauses and waits

**Human Action:** Review and approve/reject

**After Approval:**
6. Resumes execution
7. Posts to LinkedIn ✓
8. Moves to Done/
9. Logs success

---

### Example 3: Risky Task (Requires Approval)

**Task File:** `Needs_Action/cleanup_old_files.md`
```markdown
Delete all files older than 30 days from the archive folder.
```

**Ralph's Process:**
1. Analyzes: Type=file_management, Priority=medium, **Risky=YES** (keyword: delete)
2. Creates Plan_cleanup_old_files.md
3. Executes:
   - Step 1: Identify files ✓
   - Step 2: Perform operation → **Requires Approval** (risky)
4. Creates approval request
5. Pauses and waits

**Human Action:** Review and approve/reject

**Safety:** Ralph won't delete anything without explicit approval

---

## Logs

### Ralph Log
**Location:** `Logs/ralph_wiggum.log`

**Format:**
```
2026-02-25 15:00:00 - RalphWiggum - INFO - Processing task: send_email.md
2026-02-25 15:00:01 - RalphWiggum - INFO - Analyzed task: send_email (Type: email, Risky: False)
2026-02-25 15:00:02 - RalphWiggum - INFO - Created plan: Plan_send_email.md
2026-02-25 15:00:03 - RalphWiggum - INFO - Executing step: Extract Email Details
2026-02-25 15:00:04 - RalphWiggum - INFO - Step 1/3 completed
2026-02-25 15:00:05 - RalphWiggum - INFO - Task completed: send_email.md
```

---

## Best Practices

### Task Creation
- Use clear, specific task descriptions
- Include all necessary details
- Specify recipients, subjects, amounts, etc.
- Avoid ambiguous instructions

### Approval Management
- Review approval requests promptly
- Check task details before approving
- Reject if unsure or risky
- Update status clearly (approved/rejected)

### Monitoring
- Check `Logs/ralph_wiggum.log` regularly
- Review `Logs/ralph_state.json` for status
- Monitor Needs_Approval/ folder
- Verify completed tasks in Done/

---

## Troubleshooting

### Task Not Processing
- Check if task file is in Needs_Action/
- Verify file has .md extension
- Check ralph_wiggum.log for errors
- Ensure Ralph is running (scheduler or manual)

### Task Stuck
- Check ralph_state.json for current status
- Look for approval requests in Needs_Approval/
- Verify iteration count < 5
- Check for errors in logs

### Approval Not Working
- Ensure approval file exists in Needs_Approval/
- Verify status field is updated correctly
- Check file format (YAML frontmatter)
- Restart Ralph if needed

---

## Safety Guarantees

✓ **Max 5 iterations** - Prevents infinite loops
✓ **Approval for risky ops** - Human oversight required
✓ **Keyword detection** - Automatic risk assessment
✓ **State persistence** - Recovers from crashes
✓ **Comprehensive logging** - Full audit trail
✓ **Social media approval** - Always requires human review

---

## Summary

Ralph Wiggum Loop provides autonomous task execution with enterprise-grade safety features. It automatically processes tasks while ensuring human oversight for risky operations, maintaining detailed logs, and enforcing iteration limits.

**Key Benefits:**
- Autonomous operation
- Safety-first design
- Human approval for risky actions
- Comprehensive logging
- State persistence
- Integration with existing systems

**Use Cases:**
- Automated email sending
- Social media posting (with approval)
- File management
- Accounting transactions
- Report generation
- General task automation

---

**Ready for production use with built-in safety features!** ✓
