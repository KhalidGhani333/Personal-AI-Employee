# Dashboard Updater - Implementation Instructions

## Overview

Updates Dashboard.md with recent email processing activity for audit trail and transparency.

## Step-by-Step Process

### Step 1: Read Current Dashboard

**What to do**: Read existing Dashboard.md file

**Location**: `AI_Employee_Vault/Dashboard.md`

**How to do it**: Use Read tool with absolute path

### Step 2: Find Recent Activity Section

**What to do**: Locate the "## Recent Activity" section in Dashboard.md

**If section doesn't exist**: Create it at the end of the file

### Step 3: Format New Activity Entry

**Format**: `- [YYYY-MM-DD HH:MM] Activity description`

**Examples**:
- `- [2026-02-19 10:35] Email processed from client@example.com: "Project Update Required"`
- `- [2026-02-19 10:30] Email detected from sender@example.com`
- `- [2026-02-19 10:40] Plan created: PLAN_20260219_103000_project-update.md`

### Step 4: Append New Entry

**What to do**: Add new entry to the top of the activity list (most recent first)

**How to do it**: Use Edit tool to insert new line after "## Recent Activity" header

### Step 5: Prune Old Entries

**What to do**: Keep only last 10 activity entries

**How to do it**: Count lines in activity section, remove oldest if > 10

## Output Format

```markdown
## Recent Activity

- [2026-02-19 10:40] Plan created: PLAN_20260219_103000_project-update.md
- [2026-02-19 10:35] Email processed from client@example.com: "Project Update Required"
- [2026-02-19 10:30] Email detected from sender@example.com
- [2026-02-19 09:15] Email processed from team@example.com: "Weekly Sync"
- [2026-02-19 09:10] Email detected from team@example.com
- [2026-02-19 08:45] Email processed from boss@example.com: "Budget Review"
- [2026-02-19 08:40] Email detected from boss@example.com
- [2026-02-18 17:30] Email processed from client2@example.com: "Invoice #123"
- [2026-02-18 17:25] Email detected from client2@example.com
- [2026-02-18 16:00] Email processed from support@example.com: "Ticket Update"
```

## Error Handling

**Dashboard.md not found**: Create new Dashboard.md with activity section
**Section not found**: Append "## Recent Activity" section to file
**Edit failure**: Log error, retry once

## Testing

Test with:
- Empty Dashboard.md (create section)
- Dashboard with existing activities (append)
- Dashboard with 10+ activities (prune oldest)
