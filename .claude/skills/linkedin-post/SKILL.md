# LinkedIn Post Skill

## Purpose
Create real LinkedIn posts using browser automation. Automates content publishing for professional networking.

## When to Use
- Share project updates
- Publish articles or insights
- Announce achievements
- Automated content scheduling

## Requirements
Environment variables in `.env`:
```
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
```

Install Playwright:
```bash
pip install playwright python-dotenv
playwright install chromium
```

## Usage

```bash
python .claude/skills/linkedin-post/scripts/post_linkedin.py \
  --content "Your post content here"
```

## Parameters
- `--content`: Post text content (required, max 3000 chars)
- `--headless`: Run browser in headless mode (optional, default: True)

## Returns
- Exit code 0: Post created successfully
- Exit code 1: Error (authentication, network, or posting failed)

## Security Notes
- Credentials stored in .env file (never commit to git)
- Browser session is temporary and cleaned up
- Use strong passwords and 2FA when possible

## Integration Example
```python
import subprocess
result = subprocess.run([
    'python', '.claude/skills/linkedin-post/scripts/post_linkedin.py',
    '--content', 'Excited to share our latest project milestone!'
])
if result.returncode == 0:
    print("LinkedIn post published")
```
