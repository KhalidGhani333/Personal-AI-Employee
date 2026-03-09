#!/usr/bin/env python3
"""
Social Summary Skill
Logs social media posts to a centralized summary file
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Paths
VAULT_PATH = Path("AI_Employee_Vault")
REPORTS_PATH = VAULT_PATH / "Reports"
SOCIAL_LOG = REPORTS_PATH / "Social_Log.md"


class SocialSummary:
    """Manages social media post logging and summaries"""

    def __init__(self):
        self.reports_path = REPORTS_PATH
        self.social_log = SOCIAL_LOG
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure reports directory exists"""
        self.reports_path.mkdir(parents=True, exist_ok=True)

    def _initialize_log_file(self):
        """Initialize Social_Log.md if it doesn't exist"""
        if not self.social_log.exists():
            content = [
                "# Social Media Activity Log",
                "",
                "**Tracking all social media posts and activities**",
                "",
                "---",
                "",
            ]
            self.social_log.write_text('\n'.join(content), encoding='utf-8')

    def log_post(
        self,
        platform: str,
        content: str,
        date: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log a social media post

        Args:
            platform: Platform name (linkedin, twitter, facebook, etc.)
            content: Post content
            date: Post date (ISO format, defaults to now)
            metadata: Additional metadata (url, engagement, etc.)

        Returns:
            Dict with success status and details
        """
        # Initialize log file if needed
        self._initialize_log_file()

        # Use current date if not provided
        if date is None:
            date = datetime.now().isoformat()

        # Parse date for display
        try:
            dt = datetime.fromisoformat(date)
            display_date = dt.strftime("%B %d, %Y at %I:%M %p")
            date_key = dt.strftime("%Y-%m-%d")
        except:
            display_date = date
            date_key = date

        # Prepare metadata display
        metadata_lines = []
        if metadata:
            for key, value in metadata.items():
                metadata_lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")

        # Create log entry
        entry_lines = [
            "",
            f"## {platform.title()} Post - {display_date}",
            "",
            "**Content:**",
            f"> {content}",
            "",
        ]

        if metadata_lines:
            entry_lines.append("**Details:**")
            entry_lines.extend(metadata_lines)
            entry_lines.append("")

        entry_lines.append("---")
        entry_lines.append("")

        # Append to log file
        try:
            with open(self.social_log, 'a', encoding='utf-8') as f:
                f.write('\n'.join(entry_lines))

            return {
                "success": True,
                "platform": platform,
                "date": date,
                "log_file": str(self.social_log),
                "message": f"Post logged to {self.social_log.name}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to log post: {e}"
            }

    def get_summary(self, days: Optional[int] = None) -> Dict[str, Any]:
        """
        Get summary of social media activity

        Args:
            days: Number of days to include (None = all time)

        Returns:
            Dict with summary statistics
        """
        if not self.social_log.exists():
            return {
                "success": True,
                "total_posts": 0,
                "platforms": {},
                "message": "No social media activity logged yet"
            }

        try:
            content = self.social_log.read_text(encoding='utf-8')

            # Count posts by platform
            platforms = {}
            lines = content.split('\n')

            for line in lines:
                if line.startswith('## ') and ' Post - ' in line:
                    # Extract platform name
                    platform = line.split(' Post - ')[0].replace('## ', '').strip()
                    platforms[platform] = platforms.get(platform, 0) + 1

            total_posts = sum(platforms.values())

            return {
                "success": True,
                "total_posts": total_posts,
                "platforms": platforms,
                "log_file": str(self.social_log),
                "message": f"Total posts: {total_posts}"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get summary: {e}"
            }

    def get_recent_posts(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent posts

        Args:
            count: Number of recent posts to retrieve

        Returns:
            List of recent posts
        """
        if not self.social_log.exists():
            return []

        try:
            content = self.social_log.read_text(encoding='utf-8')
            lines = content.split('\n')

            posts = []
            current_post = None

            for line in lines:
                if line.startswith('## ') and ' Post - ' in line:
                    # Save previous post
                    if current_post:
                        posts.append(current_post)

                    # Start new post
                    parts = line.replace('## ', '').split(' Post - ')
                    current_post = {
                        "platform": parts[0].strip(),
                        "date": parts[1].strip() if len(parts) > 1 else "",
                        "content": ""
                    }

                elif current_post and line.startswith('> '):
                    # Extract content
                    current_post["content"] = line.replace('> ', '').strip()

            # Add last post
            if current_post:
                posts.append(current_post)

            # Return most recent posts
            return posts[-count:] if len(posts) > count else posts

        except Exception as e:
            return []


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: social_summary.py <command> [args...]")
        print("\nCommands:")
        print("  log <platform> <content>")
        print("  summary")
        print("  recent [count]")
        sys.exit(1)

    command = sys.argv[1]
    social = SocialSummary()

    try:
        if command == "log":
            if len(sys.argv) < 4:
                print("Error: Missing platform or content")
                print("Usage: social_summary.py log <platform> <content>")
                sys.exit(1)

            platform = sys.argv[2]
            content = ' '.join(sys.argv[3:])

            result = social.log_post(platform, content)

            if result["success"]:
                print(f"[OK] Post logged: {platform}")
                print(f"     Content: {content[:50]}...")
                print(f"     Log file: {result['log_file']}")
            else:
                print(f"[ERROR] Failed to log post: {result.get('error')}")
                sys.exit(1)

        elif command == "summary":
            result = social.get_summary()

            if result["success"]:
                print(f"\nSocial Media Summary:")
                print(f"  Total Posts: {result['total_posts']}")
                print(f"\n  By Platform:")
                for platform, count in sorted(result['platforms'].items()):
                    print(f"    - {platform}: {count} posts")
            else:
                print(f"✗ Failed to get summary: {result.get('error')}")
                sys.exit(1)

        elif command == "recent":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            posts = social.get_recent_posts(count)

            if posts:
                print(f"\nRecent Posts ({len(posts)}):\n")
                for i, post in enumerate(reversed(posts), 1):
                    print(f"{i}. [{post['platform']}] {post['date']}")
                    print(f"   {post['content'][:80]}...")
                    print()
            else:
                print("No posts found")

        else:
            print(f"Error: Unknown command '{command}'")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
