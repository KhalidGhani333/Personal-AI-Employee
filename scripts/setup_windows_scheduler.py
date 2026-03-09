"""
Windows Task Scheduler Setup Script
====================================
Automatically creates Windows scheduled tasks for AI Employee system.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_python_path():
    """Get full Python executable path"""
    return sys.executable


def get_project_path():
    """Get project root path"""
    return str(Path(__file__).parent.parent.absolute())


def create_task(task_name, script_path, interval_minutes, description):
    """Create a Windows scheduled task"""
    python_path = get_python_path()
    project_path = get_project_path()

    # Build schtasks command
    cmd = [
        'schtasks', '/Create',
        '/TN', f"AI Employee\\{task_name}",
        '/TR', f'"{python_path}" "{project_path}\\{script_path}"',
        '/SC', 'MINUTE',
        '/MO', str(interval_minutes),
        '/ST', '00:00',
        '/F'  # Force create (overwrite if exists)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[SUCCESS] Created task: {task_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create task: {task_name}")
        print(f"        {e.stderr}")
        return False


def delete_task(task_name):
    """Delete a Windows scheduled task"""
    cmd = ['schtasks', '/Delete', '/TN', f"AI Employee\\{task_name}", '/F']

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[SUCCESS] Deleted task: {task_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"[INFO] Task not found: {task_name}")
        return False


def enable_task(task_name):
    """Enable a Windows scheduled task"""
    cmd = ['schtasks', '/Change', '/TN', f"AI Employee\\{task_name}", '/ENABLE']

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[SUCCESS] Enabled task: {task_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to enable task: {task_name}")
        return False


def disable_task(task_name):
    """Disable a Windows scheduled task"""
    cmd = ['schtasks', '/Change', '/TN', f"AI Employee\\{task_name}", '/DISABLE']

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[SUCCESS] Disabled task: {task_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to disable task: {task_name}")
        return False


def list_tasks():
    """List all AI Employee scheduled tasks"""
    cmd = ['schtasks', '/Query', '/FO', 'LIST', '/V']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Filter for AI Employee tasks
        lines = result.stdout.split('\n')
        ai_tasks = []
        current_task = {}

        for line in lines:
            if 'TaskName:' in line and 'AI Employee' in line:
                if current_task:
                    ai_tasks.append(current_task)
                current_task = {'name': line.split(':', 1)[1].strip()}
            elif current_task and 'Status:' in line:
                current_task['status'] = line.split(':', 1)[1].strip()
            elif current_task and 'Next Run Time:' in line:
                current_task['next_run'] = line.split(':', 1)[1].strip()

        if current_task:
            ai_tasks.append(current_task)

        return ai_tasks
    except subprocess.CalledProcessError:
        return []


def setup_all_tasks():
    """Create all AI Employee scheduled tasks"""
    print("="*60)
    print("Windows Task Scheduler Setup - AI Employee")
    print("="*60)
    print()

    tasks = [
        {
            'name': 'Gmail Watcher',
            'script': 'scripts\\gmail_watcher.py --once',
            'interval': 5,
            'description': 'Monitor Gmail for new emails'
        },
        {
            'name': 'WhatsApp Watcher',
            'script': 'scripts\\whatsapp_watcher.py --once',
            'interval': 2,
            'description': 'Monitor WhatsApp for new messages'
        },
        {
            'name': 'Reply Generator',
            'script': 'scripts\\reply_generator.py',
            'interval': 5,
            'description': 'Generate AI replies for pending messages'
        },
        {
            'name': 'Reply Sender',
            'script': 'scripts\\reply_sender.py',
            'interval': 10,
            'description': 'Send approved replies'
        },
        {
            'name': 'LinkedIn Auto Poster',
            'script': 'scripts\\linkedin_auto_poster.py --process',
            'interval': 30,
            'description': 'Process LinkedIn post queue'
        },
        {
            'name': 'Main Orchestrator',
            'script': 'scripts\\run_ai_employee.py --once',
            'interval': 5,
            'description': 'Process inbox and tasks'
        }
    ]

    print(f"Creating {len(tasks)} scheduled tasks...")
    print()

    success_count = 0
    for task in tasks:
        if create_task(task['name'], task['script'], task['interval'], task['description']):
            success_count += 1

    print()
    print("="*60)
    print(f"Setup Complete: {success_count}/{len(tasks)} tasks created")
    print("="*60)
    print()
    print("Tasks will run automatically in the background.")
    print("View tasks: Open Task Scheduler > Task Scheduler Library > AI Employee")
    print()


def remove_all_tasks():
    """Remove all AI Employee scheduled tasks"""
    print("="*60)
    print("Removing AI Employee Scheduled Tasks")
    print("="*60)
    print()

    task_names = [
        'Gmail Watcher',
        'WhatsApp Watcher',
        'Reply Generator',
        'Reply Sender',
        'LinkedIn Auto Poster',
        'Main Orchestrator'
    ]

    success_count = 0
    for task_name in task_names:
        if delete_task(task_name):
            success_count += 1

    print()
    print(f"Removed {success_count} task(s)")
    print()


def enable_all_tasks():
    """Enable all AI Employee scheduled tasks"""
    print("="*60)
    print("Enabling AI Employee Scheduled Tasks")
    print("="*60)
    print()

    task_names = [
        'Gmail Watcher',
        'WhatsApp Watcher',
        'Reply Generator',
        'Reply Sender',
        'LinkedIn Auto Poster',
        'Main Orchestrator'
    ]

    success_count = 0
    for task_name in task_names:
        if enable_task(task_name):
            success_count += 1

    print()
    print(f"Enabled {success_count} task(s)")
    print()


def disable_all_tasks():
    """Disable all AI Employee scheduled tasks"""
    print("="*60)
    print("Disabling AI Employee Scheduled Tasks")
    print("="*60)
    print()

    task_names = [
        'Gmail Watcher',
        'WhatsApp Watcher',
        'Reply Generator',
        'Reply Sender',
        'LinkedIn Auto Poster',
        'Main Orchestrator'
    ]

    success_count = 0
    for task_name in task_names:
        if disable_task(task_name):
            success_count += 1

    print()
    print(f"Disabled {success_count} task(s)")
    print()


def show_status():
    """Show status of all AI Employee tasks"""
    print("="*60)
    print("AI Employee Scheduled Tasks - Status")
    print("="*60)
    print()

    tasks = list_tasks()

    if not tasks:
        print("No AI Employee tasks found.")
        print()
        print("Run: python scripts/setup_windows_scheduler.py --setup")
        print()
        return

    for task in tasks:
        print(f"Task: {task['name']}")
        print(f"  Status: {task.get('status', 'Unknown')}")
        print(f"  Next Run: {task.get('next_run', 'Unknown')}")
        print()

    print(f"Total: {len(tasks)} task(s)")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Windows Task Scheduler Setup for AI Employee',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create all scheduled tasks
  python scripts/setup_windows_scheduler.py --setup

  # Remove all scheduled tasks
  python scripts/setup_windows_scheduler.py --remove

  # Enable all tasks
  python scripts/setup_windows_scheduler.py --enable

  # Disable all tasks
  python scripts/setup_windows_scheduler.py --disable

  # Show task status
  python scripts/setup_windows_scheduler.py --status

Note: Requires Administrator privileges
        """
    )

    parser.add_argument('--setup', action='store_true', help='Create all scheduled tasks')
    parser.add_argument('--remove', action='store_true', help='Remove all scheduled tasks')
    parser.add_argument('--enable', action='store_true', help='Enable all scheduled tasks')
    parser.add_argument('--disable', action='store_true', help='Disable all scheduled tasks')
    parser.add_argument('--status', action='store_true', help='Show task status')

    args = parser.parse_args()

    # Check if running as administrator
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    if not is_admin:
        print("[WARNING] Not running as Administrator")
        print("[TIP] Right-click Command Prompt > Run as Administrator")
        print()

    if args.setup:
        setup_all_tasks()
    elif args.remove:
        remove_all_tasks()
    elif args.enable:
        enable_all_tasks()
    elif args.disable:
        disable_all_tasks()
    elif args.status:
        show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
