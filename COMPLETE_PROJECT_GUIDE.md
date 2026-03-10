# Personal AI Employee - Quick Run Guide

**How to Run Everything**

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

## 📝 Individual Scripts

### Bronze Tier Scripts

```bash
# Main Orchestrator - Processes inbox tasks
python scripts/run_ai_employee.py --once
python scripts/run_ai_employee.py --status
python scripts/run_ai_employee.py --daemon --interval 300

# Vault File Manager - Move files between folders
python .claude/skills/vault-file-manager/scripts/move_task.py --file "task.md" --from "Inbox" --to "Done"
```

### Silver Tier Scripts

```bash
# Gmail Watcher - Monitor emails
python scripts/gmail_watcher.py --once
python scripts/gmail_watcher.py --continuous --interval 300

# WhatsApp Watcher - Monitor messages (requires QR scan first time)
python scripts/whatsapp_watcher.py --once
python scripts/whatsapp_watcher.py --continuous --interval 120

# LinkedIn Watcher - Monitor LinkedIn messages
python scripts/linkedin_watcher.py --once
python scripts/linkedin_watcher.py --continuous --interval 300

# Reply Generator - Generate AI replies for messages
python scripts/reply_generator.py
python scripts/reply_generator.py --continuous --interval 300

# Reply Sender - Send approved replies
python scripts/reply_sender.py
python scripts/reply_sender.py --continuous --interval 600

# LinkedIn Auto Poster - Schedule and post to LinkedIn
python scripts/linkedin_auto_poster.py --generate      # Generate sample posts
python scripts/linkedin_auto_poster.py --show-queue    # View queue
python scripts/linkedin_auto_poster.py --process       # Post now
python scripts/linkedin_auto_poster.py --schedule --interval 1800  # Auto-post every 30 min

# Social Media Poster - Post to multiple platforms
python scripts/social_poster.py pipeline "Your content" --platforms linkedin twitter facebook
python scripts/social_poster.py generate linkedin "Topic"
```

### Gold Tier Scripts

```bash
# Accounting System - Track expenses and income
python scripts/odoo_integration.py connect
python scripts/odoo_integration.py expense 50.00 "Office supplies" --category office
python scripts/odoo_integration.py income 500.00 "Client payment" --source client
python scripts/odoo_integration.py balance

# CEO Briefing - Generate executive reports
python scripts/ceo_briefing.py daily    # Daily summary
python scripts/ceo_briefing.py weekly   # Weekly briefing
python scripts/ceo_briefing.py all      # Both reports

# Social Media Analytics - Track social media activity
python scripts/social_summary.py log linkedin "Post content"
python scripts/social_summary.py summary
python scripts/social_summary.py recent 10

# Ralph Wiggum Loop - Autonomous task execution
python scripts/ralph_wiggum_loop.py
python scripts/ralph_wiggum_loop.py continuous

# MCP Servers - Test integrations
python mcp/accounting_mcp/server.py
python mcp/social_mcp/server.py
python mcp/business_mcp/server.py
```

---

## 💡 Practical Workflows (Step-by-Step)

### Gmail: Email Reply Automation

```bash
# Step 1: Detect new emails
python scripts/gmail_watcher.py --once
# Creates task file in Needs_Action/

# Step 2: Generate AI reply
python scripts/reply_generator.py
# Reads email, generates reply, creates approval file in Needs_Approval/

# Step 3: Approve reply
# Open file in Obsidian: AI_Employee_Vault/Needs_Approval/APPROVAL_*.md
# Change: status: pending → status: approved
# Save (Ctrl+S)

# Step 4: Send approved reply
python scripts/reply_sender.py
# Sends email and moves file to Done/
```

**What happens:** Email detected → AI generates reply → You approve → Email sent automatically

---

### WhatsApp: Message Reply Automation

```bash
# Step 1: Detect WhatsApp messages
python scripts/whatsapp_watcher.py --once
# First time: Browser opens, scan QR code with phone
# Next times: Auto-login, detects unread messages
# Creates task files in Needs_Action/

# Step 2: Generate AI reply
python scripts/reply_generator.py
# Reads WhatsApp message, generates casual reply with emojis
# Creates approval file in Needs_Approval/

# Step 3: Approve reply
# Open file in Obsidian: AI_Employee_Vault/Needs_Approval/APPROVAL_*.md
# Change: status: pending → status: approved
# Save (Ctrl+S)

# Step 4: Send WhatsApp reply
python scripts/reply_sender.py
# Opens browser, types message, sends automatically
# Moves file to Done/
```

**What happens:** WhatsApp message detected → AI generates reply → You approve → Message sent via WhatsApp Web

**Note:** QR code scan only needed first time. Session saved for future use.

---

### LinkedIn: Post Content

```bash
# Method 1: Direct content (short posts)
python scripts/linkedin_poster.py --content "Your post content here! #AI #Automation"

# Method 2: From file (long posts - RECOMMENDED)
# Create file: my_post.txt with your content
python scripts/linkedin_poster.py --file my_post.txt

# What happens:
# 1. Browser opens LinkedIn
# 2. If not logged in: 60 seconds to login manually
# 3. "Start a post" clicked automatically
# 4. Content filled automatically
# 5. Browser stays open - you review and click "Post" manually
# 6. Session saved for next time
```

**What happens:** Content provided → Browser opens → Post filled → You review and publish manually

---

### Facebook: Post Content

```bash
# Post to Facebook
python scripts/social_poster.py pipeline "Your content here" --platforms facebook

# Post to multiple platforms
python scripts/social_poster.py pipeline "Your content" --platforms facebook linkedin twitter

# What happens:
# 1. Browser opens Facebook
# 2. Login if needed (session saved)
# 3. Post created automatically
# 4. You review and publish
```

**What happens:** Content provided → Browser opens → Post created → You review and publish

---

### LinkedIn: Monitor Messages

```bash
# Step 1: Check LinkedIn messages
python scripts/linkedin_watcher.py --once
# First time: Browser opens, login manually
# Next times: Auto-login, checks messages
# Creates task files in Needs_Action/

# Step 2: Generate reply
python scripts/reply_generator.py

# Step 3: Approve in Obsidian
# Change: status: pending → status: approved

# Step 4: Send reply
python scripts/reply_sender.py
```

**What happens:** LinkedIn messages detected → AI generates reply → You approve → Reply sent

---

## 🎯 Run by Tier

### Bronze Tier (Basic Automation)

```bash
# Run once
python scripts/run_ai_employee.py --once

# Check status
python scripts/run_ai_employee.py --status

# Run continuously
python scripts/run_ai_employee.py --daemon --interval 300
```

**What it does:** Monitors Inbox folder, processes tasks with Claude Code, moves completed tasks to Done folder.

---

### Silver Tier (Communication Automation)

```bash
# Start all watchers in separate terminals
python scripts/gmail_watcher.py --continuous --interval 300
python scripts/whatsapp_watcher.py --continuous --interval 120
python scripts/linkedin_watcher.py --continuous --interval 300
python scripts/reply_generator.py --continuous --interval 300
python scripts/reply_sender.py --continuous --interval 600
python scripts/linkedin_auto_poster.py --schedule --interval 1800
```

**What it does:** Monitors Gmail/WhatsApp/LinkedIn, generates AI replies, sends approved replies, auto-posts to LinkedIn.

**Simpler option:**
```bash
# Main orchestrator handles most features
python scripts/run_ai_employee.py --daemon --interval 300
```

---

### Gold Tier (Business Intelligence)

```bash
# Generate daily briefing
python scripts/ceo_briefing.py daily

# Check accounting balance
python scripts/odoo_integration.py balance

# View social media analytics
python scripts/social_summary.py summary

# Start autonomous task execution
python scripts/ralph_wiggum_loop.py continuous
```

**What it does:** Tracks finances, generates CEO briefings, analyzes social media, executes tasks autonomously.

---

## 🚀 Run Everything Together

### Option 1: Windows Task Scheduler (Recommended)

```bash
# Setup once
python scripts/setup_windows_scheduler.py --setup

# Check status
python scripts/setup_windows_scheduler.py --status

# Enable/disable
python scripts/setup_windows_scheduler.py --enable
python scripts/setup_windows_scheduler.py --disable

# Remove all tasks
python scripts/setup_windows_scheduler.py --remove
```

**What it does:** Automatically runs all components in background 24/7.

**Schedule:**
- Gmail Watcher: Every 5 minutes
- WhatsApp Watcher: Every 2 minutes
- Reply Generator: Every 5 minutes
- Reply Sender: Every 10 minutes
- LinkedIn Auto Poster: Every 30 minutes
- Main Orchestrator: Every 5 minutes

---

### Option 2: Manual Continuous Mode

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

**What it does:** Runs all watchers and processors continuously in background.

---

### Option 3: One-Time Execution

```bash
# Check all channels
python scripts/gmail_watcher.py --once
python scripts/whatsapp_watcher.py --once
python scripts/linkedin_watcher.py --once

# Generate replies
python scripts/reply_generator.py

# Approve replies manually (edit files in Needs_Approval/)
# Change: status: pending → status: approved

# Send approved replies
python scripts/reply_sender.py

# Generate reports
python scripts/ceo_briefing.py daily
python scripts/odoo_integration.py balance
python scripts/social_summary.py summary
```

**What it does:** Runs everything once without continuous monitoring.

---

## 📊 Daily Workflow

```bash
# Morning (5 minutes)
python scripts/run_ai_employee.py --status
# Review files in Needs_Approval/ and approve
python scripts/reply_sender.py
python scripts/ceo_briefing.py daily

# Weekly (15 minutes)
python scripts/ceo_briefing.py weekly
python scripts/odoo_integration.py balance
python scripts/social_summary.py summary
```

---

## 🔧 Troubleshooting

**Gmail not working:**
```bash
# Check credentials in .env
# Use App Password (not regular password)
# Enable IMAP in Gmail settings
```

**Session expired (WhatsApp/LinkedIn):**
```bash
# Delete session file
del AI_Employee_Vault\Logs\sessions\whatsapp_session.json
# Run watcher again to re-authenticate
python scripts/whatsapp_watcher.py --once
```

**Replies not sending:**
```bash
# Check approval files have: status: approved
dir AI_Employee_Vault\Needs_Approval
```

**Task Scheduler not working:**
```bash
# Run as Administrator
python scripts/setup_windows_scheduler.py --setup
```

---

## 📈 System Monitoring

```bash
# Check logs
type AI_Employee_Vault\Logs\ai_employee.log
type AI_Employee_Vault\Logs\reply_generator.log

# Check system health
python scripts/run_ai_employee.py --status
dir AI_Employee_Vault\Needs_Action
dir AI_Employee_Vault\Needs_Approval
dir AI_Employee_Vault\Done
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

**Last Updated:** 2026-03-10
**Version:** 3.0 (Gold Tier Complete)
**Status:** Production Ready ✅
