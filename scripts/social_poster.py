"""
Social Media Poster - Multi-Platform Posting with Approval Workflow
====================================================================
Supports LinkedIn, Twitter, Facebook, and Instagram with session-based auth.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
PENDING_APPROVAL = VAULT_PATH / "Pending_Approval"
APPROVED = VAULT_PATH / "Approved"
LOGS_PATH = VAULT_PATH / "Logs"
SESSION_PATH = LOGS_PATH / "sessions"

# Ensure directories exist
PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)
APPROVED.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)
SESSION_PATH.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = LOGS_PATH / "social_poster.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONTENT GENERATION FUNCTIONS
# ============================================================================

def generate_linkedin_post(topic, tone="professional"):
    """Generate LinkedIn post content"""
    templates = {
        "professional": f"""🚀 {topic}

I've been exploring {topic} and wanted to share some insights with my network.

Key takeaways:
• Innovation drives progress
• Collaboration creates opportunities
• Continuous learning is essential

What are your thoughts on {topic}? Let's discuss in the comments!

#LinkedIn #Professional #Innovation""",

        "casual": f"""Hey LinkedIn! 👋

Just wanted to share some thoughts on {topic}.

It's fascinating how this is changing the way we work and think. Would love to hear your perspectives!

#Thoughts #Discussion""",

        "technical": f"""Deep Dive: {topic}

Technical analysis and implementation considerations:

1. Architecture patterns
2. Best practices
3. Performance optimization

Full breakdown in the comments. Thoughts?

#Tech #Engineering #Development"""
    }

    return templates.get(tone, templates["professional"])


def generate_twitter_post(topic, style="informative"):
    """Generate Twitter/X post content (280 chars max)"""
    templates = {
        "informative": f"🔥 {topic}\n\nKey insight: Innovation happens at the intersection of technology and creativity.\n\n#Tech #Innovation",

        "question": f"What's your take on {topic}? 🤔\n\nDrop your thoughts below! 👇\n\n#Discussion #Community",

        "announcement": f"🚀 Exciting update on {topic}!\n\nStay tuned for more details.\n\n#News #Update",

        "thread": f"🧵 Thread on {topic}\n\n1/ Let's break this down...\n\n#Thread #Insights"
    }

    content = templates.get(style, templates["informative"])

    # Ensure under 280 characters
    if len(content) > 280:
        content = content[:277] + "..."

    return content


def generate_facebook_post(topic, format="story"):
    """Generate Facebook post content"""
    templates = {
        "story": f"""📖 {topic}

Here's something interesting I wanted to share with you all...

{topic} has been on my mind lately, and I think it's worth discussing. What do you think?

Drop a comment and let me know your thoughts! 💭

#Facebook #Community #Discussion""",

        "update": f"""✨ Update: {topic}

Quick update for everyone following along!

Things are moving forward and I'm excited to share more soon.

Stay tuned! 🚀""",

        "question": f"""❓ Question for you all:

What's your experience with {topic}?

I'm curious to hear different perspectives. Comment below! 👇

#AskingForInput #Community"""
    }

    return templates.get(format, templates["story"])


def generate_instagram_caption(topic, style="inspirational"):
    """Generate Instagram caption"""
    templates = {
        "inspirational": f"""✨ {topic} ✨

Every journey begins with a single step. Today, let's talk about {topic} and how it's shaping our future.

What inspires you? Share in the comments! 💫

#Instagram #Inspiration #Motivation #Growth #Success #Journey""",

        "educational": f"""📚 Learn: {topic}

Swipe to learn more about {topic} →

Key points:
1️⃣ Understanding the basics
2️⃣ Practical applications
3️⃣ Future implications

Save this for later! 🔖

#Education #Learning #Knowledge #Tips""",

        "lifestyle": f"""🌟 {topic}

Living my best life and exploring {topic}. Here's what I've learned...

Tag someone who needs to see this! 👇

#Lifestyle #Daily #Vibes #Aesthetic"""
    }

    return templates.get(style, templates["inspirational"])


# ============================================================================
# APPROVAL WORKFLOW FUNCTIONS
# ============================================================================

def save_post_for_approval(platform, content, metadata=None):
    """Save generated post to Pending_Approval folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"POST_{platform.upper()}_{timestamp}.md"
    filepath = PENDING_APPROVAL / filename

    # Create frontmatter
    frontmatter = {
        "platform": platform.lower(),
        "status": "pending_approval",
        "created_at": datetime.now().isoformat(),
        "approved_at": None,
        "posted_at": None
    }

    if metadata:
        frontmatter.update(metadata)

    # Create file content
    file_content = "---\n"
    for key, value in frontmatter.items():
        file_content += f"{key}: {value}\n"
    file_content += "---\n\n"
    file_content += content

    # Save file
    filepath.write_text(file_content, encoding='utf-8')
    logger.info(f"Saved post for approval: {filename}")

    return filepath


def load_approved_post(filepath):
    """Load and parse approved post file"""
    content = filepath.read_text(encoding='utf-8')

    # Parse frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1]
            post_content = parts[2].strip()

            frontmatter = {}
            for line in frontmatter_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()

            return frontmatter, post_content

    return {}, content


# ============================================================================
# PLAYWRIGHT POSTING FUNCTIONS
# ============================================================================

def post_to_linkedin(content, wait_for_confirmation=True):
    """Post to LinkedIn using Playwright with session"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("Playwright not installed")
        return False

    session_file = SESSION_PATH / "linkedin_session.json"

    logger.info("Starting LinkedIn posting...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load session if exists
        if session_file.exists():
            try:
                session_data = json.loads(session_file.read_text())
                context.add_cookies(session_data.get('cookies', []))
                logger.info("Loaded saved LinkedIn session")
            except Exception as e:
                logger.warning(f"Could not load session: {e}")

        page = context.new_page()

        try:
            # Navigate to LinkedIn
            logger.info("Opening LinkedIn...")
            page.goto("https://www.linkedin.com/feed/")
            page.wait_for_timeout(5000)

            # Check if logged in
            if "login" in page.url or "authwall" in page.url:
                logger.error("Not logged in to LinkedIn. Please login manually first.")
                logger.info("Waiting 60 seconds for manual login...")
                page.wait_for_timeout(60000)

                # Save session after login
                cookies = context.cookies()
                session_data = {'cookies': cookies}
                session_file.write_text(json.dumps(session_data, indent=2))
                logger.info("Session saved")

            # Click "Start a post" button
            logger.info("Opening post composer...")
            start_post_selectors = [
                'button:has-text("Start a post")',
                '[aria-label="Start a post"]',
                '.share-box-feed-entry__trigger'
            ]

            clicked = False
            for selector in start_post_selectors:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.click()
                    clicked = True
                    break

            if not clicked:
                logger.error("Could not find 'Start a post' button")
                browser.close()
                return False

            page.wait_for_timeout(2000)

            # Find editor and type content
            logger.info("Typing post content...")
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
                '[data-placeholder="What do you want to talk about?"]'
            ]

            editor = None
            for selector in editor_selectors:
                if page.locator(selector).count() > 0:
                    editor = page.locator(selector).first
                    break

            if not editor:
                logger.error("Could not find post editor")
                browser.close()
                return False

            # Type content with delay for better reliability
            editor.click()
            page.wait_for_timeout(500)
            editor.type(content, delay=50)
            page.wait_for_timeout(1000)

            if wait_for_confirmation:
                logger.info("=" * 60)
                logger.info("POST READY FOR REVIEW")
                logger.info("=" * 60)
                logger.info("Please review the post in the browser window.")
                logger.info("Click 'Post' button manually to publish.")
                logger.info("Browser will stay open for 2 minutes...")
                logger.info("=" * 60)
                page.wait_for_timeout(120000)  # Wait 2 minutes
            else:
                # Auto-post (not recommended)
                post_button = page.locator('button:has-text("Post")').first
                post_button.click()
                page.wait_for_timeout(3000)
                logger.info("Post published automatically")

            browser.close()
            return True

        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {e}")
            browser.close()
            return False


def post_to_twitter(content, wait_for_confirmation=True):
    """Post to Twitter/X using Playwright with session"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("Playwright not installed")
        return False

    session_file = SESSION_PATH / "twitter_session.json"

    logger.info("Starting Twitter posting...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load session if exists
        if session_file.exists():
            try:
                session_data = json.loads(session_file.read_text())
                context.add_cookies(session_data.get('cookies', []))
                logger.info("Loaded saved Twitter session")
            except Exception as e:
                logger.warning(f"Could not load session: {e}")

        page = context.new_page()

        try:
            # Navigate to Twitter
            logger.info("Opening Twitter/X...")
            page.goto("https://twitter.com/home")
            page.wait_for_timeout(5000)

            # Check if logged in
            if "login" in page.url:
                logger.error("Not logged in to Twitter. Please login manually first.")
                logger.info("Waiting 60 seconds for manual login...")
                page.wait_for_timeout(60000)

                # Save session after login
                cookies = context.cookies()
                session_data = {'cookies': cookies}
                session_file.write_text(json.dumps(session_data, indent=2))
                logger.info("Session saved")

            # Click tweet button
            logger.info("Opening tweet composer...")
            tweet_button_selectors = [
                '[data-testid="tweetButtonInline"]',
                '[aria-label="Tweet"]',
                'a[href="/compose/tweet"]'
            ]

            clicked = False
            for selector in tweet_button_selectors:
                if page.locator(selector).count() > 0:
                    page.locator(selector).first.click()
                    clicked = True
                    break

            if not clicked:
                logger.error("Could not find tweet button")
                browser.close()
                return False

            page.wait_for_timeout(2000)

            # Type content
            logger.info("Typing tweet...")
            editor_selectors = [
                '[data-testid="tweetTextarea_0"]',
                '[role="textbox"][contenteditable="true"]'
            ]

            editor = None
            for selector in editor_selectors:
                if page.locator(selector).count() > 0:
                    editor = page.locator(selector).first
                    break

            if not editor:
                logger.error("Could not find tweet editor")
                browser.close()
                return False

            editor.click()
            page.wait_for_timeout(500)
            editor.type(content, delay=50)
            page.wait_for_timeout(1000)

            if wait_for_confirmation:
                logger.info("=" * 60)
                logger.info("TWEET READY FOR REVIEW")
                logger.info("=" * 60)
                logger.info("Please review the tweet in the browser window.")
                logger.info("Click 'Post' or 'Tweet' button manually to publish.")
                logger.info("Browser will stay open for 2 minutes...")
                logger.info("=" * 60)
                page.wait_for_timeout(120000)
            else:
                # Auto-post
                post_button = page.locator('[data-testid="tweetButton"]').first
                post_button.click()
                page.wait_for_timeout(3000)
                logger.info("Tweet published automatically")

            browser.close()
            return True

        except Exception as e:
            logger.error(f"Failed to post to Twitter: {e}")
            browser.close()
            return False


def post_to_facebook(content, wait_for_confirmation=True):
    """Post to Facebook using Playwright with session"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("Playwright not installed")
        return False

    session_file = SESSION_PATH / "facebook_session.json"

    logger.info("Starting Facebook posting...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load session if exists
        if session_file.exists():
            try:
                session_data = json.loads(session_file.read_text())
                context.add_cookies(session_data.get('cookies', []))
                logger.info("Loaded saved Facebook session")
            except Exception as e:
                logger.warning(f"Could not load session: {e}")

        page = context.new_page()

        try:
            # Navigate to Facebook
            logger.info("Opening Facebook...")
            page.goto("https://www.facebook.com/")
            logger.info("Waiting for page to load (15 seconds)...")
            page.wait_for_timeout(15000)

            # Check if logged in
            if "login" in page.url:
                logger.error("Not logged in to Facebook. Please login manually first.")
                logger.info("Waiting 3 MINUTES for manual login...")
                page.wait_for_timeout(180000)

                # Save session after login
                cookies = context.cookies()
                session_data = {'cookies': cookies}
                session_file.write_text(json.dumps(session_data, indent=2))
                logger.info("Session saved")

                # Wait more after login
                logger.info("Waiting for Facebook to fully load after login...")
                page.wait_for_timeout(10000)

            # Click "What's on your mind?" to open composer
            logger.info("Looking for post composer (will try for 30 seconds)...")
            composer_selectors = [
                '[aria-label*="What\'s on your mind"]',
                '[role="button"]:has-text("What\'s on your mind")',
                '[placeholder*="What\'s on your mind"]',
                'div[role="button"]',
                '[data-pagelet="FeedComposer"]'
            ]

            clicked = False
            # Try multiple times with delays
            for attempt in range(6):
                logger.info(f"Attempt {attempt + 1}/6 to find composer...")
                for selector in composer_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click()
                            clicked = True
                            logger.info(f"Found composer with selector: {selector}")
                            break
                    except:
                        continue
                if clicked:
                    break
                page.wait_for_timeout(5000)

            if not clicked:
                logger.error("Could not find post composer after 30 seconds")
                logger.info("Browser will stay open for 2 minutes for manual posting...")
                logger.info("Please manually click 'What's on your mind?' and paste content")
                page.wait_for_timeout(120000)
                browser.close()
                return False

            page.wait_for_timeout(3000)

            # Type content
            logger.info("Typing post...")
            editor_selectors = [
                '[contenteditable="true"][role="textbox"]',
                '[aria-label*="What\'s on your mind"]',
                'div[contenteditable="true"]'
            ]

            editor = None
            for selector in editor_selectors:
                elements = page.locator(selector).all()
                for elem in elements:
                    try:
                        if elem.is_visible():
                            editor = elem
                            break
                    except:
                        continue
                if editor:
                    break

            if not editor:
                logger.error("Could not find post editor")
                browser.close()
                return False

            editor.click()
            page.wait_for_timeout(500)
            editor.type(content, delay=50)
            page.wait_for_timeout(1000)

            if wait_for_confirmation:
                logger.info("=" * 60)
                logger.info("FACEBOOK POST READY FOR REVIEW")
                logger.info("=" * 60)
                logger.info("Please review the post in the browser window.")
                logger.info("Click 'Post' button manually to publish.")
                logger.info("Browser will stay open for 2 minutes...")
                logger.info("=" * 60)
                page.wait_for_timeout(120000)
            else:
                # Auto-post
                post_button_selectors = [
                    '[aria-label="Post"]',
                    'div[role="button"]:has-text("Post")'
                ]
                for selector in post_button_selectors:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click()
                        break
                page.wait_for_timeout(3000)
                logger.info("Post published automatically")

            browser.close()
            return True

        except Exception as e:
            logger.error(f"Failed to post to Facebook: {e}")
            browser.close()
            return False


def create_text_image(text, output_path):
    """Create a simple text image for Instagram"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logger.error("Pillow not installed. Install with: pip install Pillow")
        return None

    # Create image
    width, height = 1080, 1080
    background_color = (255, 255, 255)  # White
    text_color = (0, 0, 0)  # Black

    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Wrap text
    max_width = width - 100
    lines = []
    words = text.split()
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    # Draw text centered
    y = (height - len(lines) * 50) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += 50

    # Save image
    image.save(output_path)
    logger.info(f"Text image created: {output_path}")
    return output_path


def post_to_instagram(caption, wait_for_confirmation=True, image_path=None):
    """Post to Instagram using Playwright browser automation (Desktop)"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        logger.error("Playwright not installed")
        return False

    session_file = SESSION_PATH / "instagram_session.json"

    # Generate text image if no image provided
    if not image_path:
        logger.info("No image provided, generating text image from caption...")
        temp_image = LOGS_PATH / f"instagram_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = create_text_image(caption[:200], temp_image)  # Use first 200 chars for image
        if not image_path:
            logger.error("Failed to create text image")
            return False
        logger.info(f"✓ Text image created: {image_path}")

    logger.info("Starting Instagram posting...")

    with sync_playwright() as p:
        # Use DESKTOP user agent with anti-detection
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled'
            ]
        )

        # Load complete browser state if exists
        if session_file.exists():
            try:
                logger.info("Loading saved Instagram session")
                context = browser.new_context(
                    storage_state=str(session_file),
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    no_viewport=True,
                    locale='en-US'
                )
            except Exception as e:
                logger.warning(f"Could not load session: {e}")
                logger.info("Creating new context")
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    no_viewport=True,
                    locale='en-US'
                )
        else:
            logger.info("No session file found, creating new context")
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                no_viewport=True,
                locale='en-US'
            )

        page = context.new_page()

        # Hide webdriver property
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)

        try:
            # Navigate to Instagram
            logger.info("Opening Instagram (Desktop)...")
            page.goto("https://www.instagram.com/")
            logger.info("Waiting for page to load...")
            page.wait_for_timeout(15000)  # Wait longer for full load

            # Check if we need to login
            if page.locator('input[name="username"]').count() > 0 or "login" in page.url:
                logger.info("=" * 60)
                logger.info("LOGIN REQUIRED")
                logger.info("=" * 60)
                logger.info("Please login to Instagram manually")
                logger.info("After login, wait for home page to fully load")
                logger.info("Waiting 3 MINUTES for login...")
                logger.info("=" * 60)
                page.wait_for_timeout(180000)

                # Wait a bit more after login
                logger.info("Waiting for Instagram to fully load after login...")
                page.wait_for_timeout(10000)

                # Save complete browser state after login
                try:
                    context.storage_state(path=str(session_file))
                    logger.info("✓ Session saved (complete browser state)")
                    logger.info(f"Session file: {session_file}")
                except Exception as e:
                    logger.error(f"Failed to save session: {e}")

                # Reload to ensure session is active
                logger.info("Reloading page to verify session...")
                page.goto("https://www.instagram.com/")
                page.wait_for_timeout(10000)
            else:
                # Already logged in
                logger.info("✓ Already logged in!")
                page.wait_for_timeout(5000)  # Wait for full page load

            # Click "Create" button (+ icon on left sidebar)
            logger.info("Looking for Create button (+ icon on left sidebar)...")
            create_selectors = [
                # Left sidebar + icon
                'a[href="#"][role="link"] svg',
                'svg[aria-label="New post"]',
                'svg[aria-label="Create"]',
                '[aria-label="New post"]',
                '[aria-label="Create"]',
                'a[href="#"]',
                # Try finding by position in nav
                'nav a[href="#"]',
                'div[role="link"]',
                # More generic
                'svg path[d*="M2 12"]',  # Plus icon path
            ]

            clicked = False
            for attempt in range(10):  # Try for 20 seconds
                logger.info(f"Attempt {attempt + 1}/10 to find Create button...")
                for selector in create_selectors:
                    try:
                        elements = page.locator(selector).all()
                        logger.info(f"  Trying selector: {selector} - found {len(elements)} elements")
                        for elem in elements:
                            try:
                                if elem.is_visible():
                                    # Check if it's the right element by checking parent or nearby text
                                    elem.click()
                                    clicked = True
                                    logger.info(f"✓ Clicked Create button with selector: {selector}")
                                    break
                            except Exception as e:
                                logger.debug(f"  Failed to click element: {e}")
                                continue
                        if clicked:
                            break
                    except Exception as e:
                        logger.debug(f"  Selector {selector} failed: {e}")
                        continue
                if clicked:
                    break
                page.wait_for_timeout(2000)

            if not clicked:
                logger.error("Could not find Create button automatically")
                logger.info("=" * 60)
                logger.info("MANUAL ACTION REQUIRED")
                logger.info("=" * 60)
                logger.info("Please click the '+' (Create) button on the left sidebar manually")
                logger.info("Browser will wait for 2 minutes...")
                logger.info("=" * 60)
                page.wait_for_timeout(120000)
                # Continue anyway, user might have clicked it

            page.wait_for_timeout(3000)

            # Upload image automatically
            logger.info("=" * 60)
            logger.info("STEP 1: AUTO-UPLOADING IMAGE")
            logger.info("=" * 60)
            logger.info(f"Uploading image: {image_path}")

            # Find file input and upload
            file_input_selectors = [
                'input[type="file"]',
                'input[accept*="image"]',
                'input[accept*="video"]'
            ]

            file_input = None
            for attempt in range(5):
                logger.info(f"Looking for file input (attempt {attempt + 1}/5)...")
                for selector in file_input_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            file_input = page.locator(selector).first
                            logger.info(f"✓ Found file input with selector: {selector}")
                            break
                    except:
                        continue
                if file_input:
                    break
                page.wait_for_timeout(2000)

            if file_input:
                try:
                    file_input.set_input_files(str(image_path))
                    logger.info("✓ Image uploaded!")
                    page.wait_for_timeout(5000)  # Wait for image to process

                    # Click Next button (first time)
                    logger.info("Looking for Next button (1)...")
                    next_button_selectors = [
                        'button:has-text("Next")',
                        '[role="button"]:has-text("Next")',
                        'button:text("Next")',
                        'div[role="button"]:text("Next")'
                    ]

                    next_clicked = False
                    for attempt in range(5):
                        for selector in next_button_selectors:
                            try:
                                if page.locator(selector).count() > 0:
                                    page.locator(selector).first.click()
                                    logger.info("✓ Clicked Next (1)")
                                    next_clicked = True
                                    page.wait_for_timeout(3000)
                                    break
                            except:
                                continue
                        if next_clicked:
                            break
                        page.wait_for_timeout(1000)

                    if not next_clicked:
                        logger.warning("Could not find Next button (1), continuing anyway...")

                    # Click Next again (filters page)
                    logger.info("Looking for Next button (2)...")
                    next_clicked = False
                    for attempt in range(5):
                        for selector in next_button_selectors:
                            try:
                                if page.locator(selector).count() > 0:
                                    page.locator(selector).first.click()
                                    logger.info("✓ Clicked Next (2)")
                                    next_clicked = True
                                    page.wait_for_timeout(3000)
                                    break
                            except:
                                continue
                        if next_clicked:
                            break
                        page.wait_for_timeout(1000)

                    if not next_clicked:
                        logger.warning("Could not find Next button (2), continuing anyway...")

                except Exception as e:
                    logger.error(f"Error during upload/next: {e}")
                    logger.info("Browser will stay open for manual action")
                    page.wait_for_timeout(120000)
            else:
                logger.error("Could not find file input")
                logger.info("=" * 60)
                logger.info("MANUAL ACTION REQUIRED")
                logger.info("=" * 60)
                logger.info("Please upload image manually and click Next twice")
                logger.info("Browser will wait for 2 minutes...")
                logger.info("=" * 60)
                page.wait_for_timeout(120000)

            # Wait for caption field
            logger.info("=" * 60)
            logger.info("STEP 2: AUTO-FILLING CAPTION")
            logger.info("=" * 60)

            caption_selectors = [
                'textarea[aria-label="Write a caption..."]',
                'textarea[placeholder="Write a caption..."]',
                'div[contenteditable="true"][aria-label*="caption"]'
            ]

            caption_field = None
            for attempt in range(10):
                for selector in caption_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            caption_field = page.locator(selector).first
                            if caption_field.is_visible():
                                logger.info(f"✓ Caption field found!")
                                break
                    except:
                        continue
                if caption_field:
                    break
                page.wait_for_timeout(2000)

            if caption_field:
                caption_field.click()
                page.wait_for_timeout(500)
                caption_field.fill(caption)
                page.wait_for_timeout(1000)
                logger.info("✓ Caption filled!")
            else:
                logger.warning("Could not find caption field, continuing anyway...")

            logger.info("=" * 60)
            logger.info("STEP 3: CLICK SHARE BUTTON")
            logger.info("=" * 60)
            logger.info("Everything is ready!")
            logger.info("Just click the 'Share' button to post")
            logger.info("=" * 60)
            logger.info("Browser will stay open for 5 MINUTES")
            logger.info("=" * 60)

            # Wait for user to click Share
            page.wait_for_timeout(300000)

            browser.close()
            logger.info("✓ Instagram posting completed!")
            return True

        except Exception as e:
            logger.error(f"Failed to post to Instagram: {e}")
            logger.info("Browser will stay open for manual posting...")
            page.wait_for_timeout(120000)
            browser.close()
            return False


# ============================================================================
# ORCHESTRATOR FUNCTIONS
# ============================================================================

def run_social_posting_pipeline(topic, platforms=None, auto_post=False):
    """
    Main orchestrator function for social media posting pipeline

    Workflow:
    1. Generate posts for specified platforms
    2. Save to Pending_Approval folder
    3. Wait for user approval
    4. Post approved content to platforms

    Args:
        topic: Topic/content for posts
        platforms: List of platforms ['linkedin', 'twitter', 'facebook', 'instagram']
        auto_post: If True, posts automatically without confirmation (not recommended)
    """
    if platforms is None:
        platforms = ['linkedin', 'twitter', 'facebook', 'instagram']

    logger.info("=" * 60)
    logger.info("SOCIAL MEDIA POSTING PIPELINE STARTED")
    logger.info("=" * 60)
    logger.info(f"Topic: {topic}")
    logger.info(f"Platforms: {', '.join(platforms)}")
    logger.info("=" * 60)

    generated_posts = []

    # Step 1: Generate content for each platform
    logger.info("\n[STEP 1] Generating content...")

    if 'linkedin' in platforms:
        content = generate_linkedin_post(topic)
        filepath = save_post_for_approval('linkedin', content, {'topic': topic})
        generated_posts.append(('linkedin', filepath, content))
        logger.info(f"✓ LinkedIn post generated: {filepath.name}")

    if 'twitter' in platforms:
        content = generate_twitter_post(topic)
        filepath = save_post_for_approval('twitter', content, {'topic': topic})
        generated_posts.append(('twitter', filepath, content))
        logger.info(f"✓ Twitter post generated: {filepath.name}")

    if 'facebook' in platforms:
        content = generate_facebook_post(topic)
        filepath = save_post_for_approval('facebook', content, {'topic': topic})
        generated_posts.append(('facebook', filepath, content))
        logger.info(f"✓ Facebook post generated: {filepath.name}")

    if 'instagram' in platforms:
        content = generate_instagram_caption(topic)
        filepath = save_post_for_approval('instagram', content, {'topic': topic})
        generated_posts.append(('instagram', filepath, content))
        logger.info(f"✓ Instagram caption generated: {filepath.name}")

    # Step 2: Wait for approval
    logger.info("\n[STEP 2] Posts saved to Pending_Approval folder")
    logger.info("Please review and approve posts in Obsidian:")
    logger.info(f"Location: {PENDING_APPROVAL}")
    logger.info("\nChange 'status: pending_approval' to 'status: approved'")
    logger.info("\nPress Enter when ready to check for approved posts...")
    input()

    # Step 3: Check for approved posts
    logger.info("\n[STEP 3] Checking for approved posts...")

    approved_posts = []
    for platform, filepath, content in generated_posts:
        if filepath.exists():
            frontmatter, post_content = load_approved_post(filepath)
            if frontmatter.get('status') == 'approved':
                approved_posts.append((platform, filepath, post_content))
                logger.info(f"✓ {platform.capitalize()} post approved")
            else:
                logger.info(f"✗ {platform.capitalize()} post not approved (status: {frontmatter.get('status')})")

    if not approved_posts:
        logger.info("\nNo posts approved. Exiting.")
        return

    # Step 4: Post to platforms
    logger.info(f"\n[STEP 4] Posting {len(approved_posts)} approved post(s)...")

    results = []
    for platform, filepath, content in approved_posts:
        logger.info(f"\nPosting to {platform.capitalize()}...")

        success = False
        if platform == 'linkedin':
            success = post_to_linkedin(content, wait_for_confirmation=not auto_post)
        elif platform == 'twitter':
            success = post_to_twitter(content, wait_for_confirmation=not auto_post)
        elif platform == 'facebook':
            success = post_to_facebook(content, wait_for_confirmation=not auto_post)
        elif platform == 'instagram':
            success = post_to_instagram(content)

        results.append((platform, success))

        if success:
            # Move to Approved folder
            approved_file = APPROVED / filepath.name
            filepath.rename(approved_file)
            logger.info(f"✓ {platform.capitalize()} post completed, moved to Approved/")
        else:
            logger.error(f"✗ {platform.capitalize()} post failed")

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("POSTING PIPELINE COMPLETED")
    logger.info("=" * 60)
    successful = sum(1 for _, success in results if success)
    logger.info(f"Results: {successful}/{len(results)} posts successful")
    for platform, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        logger.info(f"  {status}: {platform.capitalize()}")
    logger.info("=" * 60)


def post_approved_content(platform, filepath):
    """Post a single approved content file"""
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        return False

    frontmatter, content = load_approved_post(filepath)

    if frontmatter.get('status') != 'approved':
        logger.error(f"Post not approved (status: {frontmatter.get('status')})")
        return False

    logger.info(f"Posting to {platform}...")

    success = False
    if platform == 'linkedin':
        success = post_to_linkedin(content)
    elif platform == 'twitter':
        success = post_to_twitter(content)
    elif platform == 'facebook':
        success = post_to_facebook(content)
    elif platform == 'instagram':
        success = post_to_instagram(content)
    else:
        logger.error(f"Unknown platform: {platform}")
        return False

    if success:
        # Move to Approved folder
        approved_file = APPROVED / filepath.name
        filepath.rename(approved_file)
        logger.info(f"Post completed, moved to Approved/")

    return success


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Social Media Poster - Multi-platform posting with approval workflow'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate posts for approval')
    generate_parser.add_argument('topic', help='Topic for posts')
    generate_parser.add_argument(
        '--platforms',
        nargs='+',
        choices=['linkedin', 'twitter', 'facebook', 'instagram'],
        default=['linkedin', 'twitter', 'facebook', 'instagram'],
        help='Platforms to generate for'
    )

    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Run full posting pipeline')
    pipeline_parser.add_argument('topic', help='Topic for posts')
    pipeline_parser.add_argument(
        '--platforms',
        nargs='+',
        choices=['linkedin', 'twitter', 'facebook', 'instagram'],
        default=['linkedin', 'twitter', 'facebook', 'instagram'],
        help='Platforms to post to'
    )
    pipeline_parser.add_argument(
        '--auto-post',
        action='store_true',
        help='Auto-post without manual confirmation (not recommended)'
    )

    # Post command
    post_parser = subparsers.add_parser('post', help='Post approved content')
    post_parser.add_argument('platform', choices=['linkedin', 'twitter', 'facebook', 'instagram'])
    post_parser.add_argument('file', help='Path to approved post file')

    args = parser.parse_args()

    if args.command == 'generate':
        logger.info("Generating posts...")
        generated = []

        if 'linkedin' in args.platforms:
            content = generate_linkedin_post(args.topic)
            filepath = save_post_for_approval('linkedin', content, {'topic': args.topic})
            generated.append(filepath.name)

        if 'twitter' in args.platforms:
            content = generate_twitter_post(args.topic)
            filepath = save_post_for_approval('twitter', content, {'topic': args.topic})
            generated.append(filepath.name)

        if 'facebook' in args.platforms:
            content = generate_facebook_post(args.topic)
            filepath = save_post_for_approval('facebook', content, {'topic': args.topic})
            generated.append(filepath.name)

        if 'instagram' in args.platforms:
            content = generate_instagram_caption(args.topic)
            filepath = save_post_for_approval('instagram', content, {'topic': args.topic})
            generated.append(filepath.name)

        logger.info(f"\nGenerated {len(generated)} post(s):")
        for filename in generated:
            logger.info(f"  - {filename}")
        logger.info(f"\nLocation: {PENDING_APPROVAL}")
        logger.info("Review and approve in Obsidian, then run 'post' command")

    elif args.command == 'pipeline':
        run_social_posting_pipeline(
            args.topic,
            platforms=args.platforms,
            auto_post=args.auto_post
        )

    elif args.command == 'post':
        filepath = Path(args.file)
        success = post_approved_content(args.platform, filepath)
        sys.exit(0 if success else 1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
