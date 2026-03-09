"""
CEO Briefing System - Business Intelligence Reports
====================================================
Analyzes AI Employee activities and generates executive briefings.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
NEEDS_APPROVAL = VAULT_PATH / "Needs_Approval"
DONE = VAULT_PATH / "Done"
APPROVED = VAULT_PATH / "Approved"
LOGS_PATH = VAULT_PATH / "Logs"
BRIEFINGS = VAULT_PATH / "Briefings"

# Ensure directories exist
BRIEFINGS.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = LOGS_PATH / "ceo_briefing.log"
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
# DATA COLLECTION FUNCTIONS
# ============================================================================

def count_files_by_type(folder, days=7):
    """Count files by type in a folder within date range"""
    if not folder.exists():
        return {}

    cutoff_date = datetime.now() - timedelta(days=days)
    counts = defaultdict(int)

    for file in folder.glob("*.md"):
        try:
            # Get file modification time
            mtime = datetime.fromtimestamp(file.stat().st_mtime)

            if mtime >= cutoff_date:
                # Determine type from filename or content
                if 'email' in file.name.lower():
                    counts['email'] += 1
                elif 'whatsapp' in file.name.lower():
                    counts['whatsapp'] += 1
                elif 'linkedin' in file.name.lower():
                    counts['linkedin'] += 1
                elif 'twitter' in file.name.lower() or 'post_twitter' in file.name.lower():
                    counts['twitter'] += 1
                elif 'facebook' in file.name.lower() or 'post_facebook' in file.name.lower():
                    counts['facebook'] += 1
                elif 'instagram' in file.name.lower() or 'post_instagram' in file.name.lower():
                    counts['instagram'] += 1
                else:
                    counts['other'] += 1
        except:
            pass

    return dict(counts)


def analyze_log_file(log_file, days=7):
    """Analyze log file for activity metrics"""
    if not log_file.exists():
        return {}

    cutoff_date = datetime.now() - timedelta(days=days)
    metrics = {
        'total_entries': 0,
        'errors': 0,
        'successes': 0,
        'activities': []
    }

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    # Parse timestamp
                    if line.startswith('['):
                        timestamp_str = line[1:20]
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

                        if timestamp >= cutoff_date:
                            metrics['total_entries'] += 1

                            if 'ERROR' in line:
                                metrics['errors'] += 1
                            elif 'SUCCESS' in line or 'completed' in line.lower():
                                metrics['successes'] += 1

                            # Extract activity type
                            if 'email' in line.lower():
                                metrics['activities'].append('email')
                            elif 'whatsapp' in line.lower():
                                metrics['activities'].append('whatsapp')
                            elif 'linkedin' in line.lower():
                                metrics['activities'].append('linkedin')
                            elif 'twitter' in line.lower():
                                metrics['activities'].append('twitter')
                            elif 'facebook' in line.lower():
                                metrics['activities'].append('facebook')
                except:
                    continue
    except:
        pass

    return metrics


def get_pending_tasks():
    """Get count and details of pending tasks"""
    pending = {
        'needs_action': 0,
        'needs_approval': 0,
        'total': 0,
        'by_type': {}
    }

    if NEEDS_ACTION.exists():
        files = list(NEEDS_ACTION.glob("*.md"))
        pending['needs_action'] = len(files)

        for file in files:
            if 'email' in file.name.lower():
                pending['by_type']['email'] = pending['by_type'].get('email', 0) + 1
            elif 'whatsapp' in file.name.lower():
                pending['by_type']['whatsapp'] = pending['by_type'].get('whatsapp', 0) + 1
            elif 'linkedin' in file.name.lower():
                pending['by_type']['linkedin'] = pending['by_type'].get('linkedin', 0) + 1

    if NEEDS_APPROVAL.exists():
        files = list(NEEDS_APPROVAL.glob("*.md"))
        pending['needs_approval'] = len(files)

    pending['total'] = pending['needs_action'] + pending['needs_approval']

    return pending


def get_completed_tasks(days=7):
    """Get count of completed tasks"""
    completed = count_files_by_type(DONE, days)
    return completed


def analyze_social_media_activity(days=7):
    """Analyze social media posting activity"""
    activity = {
        'posts_created': 0,
        'posts_approved': 0,
        'posts_published': 0,
        'by_platform': {}
    }

    # Check approved posts
    if APPROVED.exists():
        approved_files = count_files_by_type(APPROVED, days)
        activity['posts_approved'] = sum(approved_files.values())
        activity['by_platform'] = approved_files

    # Check done posts (published)
    if DONE.exists():
        done_files = list(DONE.glob("POST_*.md"))
        cutoff_date = datetime.now() - timedelta(days=days)

        for file in done_files:
            try:
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime >= cutoff_date:
                    activity['posts_published'] += 1
            except:
                pass

    return activity


def detect_opportunities():
    """Detect business opportunities from tasks and messages"""
    opportunities = []

    # Keywords that indicate opportunities
    opportunity_keywords = [
        'partnership', 'collaboration', 'project', 'opportunity',
        'interested', 'proposal', 'meeting', 'discuss', 'work together',
        'hire', 'contract', 'business', 'investment'
    ]

    # Check recent tasks
    for folder in [NEEDS_ACTION, NEEDS_APPROVAL, DONE]:
        if not folder.exists():
            continue

        for file in folder.glob("*.md"):
            try:
                # Only check recent files (last 7 days)
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if datetime.now() - mtime > timedelta(days=7):
                    continue

                content = file.read_text(encoding='utf-8').lower()

                for keyword in opportunity_keywords:
                    if keyword in content:
                        # Extract context
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if keyword in line:
                                context = ' '.join(lines[max(0, i-1):min(len(lines), i+2)])
                                opportunities.append({
                                    'keyword': keyword,
                                    'source': file.name,
                                    'context': context[:150] + '...' if len(context) > 150 else context
                                })
                                break
                        break
            except:
                continue

    return opportunities[:5]  # Return top 5


def detect_bottlenecks():
    """Detect bottlenecks in workflow"""
    bottlenecks = []

    # Check for old pending tasks
    if NEEDS_ACTION.exists():
        old_tasks = []
        for file in NEEDS_ACTION.glob("*.md"):
            try:
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                age_days = (datetime.now() - mtime).days
                if age_days > 3:
                    old_tasks.append((file.name, age_days))
            except:
                pass

        if old_tasks:
            bottlenecks.append(f"{len(old_tasks)} tasks pending for more than 3 days")

    # Check for many pending approvals
    if NEEDS_APPROVAL.exists():
        approval_count = len(list(NEEDS_APPROVAL.glob("*.md")))
        if approval_count > 10:
            bottlenecks.append(f"{approval_count} items waiting for approval")

    # Check error rate in logs
    for log_file in LOGS_PATH.glob("*.log"):
        try:
            metrics = analyze_log_file(log_file, days=7)
            if metrics.get('errors', 0) > 10:
                bottlenecks.append(f"High error rate in {log_file.name}: {metrics['errors']} errors")
        except:
            pass

    return bottlenecks


def generate_ai_recommendations(data):
    """Generate AI-powered recommendations based on data"""
    recommendations = []

    # Recommendation based on pending tasks
    if data['pending']['total'] > 5:
        recommendations.append(
            f"Review and clear pending tasks backlog ({data['pending']['total']} items)"
        )

    # Recommendation based on social media activity
    if data['social_media']['posts_approved'] > 0 and data['social_media']['posts_published'] == 0:
        recommendations.append(
            "Approved social media posts are ready - run approval executor to publish"
        )

    # Recommendation based on communication volume
    email_count = data['completed'].get('email', 0)
    if email_count > 20:
        recommendations.append(
            f"High email volume ({email_count} emails) - consider setting up auto-responses"
        )

    # Recommendation based on opportunities
    if len(data['opportunities']) > 0:
        recommendations.append(
            f"Follow up on {len(data['opportunities'])} detected opportunities"
        )

    # Recommendation based on bottlenecks
    if len(data['bottlenecks']) > 0:
        recommendations.append(
            "Address workflow bottlenecks to improve efficiency"
        )

    # General recommendations
    if data['social_media']['posts_published'] < 3:
        recommendations.append(
            "Post LinkedIn content about AI automation to maintain online presence"
        )

    if not recommendations:
        recommendations.append(
            "Operations running smoothly - continue current practices"
        )

    return recommendations


# ============================================================================
# REPORT GENERATION FUNCTIONS
# ============================================================================

def generate_daily_summary():
    """Generate daily activity summary"""
    logger.info("Generating daily summary...")

    date_str = datetime.now().strftime("%Y-%m-%d")

    # Collect data for today (last 24 hours)
    data = {
        'date': date_str,
        'completed': get_completed_tasks(days=1),
        'pending': get_pending_tasks(),
        'social_media': analyze_social_media_activity(days=1)
    }

    # Generate report
    report = f"""# Daily Summary - {date_str}

## Activity Overview

**Tasks Completed Today:**
"""

    if data['completed']:
        for task_type, count in data['completed'].items():
            report += f"- {task_type.capitalize()}: {count}\n"
    else:
        report += "- No tasks completed today\n"

    report += f"""
**Pending Tasks:**
- Needs Action: {data['pending']['needs_action']}
- Needs Approval: {data['pending']['needs_approval']}
- Total: {data['pending']['total']}

**Social Media:**
- Posts Approved: {data['social_media']['posts_approved']}
- Posts Published: {data['social_media']['posts_published']}

---

*Generated by CEO Briefing System*
*{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

    # Save report
    filename = f"DAILY_SUMMARY_{date_str}.md"
    filepath = BRIEFINGS / filename
    filepath.write_text(report, encoding='utf-8')

    logger.info(f"Daily summary saved: {filename}")
    return filepath


def generate_weekly_report():
    """Generate comprehensive weekly CEO briefing"""
    logger.info("Generating weekly CEO briefing...")

    date_str = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Collect comprehensive data
    data = {
        'date': date_str,
        'week_start': week_start,
        'completed': get_completed_tasks(days=7),
        'pending': get_pending_tasks(),
        'social_media': analyze_social_media_activity(days=7),
        'opportunities': detect_opportunities(),
        'bottlenecks': detect_bottlenecks()
    }

    # Add AI recommendations
    data['recommendations'] = generate_ai_recommendations(data)

    # Calculate totals
    total_completed = sum(data['completed'].values())

    # Generate report
    report = f"""# CEO Weekly Briefing
## Week of {week_start} to {date_str}

---

## Activity Summary

### Emails Processed
**Total**: {data['completed'].get('email', 0)}

### WhatsApp Messages
**Total**: {data['completed'].get('whatsapp', 0)}

### LinkedIn Activity
**Messages**: {data['completed'].get('linkedin', 0)}
**Leads**: {data['completed'].get('linkedin', 0)}

### Social Media Posts
- LinkedIn: {data['social_media']['by_platform'].get('linkedin', 0)}
- Twitter: {data['social_media']['by_platform'].get('twitter', 0)}
- Facebook: {data['social_media']['by_platform'].get('facebook', 0)}
- Instagram: {data['social_media']['by_platform'].get('instagram', 0)}

---

## Opportunities Detected

"""

    if data['opportunities']:
        for i, opp in enumerate(data['opportunities'], 1):
            report += f"### {i}. {opp['keyword'].capitalize()}\n"
            report += f"**Source**: {opp['source']}\n"
            report += f"**Context**: {opp['context']}\n\n"
    else:
        report += "No significant opportunities detected this week.\n"

    report += "\n---\n\n## Communication Trends\n\n"

    if data['completed']:
        # Calculate percentages
        email_pct = (data['completed'].get('email', 0) / total_completed * 100) if total_completed > 0 else 0
        whatsapp_pct = (data['completed'].get('whatsapp', 0) / total_completed * 100) if total_completed > 0 else 0
        linkedin_pct = (data['completed'].get('linkedin', 0) / total_completed * 100) if total_completed > 0 else 0

        report += f"- Email: {email_pct:.1f}% of communications\n"
        report += f"- WhatsApp: {whatsapp_pct:.1f}% of communications\n"
        report += f"- LinkedIn: {linkedin_pct:.1f}% of communications\n"

        # Identify primary channel
        primary_channel = max(data['completed'].items(), key=lambda x: x[1])[0] if data['completed'] else 'None'
        report += f"\n**Primary Channel**: {primary_channel.capitalize()}\n"
    else:
        report += "Insufficient data for trend analysis.\n"

    report += "\n---\n\n## Tasks Completed\n\n"
    report += f"**Total**: {total_completed}\n\n"

    if data['completed']:
        for task_type, count in sorted(data['completed'].items(), key=lambda x: x[1], reverse=True):
            report += f"- {task_type.capitalize()}: {count}\n"

    report += "\n---\n\n## Risks\n\n"

    if data['bottlenecks']:
        for bottleneck in data['bottlenecks']:
            report += f"- {bottleneck}\n"
    else:
        report += "- No significant risks detected\n"

    if data['pending']['total'] > 10:
        report += f"- {data['pending']['total']} tasks pending approval\n"

    report += "\n---\n\n## AI Recommendations\n\n"

    for i, rec in enumerate(data['recommendations'], 1):
        report += f"{i}. {rec}\n"

    report += f"""

---

*Generated by CEO Briefing System*
*{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*Powered by Personal AI Employee*
"""

    # Save report
    filename = f"CEO_BRIEFING_{date_str}.md"
    filepath = BRIEFINGS / filename
    filepath.write_text(report, encoding='utf-8')

    logger.info(f"Weekly briefing saved: {filename}")
    return filepath


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='CEO Briefing System - Business Intelligence Reports'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Daily command
    daily_parser = subparsers.add_parser('daily', help='Generate daily summary')

    # Weekly command
    weekly_parser = subparsers.add_parser('weekly', help='Generate weekly CEO briefing')

    # All command
    all_parser = subparsers.add_parser('all', help='Generate all reports')

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("CEO BRIEFING SYSTEM")
    logger.info("=" * 60)

    if args.command == 'daily':
        filepath = generate_daily_summary()
        logger.info(f"\nDaily summary generated: {filepath}")
        print(f"\n[SUCCESS] Daily summary saved to: {filepath}")

    elif args.command == 'weekly':
        filepath = generate_weekly_report()
        logger.info(f"\nWeekly briefing generated: {filepath}")
        print(f"\n[SUCCESS] Weekly briefing saved to: {filepath}")

    elif args.command == 'all':
        daily_path = generate_daily_summary()
        weekly_path = generate_weekly_report()

        logger.info("\nAll reports generated:")
        logger.info(f"  - Daily: {daily_path}")
        logger.info(f"  - Weekly: {weekly_path}")

        print(f"\n[SUCCESS] All reports generated:")
        print(f"  - Daily: {daily_path}")
        print(f"  - Weekly: {weekly_path}")

    else:
        parser.print_help()

    logger.info("\n" + "=" * 60)
    logger.info(f"Reports location: {BRIEFINGS}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
