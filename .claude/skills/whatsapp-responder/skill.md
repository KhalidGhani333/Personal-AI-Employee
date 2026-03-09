# WhatsApp Responder Skill

Handle WhatsApp messages and draft appropriate responses.

## Metadata
- **Tier**: Silver
- **Priority**: High
- **Dependencies**: Approval Handler, Task Manager
- **Triggers**: WhatsApp message files in /Needs_Action

## Capabilities
- Read urgent WhatsApp messages
- Analyze message context
- Draft appropriate responses
- Flag for human review
- Send approved responses
- Track conversation history

## Usage
```bash
/whatsapp-responder
```

## Expected Input
- WhatsApp message files from watcher
- Contact information
- Message priority level

## Expected Output
- Response drafts in /Pending_Approval
- Tasks created for follow-ups
- Conversation logs
- Dashboard updates
