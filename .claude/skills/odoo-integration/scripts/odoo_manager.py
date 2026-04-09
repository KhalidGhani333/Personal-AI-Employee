#!/usr/bin/env python3
"""
Odoo Integration Skill Script
Manages Odoo accounting operations via MCP server
"""

import sys
import json
import asyncio
from pathlib import Path

# Add parent directories to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "mcp" / "accounting_mcp"))

from server import AccountingMCPServer


async def main():
    """Main entry point for Odoo integration skill"""

    if len(sys.argv) < 2:
        print("Usage: python odoo_manager.py <command> [args]")
        print("\nCommands:")
        print("  expense <amount> <description> [--category <cat>]")
        print("  income <amount> <description> [--source <src>]")
        print("  balance")
        print("  report [monthly|yearly|custom]")
        sys.exit(1)

    command = sys.argv[1].lower()

    # Initialize MCP server
    server = AccountingMCPServer()

    try:
        if command == "expense":
            if len(sys.argv) < 4:
                print("Error: expense requires amount and description")
                sys.exit(1)

            amount = float(sys.argv[2])
            description = sys.argv[3]
            category = "general"

            # Parse optional category
            if "--category" in sys.argv:
                idx = sys.argv.index("--category")
                if idx + 1 < len(sys.argv):
                    category = sys.argv[idx + 1]

            result = await server.record_expense({
                'amount': amount,
                'description': description,
                'category': category
            })

            if result['success']:
                storage = result.get('storage', 'unknown')
                print(f"\n✅ Expense Recorded ({storage})")
                print(f"Amount: ${result['amount']:.2f}")
                print(f"Description: {result['description']}")
                print(f"Category: {result.get('category', 'N/A')}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        elif command == "income":
            if len(sys.argv) < 4:
                print("Error: income requires amount and description")
                sys.exit(1)

            amount = float(sys.argv[2])
            description = sys.argv[3]
            source = "general"

            # Parse optional source
            if "--source" in sys.argv:
                idx = sys.argv.index("--source")
                if idx + 1 < len(sys.argv):
                    source = sys.argv[idx + 1]

            result = await server.record_income({
                'amount': amount,
                'description': description,
                'source': source
            })

            if result['success']:
                storage = result.get('storage', 'unknown')
                print(f"\n✅ Income Recorded ({storage})")
                print(f"Amount: ${result['amount']:.2f}")
                print(f"Description: {result['description']}")
                print(f"Source: {result.get('source', 'N/A')}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        elif command == "balance":
            result = await server.get_balance({})

            if result['success']:
                storage = result.get('storage', 'unknown')
                print(f"\n💰 Financial Summary ({storage})")
                print(f"Balance: ${result['balance']:.2f}")
                print(f"Total Income: ${result['total_income']:.2f}")
                print(f"Total Expenses: ${result['total_expenses']:.2f}")
                print(f"Transactions: {result.get('transaction_count', 0)}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        elif command == "report":
            report_type = sys.argv[2] if len(sys.argv) > 2 else "monthly"

            result = await server.generate_report({
                'report_type': report_type
            })

            if result['success']:
                print(f"\n📊 Report Generated")
                print(f"Type: {report_type}")
                print(f"Balance: ${result['balance']:.2f}")
                print(f"Income: ${result['total_income']:.2f}")
                print(f"Expenses: ${result['total_expenses']:.2f}")
                print(f"\nReport saved to: {result['report_file']}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
