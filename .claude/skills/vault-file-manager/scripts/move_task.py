"""
Vault File Manager - Task Workflow Management
==============================================
Moves files between vault folders to manage task lifecycle.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path


# Vault configuration
VAULT_PATH = Path("AI_Employee_Vault")
VALID_FOLDERS = ["Inbox", "Needs_Action", "Done"]


def get_folder_path(folder_name):
    """
    Get full path for a vault folder.

    Args:
        folder_name: Folder name (Inbox, Needs_Action, or Done)

    Returns:
        Path object or None if invalid
    """
    if folder_name not in VALID_FOLDERS:
        return None
    return VAULT_PATH / folder_name


def move_file(filename, from_folder, to_folder):
    """
    Move a file between vault folders.

    Args:
        filename: Name of file to move
        from_folder: Source folder name
        to_folder: Destination folder name

    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate folders
        source_path = get_folder_path(from_folder)
        dest_path = get_folder_path(to_folder)

        if not source_path:
            print(f"[ERROR] Invalid source folder: {from_folder}")
            print(f"Valid folders: {', '.join(VALID_FOLDERS)}")
            return False

        if not dest_path:
            print(f"[ERROR] Invalid destination folder: {to_folder}")
            print(f"Valid folders: {', '.join(VALID_FOLDERS)}")
            return False

        # Ensure folders exist
        source_path.mkdir(parents=True, exist_ok=True)
        dest_path.mkdir(parents=True, exist_ok=True)

        # Build file paths
        source_file = source_path / filename
        dest_file = dest_path / filename

        # Check if source file exists
        if not source_file.exists():
            print(f"[ERROR] File not found: {source_file}")
            return False

        # Check if destination file already exists
        if dest_file.exists():
            print(f"[ERROR] File already exists in destination: {dest_file}")
            print("Choose a different name or remove the existing file")
            return False

        # Move file
        print(f"[INFO] Moving {filename}")
        print(f"[INFO] From: {source_path}")
        print(f"[INFO] To: {dest_path}")
        shutil.move(str(source_file), str(dest_file))

        print(f"[SUCCESS] File moved successfully")
        return True

    except PermissionError:
        print(f"[ERROR] Permission denied")
        print("Check file permissions and try again")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to move file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Move files between vault folders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Move completed task to Done
  python move_task.py --file "task.md" --from "Needs_Action" --to "Done"

  # Move new task from Inbox to Needs_Action
  python move_task.py --file "new_task.md" --from "Inbox" --to "Needs_Action"

Valid Folders:
  - Inbox: New incoming tasks
  - Needs_Action: Active tasks requiring work
  - Done: Completed tasks
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='Filename to move (e.g., task.md)'
    )
    parser.add_argument(
        '--from',
        dest='from_folder',
        required=True,
        choices=VALID_FOLDERS,
        help='Source folder'
    )
    parser.add_argument(
        '--to',
        dest='to_folder',
        required=True,
        choices=VALID_FOLDERS,
        help='Destination folder'
    )

    args = parser.parse_args()

    # Validate not moving to same folder
    if args.from_folder == args.to_folder:
        print("[ERROR] Source and destination folders are the same")
        sys.exit(1)

    # Move file
    success = move_file(args.file, args.from_folder, args.to_folder)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
