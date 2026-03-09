#!/usr/bin/env python3
"""
Accounting Manager
Maintains accounting records and generates financial summaries
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import re

# Paths
VAULT_PATH = Path("AI_Employee_Vault")
ACCOUNTING_PATH = VAULT_PATH / "Accounting"
CURRENT_MONTH_FILE = ACCOUNTING_PATH / "Current_Month.md"


class Transaction:
    """Represents a financial transaction"""

    def __init__(self, date: str, trans_type: str, amount: float, description: str):
        self.date = date
        self.type = trans_type  # "income" or "expense"
        self.amount = amount
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "type": self.type,
            "amount": self.amount,
            "description": self.description
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Transaction':
        return Transaction(
            data["date"],
            data["type"],
            data["amount"],
            data["description"]
        )


class AccountingManager:
    """Manages accounting records and summaries"""

    def __init__(self):
        self.accounting_path = ACCOUNTING_PATH
        self.current_month_file = CURRENT_MONTH_FILE
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure accounting directories exist"""
        self.accounting_path.mkdir(parents=True, exist_ok=True)

    def _get_current_month_year(self) -> Tuple[str, int, int]:
        """Get current month name and year"""
        now = datetime.now()
        month_name = now.strftime("%B")
        year = now.year
        month_num = now.month
        return month_name, year, month_num

    def _parse_current_month_file(self) -> List[Transaction]:
        """Parse transactions from Current_Month.md"""
        if not self.current_month_file.exists():
            return []

        transactions = []
        content = self.current_month_file.read_text(encoding='utf-8')

        # Parse markdown table
        in_table = False
        for line in content.split('\n'):
            line = line.strip()

            # Skip header and separator
            if line.startswith('| Date |') or line.startswith('|---'):
                in_table = True
                continue

            if in_table and line.startswith('|'):
                # Parse table row: | Date | Type | Amount | Description |
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) == 4:
                    date, trans_type, amount_str, description = parts

                    # Parse amount (remove $ and commas)
                    amount_str = amount_str.replace('$', '').replace(',', '')
                    try:
                        amount = float(amount_str)
                        transactions.append(Transaction(
                            date,
                            trans_type.lower(),
                            amount,
                            description
                        ))
                    except ValueError:
                        continue

        return transactions

    def _calculate_totals(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Calculate total income, expenses, and balance"""
        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expenses = sum(t.amount for t in transactions if t.type == "expense")
        net_balance = total_income - total_expenses

        return {
            "income": total_income,
            "expenses": total_expenses,
            "balance": net_balance
        }

    def _write_current_month_file(self, transactions: List[Transaction]):
        """Write transactions to Current_Month.md"""
        month_name, year, _ = self._get_current_month_year()

        # Calculate totals
        totals = self._calculate_totals(transactions)

        # Build markdown content
        lines = [
            f"# Accounting - {month_name} {year}",
            "",
            "## Summary",
            f"- **Total Income**: ${totals['income']:,.2f}",
            f"- **Total Expenses**: ${totals['expenses']:,.2f}",
            f"- **Net Balance**: ${totals['balance']:,.2f}",
            "",
            "## Transactions",
            "",
            "| Date | Type | Amount | Description |",
            "|------|------|--------|-------------|"
        ]

        # Add transactions (sorted by date)
        sorted_transactions = sorted(transactions, key=lambda t: t.date)
        for trans in sorted_transactions:
            trans_type = trans.type.capitalize()
            lines.append(
                f"| {trans.date} | {trans_type} | ${trans.amount:,.2f} | {trans.description} |"
            )

        # Write file
        content = '\n'.join(lines) + '\n'
        self.current_month_file.write_text(content, encoding='utf-8')

    def add_transaction(self, trans_type: str, amount: float, description: str) -> Dict[str, Any]:
        """Add a new transaction"""
        # Validate inputs
        if trans_type not in ["income", "expense"]:
            raise ValueError("Transaction type must be 'income' or 'expense'")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        if not description:
            raise ValueError("Description is required")

        # Get current date
        date = datetime.now().strftime("%Y-%m-%d")

        # Load existing transactions
        transactions = self._parse_current_month_file()

        # Add new transaction
        new_transaction = Transaction(date, trans_type, amount, description)
        transactions.append(new_transaction)

        # Write updated file
        self._write_current_month_file(transactions)

        # Calculate new totals
        totals = self._calculate_totals(transactions)

        return {
            "success": True,
            "transaction": new_transaction.to_dict(),
            "totals": totals
        }

    def add_income(self, amount: float, description: str) -> Dict[str, Any]:
        """Add an income transaction"""
        return self.add_transaction("income", amount, description)

    def add_expense(self, amount: float, description: str) -> Dict[str, Any]:
        """Add an expense transaction"""
        return self.add_transaction("expense", amount, description)

    def get_balance(self) -> Dict[str, Any]:
        """Get current month's balance"""
        transactions = self._parse_current_month_file()
        totals = self._calculate_totals(transactions)

        return {
            "success": True,
            "month": self._get_current_month_year()[0],
            "year": self._get_current_month_year()[1],
            "totals": totals,
            "transaction_count": len(transactions)
        }

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get summary for the current week"""
        transactions = self._parse_current_month_file()

        # Get current week's date range
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())  # Monday
        week_end = week_start + timedelta(days=6)  # Sunday

        week_start_str = week_start.strftime("%Y-%m-%d")
        week_end_str = week_end.strftime("%Y-%m-%d")

        # Filter transactions for current week
        week_transactions = [
            t for t in transactions
            if week_start_str <= t.date <= week_end_str
        ]

        # Calculate weekly totals
        totals = self._calculate_totals(week_transactions)

        return {
            "success": True,
            "week_start": week_start.strftime("%b %d, %Y"),
            "week_end": week_end.strftime("%b %d, %Y"),
            "totals": totals,
            "transaction_count": len(week_transactions),
            "transactions": [t.to_dict() for t in week_transactions]
        }

    def get_monthly_summary(self) -> Dict[str, Any]:
        """Get complete monthly summary"""
        transactions = self._parse_current_month_file()
        totals = self._calculate_totals(transactions)

        # Group by week
        weeks = {}
        for trans in transactions:
            trans_date = datetime.strptime(trans.date, "%Y-%m-%d")
            week_num = trans_date.isocalendar()[1]
            week_key = f"Week {week_num}"

            if week_key not in weeks:
                weeks[week_key] = []
            weeks[week_key].append(trans)

        # Calculate weekly totals
        weekly_summaries = {}
        for week_key, week_trans in weeks.items():
            weekly_summaries[week_key] = self._calculate_totals(week_trans)

        month_name, year, _ = self._get_current_month_year()

        return {
            "success": True,
            "month": month_name,
            "year": year,
            "totals": totals,
            "transaction_count": len(transactions),
            "weekly_summaries": weekly_summaries,
            "transactions": [t.to_dict() for t in transactions]
        }


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: accounting_manager.py <command> [args...]")
        print("\nCommands:")
        print("  add-income <amount> <description>")
        print("  add-expense <amount> <description>")
        print("  balance")
        print("  weekly-summary")
        print("  monthly-summary")
        sys.exit(1)

    command = sys.argv[1]
    manager = AccountingManager()

    try:
        if command == "add-income":
            if len(sys.argv) < 4:
                print("Error: Missing amount or description")
                sys.exit(1)

            amount = float(sys.argv[2])
            description = ' '.join(sys.argv[3:])

            result = manager.add_income(amount, description)
            print(f"[OK] Income recorded: ${amount:,.2f} - {description}")
            print(f"     Current balance: ${result['totals']['balance']:,.2f}")

        elif command == "add-expense":
            if len(sys.argv) < 4:
                print("Error: Missing amount or description")
                sys.exit(1)

            amount = float(sys.argv[2])
            description = ' '.join(sys.argv[3:])

            result = manager.add_expense(amount, description)
            print(f"[OK] Expense recorded: ${amount:,.2f} - {description}")
            print(f"     Current balance: ${result['totals']['balance']:,.2f}")

        elif command == "balance":
            result = manager.get_balance()
            print(f"\n{result['month']} {result['year']} Balance:")
            print(f"  Income:   ${result['totals']['income']:,.2f}")
            print(f"  Expenses: ${result['totals']['expenses']:,.2f}")
            print(f"  Net:      ${result['totals']['balance']:,.2f}")
            print(f"\n  Transactions: {result['transaction_count']}")

        elif command == "weekly-summary":
            result = manager.get_weekly_summary()
            print(f"\nWeek of {result['week_start']} - {result['week_end']}:")
            print(f"  Income:   ${result['totals']['income']:,.2f} ({len([t for t in result['transactions'] if t['type'] == 'income'])} transactions)")
            print(f"  Expenses: ${result['totals']['expenses']:,.2f} ({len([t for t in result['transactions'] if t['type'] == 'expense'])} transactions)")
            print(f"  Net:      ${result['totals']['balance']:,.2f}")

        elif command == "monthly-summary":
            result = manager.get_monthly_summary()
            print(f"\n{result['month']} {result['year']} Summary:")
            print(f"  Total Income:   ${result['totals']['income']:,.2f}")
            print(f"  Total Expenses: ${result['totals']['expenses']:,.2f}")
            print(f"  Net Balance:    ${result['totals']['balance']:,.2f}")
            print(f"\n  Total Transactions: {result['transaction_count']}")

            if result['weekly_summaries']:
                print("\n  Weekly Breakdown:")
                for week, totals in sorted(result['weekly_summaries'].items()):
                    print(f"    {week}: ${totals['balance']:,.2f} (Income: ${totals['income']:,.2f}, Expenses: ${totals['expenses']:,.2f})")

        else:
            print(f"Error: Unknown command '{command}'")
            sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
