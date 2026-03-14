"""
Silver Scheduler - AI Employee Orchestrator
============================================
This script orchestrates the AI Employee workflow by running task-planner
in a coordinated loop with daemon mode, single execution, and status monitoring.

Features:
- Daemon mode: Continuous operation with configurable interval
- Once mode: Single execution for testing
- Status mode: System health check and monitoring
- Lock file: Prevents duplicate instances
- Log rotation: Automatic at 5MB
- Graceful shutdown: Clean Ctrl+C handling
"""

import os
import sys
import time
import argparse
import subprocess
import signal
from datetime import datetime, timedelta
from pathlib import Path


# Configuration
VAULT_PATH = Path("AI_Employee_Vault")
INBOX_FOLDER = VAULT_PATH / "Inbox"
NEEDS_ACTION_FOLDER = VAULT_PATH / "Needs_Action"
NEEDS_APPROVAL_FOLDER = VAULT_PATH / "Needs_Approval"
DONE_FOLDER = VAULT_PATH / "Done"
LOGS_FOLDER = Path("logs")
LOG_FILE = LOGS_FOLDER / "ai_employee.log"
LOCK_FILE = LOGS_FOLDER / "ai_employee.lock"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB
DEFAULT_INTERVAL = 300  # 5 minutes

# Global flag for graceful shutdown
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    shutdown_requested = True
    print("\n[INFO] Shutdown requested... cleaning up")


def get_timestamp():
    """Returns current timestamp in readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rotate_log_if_needed():
    """
    Rotates log file if it exceeds MAX_LOG_SIZE.
    Archives to timestamped file and creates fresh log.
    """
    try:
        if not LOG_FILE.exists():
            return

        file_size = LOG_FILE.stat().st_size
        if file_size > MAX_LOG_SIZE:
            # Create archive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"ai_employee_{timestamp}.log"
            archive_path = LOGS_FOLDER / archive_name

            # Rename current log to archive
            LOG_FILE.rename(archive_path)

            # Log rotation event to new file
            log_message(f"Log rotated: {archive_name} ({file_size / 1024 / 1024:.2f} MB)", "INFO")

    except Exception as e:
        # Don't fail if rotation fails, just continue
        print(f"[WARNING] Log rotation failed: {e}")


def log_message(message, level="INFO"):
    """
    Logs a message to the log file with timestamp.

    Args:
        message: The message to log
        level: Log level (INFO, WARNING, ERROR)
    """
    try:
        # Ensure logs folder exists
        LOGS_FOLDER.mkdir(exist_ok=True)

        # Check if rotation needed before writing
        rotate_log_if_needed()

        # Create log entry
        timestamp = get_timestamp()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        # Append to log file
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        # Also print to console if verbose or error
        if level in ["ERROR", "WARNING"] or getattr(log_message, 'verbose', False):
            print(f"[{level}] {message}")

    except Exception as e:
        print(f"[WARNING] Failed to write log: {e}")


def create_lock_file():
    """
    Creates a lock file with current PID and timestamp.

    Returns:
        True if lock created successfully, False if another instance is running
    """
    try:
        LOGS_FOLDER.mkdir(exist_ok=True)

        # Check if lock file exists
        if LOCK_FILE.exists():
            # Read existing lock
            lock_content = LOCK_FILE.read_text().strip().split('\n')
            if len(lock_content) >= 2:
                try:
                    existing_pid = int(lock_content[0])
                    lock_time = lock_content[1]

                    # Check if process is still running
                    if is_process_running(existing_pid):
                        print(f"[ERROR] Another instance is already running (PID: {existing_pid})")
                        print(f"Started at: {lock_time}")
                        print(f"Lock file: {LOCK_FILE}")
                        return False
                    else:
                        print(f"[WARNING] Removing stale lock file (PID {existing_pid} not running)")
                        LOCK_FILE.unlink()
                except (ValueError, IndexError):
                    print("[WARNING] Invalid lock file, removing")
                    LOCK_FILE.unlink()

        # Create new lock file
        pid = os.getpid()
        timestamp = get_timestamp()
        lock_content = f"{pid}\n{timestamp}\n"
        LOCK_FILE.write_text(lock_content)

        log_message(f"Lock file created (PID: {pid})", "INFO")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to create lock file: {e}")
        return False


def remove_lock_file():
    """Removes the lock file on shutdown."""
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
            log_message("Lock file removed", "INFO")
    except Exception as e:
        print(f"[WARNING] Failed to remove lock file: {e}")


def is_process_running(pid):
    """
    Checks if a process with given PID is running.

    Args:
        pid: Process ID to check

    Returns:
        True if process is running, False otherwise
    """
    try:
        # On Windows and Unix, sending signal 0 checks if process exists
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def run_task_planner(verbose=False):
    """
    Runs the task planner to process inbox files.

    Args:
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    try:
        log_message("Running task planner...", "INFO")

        # Run task planner
        result = subprocess.run(
            ['python', 'scripts/task_planner.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            # Parse output for summary
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if 'Processed:' in line or 'No new files' in line:
                    log_message(f"Task planner: {line.strip()}", "INFO")
            return True
        else:
            log_message(f"Task planner failed: {result.stderr}", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log_message("Task planner timeout (exceeded 5 minutes)", "ERROR")
        return False
    except Exception as e:
        log_message(f"Error running task planner: {e}", "ERROR")
        return False


def run_task_executor(verbose=False):
    """
    Runs the task executor to process Needs_Action files.

    Args:
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    try:
        log_message("Running task executor...", "INFO")

        # Run ralph wiggum loop
        result = subprocess.run(
            ['python', 'scripts/ralph_wiggum_loop.py'],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode == 0:
            # Parse output for summary
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if 'success' in line.lower() or 'completed' in line.lower() or 'No tasks' in line:
                    log_message(f"Task executor: {line.strip()}", "INFO")
            return True
        else:
            log_message(f"Task executor failed: {result.stderr}", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log_message("Task executor timeout (exceeded 10 minutes)", "ERROR")
        return False
    except Exception as e:
        log_message(f"Error running task executor: {e}", "ERROR")
        return False


def get_folder_file_count(folder_path, extension='.md'):
    """
    Counts files in a folder with given extension.

    Args:
        folder_path: Path to folder
        extension: File extension to count (default .md)

    Returns:
        Tuple of (count, list of filenames)
    """
    try:
        if not folder_path.exists():
            return 0, []

        files = [f.name for f in folder_path.iterdir()
                if f.is_file() and f.suffix.lower() == extension]
        return len(files), files

    except Exception as e:
        log_message(f"Error reading folder {folder_path}: {e}", "WARNING")
        return 0, []


def get_lock_info():
    """
    Reads lock file information.

    Returns:
        Dictionary with PID, start_time, uptime, or None if no lock
    """
    try:
        if not LOCK_FILE.exists():
            return None

        lock_content = LOCK_FILE.read_text().strip().split('\n')
        if len(lock_content) >= 2:
            pid = int(lock_content[0])
            start_time_str = lock_content[1]

            # Check if process is running
            if not is_process_running(pid):
                return None

            # Calculate uptime
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            uptime = datetime.now() - start_time

            return {
                'pid': pid,
                'start_time': start_time_str,
                'uptime': uptime,
                'running': True
            }

        return None

    except Exception as e:
        log_message(f"Error reading lock file: {e}", "WARNING")
        return None


def show_status():
    """Displays system status information."""
    print("=" * 60)
    print("AI Employee System Status")
    print("=" * 60)
    print(f"Timestamp: {get_timestamp()}\n")

    # Inbox status
    inbox_count, inbox_files = get_folder_file_count(INBOX_FOLDER)
    print(f"Inbox:")
    print(f"  Files waiting: {inbox_count}")
    if inbox_files:
        for filename in inbox_files[:5]:  # Show first 5
            print(f"  - {filename}")
        if len(inbox_files) > 5:
            print(f"  ... and {len(inbox_files) - 5} more")
    print()

    # Needs Action status
    action_count, action_files = get_folder_file_count(NEEDS_ACTION_FOLDER)
    print(f"Needs_Action:")
    print(f"  Plans pending: {action_count}")
    if action_files:
        for filename in action_files[:5]:
            print(f"  - {filename}")
        if len(action_files) > 5:
            print(f"  ... and {len(action_files) - 5} more")
    print()

    # Needs Approval status
    approval_count, approval_files = get_folder_file_count(NEEDS_APPROVAL_FOLDER)
    print(f"Needs_Approval:")
    print(f"  Approvals pending: {approval_count}")
    if approval_files:
        for filename in approval_files[:5]:
            print(f"  - {filename}")
        if len(approval_files) > 5:
            print(f"  ... and {len(approval_files) - 5} more")
    print()

    # Daemon status
    lock_info = get_lock_info()
    print(f"Daemon Status:")
    if lock_info:
        print(f"  Running: Yes")
        print(f"  PID: {lock_info['pid']}")
        uptime = lock_info['uptime']
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        print(f"  Uptime: {hours} hours {minutes} minutes")
        print(f"  Started: {lock_info['start_time']}")
    else:
        print(f"  Running: No")
    print()

    # Recent activity
    print(f"Recent Activity (last 10 entries):")
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                recent = lines[-10:] if len(lines) >= 10 else lines
                for line in recent:
                    print(f"  {line.strip()}")
        else:
            print("  No log file found")
    except Exception as e:
        print(f"  Error reading log: {e}")

    print("=" * 60)


def run_once(verbose=False):
    """
    Runs a single processing cycle.

    Args:
        verbose: Enable verbose output

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    log_message.verbose = verbose

    print("=" * 60)
    print("AI Employee - Single Execution Mode")
    print("=" * 60)

    log_message("Single execution started", "INFO")

    # Run task planner (Inbox → Needs_Action)
    planner_success = run_task_planner(verbose)

    # Run task executor (Needs_Action → Done)
    executor_success = run_task_executor(verbose)

    if planner_success and executor_success:
        print("\n[OK] Execution completed successfully")
        log_message("Single execution completed successfully", "INFO")
        return 0
    else:
        print("\n[ERROR] Execution failed - check logs")
        log_message("Single execution failed", "ERROR")
        return 1


def run_daemon(interval, verbose=False):
    """
    Runs continuous daemon mode.

    Args:
        interval: Seconds between processing cycles
        verbose: Enable verbose output

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    global shutdown_requested
    log_message.verbose = verbose

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create lock file
    if not create_lock_file():
        return 1

    print("=" * 60)
    print("AI Employee - Daemon Mode")
    print("=" * 60)
    print(f"Interval: {interval} seconds ({interval/60:.1f} minutes)")
    print(f"Log file: {LOG_FILE}")
    print(f"PID: {os.getpid()}")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    log_message(f"Daemon started (interval: {interval}s)", "INFO")

    cycle_count = 0

    try:
        while not shutdown_requested:
            cycle_count += 1
            log_message(f"Starting cycle #{cycle_count}", "INFO")

            # Run task planner (Inbox → Needs_Action)
            run_task_planner(verbose)

            # Run task executor (Needs_Action → Done)
            run_task_executor(verbose)

            log_message(f"Cycle #{cycle_count} completed", "INFO")

            # Wait for next cycle (check shutdown flag every second)
            for _ in range(interval):
                if shutdown_requested:
                    break
                time.sleep(1)

    except Exception as e:
        log_message(f"Daemon error: {e}", "ERROR")
        print(f"\n[ERROR] Daemon error: {e}")
        return 1

    finally:
        # Clean up
        remove_lock_file()
        log_message(f"Daemon stopped (completed {cycle_count} cycles)", "INFO")
        print(f"\n[OK] Daemon stopped gracefully ({cycle_count} cycles completed)")

    return 0


def ensure_folders_exist():
    """Creates required folders if they don't exist."""
    try:
        INBOX_FOLDER.mkdir(parents=True, exist_ok=True)
        NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)
        NEEDS_APPROVAL_FOLDER.mkdir(parents=True, exist_ok=True)
        DONE_FOLDER.mkdir(parents=True, exist_ok=True)
        LOGS_FOLDER.mkdir(exist_ok=True)
        return True
    except Exception as e:
        print(f"[ERROR] Error creating folders: {e}")
        return False


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Silver Scheduler - AI Employee Orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start daemon mode (continuous operation)
  python run_ai_employee.py --daemon

  # Run once (single execution)
  python run_ai_employee.py --once

  # Check system status
  python run_ai_employee.py --status

  # Custom interval (3 minutes)
  python run_ai_employee.py --daemon --interval 180

  # Verbose logging
  python run_ai_employee.py --daemon --verbose
        """
    )

    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run continuously in daemon mode'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Execute single cycle and exit'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status and exit'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=DEFAULT_INTERVAL,
        help=f'Interval between cycles in seconds (default: {DEFAULT_INTERVAL})'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Validate arguments
    mode_count = sum([args.daemon, args.once, args.status])
    if mode_count == 0:
        parser.error("Must specify one of: --daemon, --once, or --status")
    elif mode_count > 1:
        parser.error("Can only specify one mode: --daemon, --once, or --status")

    # Ensure folders exist
    if not ensure_folders_exist():
        sys.exit(1)

    # Execute based on mode
    if args.status:
        show_status()
        sys.exit(0)
    elif args.once:
        exit_code = run_once(args.verbose)
        sys.exit(exit_code)
    elif args.daemon:
        exit_code = run_daemon(args.interval, args.verbose)
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
