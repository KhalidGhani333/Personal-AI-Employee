"""
File System Watcher - Monitors Inbox folder for file drops
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import shutil

load_dotenv()

VAULT_PATH = Path(os.getenv('OBSIDIAN_VAULT_PATH', './AI_Employee_Vault'))
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
WATCH_FOLDER = VAULT_PATH / 'Inbox'

(VAULT_PATH / 'Logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / 'Logs' / 'filesystem_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FileSystemWatcher')


class DropFolderHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.processing = set()

    def on_created(self, event):
        if event.is_directory:
            return

        source = Path(event.src_path)
        if source.name.startswith('.') or source.name.startswith('~'):
            return

        if source.name in self.processing:
            return

        logger.info(f"New file: {source.name}")
        self.processing.add(source.name)
        time.sleep(2)

        try:
            self.process_file(source)
        finally:
            self.processing.discard(source.name)

    def process_file(self, source: Path):
        try:
            if not source.exists():
                return

            file_size = source.stat().st_size
            file_ext = source.suffix.lower()
            file_type = self.get_file_type(file_ext)

            dest_folder = self.get_destination(file_type)
            dest_folder.mkdir(exist_ok=True)
            dest_path = dest_folder / source.name

            shutil.copy2(source, dest_path)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            action_file = NEEDS_ACTION / f"FILE_{source.stem}_{timestamp}.md"

            content = f"""---
type: file_drop
original_name: {source.name}
file_type: {file_type}
size_bytes: {file_size}
location: {dest_path}
received: {datetime.now().isoformat()}
status: pending
---

## File Information
- **Name:** {source.name}
- **Type:** {file_type}
- **Size:** {file_size / 1024:.2f} KB
- **Location:** `{dest_path}`

## Instructions for Claude
Process this file using /file-processor skill.
"""

            action_file.write_text(content, encoding='utf-8')
            logger.info(f"Created action file: {action_file.name}")

        except Exception as e:
            logger.error(f"Error processing {source}: {e}")

    def get_file_type(self, ext):
        if ext in ['.pdf', '.doc', '.docx', '.txt']:
            return 'document'
        elif ext in ['.csv', '.xlsx', '.xls']:
            return 'spreadsheet'
        elif ext in ['.jpg', '.jpeg', '.png']:
            return 'image'
        return 'other'

    def get_destination(self, file_type):
        if file_type == 'document':
            return VAULT_PATH / 'Documents'
        elif file_type == 'spreadsheet':
            return VAULT_PATH / 'Accounting'
        return VAULT_PATH / 'Files'


def run_watcher():
    logger.info("File System Watcher started")
    WATCH_FOLDER.mkdir(exist_ok=True)

    handler = DropFolderHandler()
    observer = Observer()
    observer.schedule(handler, str(WATCH_FOLDER), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopped")

    observer.join()


if __name__ == '__main__':
    run_watcher()
