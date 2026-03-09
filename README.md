# AI Employee - Bronze & Silver Tier

Complete automation system for task management, email sending, social media posting, and workflow orchestration.

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Credentials
```bash
# Copy example file
copy .env.example .env

# Edit .env and add:
# - Gmail email and app password
# - LinkedIn credentials (optional)
```

### 3. Test the System
```bash
# Check status
python scripts/run_ai_employee.py --status

# Create test task
echo "# Test Task" > AI_Employee_Vault/Inbox/test.md

# Process it
python scripts/run_ai_employee.py --once
```

### 4. Start Automation
```bash
# Run continuously (checks every 5 minutes)
python scripts/run_ai_employee.py --daemon
```

## 📚 Documentation

- **[Complete Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[Gmail Setup](docs/GMAIL_SETUP.md)** - How to get Gmail app password
- **[LinkedIn Setup](docs/LINKEDIN_SETUP.md)** - LinkedIn automation notes
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command cheat sheet

## 🎯 What This System Does

### Bronze Tier (Basic Automation)
- ✓ File monitoring and task generation
- ✓ Manual task processing
- ✓ Error logging and management
- ✓ Basic workflow automation

### Silver Tier (Advanced Automation)
- ✓ Automated scheduling (daemon mode)
- ✓ Intelligent task analysis and planning
- ✓ Gmail email automation
- ✓ LinkedIn post automation
- ✓ Human approval workflows
- ✓ File workflow management
- ✓ Status monitoring and reporting

## 🛠️ Available Skills

### Orchestration
- **vault-watcher** - Real-time file monitoring
- **task-planner** - Intelligent task analysis
- **silver-scheduler** - Workflow orchestration

### Production Actions
- **gmail-send** - Send emails via SMTP
- **linkedin-post** - Post to LinkedIn
- **vault-file-manager** - Manage task files
- **human-approval** - Human-in-the-loop decisions

## 📁 Project Structure

```
Bronze/
├── scripts/                    # Main automation scripts
│   ├── run_ai_employee.py     # Orchestrator (daemon/once/status)
│   ├── task_planner.py        # Task analyzer
│   ├── watch_inbox.py         # Real-time monitor
│   └── request_approval.py    # Approval handler
├── .claude/skills/            # 22 production skills
│   ├── gmail-send/
│   ├── linkedin-post/
│   ├── vault-file-manager/
│   └── human-approval/
├── AI_Employee_Vault/         # Task workflow folders
│   ├── Inbox/                 # Drop new tasks here
│   ├── Needs_Action/          # Active tasks
│   ├── Needs_Approval/        # Awaiting approval
│   └── Done/                  # Completed tasks
├── logs/                      # System logs
├── docs/                      # Documentation
└── .env                       # Credentials (create from .env.example)
```

## 🔧 Common Commands

```bash
# System Control
python scripts/run_ai_employee.py --daemon    # Start continuous operation
python scripts/run_ai_employee.py --once      # Run single cycle
python scripts/run_ai_employee.py --status    # Check system status

# Send Email
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "user@example.com" --subject "Hi" --body "Message"

# Post to LinkedIn
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --content "Your post content"

# Move Files
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "task.md" --from "Inbox" --to "Done"

# Request Approval
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Send email" --details "Content..."
```

## 🔐 Required Credentials

### Gmail (Required for email automation)
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to https://myaccount.google.com/apppasswords
4. Generate app password for "Mail"
5. Add to .env file

### LinkedIn (Optional)
- Use regular login credentials
- ⚠️ Warning: May violate LinkedIn TOS
- Recommended: Use test account

## 📊 System Status

Check system health anytime:
```bash
python scripts/run_ai_employee.py --status
```

Shows:
- Files in Inbox
- Pending tasks in Needs_Action
- Pending approvals
- Daemon status
- Recent activity

## 🔄 Typical Workflow

1. **Drop file** → `AI_Employee_Vault/Inbox/task.md`
2. **System processes** → Creates plan in `Needs_Action/`
3. **AI executes** → Performs actions (email, post, etc.)
4. **Completion** → Moves to `Done/` with audit trail

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Gmail auth failed | Use app password, not regular password |
| Lock file error | `rm logs/ai_employee.lock` |
| Playwright error | `playwright install chromium` |

See [Complete Setup Guide](docs/SETUP.md) for detailed troubleshooting.

## 🔒 Security

- Store credentials in `.env` file only
- Never commit `.env` to git
- Use Gmail app passwords (not regular password)
- Rotate credentials regularly
- Monitor logs for suspicious activity

## 📈 Features

- ✅ 22 production-ready skills
- ✅ Daemon mode for continuous operation
- ✅ Lock file prevents duplicate instances
- ✅ Automatic log rotation at 5MB
- ✅ Human approval for sensitive actions
- ✅ Real Gmail and LinkedIn integration
- ✅ Complete audit trail
- ✅ Status monitoring
- ✅ Error handling and recovery

## 🎓 Learning Resources

- Read `docs/SETUP.md` for complete setup
- Check `docs/QUICK_REFERENCE.md` for commands
- Review skill documentation in `.claude/skills/*/SKILL.md`
- Test each skill individually before automation

## 🚦 Getting Started Checklist

- [ ] Python 3.10+ installed
- [ ] Dependencies installed
- [ ] .env file created with credentials
- [ ] Gmail app password obtained
- [ ] Test task processed successfully
- [ ] System status checked
- [ ] Ready for production!

## 📝 License

This is a personal AI Employee system. Use responsibly and in compliance with service terms of use.

## 🤝 Support

For issues or questions:
1. Check documentation in `docs/`
2. Review logs in `logs/`
3. Test individual skills
4. Verify credentials in `.env`

---

**Built with:** Python, Playwright, SMTP
**Tiers:** Bronze (Basic) + Silver (Advanced)
**Status:** Production Ready ✅
