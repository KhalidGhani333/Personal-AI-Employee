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

---

## 📱 Individual Platform Commands

### Gmail - Email Reply Automation

```bash
# Step 1: Detect new emails
python scripts/gmail_watcher.py --once

# Step 2: Generate AI reply
python scripts/reply_generator.py

# Step 3: Approve reply in Obsidian
# Open: AI_Employee_Vault/Needs_Approval/APPROVAL_*.md
# Change: status: pending → status: approved
# Save (Ctrl+S)

# Step 4: Send approved reply
python scripts/reply_sender.py

# Continuous mode (runs every 5 minutes)
python scripts/gmail_watcher.py --continuous --interval 300
```

**Flow:** Email detected → AI generates reply → You approve → Email sent automatically

---

### WhatsApp - Message Reply Automation

```bash
# Step 1: Detect messages (QR scan first time only)
python scripts/whatsapp_watcher.py --once

# Step 2: Generate AI reply
python scripts/reply_generator.py

# Step 3: Approve in Obsidian
# Change: status: pending → status: approved

# Step 4: Send WhatsApp reply
python scripts/reply_sender.py

# Continuous mode (runs every 2 minutes)
python scripts/whatsapp_watcher.py --continuous --interval 120
```

**Flow:** Message detected → AI generates reply → You approve → Message sent via WhatsApp Web

**Note:** QR code scan only needed first time. Session saved for future use.

---

### LinkedIn - Post Content

```bash
# Method 1: Direct content (short posts)
python scripts/linkedin_poster.py --content "Your post content! #AI #Automation"

# Method 2: From file (long posts - RECOMMENDED)
python scripts/linkedin_poster.py --file my_post.txt
```

---

### LinkedIn - Monitor Messages

```bash
# Step 1: Check messages (login first time only)
python scripts/linkedin_watcher.py
# Or: 
python scripts/linkedin_watcher.py --once

# Step 2: Generate reply
python scripts/reply_generator.py

# Step 3: Approve in Obsidian
# Change: status: pending → status: approved

# Step 4: Send reply
python scripts/reply_sender.py

# Continuous mode (runs every 5 minutes)
python scripts/linkedin_watcher.py --continuous --interval 300
```

**Flow:** Message detected → AI generates reply → You approve → Reply sent

---

### Facebook - Post Content

```bash
# Post to Facebook only
python scripts/social_poster.py pipeline "Your content here" --platforms facebook

# Post to multiple platforms
python scripts/social_poster.py pipeline "Your content" --platforms facebook linkedin twitter
```

**Flow:** Content provided → Browser opens → Post created → You review and publish

---

### Twitter - Post Content

```bash
# Post to Twitter
python scripts/social_poster.py pipeline "Your tweet content" --platforms twitter

# Generate content for Twitter
python scripts/social_poster.py generate twitter "Topic"
```

---

### Instagram - Post Content

```bash
# Post to Instagram (if configured)
python scripts/social_poster.py pipeline "Your content" --platforms instagram
```

---

## 🎯 Run by Tier

### Bronze Tier - Basic Automation

```bash
# Run once
python scripts/run_ai_employee.py --once

# Check status
python scripts/run_ai_employee.py --status

# Run continuously (every 5 minutes)
python scripts/run_ai_employee.py --daemon --interval 300

# Move files manually
python .claude/skills/vault-file-manager/scripts/move_task.py --file "task.md" --from "Inbox" --to "Done"
```

**What it does:** Monitors Inbox folder, processes tasks with Claude Code, moves completed tasks to Done folder.

---

### Silver Tier - Communication Automation

```bash
# Start all watchers (run each in separate terminal)
python scripts/gmail_watcher.py --continuous --interval 300
python scripts/whatsapp_watcher.py --continuous --interval 120
python scripts/linkedin_watcher.py --continuous --interval 300
python scripts/reply_generator.py --continuous --interval 300
python scripts/reply_sender.py --continuous --interval 600
```

**What it does:** Monitors Gmail/WhatsApp/LinkedIn, generates AI replies, sends approved replies.

**Simpler option:**
```bash
python scripts/run_ai_employee.py --daemon --interval 300
```

---

### Gold Tier - Business Intelligence

```bash
# Accounting system
python scripts/odoo_integration.py connect
python scripts/odoo_integration.py expense 50.00 "Office supplies" --category office
python scripts/odoo_integration.py income 500.00 "Client payment" --source client
python scripts/odoo_integration.py balance

# CEO briefing
python scripts/ceo_briefing.py daily
python scripts/ceo_briefing.py weekly
python scripts/ceo_briefing.py all

# Social media analytics
python scripts/social_summary.py log linkedin "Post content"
python scripts/social_summary.py summary
python scripts/social_summary.py recent 10

# Autonomous task execution
python scripts/ralph_wiggum_loop.py
python scripts/ralph_wiggum_loop.py continuous

# MCP servers
cd mcp-servers/email-mcp && npm start
cd mcp-servers/file-mcp && npm start
cd mcp-servers/approval-mcp && npm start
```

**What it does:** Tracks finances, generates CEO briefings, analyzes social media, executes tasks autonomously.

**Note:** Odoo is optional - if not configured, local storage is used automatically.

---

## 🚀 Run Complete Project

### Option 1: Windows Task Scheduler (Recommended for 24/7)

```bash
# Setup once (run as Administrator)
python scripts/setup_windows_scheduler.py --setup

# Check status
python scripts/setup_windows_scheduler.py --status

# Enable/disable
python scripts/setup_windows_scheduler.py --enable
python scripts/setup_windows_scheduler.py --disable

# Remove all tasks
python scripts/setup_windows_scheduler.py --remove
```

**Schedule:**
- Gmail Watcher: Every 5 minutes
- WhatsApp Watcher: Every 2 minutes
- LinkedIn Watcher: Every 5 minutes
- Reply Generator: Every 5 minutes
- Reply Sender: Every 10 minutes
- LinkedIn Auto Poster: Every 30 minutes
- Main Orchestrator: Every 5 minutes

---

### Option 2: Batch Script (Easiest - All Services at Once)

**Simple one-command startup for all services:**

```bash
# PowerShell
.\start_ai_employee.bat

# CMD
start_ai_employee.bat
```

**What it does:**
- Starts 6 services simultaneously in background
- Gmail Watcher (5 min interval)
- WhatsApp Watcher (2 min interval)
- LinkedIn Watcher (5 min interval)
- Reply Generator (5 min interval)
- Reply Sender (10 min interval)
- Main Orchestrator (5 min interval)

**Requirements:**
- `.env` file must be configured
- Python installed and in PATH

**To stop all services:**
```bash
.\stop_ai_employee.bat
```

---

### Option 3: Docker Deployment (Recommended for Cloud)

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

### Option 4: Manual Continuous Mode (Individual Commands)

**If you want to run services individually:**

```bash
# Run all in background (Windows)
start /B python scripts/gmail_watcher.py --interval 300
start /B python scripts/whatsapp_watcher.py --interval 120
start /B python scripts/linkedin_watcher.py --continuous --interval 300
start /B python scripts/reply_generator.py --continuous --interval 300
start /B python scripts/reply_sender.py --continuous --interval 600
start /B python scripts/run_ai_employee.py --daemon --interval 300
```

---

### Option 5: One-Time Execution (Manual Check)

```bash
# Check all channels
python scripts/gmail_watcher.py --once
python scripts/whatsapp_watcher.py --once
python scripts/linkedin_watcher.py --once

# Generate replies
python scripts/reply_generator.py

# Approve replies in Obsidian (status: pending → status: approved)

# Send approved replies
python scripts/reply_sender.py

# Generate reports
python scripts/ceo_briefing.py daily
python scripts/odoo_integration.py balance
python scripts/social_summary.py summary
```

---

## 🎉 Quick Start Summary

```bash
# 1. Setup (one time)
pip install -r requirements.txt
playwright install chromium
npm install
copy .env.example .env
# Edit .env with Gmail credentials

# 2. Production (automated 24/7)
python scripts/setup_windows_scheduler.py --setup

# 3. Development (manual testing)
python scripts/run_ai_employee.py --daemon

# 4. One-time check
python scripts/gmail_watcher.py --once
python scripts/reply_generator.py
python scripts/reply_sender.py
```

**Your AI Employee is now running! 🎉**

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
