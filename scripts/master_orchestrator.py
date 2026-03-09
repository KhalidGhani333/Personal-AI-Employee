"""
Master Orchestrator - Complete AI Employee Automation System
=============================================================
Coordinates all watchers, processors, and automation workflows.
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import logging

# Configuration
SCRIPTS_PATH = Path(__file__).parent
VAULT_PATH = SCRIPTS_PATH.parent / "AI_Employee_Vault"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = LOGS_PATH / "system.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Script paths
SCRIPTS = {
    'gmail_watcher': SCRIPTS_PATH / 'gmail_watcher.py',
    'whatsapp_watcher': SCRIPTS_PATH / 'whatsapp_watcher.py',
    'linkedin_watcher': SCRIPTS_PATH / 'linkedin_watcher.py',
    'reply_generator': SCRIPTS_PATH / 'reply_generator.py',
    'reply_sender': SCRIPTS_PATH / 'reply_sender.py',
    'approval_executor': SCRIPTS_PATH / 'approval_executor.py',
    'ceo_briefing': SCRIPTS_PATH / 'ceo_briefing.py'
}

# Global state
running_processes = {}
process_stats = defaultdict(lambda: {'runs': 0, 'successes': 0, 'failures': 0, 'last_run': None})
shutdown_flag = threading.Event()


# ============================================================================
# PROCESS MANAGEMENT
# ============================================================================

class BackgroundProcess:
    """Manages a background subprocess"""

    def __init__(self, name, script_path, args=None, restart_on_failure=True):
        self.name = name
        self.script_path = script_path
        self.args = args or []
        self.restart_on_failure = restart_on_failure
        self.process = None
        self.thread = None
        self.running = False

    def start(self):
        """Start the background process"""
        if self.running:
            logger.warning(f"{self.name} is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info(f"Started background process: {self.name}")

    def _run(self):
        """Run the process in a loop"""
        while self.running and not shutdown_flag.is_set():
            try:
                cmd = [sys.executable, str(self.script_path)] + self.args

                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                stdout, stderr = self.process.communicate(timeout=300)
                returncode = self.process.returncode

                if returncode == 0:
                    process_stats[self.name]['successes'] += 1
                    logger.debug(f"{self.name} completed successfully")
                else:
                    process_stats[self.name]['failures'] += 1
                    logger.error(f"{self.name} failed with code {returncode}: {stderr}")

                    if not self.restart_on_failure:
                        self.running = False

            except subprocess.TimeoutExpired:
                logger.error(f"{self.name} timed out")
                if self.process:
                    self.process.kill()
                process_stats[self.name]['failures'] += 1

            except Exception as e:
                logger.error(f"{self.name} error: {e}")
                process_stats[self.name]['failures'] += 1

            finally:
                process_stats[self.name]['runs'] += 1
                process_stats[self.name]['last_run'] = datetime.now()

            # Wait before next run if still running
            if self.running:
                time.sleep(5)

    def stop(self):
        """Stop the background process"""
        self.running = False
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
        logger.info(f"Stopped background process: {self.name}")


def run_script_once(name, script_path, args=None, timeout=120):
    """Run a script once and return result"""
    try:
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        process_stats[name]['runs'] += 1
        process_stats[name]['last_run'] = datetime.now()

        if result.returncode == 0:
            process_stats[name]['successes'] += 1
            return True, result.stdout, result.stderr
        else:
            process_stats[name]['failures'] += 1
            return False, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        logger.error(f"{name} timed out after {timeout}s")
        process_stats[name]['failures'] += 1
        return False, "", "Timeout"

    except Exception as e:
        logger.error(f"{name} error: {e}")
        process_stats[name]['failures'] += 1
        return False, "", str(e)


# ============================================================================
# FOLDER MONITORING
# ============================================================================

class FolderMonitor:
    """Monitors folders for changes"""

    def __init__(self, folder_path, callback, check_interval=30):
        self.folder_path = Path(folder_path)
        self.callback = callback
        self.check_interval = check_interval
        self.last_file_count = 0
        self.running = False
        self.thread = None

    def start(self):
        """Start monitoring"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
        logger.info(f"Started folder monitor: {self.folder_path}")

    def _monitor(self):
        """Monitor folder for changes"""
        while self.running and not shutdown_flag.is_set():
            try:
                if self.folder_path.exists():
                    files = list(self.folder_path.glob("*.md"))
                    current_count = len(files)

                    if current_count != self.last_file_count:
                        logger.info(f"Folder change detected in {self.folder_path.name}: {current_count} files")
                        self.callback(self.folder_path, files)
                        self.last_file_count = current_count

            except Exception as e:
                logger.error(f"Folder monitor error: {e}")

            time.sleep(self.check_interval)

    def stop(self):
        """Stop monitoring"""
        self.running = False
        logger.info(f"Stopped folder monitor: {self.folder_path}")


# ============================================================================
# ORCHESTRATION WORKFLOWS
# ============================================================================

def run_watcher_cycle():
    """Run all watchers once"""
    logger.info("=" * 60)
    logger.info("WATCHER CYCLE")
    logger.info("=" * 60)

    # Gmail watcher
    logger.info("Checking Gmail...")
    success, stdout, stderr = run_script_once(
        'gmail_watcher',
        SCRIPTS['gmail_watcher'],
        ['--once']
    )
    if success:
        logger.info("[OK] Gmail check completed")
        if "new email" in stdout.lower():
            logger.info("  -> New emails detected")
    else:
        logger.error(f"[FAIL] Gmail check failed: {stderr[:100]}")

    # LinkedIn watcher
    logger.info("Checking LinkedIn...")
    success, stdout, stderr = run_script_once(
        'linkedin_watcher',
        SCRIPTS['linkedin_watcher'],
        ['--once']
    )
    if success:
        logger.info("[OK] LinkedIn check completed")
        if "new message" in stdout.lower():
            logger.info("  -> New messages detected")
    else:
        logger.warning(f"[WARN] LinkedIn check failed: {stderr[:100]}")

    # WhatsApp watcher (optional - can be unreliable)
    # Uncomment to enable
    # logger.info("Checking WhatsApp...")
    # success, stdout, stderr = run_script_once(
    #     'whatsapp_watcher',
    #     SCRIPTS['whatsapp_watcher'],
    #     ['--once']
    # )
    # if success:
    #     logger.info("[OK] WhatsApp check completed")
    # else:
    #     logger.warning(f"[WARN] WhatsApp check failed")

    logger.info("Watcher cycle completed\n")


def run_processing_cycle():
    """Run reply generation and sending"""
    logger.info("=" * 60)
    logger.info("PROCESSING CYCLE")
    logger.info("=" * 60)

    # Reply generator
    logger.info("Generating replies...")
    success, stdout, stderr = run_script_once(
        'reply_generator',
        SCRIPTS['reply_generator']
    )
    if success:
        logger.info("[OK] Reply generation completed")
        if "generated" in stdout.lower():
            logger.info("  -> Replies generated")
    else:
        logger.error(f"[FAIL] Reply generation failed: {stderr[:100]}")

    # Reply sender
    logger.info("Sending approved replies...")
    success, stdout, stderr = run_script_once(
        'reply_sender',
        SCRIPTS['reply_sender']
    )
    if success:
        logger.info("[OK] Reply sending completed")
        if "sent" in stdout.lower():
            logger.info("  -> Replies sent")
    else:
        logger.error(f"[FAIL] Reply sending failed: {stderr[:100]}")

    logger.info("Processing cycle completed\n")


def run_approval_cycle():
    """Process approved social media posts"""
    logger.info("=" * 60)
    logger.info("APPROVAL CYCLE")
    logger.info("=" * 60)

    logger.info("Processing approved posts...")
    success, stdout, stderr = run_script_once(
        'approval_executor',
        SCRIPTS['approval_executor'],
        ['process']
    )
    if success:
        logger.info("[OK] Approval processing completed")
        if "posted" in stdout.lower():
            logger.info("  -> Posts published")
    else:
        logger.warning(f"[WARN] Approval processing failed: {stderr[:100]}")

    logger.info("Approval cycle completed\n")


def run_briefing_cycle():
    """Generate CEO briefing (weekly)"""
    # Only run on Mondays
    if datetime.now().weekday() != 0:
        return

    logger.info("=" * 60)
    logger.info("BRIEFING CYCLE (Monday)")
    logger.info("=" * 60)

    logger.info("Generating CEO briefing...")
    success, stdout, stderr = run_script_once(
        'ceo_briefing',
        SCRIPTS['ceo_briefing'],
        ['weekly'],
        timeout=180
    )
    if success:
        logger.info("[OK] CEO briefing generated")
    else:
        logger.error(f"[FAIL] CEO briefing failed: {stderr[:100]}")

    logger.info("Briefing cycle completed\n")


def on_needs_action_change(folder, files):
    """Callback when Needs_Action folder changes"""
    logger.info(f"Needs_Action changed: {len(files)} files")
    # Trigger reply generation
    run_processing_cycle()


def on_approved_change(folder, files):
    """Callback when Approved folder changes"""
    logger.info(f"Approved changed: {len(files)} files")
    # Trigger approval executor
    run_approval_cycle()


# ============================================================================
# SYSTEM HEALTH
# ============================================================================

def log_system_health():
    """Log system health statistics"""
    logger.info("=" * 60)
    logger.info("SYSTEM HEALTH")
    logger.info("=" * 60)

    for name, stats in process_stats.items():
        success_rate = (stats['successes'] / stats['runs'] * 100) if stats['runs'] > 0 else 0
        last_run = stats['last_run'].strftime('%H:%M:%S') if stats['last_run'] else 'Never'

        logger.info(f"{name}:")
        logger.info(f"  Runs: {stats['runs']}")
        logger.info(f"  Success: {stats['successes']} ({success_rate:.1f}%)")
        logger.info(f"  Failures: {stats['failures']}")
        logger.info(f"  Last run: {last_run}")

    logger.info("=" * 60 + "\n")


# ============================================================================
# ORCHESTRATOR MODES
# ============================================================================

def run_full_automation(interval=180):
    """Run complete automation with all subsystems"""
    logger.info("=" * 60)
    logger.info("MASTER ORCHESTRATOR - FULL AUTOMATION MODE")
    logger.info("=" * 60)
    logger.info(f"Cycle interval: {interval}s ({interval//60} minutes)")
    logger.info("Press Ctrl+C to stop\n")

    # Start folder monitors
    needs_action_monitor = FolderMonitor(
        VAULT_PATH / "Needs_Action",
        on_needs_action_change,
        check_interval=30
    )
    needs_action_monitor.start()

    approved_monitor = FolderMonitor(
        VAULT_PATH / "Approved",
        on_approved_change,
        check_interval=30
    )
    approved_monitor.start()

    try:
        cycle_count = 0

        while not shutdown_flag.is_set():
            cycle_count += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"ORCHESTRATION CYCLE #{cycle_count}")
            logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"{'='*60}\n")

            # Run all cycles
            run_watcher_cycle()
            time.sleep(2)

            run_processing_cycle()
            time.sleep(2)

            run_approval_cycle()
            time.sleep(2)

            run_briefing_cycle()

            # Log health every 10 cycles
            if cycle_count % 10 == 0:
                log_system_health()

            # Wait for next cycle
            logger.info(f"Cycle #{cycle_count} completed")
            logger.info(f"Next cycle in {interval}s...\n")

            for _ in range(interval):
                if shutdown_flag.is_set():
                    break
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("\nShutdown signal received")

    finally:
        # Cleanup
        needs_action_monitor.stop()
        approved_monitor.stop()
        logger.info("Master Orchestrator stopped")


def run_background_mode():
    """Run watchers and approval executor as background processes"""
    logger.info("=" * 60)
    logger.info("MASTER ORCHESTRATOR - BACKGROUND MODE")
    logger.info("=" * 60)
    logger.info("Starting background processes...")
    logger.info("Press Ctrl+C to stop\n")

    # Start approval executor in watch mode
    approval_process = BackgroundProcess(
        'approval_executor_watch',
        SCRIPTS['approval_executor'],
        ['watch', '--interval', '30']
    )
    approval_process.start()
    running_processes['approval_executor'] = approval_process

    try:
        # Run watcher and processing cycles
        cycle_count = 0

        while not shutdown_flag.is_set():
            cycle_count += 1
            logger.info(f"\nCycle #{cycle_count} - {datetime.now().strftime('%H:%M:%S')}")

            run_watcher_cycle()
            time.sleep(2)

            run_processing_cycle()

            # Log health every 10 cycles
            if cycle_count % 10 == 0:
                log_system_health()

            # Wait 3 minutes
            logger.info("Waiting 3 minutes...\n")
            for _ in range(180):
                if shutdown_flag.is_set():
                    break
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("\nShutdown signal received")

    finally:
        # Stop background processes
        for name, process in running_processes.items():
            process.stop()
        logger.info("Master Orchestrator stopped")


def run_once():
    """Run one complete cycle"""
    logger.info("=" * 60)
    logger.info("MASTER ORCHESTRATOR - SINGLE CYCLE")
    logger.info("=" * 60 + "\n")

    run_watcher_cycle()
    time.sleep(2)

    run_processing_cycle()
    time.sleep(2)

    run_approval_cycle()
    time.sleep(2)

    run_briefing_cycle()

    log_system_health()

    logger.info("Single cycle completed")


# ============================================================================
# SIGNAL HANDLING
# ============================================================================

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"\nReceived signal {signum}")
    shutdown_flag.set()


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Master Orchestrator - Complete AI Employee Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  full        Full automation with folder monitoring (default)
  background  Background processes with periodic cycles
  once        Run one complete cycle and exit

Examples:
  # Full automation (recommended)
  python scripts/master_orchestrator.py

  # Background mode
  python scripts/master_orchestrator.py --mode background

  # Single cycle
  python scripts/master_orchestrator.py --mode once

  # Custom interval (5 minutes)
  python scripts/master_orchestrator.py --interval 300
        """
    )

    parser.add_argument(
        '--mode',
        choices=['full', 'background', 'once'],
        default='full',
        help='Orchestration mode (default: full)'
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=180,
        help='Cycle interval in seconds (default: 180 = 3 minutes)'
    )

    args = parser.parse_args()

    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run orchestrator
    try:
        if args.mode == 'once':
            run_once()
        elif args.mode == 'background':
            run_background_mode()
        else:  # full
            run_full_automation(args.interval)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
