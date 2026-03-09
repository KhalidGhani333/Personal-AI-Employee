"""
Gmail Watcher - Monitors Gmail inbox for important emails
Part of Personal AI Employee project
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(os.getenv('OBSIDIAN_VAULT_PATH', './AI_Employee_Vault'))
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', 'token.pickle')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '120'))  # 2 minutes default
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Setup logging
VAULT_PATH.mkdir(exist_ok=True)
(VAULT_PATH / 'Logs').mkdir(exist_ok=True)
NEEDS_ACTION.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / 'Logs' / 'gmail_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('GmailWatcher')


class GmailWatcher:
    """Monitors Gmail inbox for important emails"""

    def __init__(self):
        self.service = self.authenticate()
        self.processed_ids = self.load_processed_ids()
        logger.info("Gmail Watcher initialized")

    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None

        # Check if token file exists
        if os.path.exists(TOKEN_PATH):
            try:
                with open(TOKEN_PATH, 'rb') as token:
                    creds = pickle.load(token)
                logger.info("Loaded existing credentials")
            except Exception as e:
                logger.error(f"Error loading token: {e}")

        # If no valid credentials available
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired credentials")
                except Exception as e:
                    logger.error(f"Error refreshing credentials: {e}")
                    creds = None

            if not creds:
                if not os.path.exists(CREDENTIALS_PATH):
                    logger.error(f"Credentials file not found: {CREDENTIALS_PATH}")
                    raise FileNotFoundError(
                        f"Please download credentials.json from Google Cloud Console "
                        f"and place it at: {CREDENTIALS_PATH}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                logger.info("Completed OAuth flow")

            # Save credentials for next run
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
            logger.info("Saved credentials")

        return build('gmail', 'v1', credentials=creds)

    def load_processed_ids(self):
        """Load previously processed email IDs"""
        processed_file = VAULT_PATH / 'Logs' / 'processed_emails.txt'
        if processed_file.exists():
            ids = set(processed_file.read_text().splitlines())
            logger.info(f"Loaded {len(ids)} processed email IDs")
            return ids
        return set()

    def save_processed_id(self, email_id):
        """Save processed email ID to avoid duplicates"""
        processed_file = VAULT_PATH / 'Logs' / 'processed_emails.txt'
        with open(processed_file, 'a') as f:
            f.write(f"{email_id}\n")
        self.processed_ids.add(email_id)

    def check_for_new_emails(self):
        """Check for new important emails"""
        try:
            # Query for unread and important emails
            # You can modify the query as needed
            query = os.getenv('GMAIL_QUERY', 'is:unread is:important')

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                logger.debug("No new emails found")
                return

            logger.info(f"Found {len(messages)} unread emails")

            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    self.process_email(msg['id'])

        except Exception as e:
            logger.error(f"Error checking emails: {e}")

    def process_email(self, email_id):
        """Process individual email and create action file"""
        try:
            # Fetch email details
            msg = self.service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {h['name']: h['value']
                      for h in msg['payload']['headers']}

            sender = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', '')

            # Extract email body snippet
            snippet = msg.get('snippet', '')

            # Determine priority based on keywords
            priority_keywords = ['urgent', 'asap', 'important', 'critical']
            priority = 'high' if any(kw in subject.lower() or kw in snippet.lower()
                                    for kw in priority_keywords) else 'normal'

            # Create action file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"EMAIL_{email_id}_{timestamp}.md"
            filepath = NEEDS_ACTION / filename

            content = f"""---
type: email
email_id: {email_id}
from: {sender}
subject: {subject}
received: {date}
priority: {priority}
status: pending
processed_at: {datetime.now().isoformat()}
---

## Email Content
{snippet}

## Suggested Actions
- [ ] Read full email
- [ ] Draft response
- [ ] Forward if needed
- [ ] Archive after processing

## Instructions for Claude
Please read this email and determine the appropriate action. If a response is needed, draft it and place in /Pending_Approval for human review.

## Email Details
- **From:** {sender}
- **Subject:** {subject}
- **Priority:** {priority}
- **Date:** {date}
"""

            filepath.write_text(content, encoding='utf-8')
            self.save_processed_id(email_id)

            logger.info(f"✓ Created action file for: {subject[:50]}...")

        except Exception as e:
            logger.error(f"Error processing email {email_id}: {e}")

    def run(self):
        """Main loop - continuously monitor Gmail"""
        logger.info("=" * 60)
        logger.info("Gmail Watcher started")
        logger.info(f"Vault path: {VAULT_PATH}")
        logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
        logger.info(f"Query: {os.getenv('GMAIL_QUERY', 'is:unread is:important')}")
        logger.info("=" * 60)

        while True:
            try:
                logger.info("Checking for new emails...")
                self.check_for_new_emails()
                logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                logger.info("Gmail Watcher stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                logger.info("Waiting 60 seconds before retry...")
                time.sleep(60)


if __name__ == '__main__':
    try:
        watcher = GmailWatcher()
        watcher.run()
    except Exception as e:
        logger.error(f"Failed to start Gmail Watcher: {e}")
        print("\n" + "=" * 60)
        print("SETUP REQUIRED:")
        print("1. Create .env file with OBSIDIAN_VAULT_PATH")
        print("2. Download credentials.json from Google Cloud Console")
        print("3. Set GMAIL_CREDENTIALS_PATH in .env")
        print("=" * 60)
