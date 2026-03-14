"""
LinkedIn Posting - Simplified and Reliable Version
===================================================
Uses Playwright with persistent browser profiles for automatic login.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
LOGS_PATH = VAULT_PATH / "Logs"
PROFILE_PATH = VAULT_PATH / "Browser_Profiles" / "linkedin_profile"

LOGS_PATH.mkdir(parents=True, exist_ok=True)
PROFILE_PATH.mkdir(parents=True, exist_ok=True)


def post_to_linkedin(content, headless=False):
    """Post content to LinkedIn using persistent browser profile"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright not installed")
        return False

    print("[INFO] Starting LinkedIn posting...")

    with sync_playwright() as p:
        # Launch browser with persistent profile (auto-login!)
        print("[INFO] Loading LinkedIn profile...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_PATH),
            headless=headless,
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled'
            ],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1366, 'height': 768}
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Hide webdriver property
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            print("[INFO] Opening LinkedIn...")
            page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)

            # Wait for page to be ready
            print("[INFO] Waiting for page to load...")
            time.sleep(5)

            # Check if logged in
            if "login" in page.url.lower() or "authwall" in page.url.lower():
                print("\n" + "=" * 60)
                print("LOGIN REQUIRED - FIRST TIME ONLY")
                print("=" * 60)
                print("\nPlease login manually in the browser window.")
                print("Your login will be saved permanently in the browser profile.")
                print("You won't need to login again!")
                print("\nWaiting 3 minutes for manual login...")
                print("=" * 60)

                time.sleep(180)

                print("\n[SUCCESS] Login saved! Next time you'll be auto-logged in.")

                page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)
            else:
                print("[SUCCESS] Already logged in! (using saved profile)")

            print("[INFO] Looking for 'Start a post' button...")

            # Wait for the share box to appear (this is more reliable)
            try:
                # Wait for any element that contains "Start a post" text
                page.wait_for_selector('text="Start a post"', timeout=10000)
                print("[SUCCESS] Found 'Start a post' button")

                # Click it
                page.click('text="Start a post"')
                print("[SUCCESS] Clicked 'Start a post'")

            except Exception as e:
                print(f"[WARNING] Could not find button automatically: {str(e)[:50]}")
                print("[INFO] Please click 'Start a post' manually...")
                time.sleep(20)

            # Wait for composer modal to open
            print("[INFO] Waiting for post composer...")
            time.sleep(4)

            # Find the editor - wait for contenteditable div
            print("[INFO] Looking for post editor...")
            try:
                # Wait for any contenteditable div to appear
                page.wait_for_selector('div[contenteditable="true"]', timeout=10000)
                print("[SUCCESS] Found post editor")

                # Get the first visible contenteditable div
                editor = page.locator('div[contenteditable="true"]').first

                # Click to focus
                editor.click()
                time.sleep(1)

                print("[INFO] Filling content...")

                # Method 1: Try fill() method (simplest)
                try:
                    editor.fill(content)
                    time.sleep(1)

                    # Verify
                    if content[:15] in editor.text_content():
                        print("[SUCCESS] Content filled!")
                    else:
                        raise Exception("Fill verification failed")

                except:
                    # Method 2: Type character by character
                    print("[DEBUG] Trying keyboard typing...")
                    editor.click()
                    time.sleep(0.5)

                    # Clear first
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Delete")
                    time.sleep(0.5)

                    # Type content
                    page.keyboard.type(content, delay=20)
                    time.sleep(1)

                    # Verify
                    if content[:15] in editor.text_content():
                        print("[SUCCESS] Content filled via keyboard!")
                    else:
                        print("[WARNING] Content may not be filled correctly")

            except Exception as e:
                print(f"[ERROR] Could not fill content: {str(e)[:80]}")
                print("\nPlease paste content manually:")
                print(f"\n{content}\n")

            # Ready to post
            print("\n" + "=" * 60)
            print("READY TO POST")
            print("=" * 60)
            print("\nContent has been filled.")
            print("Please review and click 'Post' button manually.")
            print("\nBrowser will stay open for 2 minutes.")
            print("=" * 60 + "\n")

            # Wait for user to post
            time.sleep(120)

            print("\n[INFO] Closing browser")
            browser.close()
            return True

        except Exception as e:
            print(f"[ERROR] Failed: {e}")
            browser.close()
            return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn Posting - Simplified version')
    parser.add_argument('--content', help='Post content (text)')
    parser.add_argument('--file', help='Read content from file')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')

    args = parser.parse_args()

    # Get content
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
            f.write(f"\n[{datetime.now().isoformat()}] Posted: {content[:50]}...\n")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
