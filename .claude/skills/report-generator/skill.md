---
name: report-generator
description: Generate summaries, reports, and analytics from tasks, emails, files, and activities
version: 1.0
tier: silver
---

# Report Generator Skill

## Purpose
Automatically generate comprehensive reports and summaries from various data sources including completed tasks, email activities, file processing, and system logs. Provides insights and analytics for decision-making.

## Capabilities
- Generate daily activity summaries
- Create weekly performance reports
- Produce task completion reports
- Generate email activity summaries
- Create file processing reports
- Generate custom reports on demand
- Export reports to markdown/PDF
- Analyze trends and patterns
- Provide actionable insights

## Report Types

### 1. Daily Summary Report
- Tasks completed today
- Emails processed
- Files handled
- Approvals given
- Key activities

### 2. Weekly Performance Report
- Week-over-week metrics
- Task completion rate
- Response time analysis
- Bottleneck identification
- Goal progress

### 3. Task Completion Report
- Completed vs pending tasks
- Average completion time
- Priority distribution
- Overdue tasks
- Success rate

### 4. Email Activity Report
- Emails received/sent
- Response time metrics
- Top senders/recipients
- Email categories
- Unread count

### 5. File Processing Report
- Files processed by type
- Processing success rate
- Storage usage
- File categories
- Error summary

### 6. Custom Reports
- User-defined criteria
- Flexible date ranges
- Multiple data sources
- Custom formatting

## Inputs
- `/Done/*.md` - Completed tasks
- `/Logs/*.json` - Activity logs
- `/Needs_Action/*.md` - Pending items
- `/Plans/*.md` - Active plans
- Dashboard.md - Current metrics
- Business_Goals.md - Goal tracking

## Outputs
- Daily reports in `/Briefings/Daily/`
- Weekly reports in `/Briefings/Weekly/`
- Custom reports in `/Briefings/Custom/`
- Updated Dashboard.md with insights
- Trend analysis files
- Actionable recommendations

## Dependencies
- Access to all vault folders
- Log files in JSON format
- Dashboard.md for metrics
- Business_Goals.md for targets

## Usage Examples

### Example 1: Generate Daily Summary
```
Input: "Generate daily summary for today"
Process: Scan /Done, /Logs, analyze activities
Output: Daily_Summary_2026-02-17.md in /Briefings/Daily/
```

### Example 2: Weekly Performance Report
```
Input: "Create weekly report for last 7 days"
Process: Aggregate metrics, calculate trends
Output: Weekly_Report_2026-W07.md in /Briefings/Weekly/
```

### Example 3: Task Completion Analysis
```
Input: "Analyze task completion for February"
Process: Review all tasks, calculate metrics
Output: Task_Analysis_2026-02.md with insights
```

## Configuration
```yaml
report_settings:
  daily_report_time: "18:00"  # 6 PM
  weekly_report_day: "Sunday"
  weekly_report_time: "20:00"  # 8 PM
  include_charts: true
  export_format: "markdown"
  retention_days: 90
  auto_generate: true
```

## Metrics Tracked
- Task completion rate
- Average response time
- Email processing volume
- File handling count
- Approval turnaround time
- Goal progress percentage
- System uptime
- Error rate

## Report Format
```markdown
# [Report Type] - [Date]

## Executive Summary
[High-level overview]

## Key Metrics
[Quantitative data]

## Highlights
[Notable achievements]

## Issues & Concerns
[Problems identified]

## Recommendations
[Actionable suggestions]

## Detailed Analysis
[In-depth breakdown]

## Appendix
[Supporting data]
```

## Error Handling
- Missing data: Note gaps in report
- Corrupted logs: Skip and flag for review
- Calculation errors: Use fallback values
- Export failures: Retry with different format

## Security
- Reports contain sensitive data - store securely
- Redact confidential information in shared reports
- Maintain audit trail of report generation
- Access control for report folders

## Integration Points
- Dashboard Updater skill (for metrics)
- Log Manager skill (for log analysis)
- Business Auditor skill (for CEO briefing)
- Email Processor skill (for email stats)
- Task Manager skill (for task metrics)
