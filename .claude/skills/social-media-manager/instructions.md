# Social Media Manager - Detailed Instructions

## Objective
Manage social media presence by creating engaging content, scheduling posts, and tracking performance.

## Supported Platforms

### LinkedIn
- Professional content
- Business updates
- Industry insights
- Company milestones

### Twitter/X
- Quick updates
- Engagement posts
- Industry news
- Thought leadership

### Facebook/Instagram
- Visual content
- Behind-the-scenes
- Customer stories
- Product showcases

## Content Creation Workflow

### 1. Generate Content Ideas
```
Input: Business_Goals.md, recent activities
Process:
  - Analyze recent accomplishments
  - Check industry trends
  - Review engagement history
  - Generate 5-10 content ideas
Output: Content ideas list
```

### 2. Draft Post
```
Input: Content idea + platform
Process:
  - Write platform-appropriate content
  - Add relevant hashtags
  - Include call-to-action
  - Optimize for engagement
  - Add visual suggestions
Output: Draft post in /Pending_Approval
```

### 3. Create Approval Request
```markdown
---
type: social_media_post
platform: linkedin|twitter|facebook|instagram
scheduled_time: {ISO_timestamp}
status: pending_approval
---

## Post Content
{post_text}

## Hashtags
{hashtags}

## Visual Suggestion
{image_description}

## Expected Engagement
- Reach: {estimated_reach}
- Engagement Rate: {estimated_rate}

## To Approve
Move to /Approved folder
```

### 4. Schedule Post
```
When: File moved to /Approved
Process:
  - Read approved post
  - Use Social Media MCP
  - Schedule for specified time
  - Log scheduled post
  - Update Dashboard
```

## Content Guidelines

**LinkedIn Best Practices:**
- Length: 150-300 words
- Include question or CTA
- Use 3-5 hashtags
- Post timing: Tue-Thu, 8-10 AM
- Professional tone

**Twitter/X Best Practices:**
- Length: 100-280 characters
- Use 1-2 hashtags
- Include media when possible
- Post timing: Mon-Fri, 12-3 PM
- Conversational tone

**Facebook/Instagram:**
- Length: 40-80 words
- Visual-first content
- Use 5-10 hashtags (Instagram)
- Post timing: Wed-Fri, 1-4 PM
- Engaging, personal tone

## Content Types

**Business Updates:**
```
Template:
"Excited to share that [achievement]!

This milestone represents [significance].

[Call to action]

#hashtag1 #hashtag2"
```

**Industry Insights:**
```
Template:
"[Interesting observation about industry]

Here's what this means for [audience]:
• Point 1
• Point 2
• Point 3

What's your take?

#hashtag1 #hashtag2"
```

**Behind-the-Scenes:**
```
Template:
"A peek into [process/day/project]...

[Story or insight]

[Question to audience]

#hashtag1 #hashtag2"
```

## Engagement Tracking

**Metrics to Track:**
- Impressions
- Engagement rate
- Click-through rate
- Comments/replies
- Shares/retweets
- Follower growth

**Weekly Report:**
```markdown
# Social Media Report - Week of {date}

## Summary
- Total Posts: {count}
- Total Reach: {reach}
- Avg Engagement Rate: {rate}%

## Top Performing Post
- Platform: {platform}
- Content: {snippet}
- Engagement: {metrics}

## Insights
- {insight_1}
- {insight_2}

## Recommendations
- {recommendation_1}
- {recommendation_2}
```

## Content Calendar

**Weekly Schedule:**
- Monday: Industry news/insights
- Tuesday: Business update
- Wednesday: Engagement post (question/poll)
- Thursday: Behind-the-scenes
- Friday: Week recap/achievement

## Integration Points

- **Approval Handler**: All posts require approval
- **Dashboard Updater**: Update social media stats
- **Business Auditor**: Include in weekly briefing
- **Log Manager**: Log all posts

## Success Criteria
- Consistent posting schedule maintained
- Engagement rate > 2%
- All posts approved before publishing
- Content aligns with business goals
