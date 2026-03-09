# Task Planner Skill

## Description
Analyzes new markdown files in the Inbox and creates detailed step-by-step execution plans. This skill reads task files, extracts requirements, and generates structured plans that are placed in the Needs_Action folder for execution.

## When to Trigger
Use this skill when:
- New .md files appear in `AI_Employee_Vault/Inbox`
- User says "plan the tasks" or "analyze inbox"
- Automated by vault-watcher when new files are detected
- User wants to create execution plans for pending tasks
- Need to process and organize incoming task files

## Trigger Phrases
- "Plan the tasks"
- "Analyze inbox files"
- "Create task plans"
- "Process inbox"
- "Run task planner"

## How It Works
1. Scans `AI_Employee_Vault/Inbox` for new .md files
2. Reads and analyzes each file's content
3. Extracts key information (title, description, requirements)
4. Creates a structured Plan.md with:
   - Task summary
   - Step-by-step execution plan
   - Priority assessment
   - Resource requirements
   - Success criteria
5. Saves Plan.md to `AI_Employee_Vault/Needs_Action`
6. Moves processed inbox file to `AI_Employee_Vault/Done`
7. Logs all actions to `logs/actions.log`
8. Tracks processed files to ensure idempotency

## Execution

### Process All Inbox Files
```bash
python scripts/task_planner.py
```

### Process Specific File
```bash
python scripts/task_planner.py --file "filename.md"
```

### Dry Run (No File Moves)
```bash
python scripts/task_planner.py --dry-run
```

## Output Structure

Each processed task generates a Plan.md file in Needs_Action:

```markdown
---
type: execution_plan
source_file: original_filename.md
created_at: 2026-02-20 10:30:00
status: pending
priority: medium
---

# Execution Plan: [Task Title]

## Task Summary
[Brief overview of what needs to be done]

## Step-by-Step Plan
1. [First action step]
2. [Second action step]
3. [Continue...]

## Requirements
- [Resource or dependency 1]
- [Resource or dependency 2]

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Notes
[Additional context or considerations]
```

## Integration

This skill integrates with:
- **vault-watcher**: Automatically triggered when new files arrive
- **vault-file-manager**: Moves processed files to Done folder
- **Action logging**: All operations logged to logs/actions.log

## Idempotency

The skill maintains a processed files registry at `logs/processed_inbox_files.txt` to ensure each file is only processed once, even if the script is run multiple times.

## Requirements
- Python 3.6+
- No external dependencies (standard library only)
- Folder structure: AI_Employee_Vault/{Inbox,Needs_Action,Done}

## Error Handling
- Gracefully handles missing folders (creates them)
- Logs errors without crashing
- Skips invalid or empty files
- Continues processing remaining files if one fails
