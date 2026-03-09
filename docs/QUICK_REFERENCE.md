# Quick Reference Card - AI Employee

## Essential Commands

### System Control
```bash
# Start daemon (continuous operation)
python scripts/run_ai_employee.py --daemon

# Run once (single execution)
python scripts/run_ai_employee.py --once

# Check status
python scripts/run_ai_employee.py --status

# Stop daemon
Ctrl+C
```

### Skills Usage

#### Send Email
```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "recipient@example.com" \
  --subject "Subject" \
  --body "Message"
```

#### Post to LinkedIn
```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --content "Your post content"
```

#### Move Files
```bash
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "filename.md" \
  --from "Inbox" \
  --to "Done"
```

#### Request Approval
```bash
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Action description" \
  --details "Full details"
```

### Monitoring

```bash
# View logs
tail -f logs/ai_employee.log
tail -f logs/actions.log

# Check inbox
ls AI_Employee_Vault/Inbox/

# Check pending tasks
ls AI_Employee_Vault/Needs_Action/

# Check completed
ls AI_Employee_Vault/Done/
```

## Folder Structure

```
AI_Employee_Vault/
├── Inbox/          → Drop new tasks here
├── Needs_Action/   → Active tasks/plans
├── Needs_Approval/ → Awaiting human decision
└── Done/           → Completed tasks
```

## Exit Codes

- 0 = Success
- 1 = Error/Rejected
- 2 = Timeout
- 3 = File not found

## Common Workflows

### Auto-process tasks
```bash
python scripts/run_ai_employee.py --daemon
# Drop files in Inbox/ - processed every 5 min
```

### Manual processing
```bash
echo "# Task" > AI_Employee_Vault/Inbox/task.md
python scripts/run_ai_employee.py --once
```

### Send approved email
```bash
# 1. Request approval
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Send email" --details "Content..."

# 2. Open file, add APPROVED, save

# 3. Send email
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "user@example.com" --subject "Hi" --body "Message"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Gmail auth failed | Check .env, use app password |
| Lock file error | `rm logs/ai_employee.lock` |
| Permission denied | Run as admin / `chmod +x` |

## Environment Variables

Required in `.env`:
```
EMAIL_ADDRESS=your@gmail.com
EMAIL_PASSWORD=app-password-here
LINKEDIN_EMAIL=your@linkedin.com
LINKEDIN_PASSWORD=your-password
```
