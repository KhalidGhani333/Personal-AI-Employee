# Email Processor - Implementation Instructions

## Overview

This skill reads email markdown files from /Needs_Action, analyzes content, and suggests appropriate actions.

## Step-by-Step Process

### Step 1: Read Email File

**What to do**: Read the email markdown file from /Needs_Action

**How to do it**: Use Read tool with absolute path to the email file

**Example**:
```
Read: AI_Employee_Vault/Needs_Action/EMAIL_20260219_103000_a1b2c3d4.md
```

### Step 2: Parse Frontmatter

**What to do**: Extract YAML frontmatter metadata

**Required Fields**:
- from: Sender email address
- subject: Email subject line
- received: Timestamp (ISO 8601)
- priority: Urgency level (high/medium/low)
- message_id: Unique identifier

**How to parse**: Read content between `---` delimiters at file start

### Step 3: Analyze Content

**What to do**: Read email body and identify key information

**Look for**:
- Action requests (verbs: send, create, update, review, complete)
- Deadlines (dates, time expressions like "by EOD", "tomorrow")
- Questions (question marks, interrogative words)
- Urgency indicators (urgent, asap, critical, important)

### Step 4: Generate Suggestions

**What to do**: Create list of suggested actions based on analysis

**Format**:
```markdown
- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3
```

**Examples**:
- [ ] Reply to sender with status update
- [ ] Set deadline reminder for [date]
- [ ] Forward to [person/team]
- [ ] Create task in project management system
- [ ] Schedule meeting to discuss

## Output Format

```markdown
## Email Analysis

**From**: sender@example.com
**Subject**: Project Update Required
**Priority**: High
**Received**: 2026-02-19 10:30 AM

**Key Points**:
- Requesting Q1 report by end of day
- Board meeting tomorrow morning
- Needs revenue breakdown and metrics

**Suggested Actions**:
- [ ] Reply to sender with status update
- [ ] Check if Q1 report is ready
- [ ] Set deadline reminder for today 5 PM
- [ ] Prepare revenue breakdown section
```

## Error Handling

**Missing frontmatter**: Log error, skip file
**Malformed YAML**: Log error, attempt to parse body only
**Empty email body**: Note in analysis, suggest follow-up

## Testing

Test with sample email containing:
- Clear action request
- Deadline
- Multiple questions
- Urgency keywords
