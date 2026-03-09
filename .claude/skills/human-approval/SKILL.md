# Human Approval Skill

## Purpose
Human-in-the-loop approval for sensitive actions. Blocks execution until human provides explicit approval or rejection.

## When to Use
- Send important emails
- Make financial transactions
- Delete data
- Publish content
- Any action requiring human oversight

## Folder Structure
```
AI_Employee_Vault/
└── Needs_Approval/  # Approval requests placed here
```

## Usage

```bash
# Request approval
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Send email to client" \
  --details "Subject: Project Update\nTo: client@example.com" \
  --timeout 3600
```

## Parameters
- `--action`: Brief action description (required)
- `--details`: Full action details (required)
- `--timeout`: Seconds to wait (default: 3600 = 1 hour)

## Human Workflow
1. Script creates file in Needs_Approval/
2. Human opens file and reviews
3. Human adds line: `APPROVED` or `REJECTED`
4. Human saves file
5. Script detects decision and returns

## Returns
- Exit code 0: APPROVED
- Exit code 1: REJECTED
- Exit code 2: TIMEOUT

## Integration Example
```python
import subprocess
result = subprocess.run([
    'python', '.claude/skills/human-approval/scripts/request_approval.py',
    '--action', 'Send client email',
    '--details', 'Email content...'
])
if result.returncode == 0:
    # Proceed with action
    send_email()
```
