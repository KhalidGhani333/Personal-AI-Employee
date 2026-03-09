# Silver Scheduler Skill

## Description
Orchestrates the AI Employee workflow by running vault-watcher and task-planner in a coordinated loop. This skill provides daemon mode for continuous operation, single execution mode for testing, and status monitoring for system health checks.

## When to Trigger
Use this skill when:
- Starting the complete AI Employee system
- Running scheduled task processing
- Monitoring system status and activity
- Automating the entire workflow end-to-end
- Need continuous background processing

## Trigger Phrases
- "Start the AI employee"
- "Run the scheduler"
- "Start daemon mode"
- "Check system status"
- "Process tasks once"

## How It Works

### Daemon Mode (Continuous Operation)
1. Checks for existing instances (lock file)
2. Runs task planner to process inbox files
3. Waits for configured interval (default 5 minutes)
4. Repeats until stopped (Ctrl+C)
5. Logs all activity to `logs/ai_employee.log`
6. Automatically rotates logs at 5MB

### Once Mode (Single Execution)
1. Runs task planner once
2. Reports results
3. Exits

### Status Mode (System Health Check)
1. Shows files in Inbox
2. Shows plans in Needs_Action
3. Shows pending approvals in Needs_Approval
4. Shows recent log activity
5. Shows system uptime if daemon is running

## Execution

### Start Daemon Mode (Continuous)
```bash
python scripts/run_ai_employee.py --daemon
```

### Single Execution
```bash
python scripts/run_ai_employee.py --once
```

### Check Status
```bash
python scripts/run_ai_employee.py --status
```

### Custom Interval (in seconds)
```bash
python scripts/run_ai_employee.py --daemon --interval 180  # 3 minutes
```

### Verbose Logging
```bash
python scripts/run_ai_employee.py --daemon --verbose
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--daemon` | Run continuously in background | Off |
| `--once` | Execute single cycle and exit | Off |
| `--status` | Show system status and exit | Off |
| `--interval SECONDS` | Time between cycles in daemon mode | 300 (5 min) |
| `--verbose` | Enable detailed logging | Off |

## Lock File Mechanism

The scheduler uses a lock file (`logs/ai_employee.lock`) to prevent multiple instances:
- Lock file contains PID and start time
- Automatically cleaned up on graceful shutdown
- Stale lock detection (process no longer running)
- Prevents resource conflicts and duplicate processing

## Log Management

### Log File: `logs/ai_employee.log`
- All scheduler activity logged with timestamps
- Task processing results
- Error messages and warnings
- System events (start, stop, errors)

### Automatic Log Rotation
- Triggers when log exceeds 5MB
- Archives to: `ai_employee_YYYYMMDD_HHMMSS.log`
- Creates fresh log file
- Keeps system running smoothly

## Status Output Example

```
============================================================
AI Employee System Status
============================================================
Timestamp: 2026-02-21 10:30:45

Inbox:
  Files waiting: 3
  - new_task.md
  - client_request.md
  - urgent_email.md

Needs_Action:
  Plans pending: 2
  - Plan_new_task_20260221_103000.md
  - Plan_client_request_20260221_102500.md

Needs_Approval:
  Approvals pending: 1
  - send_email_approval.md

Daemon Status:
  Running: Yes
  PID: 12345
  Uptime: 2 hours 15 minutes
  Last cycle: 2 minutes ago

Recent Activity (last 10 entries):
  [2026-02-21 10:28:30] [INFO] Task Planner completed: 1/1 files
  [2026-02-21 10:23:15] [INFO] Scheduler cycle completed
  [2026-02-21 10:18:00] [INFO] Processing inbox files...
============================================================
```

## Integration with Other Skills

### Vault Watcher Integration
The scheduler replaces the need for continuous vault-watcher by running task-planner on a schedule. This is more resource-efficient for most use cases.

### Task Planner Integration
Calls `task_planner.py` directly to process inbox files and create execution plans.

### Human Approval Integration
Status mode shows pending approvals. Can be extended to automatically call approval workflow.

## Use Cases

### 1. Production Deployment
```bash
# Start as background service
nohup python scripts/run_ai_employee.py --daemon > /dev/null 2>&1 &
```

### 2. Development/Testing
```bash
# Run once to test
python scripts/run_ai_employee.py --once --verbose
```

### 3. Monitoring
```bash
# Check status periodically
watch -n 60 python scripts/run_ai_employee.py --status
```

### 4. Cron Job (Alternative to Daemon)
```bash
# Add to crontab - run every 5 minutes
*/5 * * * * cd /path/to/project && python scripts/run_ai_employee.py --once
```

## Error Handling

- **Lock file conflicts**: Detects and reports if another instance is running
- **Stale locks**: Automatically cleans up if process no longer exists
- **Processing errors**: Logs errors but continues running in daemon mode
- **Graceful shutdown**: Ctrl+C cleanly stops daemon and removes lock file
- **Log rotation errors**: Continues operation even if rotation fails

## Requirements
- Python 3.6+
- No external dependencies (standard library only)
- Write permissions for logs/ directory
- Existing task_planner.py script

## Performance Notes

- **Resource usage**: Minimal CPU/memory when idle
- **Disk I/O**: Only during processing cycles
- **Scalability**: Handles hundreds of files efficiently
- **Recommended interval**: 5 minutes for most use cases, 1 minute for high-volume

## Security Considerations

- Lock file prevents race conditions
- Logs may contain sensitive information - secure appropriately
- PID in lock file allows process verification
- No network access required

## Troubleshooting

### "Another instance is already running"
- Check if process is actually running: `ps aux | grep run_ai_employee`
- If not running, remove stale lock: `rm logs/ai_employee.lock`

### Logs not rotating
- Check disk space
- Verify write permissions on logs/ directory
- Check log file size: `ls -lh logs/ai_employee.log`

### Daemon not processing files
- Check status: `python scripts/run_ai_employee.py --status`
- Review logs: `tail -f logs/ai_employee.log`
- Test single execution: `python scripts/run_ai_employee.py --once --verbose`
