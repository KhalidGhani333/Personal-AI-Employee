"""
Human Approval - Human-in-the-Loop Decision Making
===================================================
Creates approval request and waits for human decision.
"""

import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path


# Configuration
VAULT_PATH = Path("AI_Employee_Vault")
NEEDS_APPROVAL_FOLDER = VAULT_PATH / "Needs_Approval"
CHECK_INTERVAL = 5  # seconds
APPROVAL_KEYWORDS = ['APPROVED', 'APPROVE', 'YES']
REJECTION_KEYWORDS = ['REJECTED', 'REJECT', 'NO']


def create_approval_request(action, details):
    """
    Creates an approval request file.

    Args:
        action: Brief action description
        details: Full action details

    Returns:
        Path to created file or None on error
    """
    try:
        # Ensure folder exists
        NEEDS_APPROVAL_FOLDER.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"approval_{timestamp}.md"
        filepath = NEEDS_APPROVAL_FOLDER / filename

        # Create content
        content = f"""---
action: {action}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
status: pending
---

# Approval Required

## Action
{action}

## Details
{details}

## Decision Required
Add your decision below and save this file:

DECISION: [Type APPROVED or REJECTED here]

---
Instructions:
1. Review the action and details above
2. Replace the text in brackets with your decision
3. Save this file
4. The system will detect your decision automatically
"""

        # Write file
        filepath.write_text(content, encoding='utf-8')
        print(f"[INFO] Approval request created: {filename}")
        return filepath

    except Exception as e:
        print(f"[ERROR] Failed to create approval request: {e}")
        return None


def check_for_decision(filepath):
    """
    Checks if file contains approval or rejection.

    Args:
        filepath: Path to approval file

    Returns:
        'approved', 'rejected', or None
    """
    try:
        content = filepath.read_text(encoding='utf-8').upper()

        # Check for approval
        for keyword in APPROVAL_KEYWORDS:
            if keyword in content:
                return 'approved'

        # Check for rejection
        for keyword in REJECTION_KEYWORDS:
            if keyword in content:
                return 'rejected'

        return None

    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        return None


def wait_for_approval(filepath, timeout_seconds):
    """
    Waits for human to approve or reject.

    Args:
        filepath: Path to approval file
        timeout_seconds: Maximum wait time

    Returns:
        0 for approved, 1 for rejected, 2 for timeout
    """
    print(f"[INFO] Waiting for human decision...")
    print(f"[INFO] File location: {filepath}")
    print(f"[INFO] Timeout: {timeout_seconds} seconds")

    start_time = datetime.now()
    timeout_time = start_time + timedelta(seconds=timeout_seconds)

    while datetime.now() < timeout_time:
        # Check for decision
        decision = check_for_decision(filepath)

        if decision == 'approved':
            print(f"[SUCCESS] APPROVED by human")
            return 0
        elif decision == 'rejected':
            print(f"[INFO] REJECTED by human")
            return 1

        # Wait before next check
        time.sleep(CHECK_INTERVAL)

        # Show progress every 30 seconds
        elapsed = (datetime.now() - start_time).total_seconds()
        if int(elapsed) % 30 == 0 and elapsed > 0:
            remaining = (timeout_time - datetime.now()).total_seconds()
            print(f"[INFO] Still waiting... ({int(remaining)}s remaining)")

    # Timeout
    print(f"[TIMEOUT] No decision received within {timeout_seconds} seconds")
    return 2


def main():
    parser = argparse.ArgumentParser(
        description='Request human approval for sensitive actions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Request approval for email
  python request_approval.py \\
    --action "Send client email" \\
    --details "To: client@example.com\\nSubject: Project Update"

  # With custom timeout (30 minutes)
  python request_approval.py \\
    --action "Delete old files" \\
    --details "Remove 50 files older than 1 year" \\
    --timeout 1800

Exit Codes:
  0 - APPROVED
  1 - REJECTED
  2 - TIMEOUT
        """
    )

    parser.add_argument(
        '--action',
        required=True,
        help='Brief action description'
    )
    parser.add_argument(
        '--details',
        required=True,
        help='Full action details'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=3600,
        help='Timeout in seconds (default: 3600 = 1 hour)'
    )

    args = parser.parse_args()

    # Create approval request
    filepath = create_approval_request(args.action, args.details)
    if not filepath:
        sys.exit(1)

    # Wait for decision
    exit_code = wait_for_approval(filepath, args.timeout)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
