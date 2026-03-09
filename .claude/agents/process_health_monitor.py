"""
Watchdog - Health monitor that restarts crashed processes
"""

import subprocess
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/watchdog.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Watchdog')

PROCESSES = {
    'gmail-watcher': 'python agents/gmail_watcher.py',
    'whatsapp-watcher': 'python agents/whatsapp_watcher.py',
    'file-watcher': 'python agents/filesystem_watcher.py',
    'orchestrator': 'python agents/orchestrator.py'
}


def is_process_running(process_name):
    """Check if PM2 process is running"""
    try:
        result = subprocess.run(
            ['pm2', 'list'],
            capture_output=True,
            text=True
        )
        return process_name in result.stdout and 'online' in result.stdout
    except:
        return False


def restart_process(name):
    """Restart a PM2 process"""
    logger.warning(f"{name} not running. Restarting...")
    try:
        subprocess.run(['pm2', 'restart', name])
        logger.info(f"Restarted {name}")
    except Exception as e:
        logger.error(f"Failed to restart {name}: {e}")


def main():
    logger.info("Watchdog started")

    while True:
        try:
            for name in PROCESSES.keys():
                if not is_process_running(name):
                    restart_process(name)

            time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info("Stopped")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(60)


if __name__ == '__main__':
    main()
