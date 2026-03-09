"""
Orchestrator - Main coordinator for AI Employee
Monitors folders and triggers Claude Code for processing
"""

import os
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration
VAULT_PATH = Path(os.getenv('OBSIDIAN_VAULT_PATH', './AI_Employee_Vault'))
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
IN_PROGRESS = VAULT_PATH / 'In_Progress'
PENDING_APPROVAL = VAULT_PATH / 'Pending_Approval'
APPROVED = VAULT_PATH / 'Approved'
CHECK_INTERVAL = int(os.getenv('ORCHESTRATOR_CHECK_INTERVAL', '60'))

# Setup logging
(VAULT_PATH / 'Logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / 'Logs' / 'orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('Orchestrator')


class Orchestrator:
    def __init__(self):
        self.vault_path = VAULT_PATH
        self.ensure_folders()

    def ensure_folders(self):
        folders = ['Needs_Action', 'In_Progress', 'Pending_Approval', 'Approved',
                   'Done', 'Plans', 'Tasks', 'Logs', 'Documents', 'Invoices']
        for folder in folders:
            (self.vault_path / folder).mkdir(parents=True, exist_ok=True)

    def process_needs_action(self):
        action_files = list(NEEDS_ACTION.glob('*.md'))
        if not action_files:
            return

        logger.info(f"Processing {len(action_files)} items")
        IN_PROGRESS.mkdir(exist_ok=True)

        for file in action_files:
            file.rename(IN_PROGRESS / file.name)

        self.trigger_claude()

    def trigger_claude(self):
        try:
            prompt = "Process all files in /In_Progress using appropriate skills. Move to /Done when complete."
            subprocess.run(['claude', '--cwd', str(self.vault_path), prompt],
                         timeout=300, capture_output=True)
            logger.info("Claude processing completed")
        except Exception as e:
            logger.error(f"Error: {e}")

    def execute_approved(self):
        approved_files = list(APPROVED.glob('*.md'))
        if approved_files:
            logger.info(f"Executing {len(approved_files)} approved actions")
            try:
                subprocess.run(['claude', '--cwd', str(self.vault_path),
                              "Execute approved actions in /Approved"], timeout=300)
            except Exception as e:
                logger.error(f"Error: {e}")

    def run(self):
        logger.info("Orchestrator started")
        while True:
            try:
                self.process_needs_action()
                self.execute_approved()
                time.sleep(CHECK_INTERVAL)
            except KeyboardInterrupt:
                logger.info("Stopped")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(60)


if __name__ == '__main__':
    Orchestrator().run()
