# WhatsApp Responder - Detailed Instructions

## Objective
Process WhatsApp messages, understand context, and draft appropriate responses while maintaining professional communication.

## Message Processing Workflow

### 1. Read Message File
```markdown
Input: /Needs_Action/WHATSAPP_{contact}_{timestamp}.md

---
type: whatsapp
contact: {contact_name}
received: {timestamp}
priority: high|normal
keywords_matched: {keywords}
---

## Message Content
{message_text}
```

### 2. Analyze Message Context

**Identify Message Type:**
- **Query**: Customer asking questions
- **Request**: Client requesting service/invoice/information
- **Complaint**: Issue or problem reported
- **Urgent**: Time-sensitive matter
- **Casual**: General conversation

**Extract Key Information:**
- What is being asked?
- Is there a deadline?
- Does it require action?
- Is it related to existing project/invoice?

### 3. Check Company Handbook

```
Read: Company_Handbook.md
Find: Communication guidelines
Apply: Response templates and tone
```

### 4. Draft Response

**Professional Response Template:**
```
Hi {contact_name},

{acknowledgment}

{main_response}

{action_items}

{closing}

Best regards,
{your_name}
```

**Examples:**

**For Invoice Request:**
```
Hi {contact_name},

Thank you for reaching out!

I'll prepare your invoice right away and send it to you within the next hour.

Please let me know if you need anything else.

Best regards,
{your_name}
```

**For Query:**
```
Hi {contact_name},

Great question!

{answer_to_query}

Let me know if you need any clarification.

Best regards,
{your_name}
```

**For Complaint:**
```
Hi {contact_name},

I sincerely apologize for the inconvenience.

I'm looking into this immediately and will get back to you with a solution within {timeframe}.

Thank you for your patience.

Best regards,
{your_name}
```

### 5. Create Approval Request

```markdown
---
type: whatsapp_reply
contact: {contact_name}
original_message: {message_id}
priority: high|normal
requires_approval: true
---

## Original Message
{original_message_text}

## Drafted Response
{response_text}

## Action Items
- [ ] {action_1}
- [ ] {action_2}

## To Approve
Move to /Approved folder

## To Edit
Edit response and then move to /Approved
```

### 6. Create Follow-up Tasks

**If action required:**
```
- Invoice request → Create task: "Generate invoice for {contact}"
- Meeting request → Create task: "Schedule meeting with {contact}"
- Information request → Create task: "Send {information} to {contact}"
```

### 7. Track Conversation

```markdown
Create: /Conversations/{contact_name}.md

---
contact: {contact_name}
last_message: {timestamp}
message_count: {count}
---

## Conversation History

### {date} - {time}
**From {contact}:**
{message}

**Response:**
{response}
---
```

## Response Guidelines

**Tone:**
- Professional but friendly
- Clear and concise
- Empathetic when needed
- Action-oriented

**Timing:**
- Urgent messages: Respond within 1 hour
- Normal messages: Respond within 24 hours
- After hours: Acknowledge and set expectations

**Do's:**
- ✅ Acknowledge receipt immediately
- ✅ Set clear expectations
- ✅ Provide specific timelines
- ✅ Offer alternatives when needed
- ✅ Thank them for their patience

**Don'ts:**
- ❌ Make promises you can't keep
- ❌ Use overly technical language
- ❌ Ignore urgent messages
- ❌ Send generic responses
- ❌ Forget to follow up

## Keyword Detection

**Urgent Keywords:**
- urgent, asap, immediately, emergency
- payment, invoice, overdue
- problem, issue, not working
- deadline, today, now

**Action Keywords:**
- send, provide, share, give
- schedule, book, arrange
- fix, resolve, help
- update, change, modify

## Auto-Response Scenarios

**Out of Office:**
```
Thank you for your message. I'm currently away and will respond when I return on {date}.

For urgent matters, please contact {backup_contact}.
```

**After Hours:**
```
Thank you for your message. I've received it and will respond during business hours (9 AM - 6 PM).

For urgent matters, please call {phone_number}.
```

## Integration Points

- **Approval Handler**: All responses require approval
- **Task Manager**: Create follow-up tasks
- **Invoice Generator**: Trigger invoice creation
- **Dashboard Updater**: Update message stats
- **Log Manager**: Log all conversations

## Success Criteria
- All messages acknowledged within 1 hour
- Appropriate responses drafted
- No messages missed
- Professional tone maintained
- Follow-up tasks created
