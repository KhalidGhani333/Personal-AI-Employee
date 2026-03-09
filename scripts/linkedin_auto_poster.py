"""
LinkedIn Auto Poster - Automatic Sales Post Scheduler
======================================================
Automatically posts scheduled sales content to LinkedIn.
Reads from a queue file and posts at scheduled times.
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
QUEUE_FILE = VAULT_PATH / "Logs" / "linkedin_post_queue.json"
POSTED_FILE = VAULT_PATH / "Logs" / "linkedin_posted.json"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
LOGS_PATH.mkdir(parents=True, exist_ok=True)


def load_queue():
    """Load post queue"""
    if QUEUE_FILE.exists():
        try:
            return json.loads(QUEUE_FILE.read_text())
        except:
            return []
    return []


def save_queue(queue):
    """Save post queue"""
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))


def load_posted():
    """Load posted history"""
    if POSTED_FILE.exists():
        try:
            return json.loads(POSTED_FILE.read_text())
        except:
            return []
    return []


def save_posted(posted):
    """Save posted history"""
    POSTED_FILE.write_text(json.dumps(posted, indent=2))


def add_to_queue(content, scheduled_time=None, tags=None):
    """Add a post to the queue"""
    queue = load_queue()

    if scheduled_time is None:
        # Schedule for next business day at 10 AM
        scheduled_time = datetime.now() + timedelta(days=1)
        scheduled_time = scheduled_time.replace(hour=10, minute=0, second=0)

    post = {
        'id': f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'content': content,
        'scheduled_time': scheduled_time.isoformat() if isinstance(scheduled_time, datetime) else scheduled_time,
        'tags': tags or [],
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }

    queue.append(post)
    save_queue(queue)
    print(f"[INFO] Added post to queue: {post['id']}")
    return post


def post_to_linkedin(content):
    """Post content to LinkedIn using social_poster.py"""
    try:
        import subprocess

        script_path = Path(__file__).parent / "social_poster.py"

        result = subprocess.run(
            [sys.executable, str(script_path), 'pipeline', content, '--platforms', 'linkedin'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print(f"[SUCCESS] Posted to LinkedIn")
            return True
        else:
            print(f"[ERROR] Failed to post: {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to post to LinkedIn: {e}")
        return False


def process_queue():
    """Process pending posts in queue"""
    queue = load_queue()
    posted = load_posted()
    now = datetime.now()

    posts_to_process = []
    remaining_queue = []

    for post in queue:
        scheduled_time = datetime.fromisoformat(post['scheduled_time'])

        if scheduled_time <= now and post['status'] == 'pending':
            posts_to_process.append(post)
        else:
            remaining_queue.append(post)

    if not posts_to_process:
        print("[INFO] No posts ready to publish")
        return 0

    print(f"[INFO] Found {len(posts_to_process)} post(s) ready to publish")

    success_count = 0
    for post in posts_to_process:
        print(f"[INFO] Processing post: {post['id']}")

        if post_to_linkedin(post['content']):
            post['status'] = 'posted'
            post['posted_at'] = datetime.now().isoformat()
            posted.append(post)
            success_count += 1
        else:
            post['status'] = 'failed'
            post['failed_at'] = datetime.now().isoformat()
            remaining_queue.append(post)  # Keep failed posts in queue

    # Update files
    save_queue(remaining_queue)
    save_posted(posted)

    print(f"[SUCCESS] Posted {success_count}/{len(posts_to_process)} post(s)")
    return success_count


def generate_sales_posts():
    """Generate sample sales posts for the queue"""
    sales_templates = [
        {
            'content': """🚀 Transform Your Business with AI Automation

Are you spending hours on repetitive tasks? Our AI Employee solution can help you:

✅ Automate email responses
✅ Monitor communications 24/7
✅ Generate intelligent replies
✅ Manage social media posting

Let AI handle the routine work while you focus on growth.

Interested? Let's connect! 💼

#AIAutomation #BusinessGrowth #Productivity #Innovation""",
            'tags': ['ai', 'automation', 'business']
        },
        {
            'content': """💡 Did you know?

Businesses using AI automation save an average of 20+ hours per week on routine tasks.

Our Personal AI Employee system:
• Monitors Gmail & WhatsApp
• Generates context-aware replies
• Posts to social media automatically
• Requires human approval for sensitive actions

Ready to reclaim your time?

DM me to learn more! 📩

#TimeManagement #AIEmployee #SmartBusiness #Efficiency""",
            'tags': ['productivity', 'ai', 'business']
        },
        {
            'content': """🎯 Client Success Story

One of our clients reduced their response time from 4 hours to 15 minutes using our AI Employee system.

The result?
→ 3x faster customer service
→ Higher client satisfaction
→ More time for strategic work

Want similar results for your business?

Let's talk! Comment below or send me a message. 👇

#ClientSuccess #AITransformation #BusinessAutomation #Results""",
            'tags': ['success', 'ai', 'automation']
        }
    ]

    # Schedule posts for next 3 days
    for i, template in enumerate(sales_templates):
        scheduled_time = datetime.now() + timedelta(days=i+1)
        scheduled_time = scheduled_time.replace(hour=10, minute=0, second=0)

        add_to_queue(
            content=template['content'],
            scheduled_time=scheduled_time,
            tags=template['tags']
        )

    print(f"[SUCCESS] Generated {len(sales_templates)} sales posts")


def show_queue():
    """Display current queue"""
    queue = load_queue()

    if not queue:
        print("[INFO] Queue is empty")
        return

    print(f"\n{'='*60}")
    print(f"LinkedIn Post Queue ({len(queue)} posts)")
    print(f"{'='*60}\n")

    for post in queue:
        scheduled_time = datetime.fromisoformat(post['scheduled_time'])
        print(f"ID: {post['id']}")
        print(f"Status: {post['status']}")
        print(f"Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Content: {post['content'][:100]}...")
        print(f"Tags: {', '.join(post['tags'])}")
        print(f"{'-'*60}\n")


def show_posted():
    """Display posted history"""
    posted = load_posted()

    if not posted:
        print("[INFO] No posts in history")
        return

    print(f"\n{'='*60}")
    print(f"Posted History ({len(posted)} posts)")
    print(f"{'='*60}\n")

    for post in posted[-10:]:  # Show last 10
        posted_time = datetime.fromisoformat(post['posted_at'])
        print(f"ID: {post['id']}")
        print(f"Posted: {posted_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"Content: {post['content'][:100]}...")
        print(f"{'-'*60}\n")


def run_scheduler(check_interval=300):
    """Run scheduler continuously"""
    print(f"[INFO] LinkedIn Auto Poster started")
    print(f"[INFO] Checking every {check_interval} seconds")
    print(f"[INFO] Press Ctrl+C to stop")

    try:
        while True:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking queue...")

            try:
                process_queue()
            except Exception as e:
                print(f"[ERROR] Error processing queue: {e}")

            print(f"[INFO] Next check in {check_interval} seconds...")
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n[INFO] Scheduler stopped by user")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Auto Poster - Automatic sales post scheduler')
    parser.add_argument('--generate', action='store_true', help='Generate sample sales posts')
    parser.add_argument('--process', action='store_true', help='Process queue once')
    parser.add_argument('--schedule', action='store_true', help='Run scheduler continuously')
    parser.add_argument('--show-queue', action='store_true', help='Show current queue')
    parser.add_argument('--show-posted', action='store_true', help='Show posted history')
    parser.add_argument('--add', type=str, help='Add custom post to queue')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds (default: 300)')

    args = parser.parse_args()

    if args.generate:
        generate_sales_posts()
    elif args.process:
        process_queue()
    elif args.schedule:
        run_scheduler(args.interval)
    elif args.show_queue:
        show_queue()
    elif args.show_posted:
        show_posted()
    elif args.add:
        add_to_queue(args.add)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
