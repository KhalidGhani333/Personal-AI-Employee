# Approval Handler - Detailed Instructions

## Objective
Manage human-in-the-loop approval workflow for sensitive actions like payments, emails to new contacts, and social media posts.

## Approval Request Format

```markdown
---
type: approval_request
action: send_email|make_payment|post_social|delete_file
priority: high|normal
created: {ISO_timestamp}
expires: {ISO_timestamp}
status: pending
---

## Action Details
{detailed_description_of_action}

## To Approve
Move this file to /Approved folder

## To Reject
Move this file to /Rejected folder

## Auto-Reject After
{expiry_time}
```

## Workflow

### 1. Monitor Pending Approvals
```
Check: Every 5 minutes
Location: /Pending_Approval folder
Actions:
  - List all approval request files
  - Check expiry timestamps
  - Flag expired requests
  - Count pending approvals
```

### 2. Detect Approved Actions
```
When: File appears in /Approved folder
Process:
  - Read approval file
  - Validate action is still valid
  - Execute the approved action
  - Log approval + execution
  - Move to /Done/Approved
```

### 3. Detect Rejected Actions
```
When: File appears in /Rejected folder
Process:
  - Read rejection file
  - Log rejection decision
  - Cancel the action
  - Notify relevant skill
  - Move to /Done/Rejected
```

### 4. Handle Expired Approvals
```
When: Current time > expires timestamp
Process:
  - Auto-reject the request
  - Log as "expired"
  - Move to /Done/Expired
  - Notify user of missed approval
```

## Action Execution

### Send Email
```
1. Read email details from approval file
2. Use Email MCP to send
3. Log sent email
4. Update Dashboard
```

### Make Payment
```
1. Read payment details
2. Use Payment MCP (or browser automation)
3. Log transaction
4. Update accounting records
```

### Post Social Media
```
1. Read post content
2. Use Social Media MCP
3. Log post
4. Update Dashboard
```

## Security Rules

**Always Require Approval For:**
- Payments > $50
- Emails to new contacts
- Social media posts
- File deletions
- Database changes
- API calls to external services

**Never Auto-Approve:**
- Financial transactions
- Legal documents
- Contract signing
- Account deletions

## Notification Strategy

**High Priority Approvals:**
- Desktop notification immediately
- Email after 15 minutes
- Escalate after 1 hour

**Normal Priority:**
- Desktop notification
- Email after 1 hour
- Escalate after 24 hours

## Integration Points

- **Email Processor**: Requests approval for sensitive emails
- **Invoice Generator**: Requests approval for sending invoices
- **Social Media Manager**: Requests approval for posts
- **Log Manager**: Logs all approval decisions
- **Notification Skill**: Sends approval notifications

## Success Criteria
- No unauthorized actions executed
- All approvals logged
- Expired approvals handled gracefully
- User notified of pending approvals
