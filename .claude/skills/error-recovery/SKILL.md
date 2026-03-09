# Error Recovery Skill

Automatic error handling with logging, file management, and retry logic.

## Usage

The error recovery system works automatically when integrated into task execution, or can be used manually:

```bash
# Test retry logic
python scripts/error_recovery.py test-retry

# Test failure handling
python scripts/error_recovery.py test-failure

# View recent errors
python scripts/error_recovery.py view-errors
```

## Features

### 1. Error Logging
All errors are logged to `Logs/errors.log` with:
- Timestamp
- Error type
- Error message
- Full traceback
- Context information

### 2. File Management
Failed task files are automatically moved to:
```
AI_Employee_Vault/Errors/ERROR_<timestamp>_<filename>
```

### 3. Retry Logic
Tasks are automatically retried once after 5 minutes:
- Initial attempt
- Wait 5 minutes on failure
- Retry once
- Log all attempts

### 4. Decorator Support
Use the `@with_error_recovery` decorator for automatic error handling:

```python
from scripts.error_recovery import with_error_recovery

@with_error_recovery(retry_delay=300, max_retries=1)
def my_task():
    # Your task code here
    pass
```

## Error Handling Workflow

When a task fails:

1. **Log Error**
   - Write to `Logs/errors.log`
   - Include timestamp, error type, message, traceback
   - Add context information

2. **Move File**
   - Move task file to `AI_Employee_Vault/Errors/`
   - Add timestamp prefix: `ERROR_20260225_143000_taskname.md`
   - Preserve original filename

3. **Retry Once**
   - Wait 5 minutes (configurable)
   - Retry task execution
   - Log retry attempt

4. **Final Status**
   - Return success/failure status
   - Include attempt count
   - Provide error details if failed

## API Reference

### ErrorRecoverySystem Class

#### `log_error(error, context)`
Log error details to errors.log

**Parameters:**
- `error` (Exception): The exception that occurred
- `context` (dict): Additional context information

**Example:**
```python
from scripts.error_recovery import error_recovery

try:
    # Task code
    pass
except Exception as e:
    error_recovery.log_error(e, {
        "task": "send_email",
        "recipient": "client@example.com"
    })
```

#### `move_to_errors(file_path)`
Move failed task file to Errors folder

**Parameters:**
- `file_path` (Path): Path to the failed task file

**Returns:**
- Path to moved file, or None if failed

**Example:**
```python
from pathlib import Path
from scripts.error_recovery import error_recovery

task_file = Path("AI_Employee_Vault/Needs_Action/task.md")
error_path = error_recovery.move_to_errors(task_file)
```

#### `retry_task(task_func, task_args, task_kwargs, retry_delay, max_retries)`
Execute task with retry logic

**Parameters:**
- `task_func` (Callable): Function to execute
- `task_args` (tuple): Positional arguments
- `task_kwargs` (dict): Keyword arguments
- `retry_delay` (int): Delay in seconds before retry (default: 300)
- `max_retries` (int): Maximum retries (default: 1)

**Returns:**
- Dict with success status and result/error

**Example:**
```python
from scripts.error_recovery import error_recovery

def send_email(to, subject):
    # Email sending code
    pass

result = error_recovery.retry_task(
    send_email,
    task_args=("client@example.com", "Update"),
    retry_delay=300,
    max_retries=1
)

if result["success"]:
    print(f"Success after {result['attempts']} attempts")
else:
    print(f"Failed: {result['error']}")
```

#### `handle_task_failure(task_file, error, context)`
Complete error handling workflow

**Parameters:**
- `task_file` (Path): Path to failed task file
- `error` (Exception): The exception that occurred
- `context` (dict): Additional context

**Returns:**
- Dict with error handling results

**Example:**
```python
from pathlib import Path
from scripts.error_recovery import error_recovery

task_file = Path("AI_Employee_Vault/Needs_Action/task.md")
error = Exception("Task failed")

result = error_recovery.handle_task_failure(
    task_file,
    error,
    {"task_type": "email", "priority": "high"}
)
```

#### `execute_with_recovery(task_func, task_file, ...)`
Execute task with full error recovery

Combines retry logic with error handling workflow.

**Parameters:**
- `task_func` (Callable): Function to execute
- `task_file` (Path): Optional task file to move on failure
- `task_args` (tuple): Positional arguments
- `task_kwargs` (dict): Keyword arguments
- `retry_delay` (int): Delay before retry (default: 300)
- `max_retries` (int): Maximum retries (default: 1)

**Returns:**
- Dict with execution results

**Example:**
```python
from pathlib import Path
from scripts.error_recovery import error_recovery

def process_task():
    # Task processing code
    pass

task_file = Path("AI_Employee_Vault/Needs_Action/task.md")

result = error_recovery.execute_with_recovery(
    process_task,
    task_file=task_file,
    retry_delay=300,
    max_retries=1
)
```

### Decorator: `@with_error_recovery`

Automatic error recovery decorator

**Parameters:**
- `retry_delay` (int): Delay before retry in seconds (default: 300)
- `max_retries` (int): Maximum retries (default: 1)

**Example:**
```python
from scripts.error_recovery import with_error_recovery

@with_error_recovery(retry_delay=300, max_retries=1)
def send_email(to, subject, body):
    # Email sending code
    pass

# Automatic retry on failure
result = send_email("client@example.com", "Update", "Content")
```

## Integration

### With Task Executor

```python
from scripts.error_recovery import error_recovery
from pathlib import Path

def execute_task(task_file):
    def task_logic():
        # Your task execution code
        content = task_file.read_text()
        # Process task...
        return "Success"

    result = error_recovery.execute_with_recovery(
        task_logic,
        task_file=task_file,
        retry_delay=300,
        max_retries=1
    )

    return result
```

### With Orchestrator

```python
from scripts.error_recovery import error_recovery

# In your main orchestrator loop
for task_file in get_pending_tasks():
    try:
        result = process_task(task_file)
    except Exception as e:
        error_recovery.handle_task_failure(
            task_file,
            e,
            {"source": "orchestrator"}
        )
```

## Error Log Format

Errors are logged in JSON format:

```json
{
  "timestamp": "2026-02-25T14:30:00.123456",
  "error_type": "ConnectionError",
  "error_message": "Failed to connect to SMTP server",
  "traceback": "Traceback (most recent call last)...",
  "context": {
    "task_file": "AI_Employee_Vault/Needs_Action/send_email.md",
    "task_name": "send_email",
    "attempt": 1,
    "max_retries": 1
  }
}
```

## File Naming Convention

Failed task files are moved with this naming pattern:
```
ERROR_<YYYYMMDD>_<HHMMSS>_<original_filename>
```

Example:
```
ERROR_20260225_143000_send_client_email.md
```

## Configuration

Default settings:
- **Retry Delay:** 300 seconds (5 minutes)
- **Max Retries:** 1
- **Error Log:** `Logs/errors.log`
- **Error Folder:** `AI_Employee_Vault/Errors/`

These can be customized when calling the functions.

## Commands

### Test Retry Logic
```bash
python scripts/error_recovery.py test-retry
```
Tests the retry mechanism with a simulated failure.

### Test Failure Handling
```bash
python scripts/error_recovery.py test-failure
```
Creates a test task file and simulates a failure to test the complete workflow.

### View Recent Errors
```bash
python scripts/error_recovery.py view-errors
```
Displays the last 10 errors from the error log.

## Best Practices

1. **Always provide context** when logging errors
2. **Use meaningful task file names** for easier debugging
3. **Monitor the error log** regularly
4. **Review failed tasks** in the Errors folder
5. **Adjust retry delay** based on error type
6. **Clean up old errors** periodically

## Example: Complete Integration

```python
from pathlib import Path
from scripts.error_recovery import error_recovery

def process_email_task(task_file: Path):
    """Process email task with error recovery"""

    def send_email():
        # Read task
        content = task_file.read_text()

        # Extract email details
        # ... parsing code ...

        # Send email
        # ... email sending code ...

        return "Email sent successfully"

    # Execute with full error recovery
    result = error_recovery.execute_with_recovery(
        send_email,
        task_file=task_file,
        retry_delay=300,  # 5 minutes
        max_retries=1
    )

    if result["success"]:
        print(f"Task completed after {result['attempts']} attempts")
        # Move to Done folder
    else:
        print(f"Task failed: {result['error']}")
        # File already moved to Errors folder

    return result
```

## Notes

- Retry delay is configurable (default: 5 minutes)
- Maximum retries is configurable (default: 1)
- All errors are logged regardless of retry success
- Failed files are moved only after all retries exhausted
- Decorator provides simplified error handling
- System is thread-safe for concurrent operations
