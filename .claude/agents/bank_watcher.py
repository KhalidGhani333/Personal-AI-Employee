"""
Bank Watcher - Monitors for bank transaction CSV files
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import csv

load_dotenv()

VAULT_PATH = Path(os.getenv('OBSIDIAN_VAULT_PATH', './AI_Employee_Vault'))
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
ACCOUNTING = VAULT_PATH / 'Accounting'
WATCH_FOLDER = ACCOUNTING / 'Import'
CHECK_INTERVAL = 300  # 5 minutes

(VAULT_PATH / 'Logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / 'Logs' / 'bank_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('BankWatcher')


class BankWatcher:
    def __init__(self):
        self.processed = set()

    def check_transactions(self):
        csv_files = list(WATCH_FOLDER.glob('*.csv'))

        for csv_file in csv_files:
            if csv_file.name not in self.processed:
                self.process_csv(csv_file)
                self.processed.add(csv_file.name)

    def process_csv(self, csv_file):
        try:
            transactions = []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    transactions.append(row)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"BANK_{csv_file.stem}_{timestamp}.md"
            action_file = NEEDS_ACTION / filename

            content = f"""---
type: bank_transactions
file: {csv_file.name}
transaction_count: {len(transactions)}
received: {datetime.now().isoformat()}
status: pending
---

## Bank Transactions Import

New bank statement with {len(transactions)} transactions.

## Instructions for Claude
1. Review all transactions
2. Categorize expenses
3. Flag unusual transactions
4. Update Dashboard
5. Use /file-processor skill

## File Location
`{csv_file}`
"""

            action_file.write_text(content, encoding='utf-8')
            logger.info(f"Created action file: {filename}")

        except Exception as e:
            logger.error(f"Error processing {csv_file}: {e}")

    def run(self):
        logger.info("Bank Watcher started")
        WATCH_FOLDER.mkdir(exist_ok=True)

        while True:
            try:
                self.check_transactions()
                time.sleep(CHECK_INTERVAL)
            except KeyboardInterrupt:
                logger.info("Stopped")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(60)


if __name__ == '__main__':
    BankWatcher().run()
