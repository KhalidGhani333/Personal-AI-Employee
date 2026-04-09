"""
Social Media MCP Server
=======================
MCP server for social media operations: posting, analytics, monitoring.
Supports LinkedIn, Twitter, Facebook, Instagram.
"""

import asyncio
import json
import logging
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
VAULT_PATH = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
LOGS_PATH = VAULT_PATH / "Logs"
REPORTS_PATH = VAULT_PATH / "Reports"
SCRIPTS_PATH = Path(__file__).parent.parent.parent / "scripts"

# Ensure directories exist
LOGS_PATH.mkdir(parents=True, exist_ok=True)
REPORTS_PATH.mkdir(parents=True, exist_ok=True)


class SocialMediaMCPServer:
    """MCP Server for social media operations"""

    def __init__(self):
        self.name = "social-media-mcp"
        self.version = "1.0.0"
        self.social_log = REPORTS_PATH / "Social_Log.md"
        self.supported_platforms = ['linkedin', 'twitter', 'facebook', 'instagram']

    async def post_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post content to social media platforms

        Args:
            content: Post content/caption
            platforms: List of platforms to post to
            image_path: Optional image path for Instagram
        """
        try:
            content = params.get('content', '')
            platforms = params.get('platforms', ['linkedin'])
            image_path = params.get('image_path')

            if not content:
                return {
                    "success": False,
                    "error": "Content is required"
                }

            # Validate platforms
            invalid_platforms = [p for p in platforms if p not in self.supported_platforms]
            if invalid_platforms:
                return {
                    "success": False,
                    "error": f"Invalid platforms: {invalid_platforms}"
                }

            # Call social_poster.py
            social_poster = SCRIPTS_PATH / "social_poster.py"

            cmd = [
                sys.executable,
                str(social_poster),
                'pipeline',
                content,
                '--platforms'
            ] + platforms

            if image_path:
                cmd.extend(['--image', image_path])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                logger.info(f"Posted to {', '.join(platforms)}")

                # Log to social summary
                await self._log_post(content, platforms)

                return {
                    "success": True,
                    "platforms": platforms,
                    "content": content[:100] + "..." if len(content) > 100 else content,
                    "message": f"Posted to {', '.join(platforms)}"
                }
            else:
                logger.error(f"Failed to post: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr
                }

        except Exception as e:
            logger.error(f"Failed to post content: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _log_post(self, content: str, platforms: List[str]):
        """Log post to social summary"""
        try:
            social_summary = SCRIPTS_PATH / "social_summary.py"

            for platform in platforms:
                subprocess.run(
                    [sys.executable, str(social_summary), 'log', platform, content],
                    capture_output=True,
                    timeout=10
                )
        except Exception as e:
            logger.warning(f"Failed to log post: {e}")

    async def get_analytics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get social media analytics

        Args:
            days: Number of days to analyze (default: 7)
        """
        try:
            days = int(params.get('days', 7))

            # Call social_summary.py
            social_summary = SCRIPTS_PATH / "social_summary.py"

            result = subprocess.run(
                [sys.executable, str(social_summary), 'summary'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse output
                output = result.stdout

                return {
                    "success": True,
                    "analytics": output,
                    "days": days,
                    "message": "Analytics retrieved"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to get analytics"
                }

        except Exception as e:
            logger.error(f"Failed to get analytics: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_recent_posts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get recent social media posts

        Args:
            count: Number of posts to retrieve (default: 10)
        """
        try:
            count = int(params.get('count', 10))

            # Call social_summary.py
            social_summary = SCRIPTS_PATH / "social_summary.py"

            result = subprocess.run(
                [sys.executable, str(social_summary), 'recent', str(count)],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "posts": result.stdout,
                    "count": count,
                    "message": f"Retrieved {count} recent posts"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to get recent posts"
                }

        except Exception as e:
            logger.error(f"Failed to get recent posts: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def schedule_post(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule a post for later

        Args:
            content: Post content
            scheduled_time: When to post (ISO format)
            platforms: List of platforms
        """
        try:
            content = params.get('content', '')
            scheduled_time = params.get('scheduled_time')
            platforms = params.get('platforms', ['linkedin'])

            if not content:
                return {
                    "success": False,
                    "error": "Content is required"
                }

            if not scheduled_time:
                return {
                    "success": False,
                    "error": "Scheduled time is required"
                }

            # For LinkedIn, use linkedin_auto_poster
            if 'linkedin' in platforms:
                linkedin_poster = SCRIPTS_PATH / "linkedin_auto_poster.py"

                result = subprocess.run(
                    [sys.executable, str(linkedin_poster), '--add', content],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    logger.info(f"Scheduled LinkedIn post")
                    return {
                        "success": True,
                        "platform": "linkedin",
                        "scheduled_time": scheduled_time,
                        "message": "Post scheduled successfully"
                    }
                else:
                    return {
                        "success": False,
                        "error": "Failed to schedule post"
                    }
            else:
                return {
                    "success": False,
                    "error": "Scheduling only supported for LinkedIn currently"
                }

        except Exception as e:
            logger.error(f"Failed to schedule post: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate social media content

        Args:
            topic: Topic to generate content about
            platform: Target platform
            tone: Content tone (professional, casual, inspirational)
        """
        try:
            topic = params.get('topic', '')
            platform = params.get('platform', 'linkedin')
            tone = params.get('tone', 'professional')

            if not topic:
                return {
                    "success": False,
                    "error": "Topic is required"
                }

            # Use social_poster.py to generate content
            social_poster = SCRIPTS_PATH / "social_poster.py"

            result = subprocess.run(
                [sys.executable, str(social_poster), 'generate', platform, topic],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                content = result.stdout.strip()

                return {
                    "success": True,
                    "content": content,
                    "platform": platform,
                    "topic": topic,
                    "message": "Content generated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to generate content"
                }

        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_platform_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get status of social media platform integrations

        Returns:
            Status of each platform (connected/not connected)
        """
        try:
            status = {}

            # Check for session files
            session_path = LOGS_PATH / "sessions"

            for platform in self.supported_platforms:
                session_file = session_path / f"{platform}_session.json"
                status[platform] = {
                    "connected": session_file.exists(),
                    "session_file": str(session_file) if session_file.exists() else None
                }

            return {
                "success": True,
                "platforms": status,
                "message": "Platform status retrieved"
            }

        except Exception as e:
            logger.error(f"Failed to get platform status: {e}")
            return {
                "success": False,
                "error": str(e)
            }


async def main():
    """Test the MCP server"""
    server = SocialMediaMCPServer()

    print("Testing Social Media MCP Server...")
    print("=" * 60)

    # Test platform status
    print("\n1. Getting platform status...")
    result = await server.get_platform_status({})
    print(f"Result: {result}")

    # Test analytics
    print("\n2. Getting analytics...")
    result = await server.get_analytics({'days': 7})
    print(f"Result: {result}")

    # Test recent posts
    print("\n3. Getting recent posts...")
    result = await server.get_recent_posts({'count': 5})
    print(f"Result: {result}")

    # Test content generation
    print("\n4. Generating content...")
    result = await server.generate_content({
        'topic': 'AI Automation',
        'platform': 'linkedin',
        'tone': 'professional'
    })
    print(f"Result: {result}")

    print("\n" + "=" * 60)
    print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
