# Complete Setup Guide - AI Employee System

## Prerequisites

- Python 3.10 or higher
- Windows/Linux/Mac
- Internet connection
- Gmail account (for email automation)
- LinkedIn account (optional, for social media automation)

## Step-by-Step Setup

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd "D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Bronze"

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers (for LinkedIn automation)
playwright install chromium
```

**Expected Output:**
```
Successfully installed python-dotenv-1.0.0 playwright-1.40.0
Downloading Chromium... Done
```

### Step 2: Create .env File

```bash
# Copy example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

### Step 3: Configure Credentials

Open `.env` file in text editor and fill in your credentials:

```env
# Gmail SMTP (Required for email automation)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password

# LinkedIn (Optional - only if using linkedin-post skill)
LINKEDIN_EMAIL=your-linkedin@email.com
LINKEDIN_PASSWORD=your-linkedin-password
```

**How to Get Gmail App Password:**
1. Go to: https://myaccount.google.com/security
2. Enable 2-Factor Authentication
3. Go to: https://myaccount.google.com/apppasswords
4. Generate app password for "Mail"
5. Copy the 16-character password (remove spaces)
6. Paste in .env file

**LinkedIn Credentials:**
- Use your regular LinkedIn login
- ⚠️ Warning: LinkedIn may flag automation
- Recommended: Use test account or skip this skill

### Step 4: Verify Installation

```bash
# Test Python scripts syntax
python -m py_compile scripts/run_ai_employee.py
python -m py_compile scripts/task_planner.py
python -m py_compile .claude/skills/gmail-send/scripts/send_email.py

# Should show no errors
```

### Step 5: Test Basic Functionality

#### Test 1: Check System Status
```bash
python scripts/run_ai_employee.py --status
```

**Expected Output:**
```
============================================================
AI Employee System Status
============================================================
Timestamp: 2026-02-21 XX:XX:XX

Inbox:
  Files waiting: 0

Needs_Action:
  Plans pending: X

Daemon Status:
  Running: No
============================================================
```

#### Test 2: Create Test Task
```bash
# Create a test file
echo "# Test Task" > AI_Employee_Vault/Inbox/test_task.md
echo "This is a test task to verify the system works." >> AI_Employee_Vault/Inbox/test_task.md
```

#### Test 3: Process Task
```bash
python scripts/run_ai_employee.py --once --verbose
```

**Expected Output:**
```
============================================================
AI Employee - Single Execution Mode
============================================================
[INFO] Single execution started
[INFO] Running task planner...
[INFO] Task planner: Processed: 1/1 file(s)
[OK] Execution completed successfully
```

#### Test 4: Verify Results
```bash
# Check if plan was created
ls AI_Employee_Vault/Needs_Action/

# Check if original moved to Done
ls AI_Employee_Vault/Done/

# Should see:
# - Plan_test_task_*.md in Needs_Action
# - test_task.md in Done
```

### Step 6: Test Email Sending (Optional)

⚠️ **Only if you configured Gmail credentials**

```bash
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "your-email@gmail.com" \
  --subject "Test Email from AI Employee" \
  --body "This is a test email to verify the system works."
```

**Expected Output:**
```
[INFO] Connecting to smtp.gmail.com:587...
[INFO] Authenticating as your-email@gmail.com...
[INFO] Sending email to your-email@gmail.com...
[SUCCESS] Email sent successfully to your-email@gmail.com
```

**If you get authentication error:**
- Double-check EMAIL_ADDRESS in .env
- Verify EMAIL_PASSWORD is the app password (not regular password)
- Make sure 2FA is enabled on Gmail
- Try generating a new app password

### Step 7: Test File Management

```bash
# Create test file in Inbox
echo "# Sample Task" > AI_Employee_Vault/Inbox/sample.md

# Move it to Needs_Action
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "sample.md" \
  --from "Inbox" \
  --to "Needs_Action"

# Move it to Done
python .claude/skills/vault-file-manager/scripts/move_task.py \
  --file "sample.md" \
  --from "Needs_Action" \
  --to "Done"
```

**Expected Output:**
```
[INFO] Moving sample.md
[INFO] From: AI_Employee_Vault\Inbox
[INFO] To: AI_Employee_Vault\Needs_Action
[SUCCESS] File moved successfully
```

## Running the System

### Option 1: Daemon Mode (Continuous Operation)

```bash
# Start the scheduler (runs every 5 minutes)
python scripts/run_ai_employee.py --daemon

# To stop: Press Ctrl+C
```

**What it does:**
- Checks Inbox every 5 minutes
- Processes new files automatically
- Creates execution plans
- Logs all activity
- Runs until you stop it

### Option 2: Manual Mode (Run Once)

```bash
# Process inbox once and exit
python scripts/run_ai_employee.py --once
```

**Use when:**
- Testing the system
- Running on schedule (cron job)
- You want manual control

### Option 3: Real-time Monitoring

```bash
# Watch inbox continuously (15-second polling)
python scripts/watch_inbox.py
```

**Use when:**
- Need immediate processing
- High-priority tasks
- Development/testing

## Common Workflows

### Workflow 1: Process Tasks Automatically

```bash
# 1. Start daemon
python scripts/run_ai_employee.py --daemon

# 2. Drop files in Inbox
# (System processes automatically every 5 minutes)

# 3. Check status anytime
python scripts/run_ai_employee.py --status
```

### Workflow 2: Send Email with Approval

```bash
# 1. Request approval
python .claude/skills/human-approval/scripts/request_approval.py \
  --action "Send client email" \
  --details "To: client@example.com\nSubject: Update\nBody: Project completed."

# 2. Open file in AI_Employee_Vault/Needs_Approval/
# 3. Add: APPROVED or REJECTED
# 4. Save file
# 5. Script detects decision and returns

# 6. If approved, send email
python .claude/skills/gmail-send/scripts/send_email.py \
  --to "client@example.com" \
  --subject "Project Update" \
  --body "Project completed successfully."
```

### Workflow 3: Scheduled Processing (Cron)

```bash
# Edit crontab
crontab -e

# Add line (runs every 5 minutes)
*/5 * * * * cd /path/to/Bronze && python scripts/run_ai_employee.py --once >> logs/cron.log 2>&1
```

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Gmail authentication failed

**Solutions:**
1. Verify 2FA is enabled on Gmail
2. Generate new app password
3. Check EMAIL_ADDRESS and EMAIL_PASSWORD in .env
4. Make sure you're using app password, not regular password

### Issue: "Permission denied" on files

**Solution:**
```bash
# On Linux/Mac
chmod +x scripts/*.py

# On Windows - run as administrator
```

### Issue: Playwright browser not found

**Solution:**
```bash
playwright install chromium
```

### Issue: Lock file error "Another instance running"

**Solution:**
```bash
# Check if actually running
ps aux | grep run_ai_employee

# If not running, remove stale lock
rm logs/ai_employee.lock
```

### Issue: LinkedIn login fails

**Solutions:**
1. Run with visible browser to see what's happening:
   ```bash
   python .claude/skills/linkedin-post/scripts/post_linkedin.py \
     --content "Test" --headless false
   ```
2. LinkedIn may require CAPTCHA
3. Account may be flagged for automation
4. Consider using test account

## Security Best Practices

### 1. Protect .env File
```bash
# Never commit to git
echo ".env" >> .gitignore

# Set restrictive permissions (Linux/Mac)
chmod 600 .env
```

### 2. Rotate Credentials Regularly
- Generate new Gmail app password monthly
- Change LinkedIn password if compromised
- Revoke unused app passwords

### 3. Monitor Logs
```bash
# Check for suspicious activity
tail -f logs/ai_employee.log
tail -f logs/actions.log
```

### 4. Backup Important Data
```bash
# Backup vault regularly
tar -czf backup_$(date +%Y%m%d).tar.gz AI_Employee_Vault/
```

## Next Steps

Once setup is complete:

1. ✓ Read `docs/GMAIL_SETUP.md` for detailed Gmail setup
2. ✓ Read `docs/LINKEDIN_SETUP.md` for LinkedIn considerations
3. ✓ Test each skill individually
4. ✓ Start with manual mode (`--once`)
5. ✓ Move to daemon mode when confident
6. ✓ Monitor logs regularly
7. ✓ Create your own task workflows

## Getting Help

If you encounter issues:

1. Check logs: `logs/ai_employee.log` and `logs/actions.log`
2. Run with `--verbose` flag for detailed output
3. Test individual skills separately
4. Verify credentials in .env
5. Check Python version: `python --version` (should be 3.10+)

## System Requirements

**Minimum:**
- Python 3.10+
- 100 MB disk space
- 512 MB RAM
- Internet connection

**Recommended:**
- Python 3.11+
- 500 MB disk space
- 1 GB RAM
- Stable internet connection

## Success Checklist

- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed
- [ ] .env file created and configured
- [ ] Gmail app password obtained
- [ ] Test task processed successfully
- [ ] System status shows correct information
- [ ] Email sending tested (optional)
- [ ] File management tested
- [ ] Logs are being created

Once all items are checked, your system is ready for production use! 🎉
