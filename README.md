# 🤖 Personal AI Employee - Gold Tier Complete

**Your 24/7 Digital FTE (Full-Time Equivalent)**

Complete autonomous business automation system with multi-channel monitoring, AI-powered communications, accounting integration, social media management, and executive reporting. Built with Claude Code, MCP servers, and local-first architecture.

**Achievement Status:** 🏆 Gold Tier (100% Complete)
- ✅ Bronze Tier - Foundation & Basic Automation
- ✅ Silver Tier - Advanced Automation & Intelligence
- ✅ Gold Tier - Autonomous Employee & Business Intelligence

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

- **[System Architecture](docs/ARCHITECTURE.md)** - Complete system design and integration guide
- **[Windows Scheduler Setup](docs/WINDOWS_SCHEDULER_SETUP.md)** - OS-level automation
- **[Complete Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[Gmail Setup](docs/GMAIL_SETUP.md)** - How to get Gmail app password
- **[LinkedIn Setup](docs/LINKEDIN_SETUP.md)** - LinkedIn automation notes
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command cheat sheet
- **[Dashboard](AI_Employee_Vault/Dashboard.md)** - Real-time system status
- **[Company Handbook](AI_Employee_Vault/Company_Handbook.md)** - Business rules and preferences

## 🎯 What This System Does

### 🥉 Bronze Tier - Foundation (Complete)
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ File monitoring and task generation
- ✅ Claude Code reading/writing to vault
- ✅ Folder structure: /Inbox, /Needs_Action, /Done
- ✅ All AI functionality as Agent Skills

### 🥈 Silver Tier - Advanced Automation (Complete)
- ✅ Multiple Watcher scripts (Gmail + WhatsApp + LinkedIn)
- ✅ Automated scheduling (daemon mode + Windows Task Scheduler)
- ✅ Intelligent task analysis and planning
- ✅ AI-powered reply generation (10+ intent types)
- ✅ Context-aware replies (professional for email, casual for WhatsApp)
- ✅ LinkedIn Auto Posting - Scheduled sales post automation
- ✅ Multi-platform social media (LinkedIn, Facebook, Twitter)
- ✅ Business MCP Server - Email and activity logging
- ✅ Human-in-the-loop approval workflows
- ✅ Persistent session management (no repeated logins)

### 🏆 Gold Tier - Autonomous Employee (Complete)
- ✅ **Instagram Integration** - Desktop mode with anti-detection
- ✅ **Odoo Accounting System** - Self-hosted with local fallback
- ✅ **Multiple MCP Servers** - Business, Accounting, Social Media MCPs
- ✅ **CEO Briefing System** - Daily summaries and weekly business audits
- ✅ **Social Media Analytics** - Post logging and performance tracking
- ✅ **Ralph Wiggum Loop** - Autonomous multi-step task execution
- ✅ **Comprehensive Documentation** - Full architecture guide (docs/ARCHITECTURE.md)
- ✅ **Error Recovery** - Graceful degradation and retry logic
- ✅ **Audit Logging** - Complete activity tracking
- ✅ **Cross-domain Integration** - Personal + Business unified

## 🛠️ Available Skills & Components

### Core Orchestration
- **vault-watcher** - Real-time file monitoring
- **task-planner** - Intelligent task analysis
- **silver-scheduler** - Workflow orchestration
- **ralph-wiggum** - Autonomous multi-step task execution

### Communication & Monitoring
- **gmail-watcher** - Monitor Gmail inbox (IMAP)
- **whatsapp-watcher** - Monitor WhatsApp Web (session-based)
- **linkedin-watcher** - Monitor LinkedIn messages and notifications
- **reply-generator** - AI-powered reply generation (10+ intents)
- **reply-sender** - Send approved replies

### Social Media Management
- **social-poster** - Multi-platform posting (LinkedIn, Twitter, Facebook, Instagram)
- **linkedin-post** - LinkedIn posting with approval workflow
- **linkedin-auto-poster** - Scheduled sales post automation
- **social-summary** - Post logging and analytics

### Business Intelligence
- **ceo-briefing** - Daily summaries and weekly business audits
- **business-auditor** - Opportunity detection and bottleneck analysis
- **report-generator** - Automated report generation

### Accounting & Finance
- **odoo-integration** - Self-hosted Odoo accounting (with local fallback)
- **accounting-manager** - Expense/income tracking
- **invoice-generator** - Invoice creation and management

### MCP Servers
- **business-mcp** - Email sending and activity logging
- **accounting-mcp** - Financial operations and reporting
- **social-media-mcp** - Multi-platform posting and analytics

### Production Actions
- **gmail-send** - Send emails via SMTP
- **vault-file-manager** - Manage task files
- **human-approval** - Human-in-the-loop decisions
- **error-recovery** - Graceful degradation and retry logic

## 📁 Project Structure

```
Personal-AI-Employee/
├── scripts/                         # Main automation scripts
│   ├── run_ai_employee.py          # Main orchestrator (daemon/once/status)
│   ├── task_planner.py             # Task analyzer
│   ├── gmail_watcher.py            # Gmail monitoring (IMAP)
│   ├── whatsapp_watcher.py         # WhatsApp monitoring (Playwright)
│   ├── linkedin_watcher.py         # LinkedIn monitoring (Playwright)
│   ├── reply_generator.py          # AI reply generation (10+ intents)
│   ├── reply_sender.py             # Send approved replies
│   ├── social_poster.py            # Multi-platform posting (4 platforms)
│   ├── linkedin_auto_poster.py     # Scheduled LinkedIn sales posts
│   ├── social_summary.py           # Social media analytics
│   ├── ceo_briefing.py             # Daily/weekly business reports
│   ├── odoo_integration.py         # Accounting system integration
│   ├── ralph_wiggum_loop.py        # Autonomous task execution
│   ├── setup_windows_scheduler.py  # Windows Task Scheduler setup
│   └── test_mcp_server.py          # MCP server testing
├── mcp/                            # MCP Servers
│   ├── business_mcp/               # Business operations MCP
│   ├── accounting_mcp/             # Accounting operations MCP
│   └── social_mcp/                 # Social media operations MCP
├── .claude/skills/                 # 30+ production skills
│   ├── gmail-send/
│   ├── linkedin-post/
│   ├── vault-file-manager/
│   ├── human-approval/
│   ├── ceo-briefing/
│   ├── accounting-manager/
│   ├── social-media-manager/
│   └── ralph-wiggum/
├── AI_Employee_Vault/              # Task workflow & data
│   ├── Dashboard.md                # Real-time system status
│   ├── Company_Handbook.md         # Business rules
│   ├── Inbox/                      # Drop new tasks here
│   ├── Needs_Action/               # Active tasks & pending messages
│   ├── Needs_Approval/             # Awaiting approval (replies, posts)
│   ├── Done/                       # Completed tasks (audit trail)
│   ├── Logs/                       # Session files & system logs
│   ├── Approved/                   # Approved social posts
│   ├── Accounting/                 # Financial transactions & reports
│   ├── Briefings/                  # CEO briefings & business audits
│   └── Reports/                    # Generated reports & analytics
├── docs/                           # Comprehensive documentation
│   ├── ARCHITECTURE.md             # Complete system architecture
│   ├── WINDOWS_SCHEDULER_SETUP.md  # Automation setup guide
│   ├── SETUP.md                    # Installation guide
│   └── QUICK_REFERENCE.md          # Command cheat sheet
├── logs/                           # System logs
├── .env                            # Credentials (create from .env.example)
└── requirements.txt                # Python dependencies
```

## 🔧 Common Commands

### System Control
```bash
# Main orchestrator
python scripts/run_ai_employee.py --daemon    # Start continuous operation
python scripts/run_ai_employee.py --once      # Run single cycle
python scripts/run_ai_employee.py --status    # Check system status

# Autonomous task execution
python scripts/ralph_wiggum_loop.py           # Run once
python scripts/ralph_wiggum_loop.py continuous # Run continuously
```

### Communication Monitoring
```bash
# Check once
python scripts/gmail_watcher.py --once
python scripts/whatsapp_watcher.py --once
python scripts/linkedin_watcher.py --once

# Continuous monitoring (recommended for production)
python scripts/gmail_watcher.py --continuous --interval 300      # Every 5 min
python scripts/whatsapp_watcher.py --continuous --interval 120   # Every 2 min
python scripts/linkedin_watcher.py --continuous --interval 300   # Every 5 min
```

### AI Reply Generation
```bash
# Generate replies for pending messages
python scripts/reply_generator.py

# Send approved replies
python scripts/reply_sender.py

# Continuous reply generation
python scripts/reply_generator.py --continuous --interval 300
```

### Social Media Management
```bash
# Multi-platform posting
python scripts/social_poster.py pipeline "Your content" --platforms linkedin twitter facebook instagram

# LinkedIn auto-posting
python scripts/linkedin_auto_poster.py --generate    # Generate sample posts
python scripts/linkedin_auto_poster.py --process     # Process queue
python scripts/linkedin_auto_poster.py --schedule    # Run continuously
python scripts/linkedin_auto_poster.py --show-queue  # View queue

# Social media analytics
python scripts/social_summary.py log linkedin "Post content"
python scripts/social_summary.py summary
python scripts/social_summary.py recent 10
```

### Business Intelligence
```bash
# CEO briefings
python scripts/ceo_briefing.py daily    # Daily summary
python scripts/ceo_briefing.py weekly   # Weekly business audit
python scripts/ceo_briefing.py all      # Generate all reports
```

### Accounting & Finance
```bash
# Odoo integration (with local fallback)
python scripts/odoo_integration.py connect
python scripts/odoo_integration.py expense 50.00 "Office supplies" --category office
python scripts/odoo_integration.py income 500.00 "Client payment" --source client
python scripts/odoo_integration.py balance

# Test MCP servers
python mcp/accounting_mcp/server.py
python mcp/social_mcp/server.py
python mcp/business_mcp/server.py
```

### Windows Task Scheduler
```bash
# Setup automated scheduling
python scripts/setup_windows_scheduler.py --setup    # Create all tasks
python scripts/setup_windows_scheduler.py --status   # Check status
python scripts/setup_windows_scheduler.py --enable   # Enable all tasks
python scripts/setup_windows_scheduler.py --disable  # Disable all tasks
python scripts/setup_windows_scheduler.py --remove   # Remove all tasks
```

### Manual Operations
```bash
# Send email
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "user@example.com" --subject "Hi" --body "Message"

# Move files
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "task.md" --from "Inbox" --to "Done"

# Request approval
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
   ```env
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_APP_PASSWORD=your_16_char_app_password
   IMAP_SERVER=imap.gmail.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

### LinkedIn (Required for auto-posting)
```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```
- Session-based authentication
- First run requires manual login
- Session persists using Playwright's storage_state
- ⚠️ Use responsibly, may violate LinkedIn TOS

### WhatsApp (Optional - for message monitoring)
```env
WHATSAPP_SESSION_PATH=./AI_Employee_Vault/Logs/sessions/whatsapp_session.json
```
1. First run: `python scripts/whatsapp_watcher.py --once`
2. Scan QR code with your phone
3. Session saved automatically - no repeated QR scans
4. Browser state persists using Playwright's storage_state API

### Social Media Platforms (Optional)
- **Twitter/Facebook/Instagram**: Session-based authentication
- No credentials needed in .env
- First run requires manual login for each platform
- Sessions persist in `AI_Employee_Vault/Logs/sessions/`

### Odoo Accounting (Optional - local fallback available)
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```
- **Note:** If Odoo not configured, system automatically uses local JSON storage
- No functionality loss without Odoo
- See docs/ARCHITECTURE.md for Odoo setup guide

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

### Core Automation
- ✅ 30+ production-ready skills
- ✅ 3 MCP servers (Business, Accounting, Social Media)
- ✅ Daemon mode for 24/7 operation
- ✅ Windows Task Scheduler integration
- ✅ Ralph Wiggum autonomous loop
- ✅ Lock file prevents duplicate instances
- ✅ Automatic log rotation at 5MB

### Communication Intelligence
- ✅ Multi-channel monitoring (Gmail, WhatsApp, LinkedIn)
- ✅ AI-powered reply generation with 10+ intent types
- ✅ Context-aware replies (professional for email, casual for WhatsApp)
- ✅ Persistent session management (no repeated logins)
- ✅ Human-in-the-loop approval workflow

### Social Media Management
- ✅ Multi-platform posting (LinkedIn, Twitter, Facebook, Instagram)
- ✅ LinkedIn auto-posting with scheduling
- ✅ Social media analytics and tracking
- ✅ Post approval workflow
- ✅ Session persistence across platforms

### Business Intelligence
- ✅ Daily CEO summaries
- ✅ Weekly business audit reports
- ✅ Opportunity detection
- ✅ Bottleneck analysis
- ✅ AI-powered recommendations

### Accounting & Finance
- ✅ Odoo integration (self-hosted)
- ✅ Local JSON fallback (no Odoo required)
- ✅ Expense/income tracking
- ✅ Balance calculation
- ✅ Financial report generation
- ✅ Accounting MCP server

### Security & Reliability
- ✅ Complete audit trail
- ✅ Error handling and recovery
- ✅ Graceful degradation
- ✅ Retry logic with exponential backoff
- ✅ Comprehensive logging
- ✅ Status monitoring and health checks

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

## 🏆 Achievement Status

**Tiers Completed:**
- ✅ **Bronze Tier** - Foundation & Basic Automation (100%)
- ✅ **Silver Tier** - Advanced Automation & Intelligence (100%)
- ✅ **Gold Tier** - Autonomous Employee & Business Intelligence (100%)

**Next Level:** Platinum Tier - Cloud deployment with 24/7 operation

---

## 🌟 Key Differentiators

1. **Local-First Architecture** - Privacy-focused, data stays on your machine
2. **Human-in-the-Loop** - AI proposes, you approve critical actions
3. **Multi-Channel Intelligence** - Unified monitoring across email, WhatsApp, LinkedIn
4. **Business Intelligence** - Proactive CEO briefings and opportunity detection
5. **Graceful Degradation** - Works with or without external services (e.g., Odoo)
6. **Session Persistence** - No repeated logins across platforms
7. **Comprehensive Audit Trail** - Every action logged and traceable

---

## 📊 System Metrics

- **Channels Monitored:** 3 (Gmail, WhatsApp, LinkedIn)
- **Social Platforms:** 4 (LinkedIn, Twitter, Facebook, Instagram)
- **MCP Servers:** 3 (Business, Accounting, Social Media)
- **Agent Skills:** 30+
- **Intent Types:** 10+
- **Automation Scripts:** 15+
- **Documentation Pages:** 5+

---

**Built with:** Python, Playwright, SMTP, IMAP, MCP, Odoo
**Architecture:** Local-first, MCP-based, Agent Skills
**Status:** 🏆 Gold Tier Complete - Production Ready ✅
