# Vault File Manager Skill

## Purpose
Manage task workflow by moving files between vault folders. Handles task lifecycle from inbox to completion.

## When to Use
- Move processed tasks to Done
- Organize files by status
- Clean up completed work
- Automate file workflow

## Folder Structure
```
AI_Employee_Vault/
├── Inbox/          # New incoming tasks
├── Needs_Action/   # Active tasks requiring work
└── Done/           # Completed tasks
```

## Usage

```bash
# Move file to Done
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "task.md" \
  --from "Needs_Action" \
  --to "Done"

# Move from Inbox to Needs_Action
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "new_task.md" \
  --from "Inbox" \
  --to "Needs_Action"
```

## Parameters
- `--file`: Filename to move (required)
- `--from`: Source folder (Inbox, Needs_Action, or Done)
- `--to`: Destination folder (Inbox, Needs_Action, or Done)

## Returns
- Exit code 0: File moved successfully
- Exit code 1: Error (file not found, invalid folder, etc.)

## Integration Example
```python
import subprocess
result = subprocess.run([
    'python', '.claude/skills/vault-file-manager/scripts/move_task.py',
    '--file', 'completed_task.md',
    '--from', 'Needs_Action',
    '--to', 'Done'
])
```
