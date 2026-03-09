# Skill: Task Manager

**Version**: 1.0
**Category**: task
**Tier**: Bronze

## Description

Creates task files in /Plans folder from email analysis, tracks task completion, and updates task status.

## Capabilities

- Create Plan.md files with checkboxes
- Extract actionable items from emails
- Track task completion status
- Update task lists

## Inputs

**Required**:
- Email analysis: Output from Email Processor
- Task list: Suggested actions

**Optional**:
- Due date: Deadline for tasks
- Priority: Task urgency

## Outputs

- Plan.md file: Task list with checkboxes
- Task summary: Overview of created tasks

## Configuration

```yaml
plan_template: |
  # Plan: {title}
  
  **Created**: {date}
  **Source**: {email_file}
  
  ## Tasks
  
  {task_list}
```

## Dependencies

- Write tool (to create Plan.md)
- Email Processor output

## Usage Example

```
Create a Plan.md file in /Plans for the email analysis with 3 tasks.
```
