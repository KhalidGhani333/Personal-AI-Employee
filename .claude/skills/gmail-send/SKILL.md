# Gmail Send Skill

## Purpose
Send real emails via Gmail SMTP. Production-ready email automation for AI Employee tasks.

## When to Use
- Send client emails after approval
- Automated notifications
- Status updates to stakeholders
- Report delivery

## Requirements
Environment variables in `.env`:
```
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

Note: Use Gmail App Password, not regular password. Generate at: https://myaccount.google.com/apppasswords

## Usage

```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Project Update" \
  --body "Email content here"
```

## Parameters
- `--to`: Recipient email (required)
- `--subject`: Email subject (required)
- `--body`: Email body text (required)
- `--cc`: CC recipients (optional, comma-separated)
- `--bcc`: BCC recipients (optional, comma-separated)

## Returns
- Exit code 0: Success
- Exit code 1: Error (check output for details)

## Integration Example
```python
import subprocess
result = subprocess.run([
    'python', '.claude/skills/gmail-send/scripts/send_email.py',
    '--to', 'client@example.com',
    '--subject', 'Status Update',
    '--body', 'Project completed successfully.'
])
if result.returncode == 0:
    print("Email sent successfully")
```
