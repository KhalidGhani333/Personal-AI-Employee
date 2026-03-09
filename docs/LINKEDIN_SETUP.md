# LinkedIn Credentials Setup Guide

## What You Need:
- LinkedIn account email
- LinkedIn account password

## Important Security Notes:

### Option 1: Use Regular Password (Simple but Less Secure)
- Use your normal LinkedIn login credentials
- Store in .env file
- Risk: If .env is compromised, your LinkedIn account is at risk

### Option 2: Create Dedicated Account (Recommended for Production)
- Create a separate LinkedIn account for automation
- Use it only for AI Employee
- Less risk to your main account
- LinkedIn may flag automation - use carefully

## LinkedIn Automation Risks:

**Important Warnings:**
1. LinkedIn Terms of Service prohibit automated posting
2. Your account may be flagged or suspended
3. Use at your own risk
4. Recommended only for:
   - Testing/development
   - Personal accounts
   - Low-frequency posting (not spam)

## Best Practices:

### For Testing:
- Use a test/secondary LinkedIn account
- Post infrequently (max 1-2 times per day)
- Review posts manually before automation
- Use human-approval skill for oversight

### For Production:
- Consider using LinkedIn API instead (requires company page)
- Manual posting is safer for personal accounts
- Use automation only for drafting, not posting

## Alternative: LinkedIn API (Official Method)

If you have a LinkedIn Company Page:
1. Go to: https://www.linkedin.com/developers/
2. Create an app
3. Get API credentials
4. Use official API (more reliable, TOS-compliant)

## Setup Steps:

1. Decide which account to use
2. Note down email and password
3. Add to .env file
4. Test with --headless false first (to see what happens)
5. Use sparingly to avoid account issues

## Troubleshooting:

**"Login failed":**
- Check email/password are correct
- LinkedIn may require CAPTCHA (run with --headless false)
- Account may need verification

**"Account locked":**
- LinkedIn detected automation
- Wait 24-48 hours
- Reduce posting frequency
- Consider manual posting instead
