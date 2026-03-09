# Business Auditor Skill

Generate weekly CEO briefings with business insights and recommendations.

## Metadata
- **Tier**: Gold
- **Priority**: High
- **Dependencies**: Dashboard Updater, Log Manager
- **Triggers**: Weekly schedule (Sunday night)

## Capabilities
- Analyze bank transactions
- Review completed tasks
- Calculate revenue and expenses
- Identify bottlenecks
- Generate CEO briefing
- Provide proactive suggestions
- Track business metrics

## Usage
```bash
/business-auditor --period={week|month|quarter}
```

## Expected Input
- Bank transaction data
- Completed tasks from /Done
- Business goals from Business_Goals.md
- Previous briefings for comparison

## Expected Output
- CEO briefing in /Briefings folder
- Business insights
- Proactive recommendations
- Metric trends
- Action items
