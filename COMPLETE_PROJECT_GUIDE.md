# Personal AI Employee - Complete Project Guide

**How to Run Everything - Step by Step**

This guide shows you exactly how to run every component of the Personal AI Employee system, from individual features to full automation.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Testing Individual Components](#testing-individual-components)
4. [Running by Tier](#running-by-tier)
5. [Full System Automation](#full-system-automation)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- Python 3.13 or higher
- Git (for cloning repository)
- Text editor (VS Code, Notepad++, or any editor)

### Required Credentials
- Gmail account with App Password
- (Optional) LinkedIn account for auto-posting
- (Optional) WhatsApp for message monitoring

---

## Initial Setup

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd "Personal AI Employee"

# Install Python packages
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

**Expected Output:**
```
Successfully installed playwright-1.40.0 python-dotenv-1.0.0 ...
Chromium 120.0.6099.28 downloaded successfully
```

### Step 2: Configure Environment Variables

```bash
# Copy example file
copy .env.example .env

# Open .env in text editor and add:
```

**Minimum Configuration (.env):**
```env
# Gmail (Required for email features)
EMAIL_ADDRESS=your.email@gmail.com
EMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LinkedIn (Optional - for auto-posting)
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# WhatsApp (Optional - auto-created on first run)
WHATSAPP_SESSION_PATH=./AI_Employee_Vault/Logs/sessions/whatsapp_session.json

# Odoo (Optional - local fallback available)
# ODOO_URL=http://localhost:8069
# ODOO_DB=odoo
# ODOO_USERNAME=admin
# ODOO_PASSWORD=admin
```

**How to Get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" and generate password
5. Copy 16-character password to .env

### Step 3: Verify Installation

```bash
# Check Python version
python --version
# Should show: Python 3.13.x or higher

# Check if Playwright is installed
playwright --version
# Should show: Version 1.40.x

# Verify project structure
dir AI_Employee_Vault
# Should show: Inbox, Needs_Action, Needs_Approval, Done, Logs, etc.
```

---

## Testing Individual Components

Test each component individually before running full automation.

### Bronze Tier Components

#### 1. Test File System Watcher

```bash
# Create a test task
echo "# Test Task" > AI_Employee_Vault/Inbox/test_task.md
echo "This is a test task for the AI Employee system." >> AI_Employee_Vault/Inbox/test_task.md

# Check if file was created
dir AI_Employee_Vault\Inbox

# Expected: test_task.md should be visible
```

#### 2. Test Main Orchestrator

```bash
# Run once (processes inbox)
python scripts/run_ai_employee.py --once

# Check status
python scripts/run_ai_employee.py --status

# Expected Output:
# System Status: Operational
# Files in Inbox: 0
# Pending Tasks: 1
# Pending Approvals: 0
```

#### 3. Test Vault File Manager

```bash
# Move file between folders
python .claude/skills/vault-file-manager/scripts/move_task.py --file "test_task.md" --from "Inbox" --to "Done"

# Verify move
dir AI_Employee_Vault\Done
# Expected: test_task.md should be in Done folder
```

---

### Silver Tier Components

#### 1. Test Gmail Watcher

```bash
# Check Gmail once (requires credentials in .env)
python scripts/gmail_watcher.py --once

# Expected Output:
# [INFO] Connecting to Gmail...
# [INFO] Connected successfully
# [INFO] Checking for new emails...
# [INFO] Found X unread emails
# [INFO] Created X task files in Needs_Action/
```

**If you get errors:**
- Verify EMAIL_ADDRESS and EMAIL_APP_PASSWORD in .env
- Check if IMAP is enabled in Gmail settings
- Use App Password, not regular password

#### 2. Test WhatsApp Watcher (Optional)

```bash
# First run - requires QR code scan
python scripts/whatsapp_watcher.py --once

# Browser will open - scan QR code with your phone
# Session will be saved automatically

# Second run - no QR code needed
python scripts/whatsapp_watcher.py --once

# Expected Output:
# [INFO] Loading saved session...
# [INFO] Session loaded successfully
# [INFO] Checking for new messages...
# [INFO] Found X unread messages
```

#### 3. Test LinkedIn Watcher (Optional)

```bash
# First run - requires manual login
python scripts/linkedin_watcher.py --once

# Browser will open - login manually
# Session will be saved automatically

# Second run - no login needed
python scripts/linkedin_watcher.py --once

# Expected Output:
# [INFO] Loading saved session...
# [INFO] Checking LinkedIn messages...
# [INFO] Found X new messages
```

#### 4. Test AI Reply Generation

```bash
# Generate replies for pending messages
python scripts/reply_generator.py

# Expected Output:
# [INFO] Processing tasks from Needs_Action/
# [INFO] Found X email tasks
# [INFO] Generating reply for: [email subject]
# [INFO] Intent detected: greeting
# [INFO] Reply generated and saved to Needs_Approval/
```

**Check Generated Replies:**
```bash
# View approval files
dir AI_Employee_Vault\Needs_Approval

# Open an approval file in text editor
notepad AI_Employee_Vault\Needs_Approval\APPROVAL_email_reply_*.md
```

**Approval File Format:**
```markdown
---
type: email_reply
from: sender@example.com
subject: Hello
status: pending
---

## Original Message
Hello, how are you?

## Proposed Reply
Hi! I'm doing well, thank you for asking. How can I help you today?

## To Approve
Change status to: approved
```

#### 5. Test Reply Sender

```bash
# First, approve a reply:
# 1. Open file in Needs_Approval/
# 2. Change: status: pending → status: approved
# 3. Save file

# Send approved replies
python scripts/reply_sender.py

# Expected Output:
# [INFO] Checking for approved replies...
# [INFO] Found 1 approved reply
# [INFO] Sending email to: sender@example.com
# [SUCCESS] Email sent successfully
# [INFO] Moved to Done/
```

#### 6. Test LinkedIn Auto Posting

```bash
# Generate sample sales posts
python scripts/linkedin_auto_poster.py --generate

# View queue
python scripts/linkedin_auto_poster.py --show-queue

# Process queue (posts scheduled content)
python scripts/linkedin_auto_poster.py --process

# Expected Output:
# [INFO] Found 3 post(s) ready to publish
# [INFO] Processing post: post_20260310_120000
# [SUCCESS] Posted to LinkedIn
```

#### 7. Test Social Media Posting

```bash
# Generate content for all platforms
python scripts/social_poster.py pipeline "AI and Future of Work" --platforms linkedin twitter facebook

# Expected Output:
# [INFO] Generating content for: linkedin, twitter, facebook
# [INFO] LinkedIn post generated
# [INFO] Twitter post generated
# [INFO] Facebook post generated
# [INFO] Posts saved to Pending_Approval/
```

---

### Gold Tier Components

#### 1. Test Accounting System

```bash
# Test without Odoo (local storage)
python scripts/odoo_integration.py connect

# Expected Output:
# [INFO] Odoo not connected - using local storage

# Record expense
python scripts/odoo_integration.py expense 50.00 "Office supplies" --category office

# Expected Output:
# [SUCCESS] Expense recorded locally: $50.0
# Storage: local

# Record income
python scripts/odoo_integration.py income 500.00 "Client payment" --source client

# Check balance
python scripts/odoo_integration.py balance

# Expected Output:
# [SUCCESS] Balance Retrieved
# Balance: $450.00
# Total Income: $500.00
# Total Expenses: $50.00
# Storage: local
```

#### 2. Test Accounting MCP Server

```bash
# Run MCP server tests
python mcp/accounting_mcp/server.py

# Expected Output:
# Testing Accounting MCP Server...
# 1. Recording expense...
# Result: {'success': True, 'amount': 50.0, ...}
# 2. Recording income...
# Result: {'success': True, 'amount': 500.0, ...}
# 3. Getting balance...
# Result: {'success': True, 'balance': 450.0, ...}
# All tests completed!
```

#### 3. Test Social Media MCP Server

```bash
# Run MCP server tests
python mcp/social_mcp/server.py

# Expected Output:
# Testing Social Media MCP Server...
# 1. Getting platform status...
# Result: {'success': True, 'platforms': {...}}
# 2. Getting analytics...
# Result: {'success': True, 'analytics': '...'}
# All tests completed!
```

#### 4. Test CEO Briefing System

```bash
# Generate daily summary
python scripts/ceo_briefing.py daily

# Expected Output:
# [INFO] Generating daily summary...
# [SUCCESS] Daily summary saved to: AI_Employee_Vault/Briefings/DAILY_SUMMARY_2026-03-10.md

# View the report
notepad AI_Employee_Vault\Briefings\DAILY_SUMMARY_2026-03-10.md

# Generate weekly briefing
python scripts/ceo_briefing.py weekly

# Expected Output:
# [INFO] Generating weekly CEO briefing...
# [SUCCESS] Weekly briefing saved to: AI_Employee_Vault/Briefings/CEO_BRIEFING_2026-03-10.md
```

#### 5. Test Social Media Analytics

```bash
# Log a test post
python scripts/social_summary.py log linkedin "Test post about AI automation"

# View summary
python scripts/social_summary.py summary

# Expected Output:
# Social Media Summary:
#   Total Posts: 1
#   By Platform:
#     - LinkedIn: 1 posts

# View recent posts
python scripts/social_summary.py recent 5
```

#### 6. Test Ralph Wiggum Autonomous Loop

```bash
# Create a test task
echo "# Send Email Task" > AI_Employee_Vault/Needs_Action/test_email_task.md
echo "Send email to: test@example.com" >> AI_Employee_Vault/Needs_Action/test_email_task.md
echo "Subject: Test Email" >> AI_Employee_Vault/Needs_Action/test_email_task.md
echo "Body: This is a test email." >> AI_Employee_Vault/Needs_Action/test_email_task.md

# Run Ralph Wiggum loop
python scripts/ralph_wiggum_loop.py

# Expected Output:
# [INFO] Ralph Wiggum Loop: Checking for tasks...
# [INFO] Processing task: test_email_task.md
# [INFO] Step 1: Analyzing task...
# [INFO] Step 2: Creating execution plan...
# [INFO] Task completed successfully
```

---

## Running by Tier

### Run Bronze Tier Features

```bash
# 1. Start main orchestrator (processes inbox)
python scripts/run_ai_employee.py --once

# 2. Check system status
python scripts/run_ai_employee.py --status

# 3. Move files manually
python .claude/skills/vault-file-manager/scripts/move_task.py --file "task.md" --from "Inbox" --to "Done"
```

**What Bronze Tier Does:**
- Monitors Inbox folder for new tasks
- Processes tasks with Claude Code
- Moves completed tasks to Done folder
- Provides basic workflow automation

---

### Run Silver Tier Features

```bash
# Terminal 1: Start continuous monitoring
python scripts/gmail_watcher.py --continuous --interval 300

# Terminal 2: Start reply generation
python scripts/reply_generator.py --continuous --interval 300

# Terminal 3: Start reply sender
python scripts/reply_sender.py --continuous --interval 600

# Terminal 4: Start LinkedIn auto-poster
python scripts/linkedin_auto_poster.py --schedule --interval 1800
```

**What Silver Tier Does:**
- Monitors Gmail every 5 minutes
- Monitors WhatsApp every 2 minutes (if configured)
- Monitors LinkedIn every 5 minutes (if configured)
- Generates AI replies automatically
- Sends approved replies automatically
- Posts to LinkedIn on schedule
- Provides human-in-the-loop approval

**Simpler Option - Use Main Orchestrator:**
```bash
# Runs all Silver Tier features together
python scripts/run_ai_employee.py --daemon --interval 300
```

---

### Run Gold Tier Features

```bash
# 1. Start accounting tracking
python scripts/odoo_integration.py balance

# 2. Generate CEO briefing
python scripts/ceo_briefing.py weekly

# 3. Check social media analytics
python scripts/social_summary.py summary

# 4. Start autonomous task execution
python scripts/ralph_wiggum_loop.py continuous

# 5. Test MCP servers
python mcp/accounting_mcp/server.py
python mcp/social_mcp/server.py
```

**What Gold Tier Does:**
- Tracks business finances (expenses, income, balance)
- Generates daily and weekly CEO briefings
- Provides business intelligence and recommendations
- Detects opportunities and bottlenecks
- Manages social media across 4 platforms
- Executes multi-step tasks autonomously
- Provides comprehensive analytics

---

## Full System Automation

### Option 1: Windows Task Scheduler (Recommended for Production)

**Setup Once:**
```bash
# Create all scheduled tasks
python scripts/setup_windows_scheduler.py --setup

# Expected Output:
# [SUCCESS] Created task: Gmail Watcher
# [SUCCESS] Created task: WhatsApp Watcher
# [SUCCESS] Created task: Reply Generator
# [SUCCESS] Created task: Reply Sender
# [SUCCESS] Created task: LinkedIn Auto Poster
# [SUCCESS] Created task: Main Orchestrator
# Setup Complete: 6/6 tasks created
```

**Check Status:**
```bash
python scripts/setup_windows_scheduler.py --status

# Expected Output:
# Task: AI Employee\Gmail Watcher
#   Status: Ready
#   Next Run: 2026-03-10 14:35:00
# Task: AI Employee\WhatsApp Watcher
#   Status: Ready
#   Next Run: 2026-03-10 14:32:00
# ...
```

**Control Tasks:**
```bash
# Enable all tasks
python scripts/setup_windows_scheduler.py --enable

# Disable all tasks
python scripts/setup_windows_scheduler.py --disable

# Remove all tasks
python scripts/setup_windows_scheduler.py --remove
```

**What Gets Automated:**
- Gmail Watcher: Every 5 minutes
- WhatsApp Watcher: Every 2 minutes
- Reply Generator: Every 5 minutes
- Reply Sender: Every 10 minutes
- LinkedIn Auto Poster: Every 30 minutes
- Main Orchestrator: Every 5 minutes

---

### Option 2: Manual Continuous Mode

**Run All Components Together:**

```bash
# Terminal 1: Gmail monitoring
start /B python scripts/gmail_watcher.py --continuous --interval 300

# Terminal 2: WhatsApp monitoring (optional)
start /B python scripts/whatsapp_watcher.py --continuous --interval 120

# Terminal 3: LinkedIn monitoring (optional)
start /B python scripts/linkedin_watcher.py --continuous --interval 300

# Terminal 4: Reply generation
start /B python scripts/reply_generator.py --continuous --interval 300

# Terminal 5: Reply sending
start /B python scripts/reply_sender.py --continuous --interval 600

# Terminal 6: LinkedIn auto-posting
start /B python scripts/linkedin_auto_poster.py --schedule --interval 1800

# Terminal 7: Main orchestrator
start /B python scripts/run_ai_employee.py --daemon --interval 300
```

**Simpler - Single Command:**
```bash
# Run main orchestrator (handles most features)
python scripts/run_ai_employee.py --daemon --interval 300
```

---

### Option 3: One-Time Execution

**Run Everything Once (No Continuous Loop):**

```bash
# 1. Check all channels
python scripts/gmail_watcher.py --once
python scripts/whatsapp_watcher.py --once
python scripts/linkedin_watcher.py --once

# 2. Generate replies
python scripts/reply_generator.py

# 3. Approve replies manually
# Open AI_Employee_Vault/Needs_Approval/
# Change status: pending → approved

# 4. Send approved replies
python scripts/reply_sender.py

# 5. Process LinkedIn queue
python scripts/linkedin_auto_poster.py --process

# 6. Generate CEO briefing
python scripts/ceo_briefing.py daily

# 7. Check accounting
python scripts/odoo_integration.py balance
```

---

## Typical Daily Workflow

### Morning Routine (5 minutes)

```bash
# 1. Check system status
python scripts/run_ai_employee.py --status

# 2. Review pending approvals
dir AI_Employee_Vault\Needs_Approval

# 3. Approve replies
# Open files in Needs_Approval/
# Change status: pending → approved
# Save files

# 4. Send approved replies
python scripts/reply_sender.py

# 5. Generate daily briefing
python scripts/ceo_briefing.py daily

# 6. Review briefing
notepad AI_Employee_Vault\Briefings\DAILY_SUMMARY_2026-03-10.md
```

### Weekly Routine (15 minutes)

```bash
# 1. Generate weekly CEO briefing
python scripts/ceo_briefing.py weekly

# 2. Review business metrics
notepad AI_Employee_Vault\Briefings\CEO_BRIEFING_2026-03-10.md

# 3. Check accounting balance
python scripts/odoo_integration.py balance

# 4. Review social media analytics
python scripts/social_summary.py summary

# 5. Check LinkedIn post queue
python scripts/linkedin_auto_poster.py --show-queue

# 6. Review completed tasks
dir AI_Employee_Vault\Done
```

---

## Troubleshooting

### Gmail Not Working

**Error:** "Failed to connect to Gmail"

**Solution:**
```bash
# 1. Verify credentials
notepad .env
# Check EMAIL_ADDRESS and EMAIL_APP_PASSWORD

# 2. Test connection
python scripts/gmail_watcher.py --once

# 3. If still failing:
# - Use App Password (not regular password)
# - Enable IMAP in Gmail settings
# - Check firewall/antivirus
```

### WhatsApp Session Expired

**Error:** "Session not found" or QR code appears again

**Solution:**
```bash
# Delete old session
del AI_Employee_Vault\Logs\sessions\whatsapp_session.json

# Re-authenticate
python scripts/whatsapp_watcher.py --once
# Scan QR code with phone
```

### LinkedIn Session Expired

**Error:** "Please login" or redirected to login page

**Solution:**
```bash
# Delete old session
del AI_Employee_Vault\Logs\sessions\linkedin_session.json

# Re-authenticate
python scripts/linkedin_watcher.py --once
# Login manually in browser
```

### Replies Not Sending

**Error:** "No approved replies found"

**Solution:**
```bash
# 1. Check approval files
dir AI_Employee_Vault\Needs_Approval

# 2. Verify status is "approved"
notepad AI_Employee_Vault\Needs_Approval\APPROVAL_*.md
# Should have: status: approved

# 3. Run sender
python scripts/reply_sender.py
```

### Task Scheduler Not Working

**Error:** Tasks not running automatically

**Solution:**
```bash
# 1. Check task status
python scripts/setup_windows_scheduler.py --status

# 2. Enable tasks
python scripts/setup_windows_scheduler.py --enable

# 3. Run Task Scheduler as Administrator
# Right-click Command Prompt → Run as Administrator
python scripts/setup_windows_scheduler.py --setup
```

---

## System Monitoring

### Check Logs

```bash
# View orchestrator log
type AI_Employee_Vault\Logs\ai_employee.log

# View reply generator log
type AI_Employee_Vault\Logs\reply_generator.log

# View CEO briefing log
type AI_Employee_Vault\Logs\ceo_briefing.log

# View all logs
dir AI_Employee_Vault\Logs\*.log
```

### Check System Health

```bash
# System status
python scripts/run_ai_employee.py --status

# Pending tasks
dir AI_Employee_Vault\Needs_Action

# Pending approvals
dir AI_Employee_Vault\Needs_Approval

# Completed tasks
dir AI_Employee_Vault\Done

# Dashboard
notepad AI_Employee_Vault\Dashboard.md
```

---

## Summary

**To run everything together:**

1. **Setup (one time):**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   copy .env.example .env
   # Edit .env with credentials
   ```

2. **Production (automated):**
   ```bash
   python scripts/setup_windows_scheduler.py --setup
   ```

3. **Development (manual):**
   ```bash
   python scripts/run_ai_employee.py --daemon
   ```

4. **Testing (one-time):**
   ```bash
   python scripts/gmail_watcher.py --once
   python scripts/reply_generator.py
   python scripts/reply_sender.py
   ```

**Your AI Employee is now running 24/7!** 🎉

---

**Last Updated:** 2026-03-10
**Version:** 3.0 (Complete Guide)
**Status:** Gold Tier Complete
