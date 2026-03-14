# Personal AI Employee - Complete Run Guide

---

## 🚀 Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Configure credentials
copy .env.example .env
# Edit .env with your Gmail credentials

# 3. Verify installation
python --version  # Should be 3.13+
```

**Gmail App Password:**
1. https://myaccount.google.com/security → Enable 2FA
2. https://myaccount.google.com/apppasswords → Generate password
3. Add to .env file

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
python mcp/accounting_mcp/server.py
python mcp/social_mcp/server.py
python mcp/business_mcp/server.py
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

### Option 2: Manual Continuous Mode (All Services)

```bash
# Run all in background (Windows)
start /B python scripts/gmail_watcher.py --continuous --interval 300
start /B python scripts/whatsapp_watcher.py --continuous --interval 120
start /B python scripts/linkedin_watcher.py --continuous --interval 300
start /B python scripts/reply_generator.py --continuous --interval 300
start /B python scripts/reply_sender.py --continuous --interval 600
start /B python scripts/linkedin_auto_poster.py --schedule --interval 1800
start /B python scripts/run_ai_employee.py --daemon --interval 300
```

---

### Option 3: One-Time Execution (Manual Check)

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

**Last Updated:** 2026-03-11
**Version:** 3.1 (Reorganized)
**Status:** Production Ready ✅
