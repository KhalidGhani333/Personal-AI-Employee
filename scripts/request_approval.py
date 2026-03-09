"""
Human Approval Request - Blocks execution until human approval/rejection
=========================================================================
This script monitors files in the Needs_Approval folder and waits for
human input (APPROVED or REJECTED) before proceeding.

Features:
- Monitors specific file or all files in Needs_Approval folder
- Blocks execution until human decision is made
- Configurable timeout (default 1 hour)
- Returns exit codes for programmatic use
- Renames files based on outcome (.approved, .rejected, .timeout)
- Comprehensive logging to logs/actions.log
- Moves processed files to Done folder
"""

import os
import sys
import time
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path


# Configuration
VAULT_PATH = Path("AI_Employee_Vault")
NEEDS_APPROVAL_FOLDER = VAULT_PATH / "Needs_Approval"
DONE_FOLDER = VAULT_PATH / "Done"
LOGS_FOLDER = Path("logs")
ACTION_LOG = LOGS_FOLDER / "actions.log"

# Exit codes
EXIT_APPROVED = 0
EXIT_REJECTED = 1
EXIT_TIMEOUT = 2
EXIT_ERROR = 3

# Keywords (case-insensitive)
APPROVAL_KEYWORDS = ['APPROVED', 'APPROVE', 'YES', 'ACCEPT']
REJECTION_KEYWORDS = ['REJECTED', 'REJECT', 'NO', 'DENY', 'DECLINE']


def get_timestamp():
    """Returns current timestamp in readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_action(message, level="INFO"):
    """
    Logs an action to the action log file with timestamp.

    Args:
        message: The message to log
        level: Log level (INFO, WARNING, ERROR)
    """
    try:
        LOGS_FOLDER.mkdir(exist_ok=True)
        timestamp = get_timestamp()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        with open(ACTION_LOG, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        print(f"[{level}] {message}")

    except Exception as e:
        print(f"[WARNING] Failed to write log: {e}")


def check_file_for_decision(filepath):
    """
    Checks if file contains approval or rejection keywords.

    Args:
        filepath: Path to the file to check

    Returns:
        'approved', 'rejected', or None
    """
    try:
        content = filepath.read_text(encoding='utf-8').upper()

        # Check for approval keywords
        for keyword in APPROVAL_KEYWORDS:
            if keyword in content:
                return 'approved'

        # Check for rejection keywords
        for keyword in REJECTION_KEYWORDS:
            if keyword in content:
                return 'rejected'

        return None

    except Exception as e:
        log_action(f"Error reading file {filepath.name}: {e}", "ERROR")
        return None


def rename_and_move_file(filepath, outcome):
    """
    Renames file based on outcome and moves to Done folder.

    Args:
        filepath: Path to the file
        outcome: 'approved', 'rejected', or 'timeout'

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create new filename with outcome extension
        stem = filepath.stem
        new_filename = f"{stem}.{outcome}.md"

        # Ensure Done folder exists
        DONE_FOLDER.mkdir(parents=True, exist_ok=True)

        # Move to Done folder with new name
        dest_path = DONE_FOLDER / new_filename
        shutil.move(str(filepath), str(dest_path))

        log_action(f"Moved {filepath.name} → {new_filename} (Done folder)", "INFO")
        return True

    except Exception as e:
        log_action(f"Error moving file {filepath.name}: {e}", "ERROR")
        return False


def wait_for_approval(filename, timeout_seconds, check_interval):
    """
    Waits for human approval/rejection in the specified file.

    Args:
        filename: Name of the file to monitor
        timeout_seconds: Maximum time to wait in seconds
        check_interval: How often to check the file in seconds

    Returns:
        Exit code (0=approved, 1=rejected, 2=timeout, 3=error)
    """
    filepath = NEEDS_APPROVAL_FOLDER / filename

    # Check if file exists
    if not filepath.exists():
        log_action(f"File not found: {filename}", "ERROR")
        print(f"\n[ERROR] File not found: {filename}")
        print(f"Expected location: {filepath}")
        return EXIT_ERROR

    log_action(f"Waiting for approval: {filename}", "INFO")
    print(f"\n{'='*60}")
    print(f"Waiting for Human Approval")
    print(f"{'='*60}")
    print(f"File: {filename}")
    print(f"Location: {filepath}")
    print(f"Timeout: {timeout_seconds} seconds ({timeout_seconds/60:.1f} minutes)")
    print(f"Check interval: {check_interval} seconds")
    print(f"\nInstructions:")
    print(f"1. Open the file: {filepath}")
    print(f"2. Review the content")
    print(f"3. Add your decision: APPROVED or REJECTED")
    print(f"4. Save the file")
    print(f"\nWaiting for decision...")
    print(f"{'='*60}\n")

    # Calculate timeout time
    start_time = datetime.now()
    timeout_time = start_time + timedelta(seconds=timeout_seconds)

    checks_performed = 0

    try:
        while datetime.now() < timeout_time:
            checks_performed += 1

            # Check for decision
            decision = check_file_for_decision(filepath)

            if decision == 'approved':
                log_action(f"APPROVED: {filename}", "INFO")
                print(f"\n[APPROVED] Human approved the action")
                rename_and_move_file(filepath, 'approved')
                return EXIT_APPROVED

            elif decision == 'rejected':
                log_action(f"REJECTED: {filename}", "INFO")
                print(f"\n[REJECTED] Human rejected the action")
                rename_and_move_file(filepath, 'rejected')
                return EXIT_REJECTED

            # Calculate remaining time
            remaining = (timeout_time - datetime.now()).total_seconds()

            # Show progress every 10 checks or when less than 60 seconds remain
            if checks_performed % 10 == 0 or remaining < 60:
                print(f"[{get_timestamp()}] Still waiting... ({remaining:.0f}s remaining)")

            # Wait before next check
            time.sleep(check_interval)

        # Timeout occurred
        log_action(f"TIMEOUT: {filename} (no decision after {timeout_seconds}s)", "WARNING")
        print(f"\n[TIMEOUT] No decision received within {timeout_seconds} seconds")
        rename_and_move_file(filepath, 'timeout')
        return EXIT_TIMEOUT

    except KeyboardInterrupt:
        log_action(f"CANCELLED: {filename} (interrupted by user)", "WARNING")
        print(f"\n\n[CANCELLED] Cancelled by user (Ctrl+C)")
        print(f"File remains in Needs_Approval folder: {filename}")
        return EXIT_ERROR

    except Exception as e:
        log_action(f"ERROR waiting for approval on {filename}: {e}", "ERROR")
        print(f"\n[ERROR] Error: {e}")
        return EXIT_ERROR


def monitor_all_files(timeout_seconds, check_interval):
    """
    Monitors all files in Needs_Approval folder.

    Args:
        timeout_seconds: Maximum time to wait per file
        check_interval: How often to check files

    Returns:
        Exit code based on overall results
    """
    try:
        if not NEEDS_APPROVAL_FOLDER.exists():
            log_action("Needs_Approval folder does not exist", "ERROR")
            print(f"[ERROR] {NEEDS_APPROVAL_FOLDER} does not exist")
            return EXIT_ERROR

        # Get all .md files
        files = [f for f in NEEDS_APPROVAL_FOLDER.iterdir()
                if f.is_file() and f.suffix.lower() == '.md']

        if not files:
            log_action("No files in Needs_Approval folder", "INFO")
            print("[OK] No files waiting for approval")
            return EXIT_APPROVED

        print(f"\nFound {len(files)} file(s) waiting for approval\n")

        results = []
        for filepath in files:
            result = wait_for_approval(filepath.name, timeout_seconds, check_interval)
            results.append(result)
            print()  # Blank line between files

        # Summary
        approved = results.count(EXIT_APPROVED)
        rejected = results.count(EXIT_REJECTED)
        timeout = results.count(EXIT_TIMEOUT)
        errors = results.count(EXIT_ERROR)

        print(f"{'='*60}")
        print(f"Summary:")
        print(f"  Approved: {approved}")
        print(f"  Rejected: {rejected}")
        print(f"  Timeout:  {timeout}")
        print(f"  Errors:   {errors}")
        print(f"{'='*60}")

        # Return worst exit code
        if EXIT_ERROR in results:
            return EXIT_ERROR
        elif EXIT_TIMEOUT in results:
            return EXIT_TIMEOUT
        elif EXIT_REJECTED in results:
            return EXIT_REJECTED
        else:
            return EXIT_APPROVED

    except Exception as e:
        log_action(f"Error monitoring files: {e}", "ERROR")
        print(f"[ERROR] {e}")
        return EXIT_ERROR


def ensure_folders_exist():
    """Creates required folders if they don't exist."""
    try:
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
        description='Human Approval Request - Wait for human decision on pending actions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0 - APPROVED (action can proceed)
  1 - REJECTED (action should not proceed)
  2 - TIMEOUT (no decision within timeout period)
  3 - ERROR (file not found or other error)

Examples:
  # Wait for approval on specific file (1 hour timeout)
  python request_approval.py --file action.md

  # Custom timeout (30 minutes)
  python request_approval.py --file action.md --timeout 1800

  # Monitor all files in Needs_Approval
  python request_approval.py --monitor-all

  # Quick checks every 5 seconds
  python request_approval.py --file action.md --check-interval 5
        """
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Specific file to monitor in Needs_Approval folder'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=3600,
        help='Timeout in seconds (default: 3600 = 1 hour)'
    )
    parser.add_argument(
        '--check-interval',
        type=int,
        default=10,
        help='How often to check file in seconds (default: 10)'
    )
    parser.add_argument(
        '--monitor-all',
        action='store_true',
        help='Monitor all files in Needs_Approval folder'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.file and not args.monitor_all:
        parser.error("Either --file or --monitor-all must be specified")

    # Ensure folders exist
    if not ensure_folders_exist():
        sys.exit(EXIT_ERROR)

    log_action("Human Approval Request started", "INFO")

    # Execute based on mode
    if args.monitor_all:
        exit_code = monitor_all_files(args.timeout, args.check_interval)
    else:
        exit_code = wait_for_approval(args.file, args.timeout, args.check_interval)

    log_action(f"Human Approval Request completed with exit code: {exit_code}", "INFO")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
