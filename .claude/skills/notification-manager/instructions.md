# Notification Manager - Detailed Instructions

## Objective
Deliver timely, relevant notifications to users through appropriate channels based on priority and preferences.

## Notification Channels

### 1. Desktop Notifications
**Platform Support:**
- Windows: Windows Notification System
- macOS: Notification Center
- Linux: libnotify

**Implementation:**
```python
from plyer import notification

def send_desktop_notification(title: str, message: str, timeout: int = 10):
    """Send desktop notification"""
    notification.notify(
        title=title,
        message=message,
        app_name='AI Employee',
        timeout=timeout
    )
```

**Use Cases:**
- Urgent approvals needed
- Critical errors
- Important task completions
- Time-sensitive alerts

### 2. Email Notifications
**Implementation:**
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(
    to: str,
    subject: str,
    body: str,
    priority: str = "normal"
):
    """Send email notification"""

    msg = MIMEMultipart()
    msg['From'] = "ai-employee@yourdomain.com"
    msg['To'] = to
    msg['Subject'] = subject

    if priority == "high":
        msg['X-Priority'] = '1'
        msg['Importance'] = 'high'

    msg.attach(MIMEText(body, 'html'))

    # Send via SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
```

**Email Templates:**

**Approval Request:**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .container { font-family: Arial, sans-serif; max-width: 600px; }
        .header { background: #4CAF50; color: white; padding: 20px; }
        .content { padding: 20px; }
        .button { background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; }
        .urgent { background: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>⚠️ Approval Required</h2>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            <p>An action requires your approval:</p>
            <p><strong>{action_description}</strong></p>
            <p>Details:</p>
            <ul>
                <li>Type: {action_type}</li>
                <li>Amount: ${amount}</li>
                <li>Requested: {timestamp}</li>
            </ul>
            <p>
                <a href="{approval_link}" class="button">Review & Approve</a>
            </p>
            <p>This request will expire in {hours} hours.</p>
        </div>
    </div>
</body>
</html>
```

**Error Alert:**
```html
<div class="container">
    <div class="header" style="background: #f44336;">
        <h2>🚨 System Error</h2>
    </div>
    <div class="content">
        <p>An error occurred in your AI Employee:</p>
        <p><strong>{error_message}</strong></p>
        <p>Details:</p>
        <ul>
            <li>Component: {component}</li>
            <li>Time: {timestamp}</li>
            <li>Severity: {level}</li>
        </ul>
        <p>Action Required: {action_needed}</p>
    </div>
</div>
```

### 3. Slack Integration
**Setup:**
```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

def send_slack_notification(channel: str, message: str, priority: str = "normal"):
    """Send Slack notification"""

    # Color based on priority
    color = {
        "high": "#f44336",
        "normal": "#4CAF50",
        "low": "#2196F3"
    }[priority]

    try:
        response = slack_client.chat_postMessage(
            channel=channel,
            attachments=[{
                "color": color,
                "title": "AI Employee Notification",
                "text": message,
                "footer": "AI Employee",
                "ts": int(time.time())
            }]
        )
    except SlackApiError as e:
        log_error(f"Slack notification failed: {e}")
```

**Slack Message Formats:**

**Approval Request:**
```python
{
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "⚠️ Approval Required"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{action_description}*\n\nAmount: ${amount}\nType: {action_type}"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Approve"},
                    "style": "primary",
                    "value": "approve"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Reject"},
                    "style": "danger",
                    "value": "reject"
                }
            ]
        }
    ]
}
```

### 4. Discord Integration
```python
import discord
from discord import Webhook
import aiohttp

async def send_discord_notification(webhook_url: str, message: str, priority: str = "normal"):
    """Send Discord notification"""

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)

        embed = discord.Embed(
            title="AI Employee Notification",
            description=message,
            color=0xff0000 if priority == "high" else 0x00ff00
        )

        await webhook.send(embed=embed)
```

## Notification Rules

### Priority Levels

**High Priority (Immediate):**
- Critical errors
- Payment approvals
- Security alerts
- System failures
- Urgent client messages

**Channels:** Desktop + Email + Slack (if configured)
**Timing:** Immediate
**Escalation:** After 15 minutes if not acknowledged

**Normal Priority (Standard):**
- Task completions
- Email responses needed
- Invoice sent confirmations
- Regular approvals

**Channels:** Desktop + Email (after 1 hour)
**Timing:** Immediate desktop, delayed email
**Escalation:** After 4 hours

**Low Priority (Digest):**
- Daily summaries
- Non-urgent updates
- Informational messages
- Statistics

**Channels:** Email digest
**Timing:** Once daily (8 AM)
**Escalation:** None

## Notification Preferences

**User Preferences File:**
```json
{
  "user_id": "user@example.com",
  "preferences": {
    "desktop_enabled": true,
    "email_enabled": true,
    "slack_enabled": true,
    "discord_enabled": false,
    "quiet_hours": {
      "enabled": true,
      "start": "22:00",
      "end": "08:00",
      "timezone": "America/New_York"
    },
    "priority_routing": {
      "high": ["desktop", "email", "slack"],
      "normal": ["desktop", "email"],
      "low": ["email"]
    },
    "digest_time": "08:00",
    "escalation_enabled": true,
    "escalation_contact": "backup@example.com"
  }
}
```

## Quiet Hours

**Implementation:**
```python
from datetime import datetime, time
import pytz

def is_quiet_hours(preferences: dict) -> bool:
    """Check if current time is in quiet hours"""

    if not preferences.get('quiet_hours', {}).get('enabled'):
        return False

    tz = pytz.timezone(preferences['quiet_hours']['timezone'])
    now = datetime.now(tz).time()

    start = time.fromisoformat(preferences['quiet_hours']['start'])
    end = time.fromisoformat(preferences['quiet_hours']['end'])

    if start < end:
        return start <= now <= end
    else:  # Crosses midnight
        return now >= start or now <= end

def send_notification_with_quiet_hours(message: str, priority: str, preferences: dict):
    """Send notification respecting quiet hours"""

    if priority == "high":
        # High priority ignores quiet hours
        send_notification(message, priority, preferences)
    elif is_quiet_hours(preferences):
        # Queue for later
        queue_notification(message, priority, preferences)
    else:
        send_notification(message, priority, preferences)
```

## Escalation Workflow

**Escalation Rules:**
```python
def check_escalation(notification_id: str):
    """Check if notification needs escalation"""

    notification = get_notification(notification_id)

    if notification['priority'] != 'high':
        return  # Only escalate high priority

    time_since_sent = datetime.now() - notification['sent_at']

    if time_since_sent > timedelta(minutes=15) and not notification['acknowledged']:
        # Escalate
        escalate_notification(notification)

def escalate_notification(notification: dict):
    """Escalate unacknowledged notification"""

    # Send to backup contact
    send_email_notification(
        to=notification['escalation_contact'],
        subject=f"ESCALATED: {notification['title']}",
        body=f"This notification was not acknowledged:\n\n{notification['message']}",
        priority="high"
    )

    # Log escalation
    log_action(
        level="warning",
        action_type="notification_escalated",
        description=f"Escalated notification: {notification['title']}"
    )
```

## Digest Mode

**Daily Digest:**
```python
def generate_daily_digest():
    """Generate daily digest of low-priority notifications"""

    # Collect low-priority notifications from last 24 hours
    notifications = get_notifications(
        priority="low",
        since=datetime.now() - timedelta(days=1)
    )

    if not notifications:
        return

    # Group by category
    grouped = {}
    for notif in notifications:
        category = notif['category']
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(notif)

    # Generate digest email
    digest_html = generate_digest_html(grouped)

    send_email_notification(
        to=user_email,
        subject=f"Daily Digest - {datetime.now().strftime('%B %d, %Y')}",
        body=digest_html,
        priority="low"
    )
```

**Digest Template:**
```html
<h2>Daily Digest - {date}</h2>

<h3>📊 Summary</h3>
<ul>
    <li>Tasks Completed: {task_count}</li>
    <li>Emails Processed: {email_count}</li>
    <li>Files Processed: {file_count}</li>
</ul>

<h3>✅ Completed Tasks</h3>
<ul>
    {task_list}
</ul>

<h3>📧 Email Activity</h3>
<ul>
    {email_list}
</ul>

<h3>📁 Files Processed</h3>
<ul>
    {file_list}
</ul>
```

## Notification Tracking

**Track Delivery:**
```python
notification_log = {
    "id": "notif_12345",
    "type": "approval_request",
    "priority": "high",
    "sent_at": "2026-02-06T10:30:00Z",
    "channels": ["desktop", "email"],
    "delivery_status": {
        "desktop": "delivered",
        "email": "sent"
    },
    "acknowledged": False,
    "acknowledged_at": None,
    "escalated": False
}
```

## Integration Points

- **Approval Handler**: Notify on pending approvals
- **Log Manager**: Notify on critical errors
- **Business Auditor**: Send weekly briefing
- **Task Manager**: Notify on task deadlines
- **Email Processor**: Notify on urgent emails

## Success Criteria
- Notifications delivered within 30 seconds
- No missed critical notifications
- Quiet hours respected
- Escalation works correctly
- User preferences honored
- Delivery tracked accurately
