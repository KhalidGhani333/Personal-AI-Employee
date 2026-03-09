# Vault Watcher Skill

## Description
Continuously monitors the `AI_Employee_Vault/Inbox` folder for new markdown files and automatically triggers the AI processing workflow when files are detected.

## When to Trigger
Use this skill when the user wants to:
- Start continuous monitoring of the Inbox folder
- Automatically process new markdown files as they arrive
- Run the vault watcher in the background
- Set up automated file processing

## Trigger Phrases
- "Start vault watcher"
- "Monitor the inbox"
- "Watch for new files"
- "Start the vault monitoring"
- "Run vault watcher"

## How It Works
1. Monitors `AI_Employee_Vault/Inbox` folder every 15 seconds
2. Detects new `.md` files
3. Logs detection to `logs/actions.log`
4. Triggers AI processing workflow (`run_ai_employee.py --once`)
5. Tracks processed files to prevent duplicates
6. Runs continuously until stopped (Ctrl+C)

## Execution

When this skill is invoked, run:

```bash
python scripts/watch_inbox.py
```

The watcher will:
- Create required folders if they don't exist
- Log all activity to `logs/actions.log`
- Process each new `.md` file exactly once
- Handle errors gracefully without crashing
- Display status updates in the console

## Stopping the Watcher

Press `Ctrl+C` to stop the watcher gracefully.

## Requirements
- Python 3.6+
- No external dependencies (uses standard library only)
- `run_ai_employee.py` script should exist in the project root

## Logs
All activity is logged to `logs/actions.log` with timestamps:
- File detections
- Processing triggers
- Errors and warnings
- Start/stop events
