# Log Manager Skill

Maintain comprehensive audit logs and error tracking.

## Metadata
- **Tier**: Gold
- **Priority**: High
- **Dependencies**: None (used by all skills)
- **Triggers**: All significant actions and errors

## Capabilities
- Log all AI actions with timestamps
- Track success/failure of operations
- Record approval workflows
- Maintain daily log files
- Generate error reports
- Track system health metrics
- Create audit trails
- Support debugging

## Usage
```bash
/log-manager --action={log|report|archive}
```

## Expected Input
- Action description
- Status (success/failure)
- Metadata (user, timestamp, etc.)
- Error details (if applicable)

## Expected Output
- Log entries in /Logs folder
- Daily log files
- Error reports
- Weekly summaries
- Archived logs
