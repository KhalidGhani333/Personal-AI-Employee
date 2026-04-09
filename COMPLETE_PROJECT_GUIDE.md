# Personal AI Employee - Complete Project Guide

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.10+
python --version

# Node.js 18+ (for MCP servers)
node --version

# Docker (optional, for containerized deployment)
docker --version
```

### Installation
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Playwright browsers
playwright install chromium

# 3. Install Node.js dependencies (for MCP servers)
npm install

# 4. Configure environment
copy .env.example .env
# Edit .env with your credentials
```

---

## 📋 Essential Commands

### System Control
```bash
# Run once (single cycle)
python scripts/run_ai_employee.py --once

# Run daemon (continuous)
python scripts/run_ai_employee.py --daemon --interval 300

# Check status
python scripts/run_ai_employee.py --status

# Autonomous execution
python scripts/ralph_wiggum_loop.py
python scripts/ralph_wiggum_loop.py continuous
```

### Communication Monitoring
```bash
# Gmail
python scripts/gmail_watcher.py --once
python scripts/gmail_watcher.py --continuous --interval 300

# WhatsApp
python scripts/whatsapp_watcher.py --once
python scripts/whatsapp_watcher.py --continuous --interval 120

# LinkedIn
python scripts/linkedin_watcher.py --once
python scripts/linkedin_watcher.py --continuous --interval 300
```

### AI Reply System
```bash
# Generate replies
python scripts/reply_generator.py
python scripts/reply_generator.py --continuous --interval 300

# Send approved replies
python scripts/reply_sender.py
```

### Social Media
```bash
# Multi-platform posting
python scripts/social_poster.py pipeline "Your content" --platforms linkedin twitter facebook instagram

# LinkedIn auto-posting
python scripts/linkedin_auto_poster.py --generate
python scripts/linkedin_auto_poster.py --process
python scripts/linkedin_auto_poster.py --schedule
python scripts/linkedin_auto_poster.py --show-queue

# Analytics
python scripts/social_summary.py log linkedin "Post content"
python scripts/social_summary.py summary
python scripts/social_summary.py recent 10
```

### Business Intelligence
```bash
# CEO briefings
python scripts/ceo_briefing.py daily
python scripts/ceo_briefing.py weekly
python scripts/ceo_briefing.py all
```

### Accounting
```bash
# Odoo integration (with local fallback)
python scripts/odoo_integration.py connect
python scripts/odoo_integration.py expense 50.00 "Office supplies" --category office
python scripts/odoo_integration.py income 500.00 "Client payment" --source client
python scripts/odoo_integration.py balance
```

### Docker Deployment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache

# Windows convenience scripts
docker-start.bat
docker-stop.bat

# Linux/Mac convenience scripts
./docker-start.sh
./docker-stop.sh
```

---

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Inbox/              # Drop new tasks here
├── Needs_Action/       # Active tasks (auto-processed)
├── Needs_Approval/     # Awaiting human approval
├── Done/               # Completed tasks (archive)
├── Plans/              # Execution plans
├── Archive/            # Old messages
├── Logs/               # System logs & sessions
├── Briefings/          # CEO briefings
├── Accounting/         # Financial data
└── Reports/            # Analytics reports
```

---

## 🔄 Workflow

### Basic Task Flow
```
1. Drop task file in Inbox/
2. Task planner analyzes → creates plan in Needs_Action/
3. Ralph Wiggum executes → completes task
4. Files archived to Done/
```

### Approval Flow
```
1. Risky task detected
2. Approval request created in Needs_Approval/
3. User reviews and sets: status: approved
4. System continues execution
5. Files archived to Done/
```

### Email Reply Flow
```
1. Gmail watcher detects email → creates task in Inbox/
2. Reply generator analyzes intent → creates reply in Needs_Approval/
3. User reviews and approves
4. Reply sender sends email
5. Files archived to Done/
```

---

## 🔐 Required Credentials

### Gmail (Required)
```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_16_char_app_password
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**How to get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to https://myaccount.google.com/apppasswords
4. Generate app password for "Mail"
5. Copy 16-character password to .env

### LinkedIn (Optional)
```env
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password
```
- Session-based authentication
- First run requires manual login
- Session persists automatically

### WhatsApp (Optional)
```env
WHATSAPP_SESSION_PATH=./AI_Employee_Vault/Logs/sessions/whatsapp_session.json
```
- First run: scan QR code
- Session saved automatically
- No repeated QR scans needed

### Odoo Accounting (Optional)
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```
- Local fallback available if not configured
- No functionality loss without Odoo

---

## 🎯 Task Types

### Email Task
```markdown
# Email Task
Send email to john@example.com
Subject: Meeting Tomorrow
Body: Let's meet at 10 AM
```

### Social Media Task
```markdown
# LinkedIn Post
Post to LinkedIn:
"Excited to share my new project!"
```

### File Task (Requires Approval)
```markdown
# File Operation
Move files from folder A to folder B
```

### Accounting Task
```markdown
# Expense
Record expense: $50 for office supplies
Category: office
```

### General Task
```markdown
# General Task
Any other task description
```

---

## 🛡️ Safety Features

### Risky Keywords (Require Approval)
- delete, remove, drop, truncate
- destroy, format, wipe, erase
- reset, force, sudo, admin
- root, password, credential

### Approval Format
```yaml
---
status: pending  # Change to 'approved' or 'rejected'
task: Task description
risk_level: high
---
```

---

## 📊 MCP Servers

### Email MCP
```bash
# Start server
cd mcp-servers/email-mcp
npm start

# Tools available:
- send_email
- get_inbox
- mark_read
- search_emails
```

### File MCP
```bash
# Start server
cd mcp-servers/file-mcp
npm start

# Tools available:
- read_file
- write_file
- move_file
- list_files
```

### Approval MCP
```bash
# Start server
cd mcp-servers/approval-mcp
npm start

# Tools available:
- request_approval
- check_approval
- list_pending
```

---

## 🐛 Troubleshooting

### Issue: Tasks not processing
```bash
# Check daemon status
python scripts/run_ai_employee.py --status

# Check logs
tail -f Logs/ai_employee.log

# Remove stale lock file
rm Logs/ai_employee.lock
```

### Issue: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
playwright install chromium
```

### Issue: Gmail authentication failed
```bash
# Verify credentials in .env
# Use app password, not regular password
# Check 2FA is enabled
```

### Issue: Social media posting fails
```bash
# Delete session file
rm AI_Employee_Vault/Logs/sessions/linkedin_session.json

# Re-login manually on next run
python scripts/social_poster.py pipeline "test" --platforms linkedin
```

### Issue: Docker container won't start
```bash
# Check Docker is running
docker ps

# View logs
docker-compose logs

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📈 Monitoring

### Check System Status
```bash
# Overall status
python scripts/run_ai_employee.py --status

# View logs
tail -f Logs/ai_employee.log
tail -f Logs/ralph_wiggum.log
tail -f Logs/social_poster.log

# Docker logs
docker-compose logs -f
```

### Dashboard
```bash
# Open in Obsidian or any markdown viewer
AI_Employee_Vault/Dashboard.md
```

---

## 🔧 Configuration Files

### .env
Environment variables and credentials

### .claude/mcp-config.json
MCP server configuration for Claude Code

### docker-compose.yml
Docker multi-service orchestration

### ecosystem.config.js
PM2 process management (for Linux deployment)

### requirements.txt
Python dependencies

### package.json
Node.js dependencies

---

## 🚀 Deployment Options

### Option 1: Local Windows
```bash
# Manual start
python scripts/run_ai_employee.py --daemon

# Windows Task Scheduler
python scripts/setup_windows_scheduler.py --setup
```

### Option 2: Linux with PM2
```bash
# Install PM2
npm install -g pm2

# Start services
pm2 start ecosystem.config.js

# Monitor
pm2 monit

# Auto-start on boot
pm2 startup
pm2 save
```

### Option 3: Docker (Recommended)
```bash
# Local Docker
docker-compose up -d

# Cloud deployment (VPS/EC2/DigitalOcean)
# 1. Copy project to server
# 2. Configure .env
# 3. Run: docker-compose up -d
```

---

## 📚 Documentation Files

- **README.md** - Main project documentation
- **SUMMARY.md** - Complete system architecture and workflows
- **COMPLETE_PROJECT_GUIDE.md** - This file (quick reference)
- **DOCKER_SETUP.md** - Docker deployment guide
- **LINUX_DEPLOYMENT.md** - Linux/PM2 deployment guide
- **ODOO_SETUP.md** - Accounting system setup

---

## 🎓 Tips & Best Practices

### Task Creation
- Use clear, descriptive task names
- Include all necessary details
- Specify platform for social media tasks
- Add context for better AI understanding

### Approval Management
- Review approvals promptly
- Edit generated content if needed
- Reject risky operations if unsure
- Check logs after approval

### System Maintenance
- Monitor logs regularly
- Clean up Done/ folder periodically
- Rotate logs when they get large
- Update credentials when they expire

### Performance Optimization
- Use appropriate intervals (5 min for email, 2 min for WhatsApp)
- Don't run too many watchers simultaneously
- Use Docker for better resource isolation
- Monitor system resources

---

## 🔗 Quick Links

### Gmail Setup
https://myaccount.google.com/apppasswords

### Docker Documentation
https://docs.docker.com/

### Playwright Documentation
https://playwright.dev/

### Odoo Documentation
https://www.odoo.com/documentation/

---

## 📞 Support

### Check Logs
```bash
# Main log
tail -f Logs/ai_employee.log

# Ralph Wiggum log
tail -f Logs/ralph_wiggum.log

# Social media log
tail -f Logs/social_poster.log

# Docker logs
docker-compose logs -f
```

### Common Log Locations
- `Logs/ai_employee.log` - Main system log
- `Logs/ralph_wiggum.log` - Autonomous executor log
- `Logs/actions.log` - Action history
- `AI_Employee_Vault/Logs/` - Session files and detailed logs

---

## 🏆 Achievement Status

- ✅ **Bronze Tier** - Foundation & Basic Automation (100%)
- ✅ **Silver Tier** - Advanced Automation & Intelligence (100%)
- ✅ **Gold Tier** - Autonomous Employee & Business Intelligence (100%)
- 🚀 **Platinum Tier** - Cloud Deployment with Docker (Ready)

---

**Version:** 2.0 (Platinum Ready)
**Last Updated:** April 2026
**Status:** Production Ready + Docker Deployment

---

**End of Guide** ✅
