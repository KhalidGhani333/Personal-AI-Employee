# Business MCP Server

Production-ready MCP server for external business actions.

## Features

- **Send Email**: Send emails via Gmail SMTP with CC/BCC support
- **LinkedIn Posting**: Automated LinkedIn post creation using browser automation
- **Activity Logging**: Centralized business activity logging to vault

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js (for MCP integration)
- Gmail account with App Password
- LinkedIn account

### Setup

1. **Install Python dependencies:**

```bash
cd mcp/business_mcp
pip install -r requirements.txt
```

2. **Install Playwright browsers:**

```bash
playwright install chromium
```

3. **Configure environment variables:**

Create or update `.env` file in project root:

```env
# Email Configuration
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LinkedIn Configuration
LINKEDIN_EMAIL=your-linkedin@email.com
LINKEDIN_PASSWORD=your-linkedin-password

# Vault Path (optional)
VAULT_PATH=AI_Employee_Vault
```

4. **Add to MCP configuration:**

Add to `.claude/mcp-config.json`:

```json
{
  "mcpServers": {
    "business": {
      "command": "python",
      "args": ["D:\\path\\to\\mcp\\business_mcp\\server.py"]
    }
  }
}
```

## Usage

### Tool: send_email

Send an email via Gmail SMTP.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject line
- `body` (required): Email body content (plain text)
- `cc` (optional): CC email addresses (comma-separated)
- `bcc` (optional): BCC email addresses (comma-separated)

**Example:**

```json
{
  "to": "client@example.com",
  "subject": "Project Update",
  "body": "Hello,\n\nHere is the latest update on your project...",
  "cc": "manager@example.com"
}
```

**Response:**

```json
{
  "success": true,
  "action": "send_email",
  "to": "client@example.com",
  "subject": "Project Update",
  "timestamp": "2026-02-25T13:00:00.000000"
}
```

### Tool: post_linkedin

Create a post on LinkedIn.

**Parameters:**
- `content` (required): Content to post on LinkedIn
- `headless` (optional): Run browser in headless mode (default: true)

**Example:**

```json
{
  "content": "Excited to announce our new product launch! 🚀\n\n#ProductLaunch #Innovation",
  "headless": true
}
```

**Response:**

```json
{
  "success": true,
  "action": "post_linkedin",
  "platform": "linkedin",
  "content": "Excited to announce...",
  "timestamp": "2026-02-25T13:00:00.000000"
}
```

### Tool: log_activity

Log business activity to vault/Logs/business.log.

**Parameters:**
- `message` (required): Activity message to log
- `level` (optional): Log level - "info", "warning", "error", "success" (default: "info")
- `metadata` (optional): Additional metadata object

**Example:**

```json
{
  "message": "Client meeting scheduled for next week",
  "level": "info",
  "metadata": {
    "client": "Acme Corp",
    "date": "2026-03-01"
  }
}
```

**Response:**

```json
{
  "success": true,
  "action": "log_activity",
  "message": "Client meeting scheduled for next week",
  "level": "info",
  "log_file": "AI_Employee_Vault/Logs/business.log",
  "timestamp": "2026-02-25T13:00:00.000000"
}
```

## Architecture

### Components

1. **BusinessMCPServer**: Main server class
   - Handles MCP protocol communication
   - Manages tool registration and execution
   - Provides error handling and logging

2. **Email Handler**: SMTP email sending
   - Uses Python's smtplib
   - Supports HTML and plain text
   - CC/BCC support
   - Automatic activity logging

3. **LinkedIn Handler**: Browser automation
   - Uses Playwright for automation
   - Headless and headed modes
   - Automatic login and posting
   - Error recovery

4. **Activity Logger**: Centralized logging
   - JSON-formatted logs
   - Timestamped entries
   - Metadata support
   - Multiple log levels

### Error Handling

- All operations include try-catch blocks
- Errors are logged to stderr
- Failed operations return structured error responses
- Activity logging continues even if primary operation fails

### Security

- Credentials stored in environment variables
- No credentials in code or logs
- SMTP uses TLS encryption
- Browser automation uses secure HTTPS

## Logging

All business activities are logged to:

```
AI_Employee_Vault/Logs/business.log
```

Log format:

```json
{
  "timestamp": "2026-02-25T13:00:00.000000",
  "level": "info",
  "message": "Email sent to client@example.com: Project Update",
  "metadata": {
    "to": "client@example.com",
    "subject": "Project Update"
  }
}
```

## Testing

### Test Email Sending

```bash
python -c "
import asyncio
from server import BusinessMCPServer

async def test():
    server = BusinessMCPServer()
    result = await server._send_email({
        'to': 'test@example.com',
        'subject': 'Test Email',
        'body': 'This is a test email.'
    })
    print(result)

asyncio.run(test())
"
```

### Test Activity Logging

```bash
python -c "
import asyncio
from server import BusinessMCPServer

async def test():
    server = BusinessMCPServer()
    result = await server._log_activity({
        'message': 'Test log entry',
        'level': 'info'
    })
    print(result)

asyncio.run(test())
"
```

## Troubleshooting

### Email Issues

**Problem**: "Email credentials not configured"
- **Solution**: Set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file

**Problem**: "Authentication failed"
- **Solution**: Use Gmail App Password, not regular password
- Enable 2FA on Gmail account
- Generate App Password at: https://myaccount.google.com/apppasswords

**Problem**: "SMTP connection failed"
- **Solution**: Check SMTP_SERVER and SMTP_PORT settings
- Verify firewall allows outbound port 587

### LinkedIn Issues

**Problem**: "LinkedIn credentials not configured"
- **Solution**: Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file

**Problem**: "Selector not found"
- **Solution**: LinkedIn UI may have changed
- Try running with headless=false to debug
- Check for CAPTCHA or security challenges

**Problem**: "Browser launch failed"
- **Solution**: Install Playwright browsers: `playwright install chromium`

### Logging Issues

**Problem**: "Permission denied" writing to log file
- **Solution**: Ensure Logs directory exists and is writable
- Check VAULT_PATH environment variable

## Production Deployment

### Recommendations

1. **Use App Passwords**: Never use plain passwords for email
2. **Rate Limiting**: Implement rate limits for LinkedIn posting
3. **Monitoring**: Monitor business.log for errors
4. **Backup**: Regularly backup business.log
5. **Rotation**: Implement log rotation for large files
6. **Secrets Management**: Use proper secrets management in production

### Performance

- Email sending: ~1-3 seconds per email
- LinkedIn posting: ~10-15 seconds per post
- Activity logging: <100ms per entry

### Scalability

- Supports concurrent operations via async/await
- No state stored in memory
- Stateless design allows horizontal scaling

## License

MIT License

## Support

For issues or questions:
1. Check troubleshooting section
2. Review business.log for error details
3. Enable debug logging: Set LOG_LEVEL=DEBUG in .env

## Version

**Version**: 1.0.0
**Last Updated**: 2026-02-25
**Python**: 3.10+
**MCP SDK**: 0.9.0+
