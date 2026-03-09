# Skill: Email Processor

**Version**: 1.0
**Category**: email
**Tier**: Bronze

## Description

Reads email markdown files from /Needs_Action, analyzes content, extracts key information, and suggests appropriate actions.

## Capabilities

- Parse email frontmatter (YAML)
- Extract sender, subject, timestamp, priority
- Analyze email content for urgency and intent
- Detect action items and deadlines
- Suggest next steps

## Inputs

**Required**:
- Email file path: Path to EMAIL_*.md file in /Needs_Action

**Optional**:
- Context: Additional context from Company_Handbook.md

## Outputs

- Analysis summary: Key points from email
- Suggested actions: List of recommended next steps
- Priority assessment: Urgency level

## Configuration

```yaml
max_suggestions: 5
urgency_keywords:
  - urgent
  - asap
  - critical
  - deadline
```

## Dependencies

- Read tool (to read email files)
- YAML parser (to parse frontmatter)

## Usage Example

```
Read EMAIL_20260219_103000_a1b2c3d4.md from /Needs_Action and analyze it.
```
