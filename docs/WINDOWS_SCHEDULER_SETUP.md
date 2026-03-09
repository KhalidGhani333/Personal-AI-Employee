# Windows Task Scheduler Setup Guide

This guide helps you set up automated scheduling for the AI Employee system using Windows Task Scheduler.

## Quick Setup (Recommended)

Run the automated setup script:

```bash
python scripts/setup_windows_scheduler.py
```

This will create all necessary scheduled tasks automatically.

---

## Manual Setup

If you prefer manual setup, follow these steps:

### 1. Gmail Watcher (Every 5 minutes)

1. Open Task Scheduler (search "Task Scheduler" in Windows)
2. Click "Create Basic Task"
3. Name: `AI Employee - Gmail Watcher`
4. Trigger: Daily, repeat every 5 minutes
5. Action: Start a program
   - Program: `python`
   - Arguments: `scripts/gmail_watcher.py --once`
   - Start in: `D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Personal AI Employee`

### 2. WhatsApp Watcher (Every 2 minutes)

1. Create Basic Task
2. Name: `AI Employee - WhatsApp Watcher`
3. Trigger: Daily, repeat every 2 minutes
4. Action: Start a program
   - Program: `python`
   - Arguments: `scripts/whatsapp_watcher.py --once`
   - Start in: `D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Personal AI Employee`

### 3. Reply Generator (Every 5 minutes)

1. Create Basic Task
2. Name: `AI Employee - Reply Generator`
3. Trigger: Daily, repeat every 5 minutes
4. Action: Start a program
   - Program: `python`
   - Arguments: `scripts/reply_generator.py`
   - Start in: `D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Personal AI Employee`

### 4. Reply Sender (Every 10 minutes)

1. Create Basic Task
2. Name: `AI Employee - Reply Sender`
3. Trigger: Daily, repeat every 10 minutes
4. Action: Start a program
   - Program: `python`
   - Arguments: `scripts/reply_sender.py`
   - Start in: `D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Personal AI Employee`

### 5. LinkedIn Auto Poster (Every 30 minutes)

1. Create Basic Task
2. Name: `AI Employee - LinkedIn Auto Poster`
3. Trigger: Daily, repeat every 30 minutes
4. Action: Start a program
   - Program: `python`
   - Arguments: `scripts/linkedin_auto_poster.py --process`
   - Start in: `D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Personal AI Employee`

### 6. Main Orchestrator (Every 5 minutes)

1. Create Basic Task
2. Name: `AI Employee - Orchestrator`
3. Trigger: Daily, repeat every 5 minutes
4. Action: Start a program
   - Program: `python`
   - Arguments: `scripts/run_ai_employee.py --once`
   - Start in: `D:\Giaic\spec-kit-plus\Hackhton_0\AI Employee\Personal AI Employee`

---

## Advanced Configuration

### Set Task Priority

1. Right-click on task → Properties
2. Go to "General" tab
3. Check "Run with highest privileges" (if needed)
4. Select "Run whether user is logged on or not"

### Configure Triggers

1. Right-click on task → Properties
2. Go to "Triggers" tab
3. Edit trigger
4. Check "Repeat task every: X minutes"
5. Set "for a duration of: Indefinitely"
6. Check "Enabled"

### Set Conditions

1. Right-click on task → Properties
2. Go to "Conditions" tab
3. Uncheck "Start the task only if the computer is on AC power"
4. Check "Wake the computer to run this task" (optional)

### Configure Actions

1. Right-click on task → Properties
2. Go to "Actions" tab
3. Edit action
4. Ensure paths are absolute, not relative

---

## Verify Setup

Check if tasks are running:

```bash
# View scheduled tasks
schtasks /query /fo LIST /v | findstr "AI Employee"

# Check task status
python scripts/check_scheduler_status.py
```

---

## Troubleshooting

### Task Not Running

**Problem:** Task shows "Ready" but never runs
- **Solution:** Check trigger settings, ensure "Repeat task every" is set
- Verify "Start in" directory is correct
- Check Python path is correct

### Task Fails Immediately

**Problem:** Task runs but fails instantly
- **Solution:** Check logs in `logs/` folder
- Verify all dependencies are installed
- Test script manually first: `python scripts/script_name.py`

### Permission Denied

**Problem:** Task fails with permission error
- **Solution:** Run Task Scheduler as Administrator
- Set task to "Run with highest privileges"
- Check file/folder permissions

### Python Not Found

**Problem:** Task fails with "python not found"
- **Solution:** Use full Python path instead of just "python"
- Example: `C:\Users\YourName\AppData\Local\Programs\Python\Python313\python.exe`
- Or use: `py` instead of `python`

---

## Disable/Enable Tasks

### Disable All Tasks

```bash
python scripts/setup_windows_scheduler.py --disable
```

Or manually:
1. Open Task Scheduler
2. Find "AI Employee" tasks
3. Right-click → Disable

### Enable All Tasks

```bash
python scripts/setup_windows_scheduler.py --enable
```

---

## Remove All Tasks

```bash
python scripts/setup_windows_scheduler.py --remove
```

Or manually:
1. Open Task Scheduler
2. Find "AI Employee" tasks
3. Right-click → Delete

---

## Recommended Schedule

| Task | Interval | Reason |
|------|----------|--------|
| Gmail Watcher | 5 min | Balance between responsiveness and API limits |
| WhatsApp Watcher | 2 min | More frequent for instant messaging |
| Reply Generator | 5 min | Process pending messages regularly |
| Reply Sender | 10 min | Give time for human approval |
| LinkedIn Auto Poster | 30 min | Check for scheduled posts |
| Main Orchestrator | 5 min | Process inbox and tasks |

---

## Alternative: Use Daemon Mode

Instead of Task Scheduler, you can run watchers in daemon mode:

```bash
# Start all watchers in background
start /B python scripts/gmail_watcher.py --continuous --interval 300
start /B python scripts/whatsapp_watcher.py --continuous --interval 120
start /B python scripts/reply_generator.py --continuous --interval 300
start /B python scripts/run_ai_employee.py --daemon --interval 300
```

**Pros:**
- Simpler setup
- Lower overhead
- Easier to monitor

**Cons:**
- Requires terminal to stay open
- Stops when you log out
- No automatic restart on failure

---

## Best Practice

**For Development:** Use daemon mode
**For Production:** Use Task Scheduler

Task Scheduler provides:
- Automatic restart on failure
- Runs even when logged out
- Better resource management
- Centralized monitoring

---

## Monitoring

Check task execution:

```bash
# View task history
Get-ScheduledTask | Where-Object {$_.TaskName -like "*AI Employee*"} | Get-ScheduledTaskInfo

# Check logs
type logs\ai_employee.log
```

---

**Last Updated:** 2026-03-10
**Version:** 1.0
