# Log Manager - Detailed Instructions

## Objective
Maintain comprehensive, searchable audit logs for all AI Employee activities, errors, and system events.

## Log Structure

### Daily Log File Format
```json
{
  "date": "2026-02-06",
  "entries": [
    {
      "timestamp": "2026-02-06T10:30:45Z",
      "level": "info|warning|error|critical",
      "action_type": "email_send|task_create|file_process|etc",
      "actor": "ai_employee|human|system",
      "description": "Processed email from client@example.com",
      "metadata": {
        "email_id": "12345",
        "from": "client@example.com",
        "subject": "Invoice Request",
        "priority": "high"
      },
      "result": "success|failure",
      "duration_ms": 1234,
      "error": null
    }
  ]
}
```

### Log Levels

**INFO**: Normal operations
```json
{
  "level": "info",
  "action_type": "email_processed",
  "description": "Successfully processed email",
  "result": "success"
}
```

**WARNING**: Potential issues
```json
{
  "level": "warning",
  "action_type": "approval_timeout",
  "description": "Approval request expired",
  "metadata": {
    "approval_id": "APPROVAL_123",
    "age_hours": 25
  }
}
```

**ERROR**: Operation failures
```json
{
  "level": "error",
  "action_type": "email_send_failed",
  "description": "Failed to send email",
  "error": {
    "type": "SMTPException",
    "message": "Connection timeout",
    "stack_trace": "..."
  }
}
```

**CRITICAL**: System failures
```json
{
  "level": "critical",
  "action_type": "system_crash",
  "description": "Orchestrator crashed",
  "error": {
    "type": "MemoryError",
    "message": "Out of memory"
  }
}
```

## Logging Operations

### 1. Create Log Entry

```python
import json
from datetime import datetime
from pathlib import Path

def log_action(
    level: str,
    action_type: str,
    description: str,
    metadata: dict = None,
    result: str = "success",
    error: dict = None
):
    """Create a log entry"""

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "action_type": action_type,
        "actor": "ai_employee",
        "description": description,
        "metadata": metadata or {},
        "result": result,
        "error": error
    }

    # Append to daily log file
    log_file = Path(f"Logs/{datetime.now().strftime('%Y-%m-%d')}.json")

    if log_file.exists():
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = {"date": datetime.now().strftime('%Y-%m-%d'), "entries": []}

    log_data["entries"].append(log_entry)

    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
```

### 2. Log Action Types

**Email Operations:**
```python
log_action(
    level="info",
    action_type="email_processed",
    description=f"Processed email from {sender}",
    metadata={
        "email_id": email_id,
        "from": sender,
        "subject": subject,
        "category": category
    }
)
```

**Task Operations:**
```python
log_action(
    level="info",
    action_type="task_created",
    description=f"Created task: {task_title}",
    metadata={
        "task_id": task_id,
        "priority": priority,
        "due_date": due_date
    }
)
```

**Approval Operations:**
```python
log_action(
    level="info",
    action_type="approval_granted",
    description=f"Approved action: {action_type}",
    metadata={
        "approval_id": approval_id,
        "action": action_type,
        "approved_by": "human",
        "approved_at": timestamp
    }
)
```

**Error Operations:**
```python
log_action(
    level="error",
    action_type="file_processing_failed",
    description=f"Failed to process file: {filename}",
    metadata={
        "file_path": file_path,
        "file_type": file_type
    },
    result="failure",
    error={
        "type": type(e).__name__,
        "message": str(e),
        "stack_trace": traceback.format_exc()
    }
)
```

### 3. Generate Reports

**Daily Summary:**
```markdown
# Daily Log Summary - {date}

## Statistics
- Total Actions: {count}
- Successful: {success_count} ({percentage}%)
- Failed: {failure_count} ({percentage}%)
- Warnings: {warning_count}

## Action Breakdown
- Emails Processed: {count}
- Tasks Created: {count}
- Files Processed: {count}
- Approvals Handled: {count}

## Errors
{error_list}

## Top Actions
1. {action_type}: {count} times
2. {action_type}: {count} times
3. {action_type}: {count} times
```

**Weekly Summary:**
```markdown
# Weekly Log Summary - Week of {date}

## Overview
- Total Actions: {count}
- Success Rate: {percentage}%
- Average Actions/Day: {avg}

## Trends
- Most Active Day: {day} ({count} actions)
- Most Common Action: {action_type}
- Error Rate: {percentage}%

## Issues Detected
- {issue_1}
- {issue_2}

## Recommendations
- {recommendation_1}
- {recommendation_2}
```

**Error Report:**
```markdown
# Error Report - {date}

## Critical Errors ({count})
{list_of_critical_errors}

## Errors ({count})
{list_of_errors}

## Warnings ({count})
{list_of_warnings}

## Error Patterns
- {pattern_1}: {count} occurrences
- {pattern_2}: {count} occurrences

## Action Items
- [ ] {action_1}
- [ ] {action_2}
```

### 4. Search Logs

**Search by Action Type:**
```python
def search_logs(action_type: str, start_date: str, end_date: str):
    """Search logs for specific action type"""
    results = []

    for log_file in Path("Logs").glob("*.json"):
        with open(log_file, 'r') as f:
            log_data = json.load(f)

        for entry in log_data["entries"]:
            if entry["action_type"] == action_type:
                if start_date <= entry["timestamp"] <= end_date:
                    results.append(entry)

    return results
```

**Search by Error:**
```python
def find_errors(level: str = "error", days: int = 7):
    """Find all errors in last N days"""
    errors = []

    for log_file in get_recent_logs(days):
        with open(log_file, 'r') as f:
            log_data = json.load(f)

        for entry in log_data["entries"]:
            if entry["level"] == level:
                errors.append(entry)

    return errors
```

### 5. Archive Old Logs

**Archive Strategy:**
```
- Keep last 30 days: Full detail
- 30-90 days: Compress to .gz
- 90+ days: Archive to /Logs/Archive/
- 1+ year: Delete or move to cold storage
```

**Archive Process:**
```python
import gzip
import shutil
from datetime import datetime, timedelta

def archive_old_logs():
    """Archive logs older than 30 days"""

    cutoff_date = datetime.now() - timedelta(days=30)

    for log_file in Path("Logs").glob("*.json"):
        file_date = datetime.strptime(log_file.stem, '%Y-%m-%d')

        if file_date < cutoff_date:
            # Compress
            with open(log_file, 'rb') as f_in:
                with gzip.open(f"{log_file}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Move to archive
            archive_path = Path("Logs/Archive")
            archive_path.mkdir(exist_ok=True)
            shutil.move(f"{log_file}.gz", archive_path)

            # Delete original
            log_file.unlink()
```

## System Health Monitoring

**Health Metrics:**
```json
{
  "timestamp": "2026-02-06T10:00:00Z",
  "metrics": {
    "actions_per_hour": 45,
    "success_rate": 98.5,
    "average_response_time_ms": 234,
    "error_rate": 1.5,
    "pending_approvals": 3,
    "active_tasks": 12,
    "disk_usage_mb": 1234,
    "memory_usage_mb": 512
  }
}
```

**Health Check:**
```python
def check_system_health():
    """Check system health and log metrics"""

    metrics = {
        "actions_per_hour": calculate_action_rate(),
        "success_rate": calculate_success_rate(),
        "error_rate": calculate_error_rate(),
        "pending_approvals": count_pending_approvals(),
        "active_tasks": count_active_tasks()
    }

    # Log metrics
    log_action(
        level="info",
        action_type="health_check",
        description="System health check",
        metadata=metrics
    )

    # Alert if issues
    if metrics["error_rate"] > 5:
        log_action(
            level="warning",
            action_type="high_error_rate",
            description=f"Error rate is {metrics['error_rate']}%"
        )
```

## Integration Points

- **All Skills**: Log their actions
- **Dashboard Updater**: Display log stats
- **Notification Skill**: Alert on critical errors
- **Business Auditor**: Include in weekly briefing

## Success Criteria
- All actions logged
- No log data loss
- Searchable logs
- Reports generated on time
- Old logs archived
- System health monitored
