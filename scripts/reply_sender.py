"""
Reply Sender - Send Approved Replies
=====================================
Monitors Needs_Approval folder and sends approved replies via appropriate channels.
"""

import os
import sys
import re
import subprocess
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_APPROVAL = VAULT_PATH / "Needs_Approval"
DONE = VAULT_PATH / "Done"
LOGS_PATH = VAULT_PATH / "Logs"
SESSION_FILE = LOGS_PATH / "whatsapp_session.json"

# Script paths
SCRIPTS_PATH = Path(__file__).parent
GMAIL_SEND = SCRIPTS_PATH.parent / ".claude" / "skills" / "gmail-send" / "scripts" / "send_email.py"

# Ensure directories exist
NEEDS_APPROVAL.mkdir(parents=True, exist_ok=True)
DONE.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)


def parse_approval_file(filepath):
    """Parse approval file and extract metadata and content"""
    content = filepath.read_text(encoding='utf-8')

    # Extract frontmatter
    frontmatter = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            for line in frontmatter_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()
            content = parts[2]

    # Extract original message sender
    sender_match = re.search(r'\*\*From:\*\*\s*(.+)', content)
    sender = sender_match.group(1).strip() if sender_match else "Unknown"

    # Extract proposed reply
    reply_match = re.search(r'## Proposed Reply\s*\n\n(.+?)(?:\n\n---|\Z)', content, re.DOTALL)
    reply = reply_match.group(1).strip() if reply_match else ""

    # Extract original subject if email
    subject_match = re.search(r'\*\*Subject:\*\*\s*(.+)', content)
    subject = subject_match.group(1).strip() if subject_match else None

    return {
        'status': frontmatter.get('status', 'pending'),
        'message_type': frontmatter.get('message_type', 'email'),
        'sender': sender,
        'reply': reply,
        'subject': subject
    }


def send_email_reply(sender, subject, reply):
    """Send email reply using gmail-send skill"""
    try:
        # Prepare subject
        if subject and not subject.startswith('Re:'):
            reply_subject = f"Re: {subject}"
        else:
            reply_subject = subject or "Reply"

        # Call gmail-send script
        result = subprocess.run(
            [
                sys.executable,
                str(GMAIL_SEND),
                '--to', sender,
                '--subject', reply_subject,
                '--body', reply
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"[SUCCESS] Email sent to {sender}")
            return True
        else:
            print(f"[ERROR] Failed to send email: {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False


def send_whatsapp_reply(sender, reply):
    """Send WhatsApp reply using Playwright"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright not installed")
        print("[TIP] Run: pip install playwright")
        print("[TIP] Then run: playwright install chromium")
        return False

    print(f"[INFO] Sending WhatsApp reply to {sender}...")

    try:
        with sync_playwright() as p:
            # Launch browser with proper window settings
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--start-maximized',
                    '--disable-blink-features=AutomationControlled'
                ]
            )

            # Load complete browser state if exists
            if SESSION_FILE.exists():
                try:
                    print("[INFO] Loading saved session")
                    context = browser.new_context(
                        storage_state=str(SESSION_FILE),
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        no_viewport=True
                    )
                except Exception as e:
                    print(f"[WARNING] Could not load session: {e}")
                    print("[INFO] Creating new context")
                    context = browser.new_context(
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        no_viewport=True
                    )
            else:
                print("[INFO] No session file found")
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    no_viewport=True
                )

            page = context.new_page()

            # Navigate to WhatsApp Web
            print("[INFO] Opening WhatsApp Web...")
            page.goto("https://web.whatsapp.com")

            # Wait for WhatsApp to load
            print("[INFO] Waiting for WhatsApp to load...")
            page.wait_for_timeout(10000)

            # Wait for chat list to be visible (indicates WhatsApp is ready)
            try:
                page.wait_for_selector('div[aria-label="Chat list"]', timeout=15000)
                print("[INFO] WhatsApp loaded successfully")
            except:
                # Check if QR code is present
                if page.locator('canvas[aria-label="Scan this QR code to link a device!"]').count() > 0:
                    print("[ERROR] Session expired or invalid - QR code detected")
                    print("[TIP] Please run: python scripts/whatsapp_watcher.py")
                    print("[TIP] Scan the QR code, wait for chats to load, then try again")
                    browser.close()
                    return False
                else:
                    print("[WARNING] Chat list not detected, but continuing...")

            # Search for contact
            print(f"[INFO] Searching for contact: {sender}")

            # Try multiple search box selectors
            search_selectors = [
                'div[contenteditable="true"][data-tab="3"]',
                'div[title="Search input textbox"]',
                'div[role="textbox"][title*="Search"]',
                'div[data-testid="chat-list-search"]',
                'p[class*="selectable-text"][contenteditable="true"]',
                'div._ak1l',  # WhatsApp search class
                'div[contenteditable="true"]'  # Broader selector
            ]

            search_box = None
            for selector in search_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        search_box = page.locator(selector).first
                        print(f"[DEBUG] Found search box with: {selector}")
                        break
                except:
                    continue

            if not search_box:
                print("[ERROR] Could not find search box")
                print("[DEBUG] Trying to click on search icon first...")

                # Try to click search icon to activate search
                search_icon_selectors = [
                    'button[aria-label="Search or start new chat"]',
                    'span[data-icon="search"]',
                    'div[title="Search or start new chat"]',
                    'button[title*="Search"]'
                ]

                search_icon_clicked = False
                for icon_selector in search_icon_selectors:
                    try:
                        if page.locator(icon_selector).count() > 0:
                            page.locator(icon_selector).first.click()
                            print(f"[DEBUG] Clicked search icon: {icon_selector}")
                            page.wait_for_timeout(1000)
                            search_icon_clicked = True
                            break
                    except:
                        continue

                if search_icon_clicked:
                    # Try finding search box again
                    for selector in search_selectors:
                        try:
                            if page.locator(selector).count() > 0:
                                search_box = page.locator(selector).first
                                print(f"[DEBUG] Found search box after clicking icon: {selector}")
                                break
                        except:
                            continue

                if not search_box:
                    print("[ERROR] Still could not find search box")
                    browser.close()
                    return False

            # Click and type in search box
            search_box.click()
            page.wait_for_timeout(1000)
            search_box.type(sender, delay=100)
            page.wait_for_timeout(2000)

            # Click on the first result
            print("[INFO] Clicking on chat...")
            chat_selectors = [
                f'span[title="{sender}"]',
                'div[role="listitem"]',
                'div[data-testid="cell-frame-container"]'
            ]

            clicked = False
            for selector in chat_selectors:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.click()
                    clicked = True
                    print(f"[DEBUG] Clicked chat with: {selector}")
                    break

            if not clicked:
                print("[ERROR] Could not find chat to click")
                browser.close()
                return False

            page.wait_for_timeout(2000)

            # Find message input box
            print("[INFO] Typing message...")
            message_selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                'div[title="Type a message"]',
                'div[role="textbox"][title*="Type"]',
                'div[data-testid="conversation-compose-box-input"]'
            ]

            message_box = None
            for selector in message_selectors:
                if page.locator(selector).count() > 0:
                    message_box = page.locator(selector).first
                    print(f"[DEBUG] Found message box with: {selector}")
                    break

            if not message_box:
                print("[ERROR] Could not find message input box")
                browser.close()
                return False

            # Type the reply
            message_box.click()
            page.wait_for_timeout(500)
            message_box.type(reply, delay=50)
            page.wait_for_timeout(1000)

            # Click send button
            print("[INFO] Sending message...")
            send_selectors = [
                'button[data-testid="compose-btn-send"]',
                'button[aria-label="Send"]',
                'span[data-icon="send"]'
            ]

            send_button = None
            for selector in send_selectors:
                if page.locator(selector).count() > 0:
                    send_button = page.locator(selector).first
                    print(f"[DEBUG] Found send button with: {selector}")
                    break

            if not send_button:
                print("[ERROR] Could not find send button")
                browser.close()
                return False

            send_button.click()
            page.wait_for_timeout(2000)

            print(f"[SUCCESS] WhatsApp message sent to {sender}")

            # Close browser
            browser.close()
            return True

    except Exception as e:
        print(f"[ERROR] Failed to send WhatsApp message: {e}")
        return False


def process_approval(approval_file):
    """Process a single approval file"""
    try:
        print(f"[INFO] Processing: {approval_file.name}")

        # Parse file
        data = parse_approval_file(approval_file)

        # Check status
        if data['status'] != 'approved':
            print(f"[INFO] Status is '{data['status']}', skipping")
            return None

        print(f"[INFO] Approved reply to {data['sender']}")

        # Send based on message type
        success = False

        if data['message_type'] == 'email':
            success = send_email_reply(data['sender'], data['subject'], data['reply'])
        elif data['message_type'] == 'whatsapp':
            success = send_whatsapp_reply(data['sender'], data['reply'])
        else:
            print(f"[WARNING] Unknown message type: {data['message_type']}")
            success = False

        if success:
            # Move to Done
            done_file = DONE / approval_file.name
            approval_file.rename(done_file)
            print(f"[INFO] Moved to Done: {approval_file.name}")

            return {
                'file': approval_file.name,
                'sender': data['sender'],
                'type': data['message_type'],
                'success': True
            }
        else:
            return {
                'file': approval_file.name,
                'sender': data['sender'],
                'type': data['message_type'],
                'success': False
            }

    except Exception as e:
        print(f"[ERROR] Failed to process {approval_file.name}: {e}")
        return None


def run_reply_sender():
    """Run the reply sender to process all approved items"""
    print("[INFO] Reply Sender started")
    print(f"[INFO] Checking {NEEDS_APPROVAL} for approved items...")

    # Get all approval files
    approval_files = list(NEEDS_APPROVAL.glob("APPROVAL_*.md"))

    if not approval_files:
        print("[INFO] No approval files found")
        return []

    print(f"[INFO] Found {len(approval_files)} approval file(s)")

    results = []

    for approval_file in approval_files:
        result = process_approval(approval_file)
        if result:
            results.append(result)

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Reply Sender - Send approved replies')
    parser.add_argument('--continuous', action='store_true', help='Run continuously')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds (default: 300)')

    args = parser.parse_args()

    if args.continuous:
        import time
        print(f"[INFO] Running continuously (every {args.interval} seconds)")
        print("[INFO] Press Ctrl+C to stop")

        try:
            while True:
                print(f"\n[INFO] Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                results = run_reply_sender()

                if results:
                    sent = sum(1 for r in results if r['success'])
                    print(f"[SUCCESS] Sent {sent}/{len(results)} reply(ies)")

                print(f"[INFO] Next run in {args.interval} seconds...")
                time.sleep(args.interval)

        except KeyboardInterrupt:
            print("\n[INFO] Reply Sender stopped by user")
    else:
        results = run_reply_sender()

        if results:
            sent = sum(1 for r in results if r['success'])
            print(f"\n[SUCCESS] Sent {sent}/{len(results)} reply(ies):")
            for r in results:
                status = "[OK]" if r['success'] else "[FAIL]"
                print(f"  {status} {r['sender']} ({r['type']})")
        else:
            print("\n[INFO] No approved replies to send")


if __name__ == "__main__":
    main()
