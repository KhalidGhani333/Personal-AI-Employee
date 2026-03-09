# Report Generator - Implementation Instructions

## Overview
This skill generates comprehensive reports and summaries from tasks, emails, files, and system activities. It provides insights, analytics, and actionable recommendations.

---

## Step-by-Step Process

### 1. Data Collection

**Sources to scan:**
```yaml
data_sources:
  completed_tasks: /Done/*.md
  activity_logs: /Logs/*.json
  pending_items: /Needs_Action/*.md
  active_plans: /Plans/*.md
  current_metrics: Dashboard.md
  business_goals: Business_Goals.md
  email_records: /Done/EMAIL_*.md
  file_records: /Done/FILE_*.md
```

**Data extraction:**
```python
# Pseudo-code for data collection
def collect_data(date_range):
    tasks = read_files('/Done/*.md', date_range)
    logs = read_json_files('/Logs/*.json', date_range)
    metrics = parse_dashboard()
    goals = parse_business_goals()

    return {
        'tasks': tasks,
        'logs': logs,
        'metrics': metrics,
        'goals': goals
    }
```

### 2. Data Analysis

**Calculate key metrics:**
```python
# Task metrics
total_tasks = count(completed_tasks)
completion_rate = completed / (completed + pending) * 100
avg_completion_time = sum(completion_times) / count(tasks)
overdue_count = count(tasks where due_date < completion_date)

# Email metrics
emails_received = count(EMAIL_* in Needs_Action)
emails_sent = count(EMAIL_* in Done with action=sent)
avg_response_time = calculate_average_response_time()

# File metrics
files_processed = count(FILE_* in Done)
processing_success_rate = successful / total * 100

# System metrics
uptime_percentage = (total_time - downtime) / total_time * 100
error_rate = errors / total_operations * 100
```

---

## Report Types & Templates

### 1. Daily Summary Report

**Template:**
```markdown
# Daily Summary - [Date]

**Generated:** [Timestamp]
**Period:** [Date] 00:00 - 23:59

---

## 📊 Quick Stats

| Metric | Count | Change |
|--------|-------|--------|
| Tasks Completed | [X] | [+/-Y from yesterday] |
| Emails Processed | [X] | [+/-Y from yesterday] |
| Files Handled | [X] | [+/-Y from yesterday] |
| Approvals Given | [X] | [+/-Y from yesterday] |

---

## ✅ Completed Today

### High Priority (P0/P1)
- [Task 1] - Completed at [time]
- [Task 2] - Completed at [time]

### Regular Priority (P2/P3)
- [Task 3] - Completed at [time]
- [Task 4] - Completed at [time]

---

## 📧 Email Activity

- **Received:** [X] emails
- **Sent:** [X] emails
- **Average Response Time:** [X] hours
- **Pending Replies:** [X] emails

**Top Senders:**
1. [Sender 1] - [X] emails
2. [Sender 2] - [X] emails

---

## 📁 File Processing

- **Files Processed:** [X]
- **Success Rate:** [X]%
- **File Types:** PDF ([X]), DOCX ([X]), CSV ([X])

---

## ⚠️ Issues & Alerts

- [Issue 1 if any]
- [Issue 2 if any]

---

## 🎯 Tomorrow's Focus

- [Priority 1]
- [Priority 2]
- [Priority 3]

---

*Report generated automatically by AI Employee*
```

**Generation logic:**
```python
def generate_daily_summary(date):
    # Collect data for the day
    data = collect_data(date_range=date)

    # Calculate metrics
    metrics = calculate_metrics(data)

    # Identify highlights
    highlights = identify_top_items(data, limit=5)

    # Detect issues
    issues = detect_issues(data)

    # Generate recommendations
    recommendations = generate_recommendations(data, issues)

    # Create report
    report = format_daily_report(metrics, highlights, issues, recommendations)

    # Save to file
    save_report(report, f'/Briefings/Daily/Daily_Summary_{date}.md')

    return report
```

---

### 2. Weekly Performance Report

**Template:**
```markdown
# Weekly Performance Report - Week [W]

**Generated:** [Timestamp]
**Period:** [Start Date] - [End Date]

---

## 📈 Executive Summary

[2-3 sentence overview of the week's performance]

---

## 🎯 Goal Progress

| Goal | Target | Actual | Progress | Status |
|------|--------|--------|----------|--------|
| Weekly Revenue | $[X] | $[Y] | [Z]% | [🟢/🟡/🔴] |
| Tasks Completed | [X] | [Y] | [Z]% | [🟢/🟡/🔴] |
| Client Satisfaction | [X] | [Y] | [Z]% | [🟢/🟡/🔴] |

---

## 📊 Key Metrics

### Task Performance
- **Total Completed:** [X] tasks
- **Completion Rate:** [X]%
- **Average Time:** [X] hours
- **Overdue:** [X] tasks

### Communication
- **Emails Processed:** [X]
- **Response Time:** [X] hours (avg)
- **WhatsApp Messages:** [X]
- **Social Posts:** [X]

### Productivity
- **Working Hours:** [X] hours
- **Efficiency Score:** [X]%
- **Automation Rate:** [X]%

---

## 🏆 Highlights

### Top Achievements
1. [Achievement 1]
2. [Achievement 2]
3. [Achievement 3]

### Completed Projects
- [Project 1] - [Value/Impact]
- [Project 2] - [Value/Impact]

---

## ⚠️ Bottlenecks & Issues

| Issue | Impact | Status | Action |
|-------|--------|--------|--------|
| [Issue 1] | High | Open | [Action] |
| [Issue 2] | Medium | Resolved | [Action] |

---

## 📉 Areas for Improvement

1. **[Area 1]**
   - Current: [X]
   - Target: [Y]
   - Gap: [Z]
   - Recommendation: [Action]

2. **[Area 2]**
   - Current: [X]
   - Target: [Y]
   - Gap: [Z]
   - Recommendation: [Action]

---

## 📅 Next Week's Priorities

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---

## 📊 Trend Analysis

### Week-over-Week Comparison

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Tasks | [X] | [Y] | [+/-Z%] |
| Revenue | $[X] | $[Y] | [+/-Z%] |
| Efficiency | [X]% | [Y]% | [+/-Z%] |

---

*Report generated automatically by AI Employee*
```

---

### 3. Task Completion Report

**Template:**
```markdown
# Task Completion Report - [Period]

**Generated:** [Timestamp]
**Period:** [Start] - [End]

---

## 📊 Overview

- **Total Tasks:** [X]
- **Completed:** [X] ([Y]%)
- **In Progress:** [X] ([Y]%)
- **Pending:** [X] ([Y]%)
- **Overdue:** [X] ([Y]%)

---

## 📈 Completion Metrics

### By Priority
| Priority | Total | Completed | Rate |
|----------|-------|-----------|------|
| P0 (Critical) | [X] | [Y] | [Z]% |
| P1 (High) | [X] | [Y] | [Z]% |
| P2 (Medium) | [X] | [Y] | [Z]% |
| P3 (Low) | [X] | [Y] | [Z]% |

### By Category
| Category | Total | Completed | Rate |
|----------|-------|-----------|------|
| Email | [X] | [Y] | [Z]% |
| Files | [X] | [Y] | [Z]% |
| Projects | [X] | [Y] | [Z]% |
| Admin | [X] | [Y] | [Z]% |

---

## ⏱️ Time Analysis

- **Average Completion Time:** [X] hours
- **Fastest Task:** [X] minutes
- **Slowest Task:** [X] days
- **Median Time:** [X] hours

### Time Distribution
- < 1 hour: [X] tasks
- 1-4 hours: [X] tasks
- 4-8 hours: [X] tasks
- > 8 hours: [X] tasks

---

## 🎯 Success Rate

- **On-Time Completion:** [X]%
- **Early Completion:** [X]%
- **Late Completion:** [X]%

---

## 🔴 Overdue Tasks

| Task | Due Date | Days Overdue | Priority |
|------|----------|--------------|----------|
| [Task 1] | [Date] | [X] | [P] |
| [Task 2] | [Date] | [X] | [P] |

---

## 💡 Insights & Recommendations

1. **[Insight 1]**
   - Observation: [Details]
   - Recommendation: [Action]

2. **[Insight 2]**
   - Observation: [Details]
   - Recommendation: [Action]

---

*Report generated automatically by AI Employee*
```

---

### 4. Email Activity Report

**Template:**
```markdown
# Email Activity Report - [Period]

**Generated:** [Timestamp]
**Period:** [Start] - [End]

---

## 📧 Volume Metrics

- **Emails Received:** [X]
- **Emails Sent:** [X]
- **Emails Processed:** [X]
- **Pending Replies:** [X]

---

## ⏱️ Response Time Analysis

- **Average Response Time:** [X] hours
- **Fastest Response:** [X] minutes
- **Slowest Response:** [X] days
- **Within 24h:** [X]% of emails

### Response Time Distribution
- < 1 hour: [X] emails
- 1-4 hours: [X] emails
- 4-24 hours: [X] emails
- > 24 hours: [X] emails

---

## 👥 Top Correspondents

### Most Emails Received From
1. [Sender 1] - [X] emails
2. [Sender 2] - [X] emails
3. [Sender 3] - [X] emails

### Most Emails Sent To
1. [Recipient 1] - [X] emails
2. [Recipient 2] - [X] emails
3. [Recipient 3] - [X] emails

---

## 📂 Email Categories

| Category | Count | Percentage |
|----------|-------|------------|
| Client Communication | [X] | [Y]% |
| Internal | [X] | [Y]% |
| Marketing | [X] | [Y]% |
| Support | [X] | [Y]% |
| Other | [X] | [Y]% |

---

## 🎯 Performance Metrics

- **Response Rate:** [X]%
- **Resolution Rate:** [X]%
- **Approval Rate:** [X]%
- **Auto-Processed:** [X]%

---

## 💡 Insights

1. **Peak Email Times:** [Time range]
2. **Busiest Day:** [Day]
3. **Most Common Topics:** [Topics]

---

*Report generated automatically by AI Employee*
```

---

## Scheduling & Automation

### Daily Report Schedule
```yaml
daily_report:
  time: "18:00"  # 6 PM
  timezone: "America/New_York"
  enabled: true
  recipients: ["user@example.com"]
  format: "markdown"
```

**Cron job (Linux/Mac):**
```bash
# Add to crontab
0 18 * * * cd /path/to/project && python generate_daily_report.py
```

**Task Scheduler (Windows):**
```powershell
# Create scheduled task
schtasks /create /tn "DailyReport" /tr "python generate_daily_report.py" /sc daily /st 18:00
```

### Weekly Report Schedule
```yaml
weekly_report:
  day: "Sunday"
  time: "20:00"  # 8 PM
  timezone: "America/New_York"
  enabled: true
  recipients: ["user@example.com"]
  format: "markdown"
```

---

## Data Aggregation Logic

### Collect Task Data
```python
def collect_task_data(start_date, end_date):
    tasks = []
    done_folder = Path('/Done')

    for file in done_folder.glob('*.md'):
        # Parse frontmatter
        metadata = parse_frontmatter(file)

        # Check date range
        if start_date <= metadata['completed'] <= end_date:
            tasks.append({
                'title': metadata['title'],
                'completed': metadata['completed'],
                'priority': metadata['priority'],
                'category': metadata['type'],
                'duration': calculate_duration(metadata)
            })

    return tasks
```

### Calculate Metrics
```python
def calculate_task_metrics(tasks):
    total = len(tasks)

    # By priority
    by_priority = {
        'P0': len([t for t in tasks if t['priority'] == 'P0']),
        'P1': len([t for t in tasks if t['priority'] == 'P1']),
        'P2': len([t for t in tasks if t['priority'] == 'P2']),
        'P3': len([t for t in tasks if t['priority'] == 'P3'])
    }

    # Average time
    durations = [t['duration'] for t in tasks if t['duration']]
    avg_duration = sum(durations) / len(durations) if durations else 0

    return {
        'total': total,
        'by_priority': by_priority,
        'avg_duration': avg_duration
    }
```

---

## Integration with Other Skills

### Dashboard Updater
```python
# Report Generator provides metrics
metrics = generate_metrics()

# Dashboard Updater displays them
update_dashboard(metrics)
```

### Business Auditor
```python
# Report Generator provides weekly data
weekly_data = generate_weekly_report()

# Business Auditor uses for CEO briefing
ceo_briefing = create_ceo_briefing(weekly_data)
```

### Log Manager
```python
# Log Manager provides log data
logs = get_logs(date_range)

# Report Generator analyzes logs
analysis = analyze_logs(logs)
```

---

## Error Handling

### Missing Data
```markdown
**Note:** Some data unavailable for this period.

**Missing:**
- Email logs for [Date]
- Task completion data for [Date]

**Impact:** Metrics may be incomplete.
**Action:** Manual review recommended.
```

### Calculation Errors
```python
def safe_calculate(numerator, denominator):
    try:
        return (numerator / denominator) * 100
    except ZeroDivisionError:
        return 0
    except Exception as e:
        log_error(f"Calculation error: {e}")
        return None
```

### Export Failures
```python
def export_report(report, format='markdown'):
    try:
        if format == 'markdown':
            save_markdown(report)
        elif format == 'pdf':
            save_pdf(report)
    except Exception as e:
        log_error(f"Export failed: {e}")
        # Fallback to markdown
        save_markdown(report)
```

---

## Testing Checklist

- [ ] Generate daily summary report
- [ ] Generate weekly performance report
- [ ] Generate task completion report
- [ ] Generate email activity report
- [ ] Calculate all metrics correctly
- [ ] Handle missing data gracefully
- [ ] Export to markdown format
- [ ] Schedule automatic generation
- [ ] Integrate with Dashboard Updater
- [ ] Integrate with Business Auditor
- [ ] Test with empty data sets
- [ ] Test with large data sets
- [ ] Verify date range filtering
- [ ] Check report formatting
- [ ] Validate all calculations

---

## Configuration File

**Location:** `.env`

```bash
# Report Generator Configuration
REPORT_OUTPUT_DIR=/path/to/AI_Employee_Vault/Briefings
REPORT_TIMEZONE=America/New_York
REPORT_DATE_FORMAT=YYYY-MM-DD

# Daily Report
DAILY_REPORT_ENABLED=true
DAILY_REPORT_TIME=18:00
DAILY_REPORT_FORMAT=markdown

# Weekly Report
WEEKLY_REPORT_ENABLED=true
WEEKLY_REPORT_DAY=Sunday
WEEKLY_REPORT_TIME=20:00
WEEKLY_REPORT_FORMAT=markdown

# Retention
REPORT_RETENTION_DAYS=90

# Notifications
REPORT_NOTIFY_EMAIL=user@example.com
REPORT_NOTIFY_ON_GENERATION=true
```

---

## Success Metrics

- Reports generated on time: 100%
- Data accuracy: 95%+
- Calculation errors: < 1%
- Export success rate: 99%+
- User satisfaction with insights: Track feedback

---

**Last Updated:** 2026-02-17
**Version:** 1.0
**Tier:** Silver
