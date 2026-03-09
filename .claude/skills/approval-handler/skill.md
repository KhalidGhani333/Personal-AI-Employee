# Approval Handler Skill

Handle human-in-the-loop approval workflows for sensitive actions.

## Metadata
- **Tier**: Bronze
- **Priority**: Critical
- **Dependencies**: Log Manager
- **Triggers**: Sensitive actions requiring approval

## Capabilities
- Monitor /Pending_Approval folder
- Detect approved/rejected actions
- Execute approved actions
- Log all approval decisions
- Timeout expired approvals

## Usage
```bash
/approval-handler
```

## Expected Input
- Approval request files in /Pending_Approval
- Approved files moved to /Approved
- Rejected files moved to /Rejected

## Expected Output
- Executed approved actions
- Logged approval decisions
- Moved processed files to /Done
- Notifications for pending approvals
