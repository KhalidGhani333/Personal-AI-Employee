"""
Vault Watcher - Monitors AI_Employee_Vault/Inbox for new markdown files
=========================================================================
This script continuously monitors the Inbox folder and automatically triggers
the AI processing workflow when new .md files are detected.

Features:
- Monitors AI_Employee_Vault/Inbox every 15 seconds
- Detects new .md files only
- Triggers run_ai_employee.py --once for each new file
- Prevents duplicate processing
- Logs all activity to logs/actions.log
- Graceful error handling
- Production-ready with comprehensive logging
"""

import os
import time
import subprocess
from datetime import datetime
from pathlib import Path


# Configuration
VAULT_PATH = Path("AI_Employee_Vault")
INBOX_FOLDER = VAULT_PATH / "Inbox"
LOGS_FOLDER = Path("logs")
ACTION_LOG = LOGS_FOLDER / "actions.log"
PROCESSED_FILES_LOG = LOGS_FOLDER / "processed_files.txt"
CHECK_INTERVAL = 15  # seconds
AI_SCRIPT = "run_ai_employee.py"


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
        # Ensure logs folder exists
        LOGS_FOLDER.mkdir(exist_ok=True)

        # Create log entry
        timestamp = get_timestamp()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        # Append to log file
        with open(ACTION_LOG, 'a', encoding='utf-8') as f:
            f.write(log_entry)

        # Also print to console
        print(f"[{level}] {message}")

    except Exception as e:
        print(f"⚠ Failed to write log: {e}")


def load_processed_files():
    """
    Loads the set of already processed files from disk.

    Returns:
        Set of processed filenames
    """
    try:
        if PROCESSED_FILES_LOG.exists():
            with open(PROCESSED_FILES_LOG, 'r', encoding='utf-8') as f:
                files = set(line.strip() for line in f if line.strip())
            log_action(f"Loaded {len(files)} processed file(s) from history", "INFO")
            return files
        return set()
    except Exception as e:
        log_action(f"Error loading processed files: {e}", "WARNING")
        return set()


def save_processed_file(filename):
    """
    Saves a processed filename to disk to prevent reprocessing.

    Args:
        filename: The filename to mark as processed
    """
    try:
        LOGS_FOLDER.mkdir(exist_ok=True)
        with open(PROCESSED_FILES_LOG, 'a', encoding='utf-8') as f:
            f.write(f"{filename}\n")
    except Exception as e:
        log_action(f"Error saving processed file: {e}", "WARNING")


def get_md_files():
    """
    Returns a list of all .md files in the Inbox folder.

    Returns:
        List of .md filenames
    """
    try:
        if not INBOX_FOLDER.exists():
            return []

        md_files = []
        for item in INBOX_FOLDER.iterdir():
            if item.is_file() and item.suffix.lower() == '.md':
                md_files.append(item.name)

        return md_files

    except PermissionError:
        log_action(f"Permission denied reading {INBOX_FOLDER}", "ERROR")
        return []
    except Exception as e:
        log_action(f"Error reading inbox: {e}", "ERROR")
        return []


def trigger_ai_processing(filename):
    """
    Triggers the AI processing workflow for a detected file.

    Args:
        filename: The name of the file to process

    Returns:
        True if successful, False otherwise
    """
    try:
        log_action(f"Triggering AI processing for: {filename}", "INFO")

        # Check if AI script exists
        if not os.path.exists(AI_SCRIPT):
            log_action(f"AI script not found: {AI_SCRIPT}", "ERROR")
            return False

        # Run the AI processing script
        result = subprocess.run(
            ['python', AI_SCRIPT, '--once'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            log_action(f"Successfully processed: {filename}", "INFO")
            return True
        else:
            log_action(f"AI processing failed for {filename}: {result.stderr}", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log_action(f"AI processing timeout for {filename}", "ERROR")
        return False
    except Exception as e:
        log_action(f"Error triggering AI processing: {e}", "ERROR")
        return False


def ensure_folders_exist():
    """
    Creates required folders if they don't exist.

    Returns:
        True if successful, False otherwise
    """
    try:
        INBOX_FOLDER.mkdir(parents=True, exist_ok=True)
        LOGS_FOLDER.mkdir(exist_ok=True)
        log_action("Required folders verified", "INFO")
        return True
    except Exception as e:
        print(f"✗ Error creating folders: {e}")
        return False


def main():
    """
    Main function that runs the vault watcher loop.
    """
    print("=" * 60)
    print("Vault Watcher - AI Employee Inbox Monitor")
    print("=" * 60)
    print(f"Monitoring: {INBOX_FOLDER}")
    print(f"File type: .md files only")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print(f"Action log: {ACTION_LOG}")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    # Ensure folders exist
    if not ensure_folders_exist():
        print("\n✗ Cannot start: Required folders could not be created")
        return

    # Log startup
    log_action("Vault Watcher started", "INFO")

    # Load previously processed files
    processed_files = load_processed_files()

    # Get initial files (don't process files already in inbox)
    initial_files = get_md_files()
    processed_files.update(initial_files)
    if initial_files:
        log_action(f"Found {len(initial_files)} existing .md file(s) in Inbox (skipping)", "INFO")

    print("\nWatching for new .md files...\n")

    try:
        # Main monitoring loop
        while True:
            try:
                # Get current .md files
                current_files = get_md_files()

                # Find new files
                new_files = set(current_files) - processed_files

                # Process each new file
                for filename in new_files:
                    log_action(f"New file detected: {filename}", "INFO")

                    # Trigger AI processing
                    if trigger_ai_processing(filename):
                        # Mark as processed
                        processed_files.add(filename)
                        save_processed_file(filename)
                    else:
                        # Even if processing failed, mark as processed to avoid retry loops
                        # (manual intervention needed for failed files)
                        processed_files.add(filename)
                        save_processed_file(filename)

                # Wait before next check
                time.sleep(CHECK_INTERVAL)

            except Exception as e:
                # Catch any unexpected errors in the loop
                log_action(f"Unexpected error in main loop: {e}", "ERROR")
                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        # User pressed Ctrl+C - graceful shutdown
        print("\n")
        log_action("Vault Watcher stopped by user", "INFO")
        print("=" * 60)
        print(f"Total files processed: {len(processed_files) - len(initial_files)}")
        print("=" * 60)


if __name__ == "__main__":
    main()
