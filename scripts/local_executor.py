#!/usr/bin/env python3
"""
Local Executor - Manual Execution of Approved Tasks
Executes approved tasks from Pending_Approval
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import re

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

VAULT = Path("AI_Employee_Vault")
PENDING_APPROVAL_EMAIL = VAULT / "Pending_Approval" / "email"
PENDING_APPROVAL_SOCIAL = VAULT / "Pending_Approval" / "social"
APPROVED = VAULT / "Approved"
IN_PROGRESS_LOCAL = VAULT / "In_Progress" / "local"
DONE = VAULT / "Done"
FAILED_LOCAL = VAULT / "Failed" / "local"

# Ensure directories exist
for dir_path in [PENDING_APPROVAL_EMAIL, PENDING_APPROVAL_SOCIAL, APPROVED,
                 IN_PROGRESS_LOCAL, DONE, FAILED_LOCAL]:
    dir_path.mkdir(parents=True, exist_ok=True)


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown file"""
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        frontmatter = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        return frontmatter, content[match.end():]
    return {}, content


def check_approval_status(approval_file):
    """Check if approval file is approved, rejected, or pending"""
    try:
        with open(approval_file, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, _ = parse_frontmatter(content)
        status = frontmatter.get('status', 'pending')

        return status
    except Exception as e:
        print(f"❌ Error reading {approval_file.name}: {e}")
        return 'error'


def extract_draft_content(content):
    """Extract draft content from approval file"""
    frontmatter, body = parse_frontmatter(content)

    # Find draft section
    draft_match = re.search(r'## Draft (?:Reply|Post)\n(.*?)(?=\n## |$)', body, re.DOTALL)
    if draft_match:
        return draft_match.group(1).strip()

    return ""


def send_email(draft_content, approval_file):
    """Send email via SMTP"""
    # Placeholder - integrate with your email sending logic
    # Use scripts/gmail_send.py or similar

    print(f"📧 Sending email...")
    print(f"   Content: {draft_content[:100]}...")

    # Simulate sending
    # In production, call your actual email sending function
    # from gmail_send import send_email
    # send_email(to, subject, draft_content)

    print(f"✅ Email sent successfully")
    return True


def post_to_social(draft_content, platforms, approval_file):
    """Post to social media platforms"""
    # Placeholder - integrate with your social posting logic
    # Use scripts/social_poster.py or similar

    print(f"📱 Posting to social media...")
    print(f"   Platforms: {platforms}")
    print(f"   Content: {draft_content[:100]}...")

    # Simulate posting
    # In production, call your actual posting function
    # from social_poster import post_content
    # post_content(draft_content, platforms)

    print(f"✅ Posted successfully")
    return True


def execute_email_approval(approval_file):
    """Execute approved email task"""
    task_name = approval_file.name

    # Claim by moving to Approved
    approved_path = APPROVED / "email" / task_name
    approved_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(approval_file), str(approved_path))
        print(f"✅ Claimed: {task_name}")
    except FileNotFoundError:
        print(f"⚠️  Already claimed: {task_name}")
        return

    # Move to In_Progress/local
    in_progress_path = IN_PROGRESS_LOCAL / task_name
    shutil.move(str(approved_path), str(in_progress_path))

    try:
        # Read approval file
        with open(in_progress_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract draft
        draft_content = extract_draft_content(content)

        if not draft_content:
            raise ValueError("No draft content found")

        # Send email
        if send_email(draft_content, in_progress_path):
            # Archive to Done
            done_path = DONE / "email" / task_name
            done_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(in_progress_path), str(done_path))
            print(f"✅ Archived: {task_name}")
        else:
            raise Exception("Email sending failed")

    except Exception as e:
        print(f"❌ Error executing {task_name}: {e}")
        # Move to Failed
        failed_path = FAILED_LOCAL / task_name
        if in_progress_path.exists():
            shutil.move(str(in_progress_path), str(failed_path))
        print(f"❌ Moved to Failed: {task_name}")


def execute_social_approval(approval_file):
    """Execute approved social media task"""
    task_name = approval_file.name

    # Claim by moving to Approved
    approved_path = APPROVED / "social" / task_name
    approved_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(approval_file), str(approved_path))
        print(f"✅ Claimed: {task_name}")
    except FileNotFoundError:
        print(f"⚠️  Already claimed: {task_name}")
        return

    # Move to In_Progress/local
    in_progress_path = IN_PROGRESS_LOCAL / task_name
    shutil.move(str(approved_path), str(in_progress_path))

    try:
        # Read approval file
        with open(in_progress_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract draft and platforms
        draft_content = extract_draft_content(content)
        frontmatter, _ = parse_frontmatter(content)
        platforms = frontmatter.get('platforms', '[]')

        if not draft_content:
            raise ValueError("No draft content found")

        # Post to social media
        if post_to_social(draft_content, platforms, in_progress_path):
            # Archive to Done
            done_path = DONE / "social" / task_name
            done_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(in_progress_path), str(done_path))
            print(f"✅ Archived: {task_name}")
        else:
            raise Exception("Social posting failed")

    except Exception as e:
        print(f"❌ Error executing {task_name}: {e}")
        # Move to Failed
        failed_path = FAILED_LOCAL / task_name
        if in_progress_path.exists():
            shutil.move(str(in_progress_path), str(failed_path))
        print(f"❌ Moved to Failed: {task_name}")


def handle_rejected(approval_file, task_type):
    """Handle rejected approval"""
    task_name = approval_file.name
    done_path = DONE / task_type / f"REJECTED_{task_name}"
    done_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(approval_file), str(done_path))
        print(f"❌ Rejected and archived: {task_name}")
    except FileNotFoundError:
        print(f"⚠️  Already processed: {task_name}")


def main():
    """Main local execution loop"""
    print("💻 Local Executor Started")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    # Process email approvals
    email_approvals = list(PENDING_APPROVAL_EMAIL.glob("APPROVAL_*.md"))
    if email_approvals:
        print(f"📧 Checking {len(email_approvals)} email approval(s)...")
        for approval_file in email_approvals:
            status = check_approval_status(approval_file)

            if status == 'approved':
                print(f"✅ Approved: {approval_file.name}")
                execute_email_approval(approval_file)
            elif status == 'rejected':
                print(f"❌ Rejected: {approval_file.name}")
                handle_rejected(approval_file, 'email')
            else:
                print(f"⏳ Pending: {approval_file.name}")
    else:
        print("📧 No email approvals to process")

    print("")

    # Process social approvals
    social_approvals = list(PENDING_APPROVAL_SOCIAL.glob("APPROVAL_*.md"))
    if social_approvals:
        print(f"📱 Checking {len(social_approvals)} social approval(s)...")
        for approval_file in social_approvals:
            status = check_approval_status(approval_file)

            if status == 'approved':
                print(f"✅ Approved: {approval_file.name}")
                execute_social_approval(approval_file)
            elif status == 'rejected':
                print(f"❌ Rejected: {approval_file.name}")
                handle_rejected(approval_file, 'social')
            else:
                print(f"⏳ Pending: {approval_file.name}")
    else:
        print("📱 No social approvals to process")

    print("")
    print("✅ Local execution complete")


if __name__ == "__main__":
    main()
