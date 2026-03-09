# CEO Briefing Skill

Generate comprehensive weekly executive reports automatically.

## Usage

```
/ceo-briefing
```

Generates a complete CEO briefing report with:
- Tasks completed this week
- Email activity
- Social media posts
- Pending approvals
- Income/expense summary
- System health status
- Recommendations

## Output

**File:** `AI_Employee_Vault/Reports/CEO_Weekly.md`

The report includes:

### Executive Summary
- Tasks completed count
- Emails sent count
- Social media posts count
- Pending approvals count
- Weekly revenue and expenses
- System status

### Tasks & Productivity
- Completed tasks (with dates)
- Pending tasks list
- Task completion metrics

### Communications
- Email activity (sent/received)
- Recent emails sent
- Social media posts (LinkedIn/Twitter)
- Recent posts

### Financial Summary
- Weekly income
- Weekly expenses
- Net balance
- Transaction count

### Approvals Required
- List of pending approvals
- Approval queue status

### System Health
- System status
- Uptime hours
- Error count
- Warning count
- Issues requiring attention

### Recommendations
- Actionable insights
- Priority items
- Suggested actions

## Automatic Scheduling

The CEO briefing runs automatically every Monday at 9:00 AM via the scheduler.

To manually trigger:
```bash
python scripts/ceo_briefing.py
```

## Features

- **Comprehensive Analysis**: Analyzes all system activities
- **Financial Integration**: Pulls data from accounting system
- **Task Tracking**: Monitors task completion and pending items
- **Communication Metrics**: Tracks emails and social media
- **System Health**: Monitors errors and system status
- **Actionable Insights**: Provides recommendations
- **Auto-Generated**: Runs weekly automatically
- **Markdown Format**: Easy to read and share

## Data Sources

The briefing aggregates data from:
- `AI_Employee_Vault/Done/` - Completed tasks
- `AI_Employee_Vault/Needs_Action/` - Pending tasks
- `AI_Employee_Vault/Needs_Approval/` - Approval queue
- `AI_Employee_Vault/Accounting/Current_Month.md` - Financial data
- `Logs/email_log.json` - Email activity
- `Logs/social_log.json` - Social media activity
- `Logs/business.log` - Business activities
- `Logs/error_recovery.log` - System errors
- `Logs/ai_employee.lock` - System uptime

## Example Output

```markdown
# CEO Weekly Briefing
## Week of Feb 23 - Mar 01, 2026

**Generated:** February 25, 2026 at 02:30 PM

---

## Executive Summary

- **Tasks Completed:** 12
- **Emails Sent:** 8
- **Social Media Posts:** 3
- **Pending Approvals:** 2
- **Weekly Revenue:** $11,000.00
- **Weekly Expenses:** $1,650.00
- **Net Income:** $9,350.00
- **System Status:** Healthy

---

## Tasks & Productivity

### Completed This Week (12)
- client_completion_email (2026-02-21)
- client_followup (2026-02-22)
- demo_email_task (2026-02-24)
...

### Pending Tasks (5)
- Plan_daily_standup_20260222_010359
- Plan_demo_meeting_task_20260224_165026
...

---

## Communications

### Email Activity
- **Sent:** 8 emails
- **Received:** 15 emails

**Recent Emails Sent:**
- To: client@example.com - Project Update (2026-02-25)
...

### Social Media
- **LinkedIn Posts:** 2
- **Twitter Posts:** 1
- **Total Posts:** 3

---

## Financial Summary

### This Week
- **Income:** $11,000.00
- **Expenses:** $1,650.00
- **Net Balance:** $9,350.00
- **Transactions:** 5

---

## Approvals Required

**Pending Approvals:** 2

- approval_20260221_135139
- approval_20260222_015225

---

## System Health

- **Status:** Healthy
- **Uptime:** 24.5 hours
- **Errors:** 0
- **Warnings:** 2

---

## Recommendations

- Operations running smoothly. Continue current practices.
```

## Integration

The CEO briefing integrates with:
- **Accounting Manager**: Financial data
- **Task System**: Task completion tracking
- **Email System**: Communication metrics
- **Social Media**: Post tracking
- **System Logs**: Health monitoring

## Scheduling

Configured to run automatically via `scripts/scheduler.py`:
- **Frequency:** Weekly (every Monday)
- **Time:** 9:00 AM
- **Output:** `AI_Employee_Vault/Reports/CEO_Weekly.md`

## Manual Execution

```bash
# Generate briefing now
python scripts/ceo_briefing.py

# View latest briefing
cat AI_Employee_Vault/Reports/CEO_Weekly.md
```

## Notes

- Briefing covers the current week (Monday-Sunday)
- Historical briefings are saved with timestamps
- Latest briefing is always available as `CEO_Weekly.md`
- All metrics are calculated automatically
- Recommendations are generated based on data analysis
