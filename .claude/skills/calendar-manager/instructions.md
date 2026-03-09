# Calendar Manager - Implementation Instructions

## Overview
This skill manages calendar events by creating, updating, and syncing appointments from emails, messages, and tasks using Google Calendar MCP server.

---

## Step-by-Step Process

### 1. Event Detection

**Scan for calendar-related content in:**
- `/Needs_Action/EMAIL_*.md` - Look for meeting requests
- `/Needs_Action/WHATSAPP_*.md` - Look for scheduling keywords
- `/Plans/*.md` - Look for tasks requiring scheduled time

**Keywords to detect:**
- Meeting: "meet", "meeting", "call", "discussion", "sync"
- Scheduling: "schedule", "book", "arrange", "set up"
- Time indicators: "tomorrow", "next week", "Monday", "2 PM", "at 3"
- Duration: "30 minutes", "1 hour", "quick call"

### 2. Extract Event Details

**Required information:**
```yaml
event:
  title: [Extract from context]
  date: [Parse date/time]
  time: [Parse time, convert to 24-hour]
  duration: [Default 60 minutes if not specified]
  participants: [Extract email addresses]
  location: [Physical or virtual - Zoom, Meet, etc.]
  description: [Context from original message]
```

**Date/Time Parsing Examples:**
- "tomorrow at 2 PM" → [Current date + 1 day, 14:00]
- "next Tuesday" → [Next Tuesday's date, default 10:00]
- "Feb 20 at 3:30 PM" → [2026-02-20, 15:30]
- "in 2 hours" → [Current time + 2 hours]

### 3. Check for Conflicts

**Conflict detection:**
```python
# Pseudo-code
existing_events = get_calendar_events(date)
for event in existing_events:
    if time_overlap(new_event, event):
        create_conflict_alert()
```

**If conflict detected:**
1. Create file in `/Pending_Approval/CALENDAR_CONFLICT_[id].md`
2. Include both events with details
3. Provide options: reschedule, decline, or override
4. Wait for human decision

### 4. Create Calendar Event

**Using Google Calendar MCP:**
```javascript
// MCP call structure
{
  "action": "create_event",
  "calendar_id": "primary",
  "event": {
    "summary": "Meeting with Client A",
    "start": {
      "dateTime": "2026-02-20T14:00:00",
      "timeZone": "America/New_York"
    },
    "end": {
      "dateTime": "2026-02-20T15:00:00",
      "timeZone": "America/New_York"
    },
    "attendees": [
      {"email": "client@example.com"}
    ],
    "description": "Discuss project requirements",
    "reminders": {
      "useDefault": false,
      "overrides": [
        {"method": "popup", "minutes": 15}
      ]
    }
  }
}
```

### 5. Send Confirmation

**Create confirmation file:**
```markdown
# /Done/CALENDAR_EVENT_[id].md

---
type: calendar_event
action: created
event_id: [Google Calendar Event ID]
created: [timestamp]
status: confirmed
---

## Event Created

**Title:** Meeting with Client A
**Date:** February 20, 2026
**Time:** 2:00 PM - 3:00 PM
**Participants:** client@example.com
**Location:** Zoom (link in calendar)

## Actions Taken
- ✅ Calendar event created
- ✅ Invitation sent to participants
- ✅ Reminder set (15 minutes before)
- ✅ Dashboard updated

## Calendar Link
[View in Google Calendar](https://calendar.google.com/event?eid=[event_id])
```

### 6. Update Dashboard

**Add to Dashboard.md:**
```markdown
## 📅 Upcoming Events

### Today
- 2:00 PM - Meeting with Client A (1 hour)

### This Week
- Feb 20, 2:00 PM - Meeting with Client A
- Feb 22, 10:00 AM - Team Sync
- Feb 23, 3:00 PM - Project Review
```

---

## Event Types & Handling

### 1. One-time Meeting
- Extract date, time, duration
- Create single event
- Send invitation

### 2. Recurring Meeting
- Detect recurrence pattern ("every Monday", "weekly", "monthly")
- Set recurrence rule in calendar
- Confirm with human before creating series

### 3. All-day Event
- Detect keywords: "all day", "full day", "entire day"
- Create all-day event (no specific time)
- No reminder needed

### 4. Tentative/Pending
- Keywords: "maybe", "tentative", "possibly"
- Create event but mark as tentative
- Require confirmation before finalizing

---

## Reminder Management

### Reminder Schedule
```yaml
reminders:
  - 1 day before: For important meetings
  - 1 hour before: For all meetings
  - 15 minutes before: Final reminder
```

### Reminder Format
```markdown
🔔 **Meeting Reminder**

**In 15 minutes:** Meeting with Client A
**Time:** 2:00 PM - 3:00 PM
**Location:** Zoom
**Preparation:** Review project proposal

[Join Meeting](https://zoom.us/j/123456789)
```

---

## Conflict Resolution

### When Conflict Detected

**Create approval request:**
```markdown
# /Pending_Approval/CALENDAR_CONFLICT_[id].md

---
type: calendar_conflict
priority: high
created: [timestamp]
---

## ⚠️ Scheduling Conflict Detected

### New Meeting Request
- **Title:** Meeting with Client B
- **Time:** Feb 20, 2:00 PM - 3:00 PM
- **Requested by:** client-b@example.com

### Existing Event
- **Title:** Meeting with Client A
- **Time:** Feb 20, 2:00 PM - 3:00 PM
- **Already confirmed**

## Options

### Option 1: Reschedule New Meeting
- Suggest: Feb 20, 4:00 PM - 5:00 PM
- Suggest: Feb 21, 2:00 PM - 3:00 PM

### Option 2: Reschedule Existing Meeting
- Contact Client A to reschedule

### Option 3: Decline New Meeting
- Send polite decline with alternative times

## To Decide
Move this file to:
- `/Approved/` with chosen option number
- `/Rejected/` to decline new meeting
```

---

## Integration with Other Skills

### Email Processor
- Receives meeting requests from emails
- Passes to Calendar Manager for event creation
- Calendar Manager sends confirmation back

### WhatsApp Responder
- Detects scheduling messages
- Extracts meeting details
- Hands off to Calendar Manager

### Dashboard Updater
- Calendar Manager provides upcoming events
- Dashboard displays next 7 days of events
- Highlights today's meetings

### Notification Manager
- Calendar Manager triggers reminders
- Notification Manager sends alerts
- Multiple channels (email, dashboard, logs)

---

## Error Handling

### Invalid Date/Time
```markdown
**Error:** Could not parse date/time from: "sometime next week"

**Action Required:**
Please specify exact date and time for the meeting.

**Suggestions:**
- Next Monday at 2 PM
- February 25 at 10:00 AM
- Tomorrow at 3:30 PM
```

### Calendar API Failure
```markdown
**Error:** Google Calendar API unavailable

**Action Taken:**
- Event queued for retry
- Will attempt again in 5 minutes
- You will be notified when created

**Queued Event:**
- Title: Meeting with Client A
- Time: Feb 20, 2:00 PM
```

### Missing Participant Email
```markdown
**Warning:** No email address found for participant

**Action Required:**
Please provide email address for: "John from Marketing"

**Event Details:**
- Title: Marketing Sync
- Time: Feb 20, 3:00 PM
- Missing: Participant email
```

---

## Security & Privacy

### Approval Requirements
- **Always require approval for:**
  - Creating events with external participants
  - Modifying existing events
  - Deleting any event
  - Creating recurring events
  - All-day events

- **Can auto-execute:**
  - Reading calendar
  - Checking for conflicts
  - Generating reminders
  - Updating dashboard

### Privacy Rules
- Never share calendar details publicly
- Respect participant privacy
- Don't log sensitive meeting content
- Encrypt calendar credentials

---

## Testing Checklist

- [ ] Create simple one-time meeting
- [ ] Create recurring weekly meeting
- [ ] Detect and handle scheduling conflict
- [ ] Send meeting reminder
- [ ] Update existing event
- [ ] Handle invalid date/time gracefully
- [ ] Integrate with Email Processor
- [ ] Integrate with Dashboard Updater
- [ ] Test Google Calendar MCP connection
- [ ] Verify approval workflow

---

## Configuration File

**Location:** `.env`

```bash
# Google Calendar Configuration
GOOGLE_CALENDAR_CREDENTIALS=/path/to/calendar-credentials.json
GOOGLE_CALENDAR_ID=primary
CALENDAR_TIMEZONE=America/New_York

# Default Settings
DEFAULT_MEETING_DURATION=60  # minutes
DEFAULT_REMINDER_TIME=15     # minutes before
WORKING_HOURS_START=09:00
WORKING_HOURS_END=18:00

# Approval Settings
AUTO_APPROVE_INTERNAL=false
AUTO_APPROVE_RECURRING=false
REQUIRE_APPROVAL_EXTERNAL=true
```

---

## Success Metrics

- Events created successfully: 95%+
- Conflicts detected: 100%
- Reminders sent on time: 100%
- API errors handled gracefully: 100%
- User approval rate: Track and optimize

---

**Last Updated:** 2026-02-17
**Version:** 1.0
**Tier:** Silver
