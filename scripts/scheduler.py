#!/usr/bin/env python3
"""
Scheduler for AI Employee
Runs scheduled tasks like CEO briefing
"""

import schedule
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Scheduler')

# Paths
SCRIPTS_PATH = Path(__file__).parent


def run_ceo_briefing():
    """Run CEO briefing generation"""
    logger.info("Running CEO briefing generation...")

    try:
        result = subprocess.run(
            ['python', str(SCRIPTS_PATH / 'ceo_briefing.py')],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            logger.info("CEO briefing generated successfully")
        else:
            logger.error(f"CEO briefing failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        logger.error("CEO briefing timed out")
    except Exception as e:
        logger.error(f"CEO briefing error: {e}")


def run_accounting_summary():
    """Run accounting monthly summary"""
    logger.info("Running accounting summary...")

    try:
        result = subprocess.run(
            ['python', str(SCRIPTS_PATH / 'accounting_manager.py'), 'monthly-summary'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            logger.info("Accounting summary completed")
        else:
            logger.error(f"Accounting summary failed: {result.stderr}")

    except Exception as e:
        logger.error(f"Accounting summary error: {e}")


def run_ralph_wiggum():
    """Run Ralph Wiggum autonomous loop"""
    logger.info("Running Ralph Wiggum Loop...")

    try:
        result = subprocess.run(
            ['python', str(SCRIPTS_PATH / 'ralph_wiggum_loop.py')],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )

        if result.returncode == 0:
            logger.info("Ralph Wiggum completed")
            if result.stdout:
                logger.info(f"Result: {result.stdout}")
        else:
            logger.error(f"Ralph Wiggum failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        logger.error("Ralph Wiggum timed out")
    except Exception as e:
        logger.error(f"Ralph Wiggum error: {e}")


def setup_schedules():
    """Setup all scheduled tasks"""

    # CEO Briefing - Every Monday at 9:00 AM
    schedule.every().monday.at("09:00").do(run_ceo_briefing)
    logger.info("Scheduled: CEO Briefing - Every Monday at 9:00 AM")

    # Accounting Summary - First day of month at 8:00 AM
    schedule.every().day.at("08:00").do(run_accounting_summary)
    logger.info("Scheduled: Accounting Summary - Daily at 8:00 AM (runs on 1st)")

    # Ralph Wiggum Loop - Every 15 minutes
    schedule.every(15).minutes.do(run_ralph_wiggum)
    logger.info("Scheduled: Ralph Wiggum Loop - Every 15 minutes")

    # You can add more scheduled tasks here
    # Examples:
    # schedule.every().day.at("10:00").do(some_function)
    # schedule.every().hour.do(another_function)
    # schedule.every(10).minutes.do(frequent_task)


def main():
    """Main scheduler loop"""
    logger.info("Starting AI Employee Scheduler...")

    # Setup schedules
    setup_schedules()

    # Show next run times
    logger.info("\nScheduled Jobs:")
    for job in schedule.get_jobs():
        logger.info(f"  - {job}")

    logger.info("\nScheduler running. Press Ctrl+C to stop.")

    # Run scheduler loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        logger.info("\nScheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")


if __name__ == "__main__":
    main()
