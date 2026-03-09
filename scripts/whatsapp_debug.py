"""
WhatsApp Watcher Debug - Find Correct Selectors
================================================
Debug script to identify correct WhatsApp Web selectors.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
LOGS_PATH = VAULT_PATH / "Logs"
LOGS_PATH.mkdir(parents=True, exist_ok=True)

def debug_whatsapp():
    """Debug WhatsApp Web to find correct selectors"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright not installed")
        return

    print("[DEBUG] Starting WhatsApp Web debug...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to WhatsApp Web
        print("[DEBUG] Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com")

        # Wait for page to load
        print("[DEBUG] Waiting for page to load (10 seconds)...")
        page.wait_for_timeout(10000)

        # Take screenshot
        screenshot_path = LOGS_PATH / f"whatsapp_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=str(screenshot_path))
        print(f"[DEBUG] Screenshot saved: {screenshot_path}")

        # Try different selectors for unread messages
        print("\n[DEBUG] Testing different selectors for unread badges...")

        selectors = [
            'span[aria-label*="unread message"]',
            'span[aria-label*="unread"]',
            'span[data-icon="unread-count"]',
            'span.unread-count',
            'div[aria-label*="unread"]',
            '[data-testid="unread-count"]',
            'span[class*="unread"]',
            'div[class*="unread"]',
        ]

        for selector in selectors:
            try:
                elements = page.locator(selector).all()
                print(f"  Selector: {selector}")
                print(f"    Found: {len(elements)} element(s)")
                if elements:
                    for i, elem in enumerate(elements[:3]):
                        try:
                            text = elem.inner_text()
                            print(f"      Element {i+1}: '{text}'")
                        except:
                            print(f"      Element {i+1}: (no text)")
            except Exception as e:
                print(f"  Selector: {selector}")
                print(f"    Error: {e}")

        # Check for chat list
        print("\n[DEBUG] Checking for chat list...")
        try:
            chat_list = page.locator('div[aria-label="Chat list"]').first
            if chat_list.count() > 0:
                print("  [OK] Chat list found")

                # Get all list items
                list_items = page.locator('div[role="listitem"]').all()
                print(f"  [INFO] Found {len(list_items)} chat(s) in list")

                # Check first few chats
                print("\n[DEBUG] Analyzing first 5 chats...")
                for i, item in enumerate(list_items[:5]):
                    try:
                        html = item.inner_html()
                        print(f"\n  Chat {i+1}:")
                        print(f"    HTML length: {len(html)} chars")

                        # Check for unread indicators
                        if 'unread' in html.lower():
                            print(f"    Contains 'unread': YES")
                        else:
                            print(f"    Contains 'unread': NO")

                    except Exception as e:
                        print(f"  Chat {i+1}: Error - {e}")

            else:
                print("  [ERROR] Chat list not found")
        except Exception as e:
            print(f"  [ERROR] {e}")

        print("\n[DEBUG] Keeping browser open for 30 seconds for manual inspection...")
        print("[DEBUG] Check the browser window and look for unread message badges")
        page.wait_for_timeout(30000)

        browser.close()
        print("\n[DEBUG] Debug complete. Check the screenshot and output above.")


if __name__ == "__main__":
    debug_whatsapp()
