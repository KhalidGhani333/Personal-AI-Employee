#!/usr/bin/env python3
"""
Test script for Business MCP Server
Tests all three tools: send_email, post_linkedin, log_activity
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from server import BusinessMCPServer


async def test_log_activity():
    """Test activity logging"""
    print("\n[TEST] Testing log_activity...")

    server = BusinessMCPServer()

    try:
        result = await server._log_activity({
            "message": "Test log entry from business MCP server",
            "level": "info",
            "metadata": {
                "test": True,
                "component": "test_script"
            }
        })

        print("[PASS] Log activity test passed")
        print(json.dumps(result, indent=2))
        return True

    except Exception as e:
        print(f"[FAIL] Log activity test failed: {e}")
        return False


async def test_send_email_validation():
    """Test email validation (without actually sending)"""
    print("\n[TEST] Testing send_email validation...")

    server = BusinessMCPServer()

    try:
        # Test with missing fields
        try:
            await server._send_email({})
            print("[FAIL] Should have raised error for missing fields")
            return False
        except ValueError as e:
            print(f"[PASS] Correctly validated missing fields: {e}")

        # Test with invalid credentials check
        import os
        if not os.getenv('EMAIL_ADDRESS') or not os.getenv('EMAIL_PASSWORD'):
            print("[WARN] Email credentials not configured (expected for testing)")
            try:
                await server._send_email({
                    "to": "test@example.com",
                    "subject": "Test",
                    "body": "Test"
                })
                print("[FAIL] Should have raised error for missing credentials")
                return False
            except ValueError as e:
                print(f"[PASS] Correctly validated credentials: {e}")
        else:
            print("[PASS] Email credentials configured")

        return True

    except Exception as e:
        print(f"[FAIL] Email validation test failed: {e}")
        return False


async def test_linkedin_validation():
    """Test LinkedIn validation (without actually posting)"""
    print("\n[TEST] Testing post_linkedin validation...")

    server = BusinessMCPServer()

    try:
        # Test with missing content
        try:
            await server._post_linkedin({})
            print("[FAIL] Should have raised error for missing content")
            return False
        except ValueError as e:
            print(f"[PASS] Correctly validated missing content: {e}")

        # Test with invalid credentials check
        import os
        if not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'):
            print("[WARN] LinkedIn credentials not configured (expected for testing)")
            try:
                await server._post_linkedin({"content": "Test post"})
                print("[FAIL] Should have raised error for missing credentials")
                return False
            except ValueError as e:
                print(f"[PASS] Correctly validated credentials: {e}")
        else:
            print("[PASS] LinkedIn credentials configured")

        return True

    except Exception as e:
        print(f"[FAIL] LinkedIn validation test failed: {e}")
        return False


async def test_business_log_file():
    """Test that business log file is created and writable"""
    print("\n[TEST] Testing business log file...")

    from server import BUSINESS_LOG

    try:
        # Check if log file exists or can be created
        BUSINESS_LOG.parent.mkdir(parents=True, exist_ok=True)

        # Try writing a test entry
        test_entry = {
            "timestamp": "2026-02-25T00:00:00",
            "level": "info",
            "message": "Test entry",
            "metadata": {}
        }

        with open(BUSINESS_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(test_entry) + '\n')

        print(f"[PASS] Business log file writable: {BUSINESS_LOG}")
        return True

    except Exception as e:
        print(f"[FAIL] Business log file test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("Business MCP Server - Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Business Log File", await test_business_log_file()))
    results.append(("Log Activity", await test_log_activity()))
    results.append(("Email Validation", await test_send_email_validation()))
    results.append(("LinkedIn Validation", await test_linkedin_validation()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
