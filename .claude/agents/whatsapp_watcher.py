"""
WhatsApp Watcher - Monitors WhatsApp Web for urgent messages
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

VAULT_PATH = Path(os.getenv('OBSIDIAN_VAULT_PATH', './AI_Employee_Vault'))
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
SESSION_PATH = os.getenv('WHATSAPP_SESSION_PATH', './whatsapp-session')
KEYWORDS = os.getenv('WHATSAPP_KEYWORDS', 'urgent,asap,invoice,payment').split(',')
CHECK_INTERVAL = 30

(VAULT_PATH / 'Logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / 'Logs' / 'whatsapp_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('WhatsAppWatcher')


class WhatsAppWatcher:
    def __init__(self):
        self.keywords = [kw.strip().lower() for kw in KEYWORDS]
        self.processed = set()

    def check_messages(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    SESSION_PATH,
                    headless=True,
                    args=['--no-sandbox']
                )

                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto('https://web.whatsapp.com', timeout=60000)

                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                except:
                    logger.warning("WhatsApp not loaded")
                    browser.close()
                    return

                unread = page.query_selector_all('[aria-label*="unread"]')

                for chat in unread[:5]:
                    try:
                        text = chat.inner_text().lower()
                        if any(kw in text for kw in self.keywords):
                            chat.click()
                            time.sleep(1)
                            self.process_message(page, text)
                    except Exception as e:
                        logger.error(f"Error: {e}")

                browser.close()

        except Exception as e:
            logger.error(f"Error checking WhatsApp: {e}")

    def process_message(self, page, preview):
        try:
            contact_elem = page.query_selector('[data-testid="conversation-header"]')
            contact = contact_elem.inner_text().split('\n')[0] if contact_elem else "Unknown"

            messages = page.query_selector_all('[data-testid="msg-container"]')
            latest = [msg.inner_text() for msg in messages[-5:]]
            content = '\n'.join(latest)

            msg_hash = hash(f"{contact}_{content[:50]}")
            if msg_hash in self.processed:
                return

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"WHATSAPP_{contact.replace(' ', '_')}_{timestamp}.md"
            filepath = NEEDS_ACTION / filename

            file_content = f"""---
type: whatsapp
contact: {contact}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## Message Content
{content}

## Instructions for Claude
Process using /whatsapp-responder skill.
"""

            filepath.write_text(file_content, encoding='utf-8')
            self.processed.add(msg_hash)
            logger.info(f"Created action file: {filename}")

        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def run(self):
        logger.info("WhatsApp Watcher started")

        if not Path(SESSION_PATH).exists():
            logger.error(f"Session not found: {SESSION_PATH}")
            logger.info("Run whatsapp_login.py first")
            return

        while True:
            try:
                logger.info("Checking messages...")
                self.check_messages()
                time.sleep(CHECK_INTERVAL)
            except KeyboardInterrupt:
                logger.info("Stopped")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(60)


if __name__ == '__main__':
    WhatsAppWatcher().run()
