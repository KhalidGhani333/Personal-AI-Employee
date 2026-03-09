---
name: calendar-manager
description: Create, update, and manage calendar events from emails, messages, and tasks
version: 1.0
tier: silver
---

# Calendar Manager Skill

## Purpose
Manage calendar events by creating, updating, and syncing appointments from various sources (emails, WhatsApp messages, tasks). Integrates with Google Calendar via MCP server.

## Capabilities
- Create calendar events from email requests
- Update existing events
- Send meeting reminders
- Handle scheduling conflicts
- Sync with Google Calendar
- Generate meeting summaries
- Schedule recurring events
- Send calendar invitations

## Inputs
- Email files with meeting requests
- WhatsApp messages with scheduling keywords
- Task files requiring scheduled time
- Manual event creation requests

## Outputs
- Calendar events created in Google Calendar
- Event confirmation files in /Done
- Conflict alerts in /Pending_Approval
- Meeting reminder notifications
- Updated Dashboard.md with upcoming events

## Dependencies
- Google Calendar MCP server
- Calendar credentials in .env
- Access to /Needs_Action folder
- Dashboard.md for updates

## Usage Examples

### Example 1: Create Event from Email
```
Input: Email with "Let's meet next Tuesday at 2 PM"
Process: Extract date, time, participants
Output: Calendar event created, confirmation sent
```

### Example 2: Handle Scheduling Conflict
```
Input: Meeting request conflicts with existing event
Process: Detect conflict, create approval request
Output: File in /Pending_Approval with options
```

### Example 3: Send Meeting Reminder
```
Input: Event scheduled for tomorrow
Process: Check upcoming events, generate reminder
Output: Reminder notification sent
```

## Configuration
```yaml
calendar_settings:
  default_duration: 60  # minutes
  reminder_time: 15     # minutes before
  working_hours:
    start: "09:00"
    end: "18:00"
  timezone: "America/New_York"
  auto_accept: false    # Require approval for all events
```

## Error Handling
- Invalid date/time: Request clarification
- Scheduling conflict: Create approval request
- Calendar API failure: Queue event for retry
- Missing participant info: Flag for human review

## Security
- All calendar modifications require approval
- Never delete events without explicit permission
- Maintain audit log of all calendar actions
- Respect privacy settings

## Integration Points
- Google Calendar API via MCP
- Email Processor skill (for meeting requests)
- WhatsApp Responder skill (for scheduling messages)
- Dashboard Updater skill (for upcoming events display)
- Notification Manager skill (for reminders)
