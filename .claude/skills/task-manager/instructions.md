# Task Manager - Implementation Instructions

## Overview

Creates Plan.md files in /Plans folder with actionable tasks from email analysis.

## Step-by-Step Process

### Step 1: Extract Tasks from Email Analysis

**What to do**: Identify actionable items from email analysis

**Look for**:
- Suggested actions list
- Deadlines mentioned
- Action verbs (reply, create, send, review)

### Step 2: Create Plan File

**What to do**: Generate Plan.md file in /Plans folder

**Filename format**: `PLAN_{timestamp}_{email_subject_slug}.md`

**Example**: `PLAN_20260219_103000_project-update.md`

### Step 3: Write Plan Content

**Template**:
```markdown
# Plan: [Email Subject]

**Created**: [Date and Time]
**Source**: [Email filename]
**From**: [Sender]
**Priority**: [High/Medium/Low]

## Tasks

- [ ] Task 1: [Description]
- [ ] Task 2: [Description]
- [ ] Task 3: [Description]

## Notes

[Any additional context from email]

## Deadline

[If mentioned in email]
```

### Step 4: Save to /Plans Folder

**Location**: `AI_Employee_Vault/Plans/PLAN_*.md`

**How to do it**: Use Write tool with absolute path

## Output Format

```markdown
# Plan: Q1 Report Request

**Created**: 2026-02-19 10:35 AM
**Source**: EMAIL_20260219_103000_a1b2c3d4.md
**From**: client@example.com
**Priority**: High

## Tasks

- [ ] Check if Q1 report is ready
- [ ] Prepare revenue breakdown section
- [ ] Add customer acquisition metrics
- [ ] Include operational expenses
- [ ] Reply to sender with status

## Notes

Board meeting tomorrow morning - urgent deadline.
Report should include revenue, customer metrics, and expenses.

## Deadline

Today 5:00 PM
```

## Error Handling

**No tasks identified**: Create plan with note to review email manually
**Invalid email source**: Log error, use generic source name
**Write failure**: Retry once, then log error

## Testing

Test with:
- Email with 3-5 clear action items
- Email with deadline
- Email with no clear actions (edge case)
