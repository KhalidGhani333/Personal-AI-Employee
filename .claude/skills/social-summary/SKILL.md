# Social Summary Skill

**Track and summarize all social media activity**

---

## Overview

Social Summary is a centralized logging system for all social media posts. It automatically tracks posts to LinkedIn, Twitter, Facebook, and other platforms, maintaining a comprehensive activity log.

---

## Features

### Post Logging
- Log posts from any platform
- Automatic timestamping
- Content preservation
- Metadata support

### Activity Tracking
- Centralized log file
- Platform-specific counts
- Historical record
- Easy retrieval

### Summary Reports
- Total post counts
- Platform breakdown
- Recent activity
- Quick statistics

---

## Usage

### Log a Post
```bash
# Basic usage
python scripts/social_summary.py log <platform> <content>

# Examples
python scripts/social_summary.py log linkedin "Excited to announce our new product!"
python scripts/social_summary.py log twitter "Just shipped a major feature update"
python scripts/social_summary.py log facebook "Check out our latest blog post"
```

### Get Summary
```bash
# View total posts and platform breakdown
python scripts/social_summary.py summary
```

**Output:**
```
Social Media Summary:
  Total Posts: 3

  By Platform:
    - Linkedin: 2 posts
    - Twitter: 1 posts
```

### View Recent Posts
```bash
# View last 10 posts (default)
python scripts/social_summary.py recent

# View specific number
python scripts/social_summary.py recent 5
```

**Output:**
```
Recent Posts (3):

1. [Twitter] February 26, 2026 at 12:59 AM
   Just shipped 5 major systems in one day!...

2. [Linkedin] February 26, 2026 at 12:58 AM
   Excited to announce our new AI Employee system!...
```

---

## Via Skill Command

```
/social-summary log linkedin "Your post content here"
/social-summary summary
/social-summary recent 5
```

---

## Output File

**Location:** `AI_Employee_Vault/Reports/Social_Log.md`

**Format:**
```markdown
# Social Media Activity Log

**Tracking all social media posts and activities**

---

## Linkedin Post - February 26, 2026 at 12:58 AM

**Content:**
> Excited to announce our new AI Employee system! 🚀

---

## Twitter Post - February 26, 2026 at 12:59 AM

**Content:**
> Just shipped 5 major systems in one day!

---
```

---

## Integration

### With Business MCP Server
Automatically log posts when using Business MCP:

```python
from scripts.social_summary import SocialSummary

# After posting to LinkedIn via Business MCP
social = SocialSummary()
social.log_post("linkedin", post_content)
```

### With Ralph Wiggum Loop
Ralph can automatically log posts after execution:

```python
# In ralph_wiggum_loop.py, after social media step
if step_type == "social_media":
    social_summary.log_post(platform, content)
```

### With Social MCP Server
Log posts automatically after successful posting:

```javascript
// In social-mcp/index.js
// After successful post
await logToSocialSummary(platform, content);
```

---

## API Reference

### SocialSummary Class

#### `log_post(platform, content, date=None, metadata=None)`
Log a social media post.

**Parameters:**
- `platform` (str): Platform name (linkedin, twitter, facebook, etc.)
- `content` (str): Post content
- `date` (str, optional): ISO format date (defaults to now)
- `metadata` (dict, optional): Additional metadata

**Returns:**
```python
{
    "success": True,
    "platform": "linkedin",
    "date": "2026-02-26T00:58:00",
    "log_file": "AI_Employee_Vault/Reports/Social_Log.md",
    "message": "Post logged to Social_Log.md"
}
```

**Example:**
```python
from scripts.social_summary import SocialSummary

social = SocialSummary()
result = social.log_post(
    "linkedin",
    "Excited to announce our new product!",
    metadata={"url": "https://linkedin.com/post/123"}
)
```

---

#### `get_summary(days=None)`
Get summary statistics.

**Parameters:**
- `days` (int, optional): Number of days to include (None = all time)

**Returns:**
```python
{
    "success": True,
    "total_posts": 3,
    "platforms": {
        "Linkedin": 2,
        "Twitter": 1
    },
    "log_file": "AI_Employee_Vault/Reports/Social_Log.md",
    "message": "Total posts: 3"
}
```

---

#### `get_recent_posts(count=10)`
Get recent posts.

**Parameters:**
- `count` (int): Number of posts to retrieve (default: 10)

**Returns:**
```python
[
    {
        "platform": "Twitter",
        "date": "February 26, 2026 at 12:59 AM",
        "content": "Just shipped 5 major systems..."
    },
    {
        "platform": "Linkedin",
        "date": "February 26, 2026 at 12:58 AM",
        "content": "Excited to announce..."
    }
]
```

---

## Supported Platforms

- LinkedIn
- Twitter (X)
- Facebook
- Instagram
- TikTok
- YouTube
- Custom platforms (any string)

---

## Use Cases

### 1. Manual Logging
After posting manually, log for tracking:
```bash
python scripts/social_summary.py log linkedin "Just published a new article!"
```

### 2. Automated Logging
Integrate with posting tools to auto-log:
```python
# After successful post
social_summary.log_post(platform, content)
```

### 3. Activity Reports
Generate reports for stakeholders:
```bash
python scripts/social_summary.py summary
```

### 4. Content Review
Review recent posts before planning new content:
```bash
python scripts/social_summary.py recent 20
```

---

## Examples

### Example 1: Log LinkedIn Post
```bash
python scripts/social_summary.py log linkedin "Excited to share our Q1 results! Revenue up 50%."
```

**Result:**
```
[OK] Post logged: linkedin
     Content: Excited to share our Q1 results! Revenue up 50%....
     Log file: AI_Employee_Vault\Reports\Social_Log.md
```

---

### Example 2: Weekly Summary
```bash
python scripts/social_summary.py summary
```

**Result:**
```
Social Media Summary:
  Total Posts: 15

  By Platform:
    - Linkedin: 8 posts
    - Twitter: 5 posts
    - Facebook: 2 posts
```

---

### Example 3: Review Recent Activity
```bash
python scripts/social_summary.py recent 5
```

**Result:**
```
Recent Posts (5):

1. [Linkedin] February 26, 2026 at 03:00 PM
   Excited to share our Q1 results! Revenue up 50%.

2. [Twitter] February 26, 2026 at 02:30 PM
   New blog post: 5 Tips for AI Implementation

3. [Linkedin] February 26, 2026 at 12:58 AM
   Excited to announce our new AI Employee system!

4. [Twitter] February 26, 2026 at 12:59 AM
   Just shipped 5 major systems in one day!

5. [Facebook] February 25, 2026 at 05:00 PM
   Join us for our webinar next week!
```

---

## Best Practices

### Consistent Logging
- Log every post immediately after publishing
- Include relevant metadata (URLs, engagement)
- Use consistent platform names

### Regular Reviews
- Check summary weekly
- Review recent posts before creating new content
- Track posting frequency by platform

### Integration
- Integrate with posting tools
- Automate logging where possible
- Use in CEO briefing reports

---

## Troubleshooting

### Posts Not Appearing
- Check if Social_Log.md exists
- Verify file permissions
- Check for errors in command output

### Summary Shows Wrong Count
- Ensure all posts are logged
- Check for duplicate entries
- Verify platform names are consistent

### Recent Posts Missing
- Check if posts were logged with correct format
- Verify file is not corrupted
- Try logging a new test post

---

## Configuration

### Log File Location
Default: `AI_Employee_Vault/Reports/Social_Log.md`

Change in `social_summary.py`:
```python
SOCIAL_LOG = REPORTS_PATH / "Social_Log.md"
```

### Date Format
Default: "February 26, 2026 at 12:58 AM"

Modify in `log_post()` method:
```python
display_date = dt.strftime("%B %d, %Y at %I:%M %p")
```

---

## Statistics

**Code Metrics:**
- Total Lines: 250+ lines
- Commands: 3 (log, summary, recent)
- API Methods: 3
- Supported Platforms: Unlimited

**Test Results:**
- Log command: ✓ Working
- Summary command: ✓ Working
- Recent command: ✓ Working
- File generation: ✓ Working

---

## Summary

Social Summary provides centralized tracking for all social media activity. It maintains a comprehensive log, generates summaries, and integrates seamlessly with existing posting tools.

**Key Benefits:**
- Centralized logging
- Platform-agnostic
- Easy integration
- Historical tracking
- Quick summaries

**Use Cases:**
- Activity tracking
- Content planning
- Reporting
- Compliance
- Analytics

---

**Ready for production use!** ✓
