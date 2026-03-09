"""
Approval Manager - Review and Approve/Reject Generated Content
===============================================================
Human-in-the-loop approval system for social media posts.

SAFETY: All content must be manually reviewed before posting.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
PENDING_APPROVAL = VAULT_PATH / "Pending_Approval"
APPROVED = VAULT_PATH / "Approved"
REJECTED = VAULT_PATH / "Rejected"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)
APPROVED.mkdir(parents=True, exist_ok=True)
REJECTED.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)


def log_action(action, platform, filename, result):
    """Log all actions to orchestrator.log"""
    log_file = LOGS_PATH / "orchestrator.log"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "platform": platform,
        "filename": filename,
        "result": result
    }

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')


def list_pending_files():
    """List all files in Pending_Approval folder"""
    files = list(PENDING_APPROVAL.glob("*.md"))

    if not files:
        print("\n[INFO] No pending approvals found.")
        return []

    print("\n" + "=" * 60)
    print("Pending Approvals")
    print("=" * 60)

    for i, file in enumerate(files, 1):
        # Read file to get metadata
        try:
            content = file.read_text(encoding='utf-8')
            lines = content.split('\n')

            platform = "Unknown"
            topic = "Unknown"
            created = "Unknown"

            for line in lines[:10]:
                if line.startswith('platform:'):
                    platform = line.split(':', 1)[1].strip()
                elif line.startswith('topic:'):
                    topic = line.split(':', 1)[1].strip()
                elif line.startswith('created:'):
                    created = line.split(':', 1)[1].strip()

            print(f"\n[{i}] {file.name}")
            print(f"    Platform: {platform}")
            print(f"    Topic: {topic}")
            print(f"    Created: {created}")

        except Exception as e:
            print(f"\n[{i}] {file.name}")
            print(f"    [ERROR] Could not read metadata: {e}")

    print("\n" + "=" * 60)

    return files


def read_file_preview(filepath):
    """Read and display file preview"""
    try:
        content = filepath.read_text(encoding='utf-8')

        # Extract main content section
        lines = content.split('\n')
        in_content = False
        content_lines = []

        for line in lines:
            if line.strip() == "## Generated Content":
                in_content = True
                continue
            elif line.strip().startswith("---") and in_content:
                break
            elif in_content:
                content_lines.append(line)

        preview = '\n'.join(content_lines).strip()

        print("\n" + "=" * 60)
        print("Content Preview")
        print("=" * 60)
        print(preview)
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")


def approve_file(filename):
    """Approve a file and move to Approved folder"""
    source = PENDING_APPROVAL / filename
    destination = APPROVED / filename

    if not source.exists():
        print(f"[ERROR] File not found: {filename}")
        return False

    try:
        # Update status in file
        content = source.read_text(encoding='utf-8')
        content = content.replace('status: Pending', 'status: Approved')
        content = content.replace('Status: Pending', 'Status: Approved')

        # Add approval timestamp
        approval_note = f"\n\n---\n\n**Approved:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += approval_note

        # Write to destination
        destination.write_text(content, encoding='utf-8')

        # Remove from pending
        source.unlink()

        print(f"[SUCCESS] Approved: {filename}")
        print(f"[INFO] Moved to: {APPROVED}")

        # Extract platform for logging
        platform = "Unknown"
        for line in content.split('\n')[:10]:
            if line.startswith('platform:'):
                platform = line.split(':', 1)[1].strip()
                break

        log_action("approve", platform, filename, "success")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to approve: {e}")
        log_action("approve", "Unknown", filename, f"error: {e}")
        return False


def reject_file(filename):
    """Reject a file and move to Rejected folder"""
    source = PENDING_APPROVAL / filename
    destination = REJECTED / filename

    if not source.exists():
        print(f"[ERROR] File not found: {filename}")
        return False

    try:
        # Update status in file
        content = source.read_text(encoding='utf-8')
        content = content.replace('status: Pending', 'status: Rejected')
        content = content.replace('Status: Pending', 'Status: Rejected')

        # Add rejection timestamp
        rejection_note = f"\n\n---\n\n**Rejected:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += rejection_note

        # Write to destination
        destination.write_text(content, encoding='utf-8')

        # Remove from pending
        source.unlink()

        print(f"[INFO] Rejected: {filename}")
        print(f"[INFO] Moved to: {REJECTED}")

        # Extract platform for logging
        platform = "Unknown"
        for line in content.split('\n')[:10]:
            if line.startswith('platform:'):
                platform = line.split(':', 1)[1].strip()
                break

        log_action("reject", platform, filename, "success")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to reject: {e}")
        log_action("reject", "Unknown", filename, f"error: {e}")
        return False


def interactive_mode():
    """Interactive approval mode"""
    print("\n" + "=" * 60)
    print("Approval Manager - Interactive Mode")
    print("=" * 60)
    print("\nCommands:")
    print("  list                  - List all pending files")
    print("  preview <filename>    - Preview file content")
    print("  approve <filename>    - Approve and move to Approved/")
    print("  reject <filename>     - Reject and move to Rejected/")
    print("  exit                  - Exit interactive mode")
    print("=" * 60)

    while True:
        try:
            command = input("\n> ").strip()

            if not command:
                continue

            parts = command.split(maxsplit=1)
            action = parts[0].lower()

            if action == "exit":
                print("\n[INFO] Exiting approval manager.")
                break

            elif action == "list":
                list_pending_files()

            elif action == "preview":
                if len(parts) < 2:
                    print("[ERROR] Usage: preview <filename>")
                    continue

                filename = parts[1]
                filepath = PENDING_APPROVAL / filename

                if not filepath.exists():
                    print(f"[ERROR] File not found: {filename}")
                    continue

                read_file_preview(filepath)

            elif action == "approve":
                if len(parts) < 2:
                    print("[ERROR] Usage: approve <filename>")
                    continue

                filename = parts[1]
                approve_file(filename)

            elif action == "reject":
                if len(parts) < 2:
                    print("[ERROR] Usage: reject <filename>")
                    continue

                filename = parts[1]
                reject_file(filename)

            else:
                print(f"[ERROR] Unknown command: {action}")
                print("[INFO] Type 'list', 'preview', 'approve', 'reject', or 'exit'")

        except KeyboardInterrupt:
            print("\n\n[INFO] Exiting approval manager.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Approval Manager - Review and approve/reject generated content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python scripts/approval_manager.py

  # List pending files
  python scripts/approval_manager.py list

  # Approve a file
  python scripts/approval_manager.py approve linkedin_ai_trends_20260305.md

  # Reject a file
  python scripts/approval_manager.py reject twitter_ai_trends_20260305.md

  # Preview a file
  python scripts/approval_manager.py preview linkedin_ai_trends_20260305.md

Safety:
  - All content must be manually reviewed
  - Approved content moved to Approved/
  - Rejected content moved to Rejected/
  - All actions logged
        """
    )

    parser.add_argument('action', nargs='?', choices=['list', 'approve', 'reject', 'preview'],
                       help='Action to perform')
    parser.add_argument('filename', nargs='?', help='Filename to approve/reject/preview')

    args = parser.parse_args()

    # If no arguments, run interactive mode
    if not args.action:
        interactive_mode()
        return

    # Handle specific actions
    if args.action == 'list':
        list_pending_files()

    elif args.action == 'preview':
        if not args.filename:
            print("[ERROR] Filename required for preview")
            sys.exit(1)

        filepath = PENDING_APPROVAL / args.filename
        if not filepath.exists():
            print(f"[ERROR] File not found: {args.filename}")
            sys.exit(1)

        read_file_preview(filepath)

    elif args.action == 'approve':
        if not args.filename:
            print("[ERROR] Filename required for approval")
            sys.exit(1)

        success = approve_file(args.filename)
        sys.exit(0 if success else 1)

    elif args.action == 'reject':
        if not args.filename:
            print("[ERROR] Filename required for rejection")
            sys.exit(1)

        success = reject_file(args.filename)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
