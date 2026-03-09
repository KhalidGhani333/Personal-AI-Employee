"""
Business MCP Server Test Script
================================
Tests the Business MCP Server functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add MCP server path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp" / "business_mcp"))

try:
    from server import BusinessMCPServer
except ImportError:
    print("[ERROR] Could not import BusinessMCPServer")
    print("[TIP] Make sure mcp/business_mcp/server.py exists")
    sys.exit(1)


async def test_activity_logging():
    """Test activity logging functionality"""
    print("\n" + "="*60)
    print("TEST 1: Activity Logging")
    print("="*60)

    try:
        server = BusinessMCPServer()

        result = await server._log_activity({
            'message': 'Test log entry from MCP test script',
            'level': 'info',
            'metadata': {
                'test': True,
                'timestamp': 'test'
            }
        })

        if result.get('success'):
            print("[PASS] Activity logging: PASSED")
            print(f"    Log file: {result.get('log_file')}")
            return True
        else:
            print("[FAIL] Activity logging: FAILED")
            print(f"    Error: {result.get('error')}")
            return False

    except Exception as e:
        print(f"[FAIL] Activity logging: FAILED")
        print(f"    Exception: {e}")
        return False


async def test_email_sending():
    """Test email sending functionality"""
    print("\n" + "="*60)
    print("TEST 2: Email Sending")
    print("="*60)

    try:
        server = BusinessMCPServer()

        # Check if credentials are configured
        from dotenv import load_dotenv
        import os
        load_dotenv()

        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_APP_PASSWORD') or os.getenv('EMAIL_PASSWORD')

        if not email_address or not email_password:
            print("[SKIP] Email sending: SKIPPED")
            print("    Reason: EMAIL_ADDRESS or EMAIL_APP_PASSWORD not configured in .env")
            return None

        # Send test email to self
        result = await server._send_email({
            'to': email_address,
            'subject': 'MCP Server Test - Email Functionality',
            'body': 'This is a test email from the Business MCP Server.\n\nIf you receive this, email sending is working correctly!'
        })

        if result.get('success'):
            print("[PASS] Email sending: PASSED")
            print(f"    Sent to: {result.get('to')}")
            print(f"    Subject: {result.get('subject')}")
            return True
        else:
            print("[FAIL] Email sending: FAILED")
            print(f"    Error: {result.get('error')}")
            return False

    except Exception as e:
        print(f"[FAIL] Email sending: FAILED")
        print(f"    Exception: {e}")
        return False


async def test_linkedin_posting():
    """Test LinkedIn posting functionality"""
    print("\n" + "="*60)
    print("TEST 3: LinkedIn Posting")
    print("="*60)

    try:
        server = BusinessMCPServer()

        # Check if credentials are configured
        from dotenv import load_dotenv
        import os
        load_dotenv()

        linkedin_email = os.getenv('LINKEDIN_EMAIL')
        linkedin_password = os.getenv('LINKEDIN_PASSWORD')

        if not linkedin_email or not linkedin_password:
            print("[SKIP] LinkedIn posting: SKIPPED")
            print("    Reason: LINKEDIN_EMAIL or LINKEDIN_PASSWORD not configured in .env")
            return None

        print("[INFO] LinkedIn posting test requires manual verification")
        print("[INFO] This test is SKIPPED in automated mode")
        print("[TIP] Use: python scripts/social_poster.py pipeline 'Test' --platforms linkedin")
        return None

    except Exception as e:
        print(f"[FAIL] LinkedIn posting: FAILED")
        print(f"    Exception: {e}")
        return False


async def run_all_tests():
    """Run all MCP server tests"""
    print("\n" + "="*60)
    print("Business MCP Server - Test Suite")
    print("="*60)

    results = {
        'activity_logging': await test_activity_logging(),
        'email_sending': await test_email_sending(),
        'linkedin_posting': await test_linkedin_posting()
    }

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)

    for test_name, result in results.items():
        status = "PASSED" if result is True else "FAILED" if result is False else "SKIPPED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")

    if failed > 0:
        print("\n[WARNING] Some tests failed. Check configuration and logs.")
        return False
    elif passed > 0:
        print("\n[SUCCESS] All configured tests passed!")
        return True
    else:
        print("\n[INFO] All tests skipped. Configure credentials to enable testing.")
        return None


def main():
    """Main entry point"""
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n[INFO] Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test suite failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
