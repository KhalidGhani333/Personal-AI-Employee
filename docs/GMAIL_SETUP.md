# Gmail App Password Setup Guide

## Step 1: Enable 2-Factor Authentication
1. Go to: https://myaccount.google.com/security
2. Scroll to "2-Step Verification"
3. Click "Get Started" and follow instructions
4. Verify with phone number

## Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select app: "Mail"
3. Select device: "Other (Custom name)"
4. Enter name: "AI Employee"
5. Click "Generate"
6. Copy the 16-character password (e.g., "abcd efgh ijkl mnop")
7. Remove spaces: "abcdefghijklmnop"

## Important Notes:
- This is NOT your regular Gmail password
- App passwords bypass 2FA for specific apps
- Keep this password secure
- You can revoke it anytime from the same page

## Troubleshooting:
- If you don't see "App passwords" option:
  - Make sure 2FA is enabled first
  - Wait 5-10 minutes after enabling 2FA
  - Try logging out and back in

## Security:
- Never share this password
- Store in .env file only
- Add .env to .gitignore
- Revoke if compromised
