# Email MCP Server

MCP server for email operations using Gmail SMTP.

## Features

- Send plain text emails
- Send HTML emails
- CC and BCC support
- Email configuration verification
- Error handling and logging

## Installation

```bash
cd mcp-servers/email-mcp
npm install
```

## Configuration

Add to your `.env` file:

```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## Usage

### With Claude Code

Add to your Claude Code MCP configuration (`~/.config/claude-code/mcp.json`):

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["D:\\Giaic\\spec-kit-plus\\Hackhton_0\\AI Employee\\Bronze\\mcp-servers\\email-mcp\\index.js"],
      "env": {
        "EMAIL_ADDRESS": "your-email@gmail.com",
        "EMAIL_PASSWORD": "your-app-password"
      }
    }
  }
}
```

### Available Tools

#### 1. send_email
Send a plain text email.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body (plain text)
- `cc` (optional): CC addresses (comma-separated)
- `bcc` (optional): BCC addresses (comma-separated)

**Example:**
```javascript
{
  "to": "recipient@example.com",
  "subject": "Test Email",
  "body": "This is a test email from MCP server."
}
```

#### 2. send_email_html
Send an HTML email.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `html` (required): Email body (HTML)
- `cc` (optional): CC addresses (comma-separated)

**Example:**
```javascript
{
  "to": "recipient@example.com",
  "subject": "HTML Email",
  "html": "<h1>Hello</h1><p>This is an HTML email.</p>"
}
```

#### 3. verify_email_config
Verify email configuration and test SMTP connection.

**Parameters:** None

**Example:**
```javascript
{}
```

## Testing

```bash
# Test the server
node index.js

# Send test email
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"send_email","arguments":{"to":"test@example.com","subject":"Test","body":"Test message"}}}' | node index.js
```

## Error Handling

The server returns structured error responses:

```json
{
  "success": false,
  "error": "Error message",
  "tool": "tool_name"
}
```

## Logging

Logs are written to stderr for MCP protocol compliance.

## Security

- Never commit `.env` file
- Use Gmail App Passwords (not regular password)
- Rotate credentials regularly
- Monitor for suspicious activity
