# AI Employee - Personal AI Assistant

Complete automation system for task management, email/WhatsApp monitoring, AI-powered reply generation, social media posting, and workflow orchestration.

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
- ✓ Gmail email monitoring and automation
- ✓ WhatsApp message monitoring and automation
- ✓ AI-powered reply generation (10+ intent types)
- ✓ Context-aware email and WhatsApp replies
- ✓ LinkedIn/Facebook/Twitter post automation
- ✓ Human approval workflows
- ✓ File workflow management
- ✓ Status monitoring and reporting
- ✓ Persistent session management (no repeated logins)

## 🛠️ Available Skills

### Orchestration
- **vault-watcher** - Real-time file monitoring
- **task-planner** - Intelligent task analysis
- **silver-scheduler** - Workflow orchestration

### Communication & Monitoring
- **gmail-watcher** - Monitor Gmail inbox for new emails
- **whatsapp-watcher** - Monitor WhatsApp Web for messages
- **reply-generator** - AI-powered reply generation
- **reply-sender** - Send approved replies

### Production Actions
- **gmail-send** - Send emails via SMTP
- **linkedin-post** - Post to LinkedIn
- **social-poster** - Multi-platform social media posting
- **vault-file-manager** - Manage task files
- **human-approval** - Human-in-the-loop decisions

## 📁 Project Structure

```
Personal-AI-Employee/
├── scripts/                    # Main automation scripts
│   ├── run_ai_employee.py     # Orchestrator (daemon/once/status)
│   ├── task_planner.py        # Task analyzer
│   ├── gmail_watcher.py       # Gmail monitoring
│   ├── whatsapp_watcher.py    # WhatsApp monitoring
│   ├── reply_generator.py     # AI reply generation
│   ├── reply_sender.py        # Send approved replies
│   ├── social_poster.py       # Multi-platform posting
│   └── watch_inbox.py         # Real-time monitor
├── .claude/skills/            # 22 production skills
│   ├── gmail-send/
│   ├── linkedin-post/
│   ├── vault-file-manager/
│   └── human-approval/
├── AI_Employee_Vault/         # Task workflow folders
│   ├── Inbox/                 # Drop new tasks here
│   ├── Needs_Action/          # Active tasks & pending messages
│   ├── Needs_Approval/        # Awaiting approval (replies, posts)
│   ├── Done/                  # Completed tasks
│   ├── Logs/                  # Session files & logs
│   └── Approved/              # Approved social posts
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

# AI Reply Generation
python scripts/gmail_watcher.py --once        # Check Gmail once
python scripts/whatsapp_watcher.py --once     # Check WhatsApp once
python scripts/reply_generator.py             # Generate replies for pending messages
python scripts/reply_sender.py                # Send approved replies

# Continuous Monitoring (Recommended)
python scripts/gmail_watcher.py --continuous --interval 300      # Check every 5 min
python scripts/whatsapp_watcher.py --continuous --interval 120   # Check every 2 min
python scripts/reply_generator.py --continuous --interval 300    # Generate every 5 min

# Send Email
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "user@example.com" --subject "Hi" --body "Message"

# Social Media Posting
python scripts/social_poster.py pipeline "Your content" --platforms linkedin facebook

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
5. Add to .env file:
   ```
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_APP_PASSWORD=your_16_char_app_password
   ```

### WhatsApp (For message monitoring)
1. First run: `python scripts/whatsapp_watcher.py --once`
2. Scan QR code with your phone
3. Session saved automatically - no need to scan again
4. Browser state persists using Playwright's storage_state API

### LinkedIn (Optional)
- Use regular login credentials
- ⚠️ Warning: May violate LinkedIn TOS
- Recommended: Use test account
- Session persists after first login

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

### Task Processing Workflow
1. **Drop file** → `AI_Employee_Vault/Inbox/task.md`
2. **System processes** → Creates plan in `Needs_Action/`
3. **AI executes** → Performs actions (email, post, etc.)
4. **Completion** → Moves to `Done/` with audit trail

### AI Reply Generation Workflow
1. **Monitor** → Gmail/WhatsApp watchers detect new messages
2. **Create Task** → Message saved to `Needs_Action/` folder
3. **AI Analysis** → Reply generator detects intent (greeting, question, urgent, etc.)
4. **Generate Reply** → Context-aware reply created based on platform and intent
5. **Human Review** → Reply saved to `Needs_Approval/` for review
6. **Approval** → User edits if needed and sets `status: approved`
7. **Send** → Reply sender sends via appropriate channel
8. **Archive** → Moved to `Done/` with complete audit trail

### Supported Intent Types
- **Greeting** - "Hello", "How are you?"
- **Gratitude** - "Thanks for your help"
- **Question** - "Can you help me with...?"
- **Urgent** - "This is urgent, ASAP"
- **Issue** - "I'm having a problem with..."
- **Meeting** - "Can we schedule a meeting?"
- **Project Update** - "What's the status of...?"
- **Follow-up** - "Following up on..."
- **Info Request** - "Can you provide details about...?"
- **Confirmation** - "Please confirm..."

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
- ✅ AI-powered reply generation with 10+ intent types
- ✅ Gmail and WhatsApp monitoring
- ✅ Context-aware replies (professional for email, casual for WhatsApp)
- ✅ Persistent session management (no repeated logins)
- ✅ Multi-platform social media posting (LinkedIn, Facebook, Twitter)
- ✅ Daemon mode for continuous operation
- ✅ Lock file prevents duplicate instances
- ✅ Automatic log rotation at 5MB
- ✅ Human approval for sensitive actions
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
