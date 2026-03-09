"""
Gmail Send - Production Email Automation
=========================================
Sends real emails via Gmail SMTP using app passwords.
"""

import os
import sys
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to, subject, body, cc=None, bcc=None):
    """
    Send email via Gmail SMTP.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body text
        cc: CC recipients (comma-separated string)
        bcc: BCC recipients (comma-separated string)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Get credentials from environment
        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_PASSWORD')

        if not email_address or not email_password:
            print("[ERROR] Missing EMAIL_ADDRESS or EMAIL_PASSWORD in environment")
            print("Set these in .env file or environment variables")
            return False

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = to
        msg['Subject'] = subject

        # Add CC and BCC if provided
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc

        # Attach body
        msg.attach(MIMEText(body, 'plain'))

        # Build recipient list
        recipients = [to]
        if cc:
            recipients.extend([addr.strip() for addr in cc.split(',')])
        if bcc:
            recipients.extend([addr.strip() for addr in bcc.split(',')])

        # Connect and send
        print(f"[INFO] Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            print(f"[INFO] Authenticating as {email_address}...")
            server.login(email_address, email_password)
            print(f"[INFO] Sending email to {to}...")
            server.send_message(msg)

        print(f"[SUCCESS] Email sent successfully to {to}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Authentication failed")
        print("Make sure you're using a Gmail App Password, not your regular password")
        print("Generate one at: https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Send email via Gmail SMTP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple email
  python send_email.py --to "user@example.com" --subject "Hello" --body "Test message"

  # With CC and BCC
  python send_email.py --to "user@example.com" --subject "Update" --body "Content" --cc "manager@example.com" --bcc "archive@example.com"
        """
    )

    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body text')
    parser.add_argument('--cc', help='CC recipients (comma-separated)')
    parser.add_argument('--bcc', help='BCC recipients (comma-separated)')

    args = parser.parse_args()

    # Send email
    success = send_email(
        to=args.to,
        subject=args.subject,
        body=args.body,
        cc=args.cc,
        bcc=args.bcc
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
