# Skill: Dashboard Updater

**Version**: 1.0
**Category**: dashboard
**Tier**: Bronze

## Description

Updates Dashboard.md with recent email processing activity, maintains activity log, and shows last 10 events.

## Capabilities

- Append activity entries to Dashboard.md
- Format timestamps consistently
- Maintain last 10 events (prune old entries)
- Show email subject and sender

## Inputs

**Required**:
- Activity type: email_detected | email_processed | task_created
- Timestamp: When activity occurred
- Details: Activity-specific information

**Optional**:
- Email subject: Subject line
- Sender: Email sender

## Outputs

- Updated Dashboard.md: With new activity entry

## Configuration

```yaml
max_activities: 10
timestamp_format: "YYYY-MM-DD HH:MM"
activity_section: "## Recent Activity"
```

## Dependencies

- Read tool (to read current Dashboard.md)
- Edit tool (to update Dashboard.md)

## Usage Example

```
Update Dashboard.md with email_processed activity for email from client@example.com.
```
