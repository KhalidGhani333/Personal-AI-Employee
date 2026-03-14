"""
Browser Profile Manager - Persistent Login Sessions
====================================================
Creates and manages persistent browser profiles for each platform.
Login once, stay logged in forever!
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base directory for browser profiles
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
PROFILES_PATH = VAULT_PATH / "Browser_Profiles"
PROFILES_PATH.mkdir(parents=True, exist_ok=True)

# Platform-specific profile directories
PROFILES = {
    'instagram': PROFILES_PATH / 'instagram_profile',
    'linkedin': PROFILES_PATH / 'linkedin_profile',
    'facebook': PROFILES_PATH / 'facebook_profile',
    'twitter': PROFILES_PATH / 'twitter_profile',
    'whatsapp': PROFILES_PATH / 'whatsapp_profile',
}

# Create all profile directories
for platform, path in PROFILES.items():
    path.mkdir(parents=True, exist_ok=True)


def get_profile_path(platform):
    """Get the browser profile path for a platform"""
    return str(PROFILES.get(platform.lower(), PROFILES_PATH / f'{platform}_profile'))


def get_browser_context(browser, platform, headless=False):
    """
    Create a browser context with persistent profile

    Args:
        browser: Playwright browser instance
        platform: Platform name (instagram, linkedin, etc.)
        headless: Run in headless mode

    Returns:
        Browser context with persistent profile
    """
    profile_path = get_profile_path(platform)

    # Create context with persistent profile
    context = browser.new_context(
        user_data_dir=profile_path,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1366, 'height': 768},
        locale='en-US',
        timezone_id='Asia/Karachi'
    )

    return context


def launch_browser_with_profile(p, platform, headless=False):
    """
    Launch browser with persistent profile for a platform

    Args:
        p: Playwright instance
        platform: Platform name
        headless: Run in headless mode

    Returns:
        (browser, context) tuple
    """
    profile_path = get_profile_path(platform)

    # Launch browser with persistent profile
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=headless,
        args=[
            '--start-maximized',
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ],
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1366, 'height': 768},
        locale='en-US',
        timezone_id='Asia/Karachi'
    )

    return browser


if __name__ == "__main__":
    print("Browser Profile Manager")
    print("=" * 60)
    print("\nProfile directories:")
    for platform, path in PROFILES.items():
        exists = "✓" if path.exists() else "✗"
        print(f"  {exists} {platform}: {path}")
    print("\n" + "=" * 60)
