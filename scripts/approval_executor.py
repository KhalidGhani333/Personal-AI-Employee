"""
Approval Executor - Automated Social Media Posting from Approved Folder
========================================================================
Monitors Approved/ folder and automatically posts approved content to social media.
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path to import social_poster
sys.path.insert(0, str(Path(__file__).parent))

# Import posting functions from social_poster
try:
    from social_poster import (
        post_to_linkedin,
        post_to_twitter,
        post_to_facebook,
        post_to_instagram,
        load_approved_post
    )
    SOCIAL_POSTER_AVAILABLE = True
except ImportError:
    SOCIAL_POSTER_AVAILABLE = False
    print("[WARNING] Could not import social_poster.py functions")

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
PENDING_APPROVAL = VAULT_PATH / "Pending_Approval"
APPROVED = VAULT_PATH / "Approved"
DONE = VAULT_PATH / "Done"
LOGS_PATH = VAULT_PATH / "Logs"
PROCESSED_FILE = LOGS_PATH / "processed_approvals.json"

# Ensure directories exist
PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)
APPROVED.mkdir(parents=True, exist_ok=True)
DONE.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = LOGS_PATH / "approval_actions.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# PROCESSED FILES TRACKING
# ============================================================================

def load_processed_files():
    """Load list of already processed approval files"""
    if PROCESSED_FILE.exists():
        try:
            return json.loads(PROCESSED_FILE.read_text())
        except:
            return []
    return []


def save_processed_files(processed_list):
    """Save list of processed approval files"""
    PROCESSED_FILE.write_text(json.dumps(processed_list, indent=2))


def mark_as_processed(filename):
    """Mark a file as processed"""
    processed = load_processed_files()
    if filename not in processed:
        processed.append(filename)
        save_processed_files(processed)


def is_processed(filename):
    """Check if file has been processed"""
    processed = load_processed_files()
    return filename in processed


# ============================================================================
# FILE PARSING
# ============================================================================

def parse_approval_file(filepath):
    """Parse approval file and extract metadata and content"""
    try:
        content = filepath.read_text(encoding='utf-8')

        # Parse frontmatter
        frontmatter = {}
        post_content = content

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                post_content = parts[2].strip()

                for line in frontmatter_text.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()

        return {
            'frontmatter': frontmatter,
            'content': post_content,
            'platform': frontmatter.get('platform', 'unknown'),
            'status': frontmatter.get('status', 'unknown')
        }

    except Exception as e:
        logger.error(f"Failed to parse file {filepath.name}: {e}")
        return None


# ============================================================================
# POSTING EXECUTION
# ============================================================================

def execute_posting(filepath, platform, content):
    """Execute posting to specified platform"""
    logger.info(f"Executing post to {platform}...")
    logger.info("=" * 60)

    success = False

    try:
        if platform == 'linkedin':
            logger.info("Platform: LinkedIn")
            success = post_to_linkedin(content, wait_for_confirmation=True)

        elif platform == 'twitter':
            logger.info("Platform: Twitter/X")
            success = post_to_twitter(content, wait_for_confirmation=True)

        elif platform == 'facebook':
            logger.info("Platform: Facebook")
            success = post_to_facebook(content, wait_for_confirmation=True)

        elif platform == 'instagram':
            logger.info("Platform: Instagram")
            success = post_to_instagram(content)

        else:
            logger.error(f"Unknown platform: {platform}")
            return False

        if success:
            logger.info(f"Successfully posted to {platform}")
            logger.info("=" * 60)
        else:
            logger.error(f"Failed to post to {platform}")
            logger.info("=" * 60)

        return success

    except Exception as e:
        logger.error(f"Error posting to {platform}: {e}")
        logger.info("=" * 60)
        return False


def move_to_done(filepath):
    """Move completed file to Done folder"""
    try:
        done_file = DONE / filepath.name

        # If file already exists in Done, add timestamp
        if done_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = filepath.stem.split('_')
            new_name = f"{filepath.stem}_{timestamp}{filepath.suffix}"
            done_file = DONE / new_name

        filepath.rename(done_file)
        logger.info(f"Moved to Done: {done_file.name}")
        return True

    except Exception as e:
        logger.error(f"Failed to move file to Done: {e}")
        return False


# ============================================================================
# APPROVAL MONITORING
# ============================================================================

def process_approved_file(filepath):
    """Process a single approved file"""
    logger.info("\n" + "=" * 60)
    logger.info(f"PROCESSING: {filepath.name}")
    logger.info("=" * 60)

    # Check if already processed
    if is_processed(filepath.name):
        logger.info("File already processed, skipping")
        return

    # Parse file
    parsed = parse_approval_file(filepath)
    if not parsed:
        logger.error("Failed to parse file")
        return

    platform = parsed['platform']
    content = parsed['content']
    status = parsed['status']

    logger.info(f"Platform: {platform}")
    logger.info(f"Status: {status}")
    logger.info(f"Content length: {len(content)} characters")

    # Verify status is approved
    if status != 'approved':
        logger.warning(f"File status is '{status}', not 'approved'. Skipping.")
        return

    # Execute posting
    success = execute_posting(filepath, platform, content)

    if success:
        # Move to Done
        if move_to_done(filepath):
            # Mark as processed
            mark_as_processed(filepath.name)
            logger.info(f"✓ Successfully completed: {filepath.name}")
        else:
            logger.error(f"✗ Posted but failed to move file: {filepath.name}")
    else:
        logger.error(f"✗ Failed to post: {filepath.name}")
        logger.info("File remains in Approved/ folder for retry")


def scan_approved_folder():
    """Scan Approved folder for new files"""
    try:
        # Get all .md files in Approved folder
        approved_files = list(APPROVED.glob("*.md"))

        if not approved_files:
            return []

        # Filter out already processed files
        new_files = [f for f in approved_files if not is_processed(f.name)]

        return new_files

    except Exception as e:
        logger.error(f"Error scanning Approved folder: {e}")
        return []


def watch_approved_folder(check_interval=30):
    """Continuously watch Approved folder for new files"""
    logger.info("=" * 60)
    logger.info("APPROVAL EXECUTOR STARTED")
    logger.info("=" * 60)
    logger.info(f"Monitoring: {APPROVED}")
    logger.info(f"Check interval: {check_interval} seconds")
    logger.info(f"Logs: {log_file}")
    logger.info("=" * 60)
    logger.info("\nWaiting for approved files...")
    logger.info("Move files from Pending_Approval/ to Approved/ to trigger posting")
    logger.info("Press Ctrl+C to stop\n")

    try:
        while True:
            # Scan for new files
            new_files = scan_approved_folder()

            if new_files:
                logger.info(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Found {len(new_files)} new file(s)")

                for filepath in new_files:
                    process_approved_file(filepath)

                logger.info("\nWaiting for more files...")

            # Wait before next check
            time.sleep(check_interval)

    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("APPROVAL EXECUTOR STOPPED")
        logger.info("=" * 60)


# ============================================================================
# MANUAL PROCESSING
# ============================================================================

def process_all_approved():
    """Process all files in Approved folder (one-time run)"""
    logger.info("=" * 60)
    logger.info("PROCESSING ALL APPROVED FILES")
    logger.info("=" * 60)

    approved_files = list(APPROVED.glob("*.md"))

    if not approved_files:
        logger.info("No files found in Approved folder")
        return

    logger.info(f"Found {len(approved_files)} file(s)")

    processed_count = 0
    success_count = 0

    for filepath in approved_files:
        # Skip already processed
        if is_processed(filepath.name):
            logger.info(f"Skipping (already processed): {filepath.name}")
            continue

        process_approved_file(filepath)
        processed_count += 1

        # Check if file was moved to Done (indicates success)
        if not filepath.exists():
            success_count += 1

    logger.info("\n" + "=" * 60)
    logger.info("PROCESSING COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Processed: {processed_count} file(s)")
    logger.info(f"Successful: {success_count} file(s)")
    logger.info(f"Failed: {processed_count - success_count} file(s)")
    logger.info("=" * 60)


def process_single_file(filename):
    """Process a single file by name"""
    filepath = APPROVED / filename

    if not filepath.exists():
        logger.error(f"File not found: {filename}")
        logger.info(f"Looking in: {APPROVED}")
        return False

    process_approved_file(filepath)
    return True


def list_approved_files():
    """List all files in Approved folder"""
    approved_files = list(APPROVED.glob("*.md"))

    if not approved_files:
        logger.info("No files in Approved folder")
        return

    logger.info("=" * 60)
    logger.info("FILES IN APPROVED FOLDER")
    logger.info("=" * 60)

    for filepath in approved_files:
        parsed = parse_approval_file(filepath)
        if parsed:
            platform = parsed['platform']
            status = parsed['status']
            processed = "✓ Processed" if is_processed(filepath.name) else "○ Pending"

            logger.info(f"\n{filepath.name}")
            logger.info(f"  Platform: {platform}")
            logger.info(f"  Status: {status}")
            logger.info(f"  {processed}")

    logger.info("\n" + "=" * 60)
    logger.info(f"Total: {len(approved_files)} file(s)")
    logger.info("=" * 60)


def reset_processed_tracking():
    """Reset processed files tracking (for testing)"""
    if PROCESSED_FILE.exists():
        PROCESSED_FILE.unlink()
        logger.info("Processed files tracking reset")
    else:
        logger.info("No processed files tracking to reset")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Approval Executor - Automated social media posting from Approved folder'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Watch command
    watch_parser = subparsers.add_parser('watch', help='Watch Approved folder continuously')
    watch_parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Check interval in seconds (default: 30)'
    )

    # Process command
    process_parser = subparsers.add_parser('process', help='Process all approved files once')

    # Single command
    single_parser = subparsers.add_parser('single', help='Process a single file')
    single_parser.add_argument('filename', help='Filename in Approved folder')

    # List command
    list_parser = subparsers.add_parser('list', help='List files in Approved folder')

    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset processed files tracking')

    args = parser.parse_args()

    # Check if social_poster is available
    if not SOCIAL_POSTER_AVAILABLE:
        logger.error("social_poster.py not available. Cannot proceed.")
        logger.error("Make sure social_poster.py is in the scripts/ directory")
        sys.exit(1)

    if args.command == 'watch':
        watch_approved_folder(check_interval=args.interval)

    elif args.command == 'process':
        process_all_approved()

    elif args.command == 'single':
        process_single_file(args.filename)

    elif args.command == 'list':
        list_approved_files()

    elif args.command == 'reset':
        reset_processed_tracking()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
