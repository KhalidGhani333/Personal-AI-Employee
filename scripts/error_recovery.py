#!/usr/bin/env python3
"""
Error Recovery System
Handles task failures with logging, file management, and retry logic
"""

import json
import time
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import traceback

# Paths
VAULT_PATH = Path("AI_Employee_Vault")
ERRORS_PATH = VAULT_PATH / "Errors"
LOGS_PATH = Path("Logs")
ERROR_LOG = LOGS_PATH / "errors.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ErrorRecovery')


class ErrorRecoverySystem:
    """Manages error handling, logging, and retry logic"""

    def __init__(self):
        self.errors_path = ERRORS_PATH
        self.error_log = ERROR_LOG
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure error directories exist"""
        self.errors_path.mkdir(parents=True, exist_ok=True)
        self.error_log.parent.mkdir(parents=True, exist_ok=True)

    def log_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """Log error details to errors.log"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context
        }

        try:
            with open(self.error_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(error_entry) + '\n')

            logger.error(f"Error logged: {error_entry['error_type']} - {error_entry['error_message']}")

        except Exception as e:
            logger.error(f"Failed to write error log: {e}")

    def move_to_errors(self, file_path: Path) -> Optional[Path]:
        """Move failed task file to Errors folder"""
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return None

        try:
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            error_filename = f"ERROR_{timestamp}_{file_path.name}"
            error_filepath = self.errors_path / error_filename

            # Move file
            shutil.move(str(file_path), str(error_filepath))
            logger.info(f"Moved failed file to: {error_filepath}")

            return error_filepath

        except Exception as e:
            logger.error(f"Failed to move file to Errors: {e}")
            return None

    def retry_task(
        self,
        task_func: Callable,
        task_args: tuple = (),
        task_kwargs: dict = None,
        retry_delay: int = 300,  # 5 minutes
        max_retries: int = 1
    ) -> Dict[str, Any]:
        """
        Execute task with retry logic

        Args:
            task_func: Function to execute
            task_args: Positional arguments for function
            task_kwargs: Keyword arguments for function
            retry_delay: Delay in seconds before retry (default: 300 = 5 minutes)
            max_retries: Maximum number of retries (default: 1)

        Returns:
            Dict with success status and result/error
        """
        if task_kwargs is None:
            task_kwargs = {}

        attempt = 0
        last_error = None

        while attempt <= max_retries:
            try:
                logger.info(f"Executing task (attempt {attempt + 1}/{max_retries + 1})")

                # Execute task
                result = task_func(*task_args, **task_kwargs)

                logger.info(f"Task succeeded on attempt {attempt + 1}")
                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt + 1
                }

            except Exception as e:
                last_error = e
                attempt += 1

                logger.error(f"Task failed on attempt {attempt}: {e}")

                # Log error
                self.log_error(e, {
                    "task_function": task_func.__name__,
                    "attempt": attempt,
                    "max_retries": max_retries
                })

                # Retry if attempts remaining
                if attempt <= max_retries:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)

        # All retries exhausted
        logger.error(f"Task failed after {attempt} attempts")
        return {
            "success": False,
            "error": str(last_error),
            "error_type": type(last_error).__name__,
            "attempts": attempt
        }

    def handle_task_failure(
        self,
        task_file: Path,
        error: Exception,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Complete error handling workflow for a failed task

        Args:
            task_file: Path to the failed task file
            error: The exception that occurred
            context: Additional context about the failure

        Returns:
            Dict with error handling results
        """
        if context is None:
            context = {}

        logger.info(f"Handling task failure: {task_file.name}")

        # Add file info to context
        context["task_file"] = str(task_file)
        context["task_name"] = task_file.stem

        # Log error
        self.log_error(error, context)

        # Move file to Errors folder
        error_filepath = self.move_to_errors(task_file)

        return {
            "success": True,
            "error_logged": True,
            "file_moved": error_filepath is not None,
            "error_filepath": str(error_filepath) if error_filepath else None,
            "timestamp": datetime.now().isoformat()
        }

    def execute_with_recovery(
        self,
        task_func: Callable,
        task_file: Optional[Path] = None,
        task_args: tuple = (),
        task_kwargs: dict = None,
        retry_delay: int = 300,
        max_retries: int = 1
    ) -> Dict[str, Any]:
        """
        Execute task with full error recovery

        Combines retry logic with error handling workflow

        Args:
            task_func: Function to execute
            task_file: Optional task file to move on failure
            task_args: Positional arguments
            task_kwargs: Keyword arguments
            retry_delay: Delay before retry (seconds)
            max_retries: Maximum retries

        Returns:
            Dict with execution results
        """
        if task_kwargs is None:
            task_kwargs = {}

        # Execute with retry
        result = self.retry_task(
            task_func,
            task_args,
            task_kwargs,
            retry_delay,
            max_retries
        )

        # If failed and task file provided, handle failure
        if not result["success"] and task_file:
            error = Exception(result.get("error", "Unknown error"))
            self.handle_task_failure(
                task_file,
                error,
                {
                    "function": task_func.__name__,
                    "attempts": result["attempts"],
                    "error_type": result.get("error_type")
                }
            )

        return result


# Global error recovery instance
error_recovery = ErrorRecoverySystem()


def with_error_recovery(retry_delay: int = 300, max_retries: int = 1):
    """
    Decorator for automatic error recovery

    Usage:
        @with_error_recovery(retry_delay=300, max_retries=1)
        def my_task():
            # Task code here
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            return error_recovery.retry_task(
                func,
                args,
                kwargs,
                retry_delay,
                max_retries
            )
        return wrapper
    return decorator


def main():
    """Test error recovery system"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: error_recovery.py <command>")
        print("\nCommands:")
        print("  test-retry    - Test retry logic")
        print("  test-failure  - Test failure handling")
        print("  view-errors   - View recent errors")
        sys.exit(1)

    command = sys.argv[1]
    recovery = ErrorRecoverySystem()

    if command == "test-retry":
        print("Testing retry logic...")

        attempt_count = [0]

        def flaky_task():
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                raise Exception("Simulated failure")
            return "Success!"

        result = recovery.retry_task(flaky_task, retry_delay=2, max_retries=1)
        print(f"\nResult: {json.dumps(result, indent=2)}")

    elif command == "test-failure":
        print("Testing failure handling...")

        # Create test file
        test_file = VAULT_PATH / "Needs_Action" / "test_error_task.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("# Test Task\n\nThis is a test task for error handling.")

        # Simulate failure
        error = Exception("Test error for demonstration")
        result = recovery.handle_task_failure(
            test_file,
            error,
            {"test": True, "reason": "demonstration"}
        )

        print(f"\nResult: {json.dumps(result, indent=2)}")

    elif command == "view-errors":
        print("Recent errors:\n")

        if not ERROR_LOG.exists():
            print("No errors logged yet.")
            return

        # Read last 10 errors
        with open(ERROR_LOG, 'r') as f:
            lines = f.readlines()
            recent = lines[-10:] if len(lines) > 10 else lines

            for line in recent:
                try:
                    error = json.loads(line)
                    print(f"[{error['timestamp']}] {error['error_type']}: {error['error_message']}")
                    if error.get('context'):
                        print(f"  Context: {error['context']}")
                    print()
                except:
                    continue

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
