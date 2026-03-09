#!/usr/bin/env python3
"""
Business MCP Server
Production-ready MCP server for external business actions
Provides email, LinkedIn posting, and business activity logging
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from playwright.async_api import async_playwright
from dotenv import load_dotenv

# MCP SDK imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('business-mcp')

# Configuration
VAULT_PATH = Path(os.getenv('VAULT_PATH', 'AI_Employee_Vault'))
BUSINESS_LOG = VAULT_PATH / 'Logs' / 'business.log'

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# LinkedIn configuration
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


class BusinessMCPServer:
    """Business MCP Server implementation"""

    def __init__(self):
        self.server = Server("business-mcp")
        self._setup_handlers()

        # Ensure log directory exists
        BUSINESS_LOG.parent.mkdir(parents=True, exist_ok=True)

    def _setup_handlers(self):
        """Setup MCP request handlers"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available business tools"""
            return [
                Tool(
                    name="send_email",
                    description="Send an email via Gmail SMTP",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "string",
                                "description": "Recipient email address"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Email subject line"
                            },
                            "body": {
                                "type": "string",
                                "description": "Email body content (plain text)"
                            },
                            "cc": {
                                "type": "string",
                                "description": "CC email addresses (comma-separated)"
                            },
                            "bcc": {
                                "type": "string",
                                "description": "BCC email addresses (comma-separated)"
                            }
                        },
                        "required": ["to", "subject", "body"]
                    }
                ),
                Tool(
                    name="post_linkedin",
                    description="Create a post on LinkedIn",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content to post on LinkedIn"
                            },
                            "headless": {
                                "type": "boolean",
                                "description": "Run browser in headless mode (default: true)"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                Tool(
                    name="log_activity",
                    description="Log business activity to vault/Logs/business.log",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Activity message to log"
                            },
                            "level": {
                                "type": "string",
                                "enum": ["info", "warning", "error", "success"],
                                "description": "Log level (default: info)"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Additional metadata to include"
                            }
                        },
                        "required": ["message"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls"""
            try:
                if name == "send_email":
                    result = await self._send_email(arguments)
                elif name == "post_linkedin":
                    result = await self._post_linkedin(arguments)
                elif name == "log_activity":
                    result = await self._log_activity(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]

            except Exception as e:
                logger.error(f"Error executing {name}: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": str(e),
                        "tool": name
                    }, indent=2)
                )]

    async def _send_email(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send email via Gmail SMTP"""
        to = args.get("to")
        subject = args.get("subject")
        body = args.get("body")
        cc = args.get("cc")
        bcc = args.get("bcc")

        # Validate configuration
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            raise ValueError("Email credentials not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD in .env")

        # Validate inputs
        if not to or not subject or not body:
            raise ValueError("Missing required fields: to, subject, body")

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = to
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = cc
            if bcc:
                msg['Bcc'] = bcc

            # Attach body
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                recipients = [to]
                if cc:
                    recipients.extend([addr.strip() for addr in cc.split(',')])
                if bcc:
                    recipients.extend([addr.strip() for addr in bcc.split(',')])

                server.sendmail(EMAIL_ADDRESS, recipients, msg.as_string())

            # Log activity
            await self._log_activity({
                "message": f"Email sent to {to}: {subject}",
                "level": "success",
                "metadata": {"to": to, "subject": subject}
            })

            return {
                "success": True,
                "action": "send_email",
                "to": to,
                "subject": subject,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            await self._log_activity({
                "message": f"Email send failed: {str(e)}",
                "level": "error",
                "metadata": {"to": to, "subject": subject, "error": str(e)}
            })
            raise

    async def _post_linkedin(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Post content to LinkedIn"""
        content = args.get("content")
        headless = args.get("headless", True)

        # Validate configuration
        if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
            raise ValueError("LinkedIn credentials not configured. Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env")

        # Validate input
        if not content:
            raise ValueError("Missing required field: content")

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                context = await browser.new_context()
                page = await context.new_page()

                try:
                    # Navigate to LinkedIn
                    await page.goto('https://www.linkedin.com/login', timeout=30000)

                    # Login
                    await page.fill('input[name="session_key"]', LINKEDIN_EMAIL)
                    await page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
                    await page.click('button[type="submit"]')

                    # Wait for feed to load
                    await page.wait_for_selector('[aria-label*="Start a post"]', timeout=15000)

                    # Click "Start a post"
                    await page.click('[aria-label*="Start a post"]')

                    # Wait for editor
                    await page.wait_for_selector('.ql-editor', timeout=10000)

                    # Type content
                    await page.fill('.ql-editor', content)

                    # Wait a moment for content to register
                    await page.wait_for_timeout(1000)

                    # Click Post button
                    await page.click('button[aria-label*="Post"]')

                    # Wait for confirmation
                    await page.wait_for_timeout(3000)

                    # Log activity
                    await self._log_activity({
                        "message": f"LinkedIn post created: {content[:50]}...",
                        "level": "success",
                        "metadata": {"content_length": len(content)}
                    })

                    return {
                        "success": True,
                        "action": "post_linkedin",
                        "platform": "linkedin",
                        "content": content,
                        "timestamp": datetime.now().isoformat()
                    }

                finally:
                    await browser.close()

        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {e}")
            await self._log_activity({
                "message": f"LinkedIn post failed: {str(e)}",
                "level": "error",
                "metadata": {"error": str(e)}
            })
            raise

    async def _log_activity(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Log business activity"""
        message = args.get("message")
        level = args.get("level", "info")
        metadata = args.get("metadata", {})

        if not message:
            raise ValueError("Missing required field: message")

        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "metadata": metadata
        }

        # Write to log file
        try:
            with open(BUSINESS_LOG, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')

            # Also log to stderr for debugging
            log_method = getattr(logger, level if level != "success" else "info")
            log_method(f"Business Activity: {message}")

            return {
                "success": True,
                "action": "log_activity",
                "message": message,
                "level": level,
                "log_file": str(BUSINESS_LOG),
                "timestamp": log_entry["timestamp"]
            }

        except Exception as e:
            logger.error(f"Failed to write to business log: {e}")
            raise

    async def run(self):
        """Run the MCP server"""
        logger.info("Starting Business MCP Server")
        logger.info(f"Business log: {BUSINESS_LOG}")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = BusinessMCPServer()
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
