"""
LinkedIn Posting - Safe Human-Supervised Posting
=================================================
Uses Playwright with session-based authentication.
Auto-fills content but STOPS before publishing.
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
LOGS_PATH = VAULT_PATH / "Logs"
SESSION_FILE = Path(os.getenv('LINKEDIN_SESSION_PATH', './sessions/linkedin_session.json'))

LOGS_PATH.mkdir(parents=True, exist_ok=True)
SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)


def post_to_linkedin(content, headless=False):
    """Post content to LinkedIn using Playwright with session-based auth"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright not installed")
        return False

    print("[INFO] Starting LinkedIn posting...")

    with sync_playwright() as p:
        # Launch browser with stealth settings to avoid detection
        browser = p.chromium.launch(
            headless=headless,
            args=[
                '--start-maximized',  # Maximize window
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )

        # Create context with realistic settings
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='Asia/Karachi',
            no_viewport=True  # Use full window size instead of fixed viewport
        )

        if SESSION_FILE.exists():
            try:
                session_data = json.loads(SESSION_FILE.read_text())
                context.add_cookies(session_data.get('cookies', []))
                print("[INFO] Loaded saved session")
            except:
                print("[INFO] No valid session found")

        page = context.new_page()

        # Add extra JavaScript to hide automation
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            print("[INFO] Opening LinkedIn...")
            # Use domcontentloaded instead of load - it's faster and more reliable
            page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
            print("[INFO] Waiting for page to load...")
            page.wait_for_timeout(8000)

            if "login" in page.url.lower() or "authwall" in page.url.lower():
                print("\n" + "=" * 60)
                print("WARNING: NOT LOGGED IN")
                print("=" * 60)
                print("\nPlease login manually in the browser window.")
                print("After login, the session will be saved automatically.")
                print("\nWaiting 90 seconds for manual login...")
                print("=" * 60)

                page.wait_for_timeout(90000)

                cookies = context.cookies()
                session_data = {'cookies': cookies}
                SESSION_FILE.write_text(json.dumps(session_data, indent=2))
                print("\n[SUCCESS] Session saved for future use")

                page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
                print("[INFO] Waiting for feed to load...")
                page.wait_for_timeout(5000)

            print("[INFO] Looking for post composer...")
            page.wait_for_timeout(3000)

            start_post_selectors = [
                'button:has-text("Start a post")',
                'button[aria-label*="Start a post"]',
                'div[role="button"]:has-text("Start a post")',
                'button.share-box-feed-entry__trigger',
                'div.share-box-feed-entry__trigger'
            ]

            clicked = False
            for selector in start_post_selectors:
                try:
                    print(f"[DEBUG] Trying selector: {selector}")
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click()
                        clicked = True
                        print("[SUCCESS] Clicked 'Start a post'")
                        break
                except Exception as e:
                    print(f"[DEBUG] Selector failed: {e}")
                    pass

            if not clicked:
                print("[WARNING] Could not find 'Start a post' button automatically")
                print("[INFO] Please click 'Start a post' manually in the next 15 seconds...")
                page.wait_for_timeout(15000)

            print("[INFO] Waiting for composer to open...")
            page.wait_for_timeout(4000)

            print("[INFO] Writing post content...")
            page.wait_for_timeout(3000)

            editor_selectors = [
                'div[role="textbox"][contenteditable="true"]',
                'div.ql-editor[contenteditable="true"]',
                'div[data-placeholder*="share"]',
                'div[contenteditable="true"]',
                'div.ql-editor',
                'p[contenteditable="true"]'
            ]

            filled = False
            for selector in editor_selectors:
                try:
                    print(f"[DEBUG] Trying editor selector: {selector}")
                    if page.locator(selector).count() > 0:
                        editor = page.locator(selector).first
                        editor.click()
                        page.wait_for_timeout(1500)

                        # Clear any existing content
                        page.keyboard.press("Control+A")
                        page.wait_for_timeout(200)

                        # Type content
                        page.keyboard.type(content, delay=30)
                        filled = True
                        print("[SUCCESS] Content filled successfully!")
                        break
                except Exception as e:
                    print(f"[DEBUG] Editor selector failed: {e}")
                    continue

            if not filled:
                try:
                    print("[INFO] Trying direct keyboard input method...")
                    page.keyboard.press("Tab")
                    page.wait_for_timeout(500)
                    page.keyboard.type(content, delay=30)
                    filled = True
                    print("[SUCCESS] Content filled via keyboard")
                except Exception as e:
                    print(f"[DEBUG] Keyboard method failed: {e}")
                    pass

            if not filled:
                print("\n" + "=" * 60)
                print("[WARNING] Could not auto-fill content")
                print("=" * 60)
                print("\nPlease paste content manually:")
                print(f"\n{content}\n")
                print("=" * 60)

            page.wait_for_timeout(2000)

            print("\n" + "=" * 60)
            print("READY TO POST - HUMAN REVIEW REQUIRED")
            print("=" * 60)
            print("\nContent has been filled in the post editor.")
            print("\nIMPORTANT STEPS:")
            print("1. Review the post content carefully")
            print("2. Make any edits if needed")
            print("3. Click 'Post' button MANUALLY when ready")
            print("4. This script will NOT auto-publish (safety)")
            print("\nBrowser will stay open for 5 minutes.")
            print("Close browser manually when done posting.")
            print("=" * 60 + "\n")

            # Wait 5 minutes for user to review and post
            page.wait_for_timeout(300000)

            print("\n[INFO] Session timeout - closing browser")
            browser.close()
            return True

        except Exception as e:
            print(f"[ERROR] Failed to post: {e}")
            browser.close()
            return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Posting - Safe human-supervised posting')
    parser.add_argument('--content', help='Post content (text)')
    parser.add_argument('--file', help='Read content from file')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')

    args = parser.parse_args()

    # Get content from file or argument
    content = None
    if args.file:
        try:
            content = Path(args.file).read_text(encoding='utf-8')
            print(f"[INFO] Loaded content from: {args.file}")
        except Exception as e:
            print(f"[ERROR] Could not read file: {e}")
            sys.exit(1)
    elif args.content:
        content = args.content
    else:
        print("[ERROR] Please provide --content or --file")
        sys.exit(1)

    success = post_to_linkedin(content, args.headless)

    if success:
        log_file = LOGS_PATH / "linkedin_posts.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{datetime.now().isoformat()}] Posted: {args.content[:50]}...\n")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
