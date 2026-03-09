"""
Reply Generator (Orchestrator) - AI-Powered Reply Generation
=============================================================
Analyzes incoming messages and generates appropriate replies using intelligent templates.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
NEEDS_APPROVAL = VAULT_PATH / "Needs_Approval"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
NEEDS_ACTION.mkdir(parents=True, exist_ok=True)
NEEDS_APPROVAL.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)


def analyze_message(content):
    """Analyze message content and extract key information"""
    content_lower = content.lower()

    # Determine message type
    if 'email' in content_lower:
        msg_type = 'email'
    elif 'whatsapp' in content_lower:
        msg_type = 'whatsapp'
    else:
        msg_type = 'general'

    # Extract sender
    sender = "Unknown"
    for line in content.split('\n'):
        if line.startswith('**From:**'):
            sender = line.replace('**From:**', '').strip()
            break

    # Extract original message
    original_msg = ""
    in_message_section = False
    for line in content.split('\n'):
        if '**Message:**' in line:
            in_message_section = True
            continue
        if in_message_section:
            if line.startswith('---') or line.startswith('##'):
                break
            original_msg += line + '\n'

    return {
        'type': msg_type,
        'sender': sender,
        'original_message': original_msg.strip()
    }


def generate_reply(analysis):
    """Generate appropriate reply using intelligent templates (similar to social_poster.py)"""
    original = analysis['original_message']
    sender = analysis['sender']
    msg_type = analysis['type']

    original_lower = original.lower()

    print(f"[INFO] Generating reply for {sender} ({msg_type})...")

    # Detect message intent and context
    intent = detect_intent(original_lower)

    # Generate reply based on intent and message type
    if msg_type == 'email':
        reply = generate_email_reply(sender, original, intent)
    elif msg_type == 'whatsapp':
        reply = generate_whatsapp_reply(sender, original, intent)
    else:
        reply = generate_general_reply(sender, original, intent)

    print(f"[SUCCESS] Reply generated ({len(reply)} chars, intent: {intent})")
    return reply


def detect_intent(message_lower):
    """Detect the intent/purpose of the message (prioritizes specific intents over greetings)"""

    # Score different intents (higher priority intents checked first)
    intents = []

    # Special case: "how are you?" is a greeting, not a question
    if any(phrase in message_lower for phrase in ['how are you', 'how r u', 'how are u', 'how r you', 'how have you been', 'how\'s it going', 'how is it going']):
        intents.append(('greeting', 10))

    # Gratitude (check FIRST before question keywords interfere)
    # Strong gratitude indicators
    if any(phrase in message_lower for phrase in ['thank you', 'thanks for', 'appreciate your', 'appreciate it', 'grateful for']):
        intents.append(('gratitude', 10))
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']):
        intents.append(('gratitude', 9))

    # Urgent Request (highest priority for action items)
    if any(word in message_lower for word in ['urgent', 'asap', 'immediately', 'emergency', 'critical']):
        intents.append(('urgent', 10))

    # Complaint/Issue (high priority)
    if any(word in message_lower for word in ['problem', 'issue', 'error', 'not working', 'broken', 'bug', 'complaint']):
        intents.append(('issue', 9))

    # Question/Help Request (check for actual questions, not past help)
    # Exclude if it's about past help (your help, for helping, for your help)
    if not any(phrase in message_lower for phrase in ['your help', 'for helping', 'for your help', 'for the help']):
        if any(word in message_lower for word in ['?', 'question', 'ask', 'how', 'what', 'when', 'where', 'why', 'could you', 'can you', 'would you', 'please provide']):
            intents.append(('question', 8))
        elif 'help' in message_lower and any(phrase in message_lower for phrase in ['need help', 'can help', 'help me', 'help with']):
            intents.append(('question', 8))

    # Meeting/Schedule
    if any(word in message_lower for word in ['meeting', 'schedule', 'appointment', 'call', 'zoom', 'meet', 'available', 'calendar']):
        intents.append(('meeting', 7))

    # Project/Work Update
    if any(word in message_lower for word in ['project', 'update', 'status', 'progress', 'deadline', 'task', 'deliverable']):
        intents.append(('project_update', 7))

    # Follow-up
    if any(word in message_lower for word in ['follow up', 'following up', 'checking in', 'any update', 'heard back']):
        intents.append(('follow_up', 6))

    # Request for Information
    if any(word in message_lower for word in ['information', 'details', 'tell me', 'let me know', 'inform', 'clarify']):
        intents.append(('info_request', 6))

    # Confirmation
    if any(word in message_lower for word in ['confirm', 'confirmation', 'verify', 'correct', 'right']):
        intents.append(('confirmation', 5))

    # Greeting (lowest priority - only if nothing else matches)
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        intents.append(('greeting', 1))

    # Return highest priority intent
    if intents:
        intents.sort(key=lambda x: x[1], reverse=True)
        return intents[0][0]

    return 'general'


def generate_email_reply(sender, original, intent):
    """Generate professional email reply"""

    # Extract first name from sender if possible
    first_name = sender.split()[0] if ' ' in sender else sender.split('@')[0] if '@' in sender else sender

    # Check if it's a "how are you?" greeting
    is_how_are_you = any(phrase in original.lower() for phrase in ['how are you', 'how r u', 'how are u', 'how r you', 'how have you been', 'how\'s it going', 'how is it going'])

    templates = {
        'greeting': f"""Hello {first_name},

{"I'm doing well, thank you for asking! How are you?" if is_how_are_you else "Thank you for reaching out! It's great to hear from you."}

{"Is there anything I can help you with today?" if is_how_are_you else "How can I assist you today? Please feel free to share any questions or information you need."}

Best regards""",

        'gratitude': f"""Hello {first_name},

You're very welcome! I'm glad I could help.

If you need anything else or have any questions, please don't hesitate to reach out.

Best regards""",

        'question': f"""Hello {first_name},

Thank you for your question. I'd be happy to help you with this.

Could you please provide a bit more detail about your specific needs? This will help me give you the most accurate and helpful response.

Looking forward to assisting you.

Best regards""",

        'meeting': f"""Hello {first_name},

Thank you for reaching out about scheduling a meeting.

I'd be happy to arrange a time to discuss this. Could you please share your availability for the coming days? I'll do my best to accommodate your schedule.

Alternatively, feel free to suggest a few time slots that work best for you.

Best regards""",

        'project_update': f"""Hello {first_name},

Thank you for your inquiry about the project status.

I appreciate your interest in staying updated. I'll compile the latest information and get back to you with a detailed update shortly.

If there are specific aspects you'd like me to focus on, please let me know.

Best regards""",

        'urgent': f"""Hello {first_name},

I understand this is urgent and requires immediate attention.

I'm prioritizing this matter and will address it as quickly as possible. I'll keep you updated on the progress and reach out as soon as I have more information.

Thank you for bringing this to my attention.

Best regards""",

        'issue': f"""Hello {first_name},

Thank you for reporting this issue. I apologize for any inconvenience this may have caused.

I'm looking into this matter right away to understand what happened and how we can resolve it. I'll get back to you with a solution as soon as possible.

If you have any additional details that might help, please feel free to share them.

Best regards""",

        'info_request': f"""Hello {first_name},

Thank you for your request for information.

I'll gather the details you need and send them over shortly. If there's anything specific you'd like me to include or prioritize, please let me know.

Best regards""",

        'confirmation': f"""Hello {first_name},

Thank you for reaching out for confirmation.

I'll verify the details and get back to you with confirmation shortly. This will ensure everything is accurate and up to date.

Best regards""",

        'follow_up': f"""Hello {first_name},

Thank you for following up on this.

I appreciate your patience. I'm working on this and will have an update for you very soon. I'll make sure to keep you informed of any developments.

Best regards""",

        'general': f"""Hello {first_name},

Thank you for your message. I've received it and reviewed the contents.

I'll look into this and get back to you with a detailed response shortly. If you have any additional information or questions in the meantime, please feel free to reach out.

Best regards"""
    }

    return templates.get(intent, templates['general'])


def generate_whatsapp_reply(sender, original, intent):
    """Generate casual WhatsApp reply"""

    first_name = sender.split()[0] if ' ' in sender else sender

    # Check if it's a "how are you?" greeting
    is_how_are_you = any(phrase in original.lower() for phrase in ['how are you', 'how r u', 'how are u', 'how r you', 'how have you been', 'how\'s it going', 'how is it going'])

    templates = {
        'greeting': f"""Hi {first_name}! 👋

{"I'm doing great, thanks for asking! How about you? 😊" if is_how_are_you else "Thanks for reaching out! How can I help you today?"}""",

        'gratitude': f"""You're welcome, {first_name}! 😊

Happy to help! Let me know if you need anything else.""",

        'question': f"""Hi {first_name}!

Good question! I'd be happy to help with that.

Could you give me a bit more detail so I can give you the best answer?""",

        'meeting': f"""Hi {first_name}!

Sure, I'd be happy to meet up or have a call.

When works best for you? Let me know a few times and I'll make it work! 📅""",

        'project_update': f"""Hi {first_name}!

Thanks for checking in on the project.

Let me get you the latest update - I'll send it over shortly! 👍""",

        'urgent': f"""Hi {first_name}!

Got it - I understand this is urgent! ⚡

I'm on it right now and will get back to you ASAP. Thanks for letting me know!""",

        'issue': f"""Hi {first_name}!

Sorry to hear about this issue! 😕

I'm looking into it right now and will get it sorted out. I'll keep you updated!""",

        'info_request': f"""Hi {first_name}!

Sure thing! I'll get you that information.

Give me a moment to gather everything and I'll send it over! 📋""",

        'confirmation': f"""Hi {first_name}!

Let me confirm that for you.

I'll double-check everything and get back to you shortly! ✓""",

        'follow_up': f"""Hi {first_name}!

Thanks for following up!

I'm working on this and should have an update for you soon. Appreciate your patience! 🙏""",

        'general': f"""Hi {first_name}!

Thanks for your message! I got it.

Let me look into this and I'll get back to you soon! 👍"""
    }

    return templates.get(intent, templates['general'])


def generate_general_reply(sender, original, intent):
    """Generate general reply for other message types"""

    first_name = sender.split()[0] if ' ' in sender else sender

    templates = {
        'greeting': f"""Hello {first_name},

Thank you for reaching out. How can I assist you?""",

        'gratitude': f"""You're welcome, {first_name}!

Feel free to reach out if you need anything else.""",

        'question': f"""Hello {first_name},

I'd be happy to help with your question.

Could you provide more details so I can assist you better?""",

        'meeting': f"""Hello {first_name},

I'd be glad to schedule a meeting.

Please share your availability and I'll coordinate accordingly.""",

        'project_update': f"""Hello {first_name},

Thank you for your inquiry.

I'll provide you with a detailed update shortly.""",

        'urgent': f"""Hello {first_name},

I understand this is urgent.

I'm addressing this immediately and will update you soon.""",

        'issue': f"""Hello {first_name},

Thank you for bringing this to my attention.

I'm investigating this issue and will resolve it as quickly as possible.""",

        'info_request': f"""Hello {first_name},

I'll gather the information you requested.

I'll send it over shortly.""",

        'confirmation': f"""Hello {first_name},

I'll confirm those details for you.

I'll get back to you with verification soon.""",

        'follow_up': f"""Hello {first_name},

Thank you for following up.

I'm working on this and will have an update for you soon.""",

        'general': f"""Hello {first_name},

Thank you for your message.

I'll review this and respond with more details shortly."""
    }

    return templates.get(intent, templates['general'])


def create_approval_request(task_file, analysis, reply):
    """Create approval request in Needs_Approval folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"APPROVAL_{timestamp}_{task_file.stem}.md"
    filepath = NEEDS_APPROVAL / filename

    content = f"""---
action: Send Reply
task: {task_file.stem}
created: {datetime.now().isoformat()}
status: pending
message_type: {analysis['type']}
---

# Reply Approval Required

## Original Message

**From:** {analysis['sender']}

**Message:**
{analysis['original_message']}

---

## Proposed Reply

{reply}

---

## Decision Required

Please review and update the status above to either:
- `status: approved` - Send this reply
- `status: rejected` - Don't send this reply

You can also edit the reply text above before approving.

---

*Generated by Reply Generator (Orchestrator)*
"""

    filepath.write_text(content, encoding='utf-8')
    print(f"[INFO] Created approval request: {filename}")
    return filepath


def process_message_task(task_file):
    """Process a single message task and generate reply"""
    try:
        content = task_file.read_text(encoding='utf-8')

        # Check if it's a reply task
        if 'email_reply' not in content and 'whatsapp_reply' not in content:
            return None

        print(f"[INFO] Processing: {task_file.name}")

        # Analyze message
        analysis = analyze_message(content)
        print(f"[INFO] From: {analysis['sender']}")

        # Generate reply
        reply = generate_reply(analysis)
        print(f"[INFO] Generated reply ({len(reply)} chars)")

        # Create approval request
        approval_file = create_approval_request(task_file, analysis, reply)

        # Move original task to archive (it's now in approval workflow)
        archive_path = VAULT_PATH / "Archive"
        archive_path.mkdir(exist_ok=True)
        task_file.rename(archive_path / task_file.name)
        print(f"[INFO] Moved task to Archive")

        return {
            'task': task_file.name,
            'approval_file': approval_file.name,
            'sender': analysis['sender']
        }

    except Exception as e:
        print(f"[ERROR] Failed to process {task_file.name}: {e}")
        return None


def run_orchestrator():
    """Run the orchestrator to process all pending messages"""
    print("[INFO] Reply Generator (Orchestrator) started")
    print(f"[INFO] Checking {NEEDS_ACTION} for messages...")

    # Get all task files
    task_files = list(NEEDS_ACTION.glob("*.md"))

    if not task_files:
        print("[INFO] No tasks found")
        return []

    print(f"[INFO] Found {len(task_files)} task(s)")

    results = []

    for task_file in task_files:
        result = process_message_task(task_file)
        if result:
            results.append(result)

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Reply Generator - Generate AI-powered replies')
    parser.add_argument('--continuous', action='store_true', help='Run continuously')
    parser.add_argument('--interval', type=int, default=900, help='Check interval in seconds (default: 900)')

    args = parser.parse_args()

    if args.continuous:
        import time
        print(f"[INFO] Running continuously (every {args.interval} seconds)")
        print("[INFO] Press Ctrl+C to stop")

        try:
            while True:
                print(f"\n[INFO] Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                results = run_orchestrator()

                if results:
                    print(f"[SUCCESS] Generated {len(results)} reply approval(s)")

                print(f"[INFO] Next run in {args.interval} seconds...")
                time.sleep(args.interval)

        except KeyboardInterrupt:
            print("\n[INFO] Orchestrator stopped by user")
    else:
        results = run_orchestrator()

        if results:
            print(f"\n[SUCCESS] Generated {len(results)} reply approval(s):")
            for r in results:
                print(f"  - {r['sender']}: {r['approval_file']}")
        else:
            print("\n[INFO] No messages to process")


if __name__ == "__main__":
    main()
