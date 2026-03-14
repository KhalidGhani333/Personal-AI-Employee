#!/usr/bin/env python3
"""
Ralph Wiggum Autonomous Loop
Autonomous task execution system with safety features
"""

import json
import time
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import re
import shutil

# Paths
VAULT_PATH = Path("AI_Employee_Vault")
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
NEEDS_APPROVAL = VAULT_PATH / "Needs_Approval"
DONE = VAULT_PATH / "Done"
PLANS = VAULT_PATH / "Plans"
LOGS_PATH = Path("Logs")
RALPH_LOG = LOGS_PATH / "ralph_wiggum.log"
RALPH_STATE = LOGS_PATH / "ralph_state.json"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(RALPH_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('RalphWiggum')

# Safety configuration
MAX_ITERATIONS = 5
RISKY_KEYWORDS = [
    'delete', 'remove', 'drop', 'truncate', 'destroy',
    'format', 'wipe', 'erase', 'reset', 'force',
    'sudo', 'admin', 'root', 'password', 'credential'
]


class TaskAnalyzer:
    """Analyzes tasks and creates execution plans"""

    def __init__(self):
        self.plans_path = PLANS
        self.plans_path.mkdir(parents=True, exist_ok=True)

    def analyze_task(self, task_file: Path) -> Dict[str, Any]:
        """Analyze task and extract key information"""
        try:
            content = task_file.read_text(encoding='utf-8')

            analysis = {
                "task_name": task_file.stem,
                "task_file": str(task_file),
                "content": content,
                "type": self._determine_task_type(content),
                "priority": self._determine_priority(content),
                "is_risky": self._is_risky(content),
                "estimated_steps": self._estimate_steps(content)
            }

            logger.info(f"Analyzed task: {analysis['task_name']} (Type: {analysis['type']}, Risky: {analysis['is_risky']})")
            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze task {task_file}: {e}")
            raise

    def _determine_task_type(self, content: str) -> str:
        """Determine task type from content"""
        content_lower = content.lower()

        if 'email' in content_lower or 'send' in content_lower and '@' in content_lower:
            return "email"
        elif 'linkedin' in content_lower or 'post' in content_lower or 'social' in content_lower:
            return "social_media"
        elif 'file' in content_lower or 'document' in content_lower:
            return "file_management"
        elif 'accounting' in content_lower or 'expense' in content_lower or 'income' in content_lower:
            return "accounting"
        elif 'report' in content_lower or 'summary' in content_lower:
            return "reporting"
        else:
            return "general"

    def _determine_priority(self, content: str) -> str:
        """Determine task priority"""
        content_lower = content.lower()

        if 'urgent' in content_lower or 'asap' in content_lower or 'critical' in content_lower:
            return "high"
        elif 'low priority' in content_lower or 'when possible' in content_lower:
            return "low"
        else:
            return "medium"

    def _is_risky(self, content: str) -> bool:
        """Check if task contains risky operations"""
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in RISKY_KEYWORDS)

    def _estimate_steps(self, content: str) -> int:
        """Estimate number of steps needed"""
        # Count action verbs and numbered lists
        action_verbs = ['send', 'create', 'update', 'delete', 'post', 'generate', 'analyze']
        steps = sum(1 for verb in action_verbs if verb in content.lower())

        # Check for numbered lists
        numbered_items = len(re.findall(r'^\d+\.', content, re.MULTILINE))

        return max(steps, numbered_items, 1)

    def create_plan(self, analysis: Dict[str, Any]) -> Path:
        """Create execution plan for task"""
        task_name = analysis['task_name']
        content = analysis['content']

        # Generate plan content
        plan_lines = [
            f"# Execution Plan: {task_name}",
            f"",
            f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Task Type:** {analysis['type']}",
            f"**Priority:** {analysis['priority']}",
            f"**Risky:** {'Yes' if analysis['is_risky'] else 'No'}",
            f"**Estimated Steps:** {analysis['estimated_steps']}",
            f"",
            f"---",
            f"",
            f"## Original Task",
            f"",
            content,
            f"",
            f"---",
            f"",
            f"## Execution Steps",
            f"",
        ]

        # Generate steps based on task type
        steps = self._generate_steps(analysis)
        for i, step in enumerate(steps, 1):
            plan_lines.append(f"### Step {i}: {step['title']}")
            plan_lines.append(f"")
            plan_lines.append(f"**Action:** {step['action']}")
            plan_lines.append(f"**Expected Result:** {step['expected']}")
            if step.get('requires_approval'):
                plan_lines.append(f"**⚠️ Requires Approval:** Yes")
            plan_lines.append(f"**Status:** Pending")
            plan_lines.append(f"")

        plan_lines.extend([
            f"---",
            f"",
            f"## Execution Log",
            f"",
            f"*Execution log will be updated here*",
            f""
        ])

        # Save plan
        plan_file = self.plans_path / f"Plan_{task_name}.md"
        plan_file.write_text('\n'.join(plan_lines), encoding='utf-8')

        logger.info(f"Created plan: {plan_file}")
        return plan_file

    def _generate_steps(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate execution steps based on task type"""
        task_type = analysis['type']
        is_risky = analysis['is_risky']

        steps = []

        if task_type == "email":
            steps = [
                {
                    "title": "Extract Email Details",
                    "action": "Parse recipient, subject, and body from task",
                    "expected": "Email details extracted successfully"
                },
                {
                    "title": "Validate Email",
                    "action": "Verify email address format and content",
                    "expected": "Email validated"
                },
                {
                    "title": "Send Email",
                    "action": "Use Business MCP to send email",
                    "expected": "Email sent successfully",
                    "requires_approval": is_risky
                }
            ]

        elif task_type == "social_media":
            steps = [
                {
                    "title": "Extract Post Content",
                    "action": "Parse post content and platform",
                    "expected": "Content extracted"
                },
                {
                    "title": "Validate Content",
                    "action": "Check content length and format",
                    "expected": "Content validated"
                },
                {
                    "title": "Post to Platform",
                    "action": "Use Social/Business MCP to post",
                    "expected": "Post published successfully",
                    "requires_approval": True  # Always require approval for social posts
                }
            ]

        elif task_type == "accounting":
            steps = [
                {
                    "title": "Extract Transaction Details",
                    "action": "Parse amount, type, and description",
                    "expected": "Transaction details extracted"
                },
                {
                    "title": "Validate Transaction",
                    "action": "Verify amount and type",
                    "expected": "Transaction validated"
                },
                {
                    "title": "Record Transaction",
                    "action": "Use accounting manager to record",
                    "expected": "Transaction recorded successfully"
                }
            ]

        elif task_type == "file_management":
            steps = [
                {
                    "title": "Identify Files",
                    "action": "Locate files to be managed",
                    "expected": "Files identified"
                },
                {
                    "title": "Perform Operation",
                    "action": "Execute file operation",
                    "expected": "Operation completed",
                    "requires_approval": is_risky
                }
            ]

        else:  # general
            steps = [
                {
                    "title": "Analyze Task",
                    "action": "Understand task requirements",
                    "expected": "Task understood"
                },
                {
                    "title": "Execute Task",
                    "action": "Perform required actions",
                    "expected": "Task completed",
                    "requires_approval": is_risky
                }
            ]

        return steps


class RalphWiggumLoop:
    """Autonomous task execution loop"""

    def __init__(self):
        self.analyzer = TaskAnalyzer()
        self.needs_action = NEEDS_ACTION
        self.needs_approval = NEEDS_APPROVAL
        self.done = DONE
        self.state_file = RALPH_STATE
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.needs_approval.mkdir(parents=True, exist_ok=True)
        self.done.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> Dict[str, Any]:
        """Load Ralph's state"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                pass
        return {
            "current_task": None,
            "iteration": 0,
            "started_at": None,
            "completed_tasks": [],
            "failed_tasks": []
        }

    def _save_state(self, state: Dict[str, Any]):
        """Save Ralph's state"""
        try:
            self.state_file.write_text(json.dumps(state, indent=2))
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def get_next_task(self) -> Optional[Path]:
        """Get next task from Needs_Action"""
        if not self.needs_action.exists():
            return None

        tasks = sorted(self.needs_action.glob("*.md"))
        return tasks[0] if tasks else None

    def request_approval(self, task_name: str, action: str, reason: str) -> Path:
        """Request human approval for risky operation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        approval_file = self.needs_approval / f"APPROVAL_{timestamp}_{task_name}.md"

        content = f"""---
action: {action}
task: {task_name}
created: {datetime.now().isoformat()}
status: pending
---

# Approval Required

## Task
{task_name}

## Action
{action}

## Reason
{reason}

## Decision Required
Please review and update the status above to either:
- `status: approved`
- `status: rejected`

---

*Generated by Ralph Wiggum Autonomous Loop*
"""

        approval_file.write_text(content, encoding='utf-8')
        logger.info(f"Approval requested: {approval_file}")
        return approval_file

    def check_approval(self, approval_file: Path) -> Optional[str]:
        """Check if approval has been granted"""
        if not approval_file.exists():
            return None

        try:
            content = approval_file.read_text(encoding='utf-8')
            if 'status: approved' in content:
                return "approved"
            elif 'status: rejected' in content:
                return "rejected"
            return "pending"
        except:
            return None

    def _execute_email_task(self, task_analysis: Dict[str, Any]) -> bool:
        """Execute email sending task"""
        try:
            content = task_analysis['content']

            # Extract email details - handle both direct email and email_reply types
            to_match = re.search(r'(?:Send email to|To):\s*(.+)', content, re.IGNORECASE)

            # If not found, check if it's an email_reply type (extract from From field)
            if not to_match:
                from_match = re.search(r'\*\*From:\*\*\s*(.+)', content)
                if from_match:
                    to_match = from_match

            subject_match = re.search(r'\*\*Subject:\*\*\s*(.+)', content)
            body_match = re.search(r'\*\*Body:\*\*\s*\n(.+?)(?:\n\n---|\Z)', content, re.DOTALL)

            if not to_match:
                logger.error("Could not extract recipient email")
                return False

            to_email = to_match.group(1).strip()
            # Clean email address (remove < > if present)
            to_email = to_email.replace('<', '').replace('>', '').strip()

            subject = subject_match.group(1).strip() if subject_match else "Message from AI Employee"
            body = body_match.group(1).strip() if body_match else content

            # Call gmail-send script
            gmail_send = Path(__file__).parent.parent / ".claude" / "skills" / "gmail-send" / "scripts" / "send_email.py"

            result = subprocess.run(
                [sys.executable, str(gmail_send), '--to', to_email, '--subject', subject, '--body', body],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Email execution failed: {e}")
            return False

    def _execute_social_task(self, task_analysis: Dict[str, Any]) -> bool:
        """Execute social media posting task"""
        try:
            content = task_analysis['content']

            # Determine platform
            platform = None
            if 'linkedin' in content.lower():
                platform = 'linkedin'
            elif 'twitter' in content.lower():
                platform = 'twitter'
            elif 'facebook' in content.lower():
                platform = 'facebook'

            if not platform:
                logger.error("Could not determine social media platform")
                return False

            # Extract post content
            post_match = re.search(r'(?:Post|Content):\s*\n(.+?)(?:\n\n---|\Z)', content, re.DOTALL)
            if not post_match:
                logger.error("Could not extract post content")
                return False

            post_content = post_match.group(1).strip()

            # Call appropriate poster script
            if platform == 'linkedin':
                script = Path(__file__).parent / "linkedin_poster.py"
                result = subprocess.run(
                    [sys.executable, str(script), '--content', post_content],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            else:
                script = Path(__file__).parent / "social_poster.py"
                result = subprocess.run(
                    [sys.executable, str(script), '--platform', platform, '--content', post_content],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

            if result.returncode == 0:
                logger.info(f"Posted to {platform} successfully")
                return True
            else:
                logger.error(f"Failed to post: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Social media execution failed: {e}")
            return False

    def execute_step(self, step: Dict[str, Any], task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single step"""
        logger.info(f"Executing step: {step['title']}")

        # Check if approval required
        if step.get('requires_approval'):
            # Check for existing approval files first
            task_name = task_analysis['task_name']
            existing_approvals = list(self.needs_approval.glob(f"APPROVAL_*_{task_name}.md"))

            approval_file = None
            approval_status = None

            # Check if any existing approval is approved
            for existing_file in existing_approvals:
                status = self.check_approval(existing_file)
                if status == "approved":
                    logger.info(f"Found approved approval: {existing_file.name}")
                    # Move approval to Done and continue execution
                    done_file = self.done / existing_file.name
                    existing_file.rename(done_file)
                    approval_status = "approved"
                    break
                elif status == "rejected":
                    logger.info(f"Task rejected: {existing_file.name}")
                    return {
                        "success": False,
                        "status": "rejected",
                        "message": "Task rejected by human"
                    }
                elif status == "pending":
                    approval_file = existing_file
                    approval_status = "pending"

            # If no approved status found and no pending approval, create new request
            if approval_status != "approved":
                if not approval_file:
                    approval_file = self.request_approval(
                        task_analysis['task_name'],
                        step['action'],
                        "This operation requires human approval for safety"
                    )

                logger.info(f"Waiting for approval: {approval_file.name}")
                return {
                    "success": False,
                    "status": "awaiting_approval",
                    "approval_file": str(approval_file),
                    "message": "Waiting for human approval"
                }

            # If approved, continue with execution
            logger.info("Approval granted, continuing execution...")

        # Execute based on task type
        try:
            logger.info(f"Action: {step['action']}")

            task_type = task_analysis.get('type', 'general')
            success = False

            # Execute actual tasks based on type
            if task_type == 'email' and 'Send Email' in step['title']:
                logger.info("Executing email sending...")
                success = self._execute_email_task(task_analysis)
            elif task_type == 'social_media' and 'Post to Platform' in step['title']:
                logger.info("Executing social media posting...")
                success = self._execute_social_task(task_analysis)
            else:
                # For other steps, just simulate
                time.sleep(1)
                success = True

            if success:
                return {
                    "success": True,
                    "status": "completed",
                    "message": f"Step completed: {step['title']}"
                }
            else:
                return {
                    "success": False,
                    "status": "failed",
                    "message": f"Step failed: {step['title']}"
                }

        except Exception as e:
            logger.error(f"Step failed: {e}")
            return {
                "success": False,
                "status": "failed",
                "error": str(e)
            }

    def process_task(self, task_file: Path) -> Dict[str, Any]:
        """Process a single task through the autonomous loop"""
        logger.info(f"Processing task: {task_file.name}")

        state = self._load_state()
        state["current_task"] = str(task_file)
        state["iteration"] = 0
        state["started_at"] = datetime.now().isoformat()
        self._save_state(state)

        try:
            # Step 1: Analyze task
            logger.info("Step 1: Analyzing task...")
            analysis = self.analyzer.analyze_task(task_file)

            # Step 2: Create plan
            logger.info("Step 2: Creating execution plan...")
            plan_file = self.analyzer.create_plan(analysis)

            # Step 3: Execute steps
            logger.info("Step 3: Executing steps...")
            steps = self.analyzer._generate_steps(analysis)

            for i, step in enumerate(steps, 1):
                if state["iteration"] >= MAX_ITERATIONS:
                    logger.warning(f"Max iterations ({MAX_ITERATIONS}) reached")
                    return {
                        "success": False,
                        "reason": "max_iterations",
                        "message": f"Task exceeded maximum iterations ({MAX_ITERATIONS})"
                    }

                state["iteration"] += 1
                self._save_state(state)

                result = self.execute_step(step, analysis)

                if result["status"] == "awaiting_approval":
                    logger.info("Task paused for approval")
                    return {
                        "success": False,
                        "reason": "awaiting_approval",
                        "approval_file": result["approval_file"],
                        "message": "Task paused pending human approval"
                    }

                if not result["success"]:
                    logger.error(f"Step {i} failed: {result.get('error')}")
                    return {
                        "success": False,
                        "reason": "step_failed",
                        "step": i,
                        "error": result.get("error")
                    }

                logger.info(f"Step {i}/{len(steps)} completed")

            # Step 4: Move to Done
            logger.info("Step 4: Moving task to Done...")
            done_file = self.done / task_file.name
            shutil.move(str(task_file), str(done_file))

            # Update state
            state["completed_tasks"].append({
                "task": task_file.name,
                "completed_at": datetime.now().isoformat(),
                "iterations": state["iteration"]
            })
            state["current_task"] = None
            self._save_state(state)

            logger.info(f"Task completed: {task_file.name}")
            return {
                "success": True,
                "iterations": state["iteration"],
                "message": f"Task completed successfully in {state['iteration']} iterations"
            }

        except Exception as e:
            logger.error(f"Task processing failed: {e}")
            state["failed_tasks"].append({
                "task": task_file.name,
                "failed_at": datetime.now().isoformat(),
                "error": str(e)
            })
            self._save_state(state)

            return {
                "success": False,
                "reason": "exception",
                "error": str(e)
            }

    def run_once(self) -> Dict[str, Any]:
        """Run one iteration of the loop"""
        logger.info("Ralph Wiggum Loop: Checking for tasks...")

        task = self.get_next_task()
        if not task:
            logger.info("No tasks found")
            return {"success": True, "message": "No tasks to process"}

        return self.process_task(task)

    def run_continuous(self, check_interval: int = 60):
        """Run continuously, checking for tasks"""
        logger.info("Ralph Wiggum Loop: Starting continuous mode")

        while True:
            try:
                self.run_once()
                time.sleep(check_interval)
            except KeyboardInterrupt:
                logger.info("Stopped by user")
                break
            except Exception as e:
                logger.error(f"Loop error: {e}")
                time.sleep(check_interval)


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        loop = RalphWiggumLoop()
        loop.run_continuous()
    else:
        loop = RalphWiggumLoop()
        result = loop.run_once()
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
