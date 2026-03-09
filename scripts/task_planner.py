"""
Task Planner - Analyzes inbox files and creates execution plans
================================================================
This script reads markdown files from the Inbox, analyzes their content,
and creates detailed step-by-step execution plans in the Needs_Action folder.

Features:
- Analyzes .md files in AI_Employee_Vault/Inbox
- Extracts task information and requirements
- Generates structured execution plans
- Moves processed files to Done folder
- Logs all actions to logs/actions.log
- Idempotent (processes each file only once)
- Supports command-line arguments for flexibility
"""

import os
import re
import argparse
from datetime import datetime
from pathlib import Path
import shutil


# Configuration
VAULT_PATH = Path("AI_Employee_Vault")
INBOX_FOLDER = VAULT_PATH / "Inbox"
NEEDS_ACTION_FOLDER = VAULT_PATH / "Needs_Action"
DONE_FOLDER = VAULT_PATH / "Done"
LOGS_FOLDER = Path("logs")
ACTION_LOG = LOGS_FOLDER / "actions.log"
PROCESSED_REGISTRY = LOGS_FOLDER / "processed_inbox_files.txt"


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


def load_processed_files():
    """
    Loads the set of already processed files from registry.

    Returns:
        Set of processed filenames
    """
    try:
        if PROCESSED_REGISTRY.exists():
            with open(PROCESSED_REGISTRY, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
    except Exception as e:
        log_action(f"Error loading processed registry: {e}", "WARNING")
        return set()


def save_processed_file(filename):
    """
    Saves a processed filename to registry.

    Args:
        filename: The filename to mark as processed
    """
    try:
        LOGS_FOLDER.mkdir(exist_ok=True)
        with open(PROCESSED_REGISTRY, 'a', encoding='utf-8') as f:
            f.write(f"{filename}\n")
    except Exception as e:
        log_action(f"Error saving to registry: {e}", "WARNING")


def parse_frontmatter(content):
    """
    Extracts YAML frontmatter from markdown content.

    Args:
        content: The markdown file content

    Returns:
        Tuple of (frontmatter_dict, content_without_frontmatter)
    """
    frontmatter = {}
    body = content

    # Check for frontmatter (--- at start)
    if content.strip().startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Parse frontmatter
            fm_lines = parts[1].strip().split('\n')
            for line in fm_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()

    return frontmatter, body


def extract_task_info(content):
    """
    Analyzes markdown content and extracts key task information.

    Args:
        content: The markdown file content

    Returns:
        Dictionary with extracted information
    """
    frontmatter, body = parse_frontmatter(content)

    # Extract title (first # heading or from frontmatter)
    title = "Untitled Task"
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()

    # Extract description (text after title, before next heading)
    description = ""
    desc_match = re.search(r'^#\s+.+?\n\n(.+?)(?=\n##|\Z)', body, re.MULTILINE | re.DOTALL)
    if desc_match:
        description = desc_match.group(1).strip()
    elif body:
        # If no clear structure, use first paragraph
        paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
        if paragraphs:
            description = paragraphs[0]

    # Extract checklist items (potential steps)
    checklist_items = re.findall(r'^\s*[-*]\s*\[[ x]\]\s*(.+)$', body, re.MULTILINE)

    # Extract bullet points (potential requirements)
    bullet_points = re.findall(r'^\s*[-*]\s+(?!\[)(.+)$', body, re.MULTILINE)

    # Determine priority from frontmatter or keywords
    priority = frontmatter.get('priority', 'medium').lower()
    if any(word in content.lower() for word in ['urgent', 'asap', 'critical', 'high priority']):
        priority = 'high'
    elif any(word in content.lower() for word in ['low priority', 'whenever', 'optional']):
        priority = 'low'

    # Extract file type from frontmatter
    task_type = frontmatter.get('type', 'general_task')

    return {
        'title': title,
        'description': description,
        'checklist_items': checklist_items,
        'bullet_points': bullet_points,
        'priority': priority,
        'type': task_type,
        'frontmatter': frontmatter,
        'full_content': body
    }


def generate_execution_plan(task_info, source_filename):
    """
    Generates a structured execution plan based on task information.

    Args:
        task_info: Dictionary with extracted task information
        source_filename: Original filename for reference

    Returns:
        String containing the formatted plan
    """
    timestamp = get_timestamp()

    # Build step-by-step plan
    steps = []
    if task_info['checklist_items']:
        # Use existing checklist items as steps
        steps = task_info['checklist_items']
    else:
        # Generate intelligent steps based on task type and content
        if task_info['type'] == 'file_review':
            steps = [
                "Open and review the file contents",
                "Identify the file type and purpose",
                "Extract key information or data",
                "Determine appropriate action (process, archive, respond)",
                "Execute the required action",
                "Document the outcome"
            ]
        elif 'email' in task_info['type'].lower():
            steps = [
                "Read the complete email content",
                "Identify sender and context",
                "Determine required response or action",
                "Draft response if needed",
                "Execute action (reply, forward, archive)",
                "Update status and log completion"
            ]
        elif 'whatsapp' in task_info['type'].lower() or 'message' in task_info['type'].lower():
            steps = [
                "Read the message content and context",
                "Identify the sender and urgency level",
                "Determine appropriate response",
                "Draft reply message",
                "Send response via appropriate channel",
                "Log the interaction"
            ]
        else:
            # Generic steps based on description
            steps = [
                "Review task requirements and context",
                "Gather necessary resources or information",
                "Execute the primary task objective",
                "Verify completion and quality",
                "Document results and outcomes",
                "Update status and notify if needed"
            ]

    # Build requirements list
    requirements = task_info['bullet_points'][:5] if task_info['bullet_points'] else [
        "Access to relevant files and resources",
        "Appropriate permissions and credentials",
        "Clear understanding of success criteria"
    ]

    # Build success criteria
    success_criteria = [
        "Task completed as specified",
        "All steps executed successfully",
        "Results documented and logged",
        "No errors or issues remaining"
    ]

    # Generate the plan content
    plan_content = f"""---
type: execution_plan
source_file: {source_filename}
created_at: {timestamp}
status: pending
priority: {task_info['priority']}
task_type: {task_info['type']}
---

# Execution Plan: {task_info['title']}

## Task Summary
{task_info['description'] if task_info['description'] else 'Process and complete the task as specified in the source file.'}

## Step-by-Step Plan
"""

    # Add numbered steps
    for i, step in enumerate(steps, 1):
        plan_content += f"{i}. {step}\n"

    plan_content += f"""
## Requirements
"""
    for req in requirements:
        plan_content += f"- {req}\n"

    plan_content += f"""
## Success Criteria
"""
    for criterion in success_criteria:
        plan_content += f"- [ ] {criterion}\n"

    plan_content += f"""
## Source Information
- **Original File:** `{source_filename}`
- **File Type:** {task_info['type']}
- **Priority:** {task_info['priority']}
- **Plan Created:** {timestamp}

## Notes
This execution plan was automatically generated by the Task Planner. Review the source file for complete context and details. Adjust steps as needed based on actual requirements.
"""

    return plan_content


def process_inbox_file(filename, dry_run=False):
    """
    Processes a single inbox file and creates an execution plan.

    Args:
        filename: Name of the file to process
        dry_run: If True, don't move files or save plans

    Returns:
        True if successful, False otherwise
    """
    try:
        inbox_path = INBOX_FOLDER / filename

        # Check if file exists
        if not inbox_path.exists():
            log_action(f"File not found: {filename}", "WARNING")
            return False

        # Read file content
        log_action(f"Processing: {filename}", "INFO")
        content = inbox_path.read_text(encoding='utf-8')

        # Skip empty files
        if not content.strip():
            log_action(f"Skipping empty file: {filename}", "WARNING")
            return False

        # Extract task information
        task_info = extract_task_info(content)
        log_action(f"Analyzed task: {task_info['title']} (Priority: {task_info['priority']})", "INFO")

        # Generate execution plan
        plan_content = generate_execution_plan(task_info, filename)

        if not dry_run:
            # Save plan to Needs_Action
            NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)
            plan_filename = f"Plan_{Path(filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            plan_path = NEEDS_ACTION_FOLDER / plan_filename
            plan_path.write_text(plan_content, encoding='utf-8')
            log_action(f"Created plan: {plan_filename}", "INFO")

            # Move original file to Done
            DONE_FOLDER.mkdir(parents=True, exist_ok=True)
            done_path = DONE_FOLDER / filename
            shutil.move(str(inbox_path), str(done_path))
            log_action(f"Moved to Done: {filename}", "INFO")

            # Mark as processed
            save_processed_file(filename)
        else:
            log_action(f"[DRY RUN] Would create plan and move {filename} to Done", "INFO")

        return True

    except Exception as e:
        log_action(f"Error processing {filename}: {e}", "ERROR")
        return False


def ensure_folders_exist():
    """Creates required folders if they don't exist."""
    try:
        INBOX_FOLDER.mkdir(parents=True, exist_ok=True)
        NEEDS_ACTION_FOLDER.mkdir(parents=True, exist_ok=True)
        DONE_FOLDER.mkdir(parents=True, exist_ok=True)
        LOGS_FOLDER.mkdir(exist_ok=True)
        return True
    except Exception as e:
        print(f"[ERROR] Error creating folders: {e}")
        return False


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Task Planner - Analyzes inbox files and creates execution plans'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Process specific file only'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without moving files or creating plans'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Task Planner - AI Employee")
    print("=" * 60)

    # Ensure folders exist
    if not ensure_folders_exist():
        print("\n[ERROR] Cannot start: Required folders could not be created")
        return

    log_action("Task Planner started", "INFO")

    # Load processed files registry
    processed_files = load_processed_files()

    # Get files to process
    if args.file:
        # Process specific file
        files_to_process = [args.file] if args.file not in processed_files else []
        if not files_to_process:
            log_action(f"File already processed: {args.file}", "INFO")
            print(f"\n[OK] File already processed: {args.file}")
            return
    else:
        # Process all unprocessed .md files in Inbox
        try:
            all_files = [f.name for f in INBOX_FOLDER.iterdir()
                        if f.is_file() and f.suffix.lower() == '.md']
            files_to_process = [f for f in all_files if f not in processed_files]
        except Exception as e:
            log_action(f"Error reading inbox: {e}", "ERROR")
            print(f"[ERROR] Error reading inbox: {e}")
            return

    if not files_to_process:
        log_action("No new files to process", "INFO")
        print("\n[OK] No new files to process")
        return

    print(f"\nFound {len(files_to_process)} file(s) to process")
    if args.dry_run:
        print("[DRY RUN MODE - No files will be moved]\n")

    # Process each file
    success_count = 0
    for filename in files_to_process:
        if process_inbox_file(filename, dry_run=args.dry_run):
            success_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Processed: {success_count}/{len(files_to_process)} file(s)")
    print("=" * 60)

    log_action(f"Task Planner completed: {success_count}/{len(files_to_process)} files processed", "INFO")


if __name__ == "__main__":
    main()
