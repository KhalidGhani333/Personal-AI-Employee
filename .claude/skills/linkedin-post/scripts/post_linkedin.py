"""
LinkedIn Post - Production Browser Automation
==============================================
Creates real LinkedIn posts using Playwright browser automation.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("[ERROR] Playwright not installed")
    print("Install with: pip install playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)

# Load environment variables
load_dotenv()


def post_to_linkedin(content, headless=True):
    """
    Post content to LinkedIn using browser automation.

    Args:
        content: Post text content
        headless: Run browser in headless mode

    Returns:
        True if successful, False otherwise
    """
    try:
        # Get credentials
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')

        if not email or not password:
            print("[ERROR] Missing LINKEDIN_EMAIL or LINKEDIN_PASSWORD in environment")
            print("Set these in .env file or environment variables")
            return False

        print("[INFO] Starting browser automation...")

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()

            try:
                # Navigate to LinkedIn
                print("[INFO] Navigating to LinkedIn...")
                page.goto('https://www.linkedin.com/login', timeout=30000)

                # Login
                print(f"[INFO] Logging in as {email}...")
                page.fill('input[name="session_key"]', email)
                page.fill('input[name="session_password"]', password)
                page.click('button[type="submit"]')

                # Wait for feed to load
                print("[INFO] Waiting for feed to load...")
                page.wait_for_url('**/feed/**', timeout=30000)

                # Click "Start a post" button
                print("[INFO] Opening post composer...")
                page.click('button[aria-label*="Start a post"]', timeout=10000)

                # Wait for editor to appear
                page.wait_for_selector('.ql-editor', timeout=10000)

                # Enter content
                print("[INFO] Entering post content...")
                page.fill('.ql-editor', content)

                # Click Post button
                print("[INFO] Publishing post...")
                page.click('button[aria-label*="Post"]', timeout=5000)

                # Wait a moment for post to be created
                page.wait_for_timeout(3000)

                print("[SUCCESS] LinkedIn post published successfully")
                return True

            except PlaywrightTimeout as e:
                print(f"[ERROR] Timeout: {e}")
                print("This could be due to:")
                print("- Slow network connection")
                print("- LinkedIn requiring additional verification")
                print("- Changed page structure")
                return False

            except Exception as e:
                print(f"[ERROR] Failed during automation: {e}")
                return False

            finally:
                browser.close()

    except Exception as e:
        print(f"[ERROR] Failed to post to LinkedIn: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Post to LinkedIn using browser automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple post
  python post_linkedin.py --content "Excited to share our latest project!"

  # With visible browser (for debugging)
  python post_linkedin.py --content "Update" --headless false

Notes:
  - Requires Playwright: pip install playwright
  - Run: playwright install chromium
  - Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env
  - LinkedIn may require additional verification for new devices
        """
    )

    parser.add_argument(
        '--content',
        required=True,
        help='Post text content (max 3000 characters)'
    )
    parser.add_argument(
        '--headless',
        type=lambda x: x.lower() == 'true',
        default=True,
        help='Run browser in headless mode (default: true)'
    )

    args = parser.parse_args()

    # Validate content length
    if len(args.content) > 3000:
        print("[ERROR] Content exceeds 3000 character limit")
        sys.exit(1)

    # Post to LinkedIn
    success = post_to_linkedin(args.content, args.headless)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
