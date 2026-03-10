"""
Accounting MCP Server
=====================
MCP server for accounting operations: expenses, income, reports.
Integrates with Odoo for self-hosted accounting.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
VAULT_PATH = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
ACCOUNTING_PATH = VAULT_PATH / "Accounting"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
ACCOUNTING_PATH.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)


class AccountingMCPServer:
    """MCP Server for accounting operations"""

    def __init__(self):
        self.name = "accounting-mcp"
        self.version = "1.0.0"
        self.transactions_file = ACCOUNTING_PATH / "transactions.json"
        self.reports_path = ACCOUNTING_PATH / "Reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)
        self._ensure_transactions_file()

    def _ensure_transactions_file(self):
        """Initialize transactions file if it doesn't exist"""
        if not self.transactions_file.exists():
            self.transactions_file.write_text(json.dumps([], indent=2))

    def _load_transactions(self) -> List[Dict[str, Any]]:
        """Load all transactions"""
        try:
            return json.loads(self.transactions_file.read_text())
        except:
            return []

    def _save_transactions(self, transactions: List[Dict[str, Any]]):
        """Save transactions to file"""
        self.transactions_file.write_text(json.dumps(transactions, indent=2))

    async def record_expense(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record an expense transaction

        Args:
            amount: Expense amount (positive number)
            description: Description of expense
            category: Expense category (e.g., 'office', 'marketing', 'software')
            date: Transaction date (ISO format, optional)
            payment_method: Payment method (optional)
        """
        try:
            amount = float(params.get('amount', 0))
            description = params.get('description', 'Expense')
            category = params.get('category', 'general')
            date = params.get('date', datetime.now().isoformat())
            payment_method = params.get('payment_method', 'unknown')

            if amount <= 0:
                return {
                    "success": False,
                    "error": "Amount must be positive"
                }

            # Load transactions
            transactions = self._load_transactions()

            # Create transaction
            transaction = {
                "id": f"EXP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": "expense",
                "amount": -abs(amount),  # Negative for expense
                "description": description,
                "category": category,
                "date": date,
                "payment_method": payment_method,
                "created_at": datetime.now().isoformat()
            }

            transactions.append(transaction)
            self._save_transactions(transactions)

            logger.info(f"Recorded expense: {description} - ${amount}")

            return {
                "success": True,
                "transaction_id": transaction["id"],
                "amount": amount,
                "description": description,
                "category": category,
                "message": f"Expense recorded: ${amount}"
            }

        except Exception as e:
            logger.error(f"Failed to record expense: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def record_income(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record an income transaction

        Args:
            amount: Income amount (positive number)
            description: Description of income
            source: Income source (e.g., 'client', 'product', 'service')
            date: Transaction date (ISO format, optional)
            payment_method: Payment method (optional)
        """
        try:
            amount = float(params.get('amount', 0))
            description = params.get('description', 'Income')
            source = params.get('source', 'general')
            date = params.get('date', datetime.now().isoformat())
            payment_method = params.get('payment_method', 'unknown')

            if amount <= 0:
                return {
                    "success": False,
                    "error": "Amount must be positive"
                }

            # Load transactions
            transactions = self._load_transactions()

            # Create transaction
            transaction = {
                "id": f"INC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "type": "income",
                "amount": abs(amount),  # Positive for income
                "description": description,
                "source": source,
                "date": date,
                "payment_method": payment_method,
                "created_at": datetime.now().isoformat()
            }

            transactions.append(transaction)
            self._save_transactions(transactions)

            logger.info(f"Recorded income: {description} - ${amount}")

            return {
                "success": True,
                "transaction_id": transaction["id"],
                "amount": amount,
                "description": description,
                "source": source,
                "message": f"Income recorded: ${amount}"
            }

        except Exception as e:
            logger.error(f"Failed to record income: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_balance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get current balance

        Args:
            start_date: Start date for calculation (ISO format, optional)
            end_date: End date for calculation (ISO format, optional)
        """
        try:
            transactions = self._load_transactions()

            start_date = params.get('start_date')
            end_date = params.get('end_date')

            # Filter by date if provided
            filtered = transactions
            if start_date or end_date:
                filtered = []
                for t in transactions:
                    t_date = t.get('date', '')
                    if start_date and t_date < start_date:
                        continue
                    if end_date and t_date > end_date:
                        continue
                    filtered.append(t)

            # Calculate totals
            total_income = sum(t['amount'] for t in filtered if t['amount'] > 0)
            total_expenses = abs(sum(t['amount'] for t in filtered if t['amount'] < 0))
            balance = total_income - total_expenses

            return {
                "success": True,
                "balance": balance,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "transaction_count": len(filtered),
                "message": f"Current balance: ${balance:.2f}"
            }

        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate financial report

        Args:
            report_type: Type of report ('monthly', 'yearly', 'custom')
            start_date: Start date (ISO format, optional)
            end_date: End date (ISO format, optional)
        """
        try:
            report_type = params.get('report_type', 'monthly')
            start_date = params.get('start_date')
            end_date = params.get('end_date')

            transactions = self._load_transactions()

            # Filter transactions
            if start_date or end_date:
                filtered = []
                for t in transactions:
                    t_date = t.get('date', '')
                    if start_date and t_date < start_date:
                        continue
                    if end_date and t_date > end_date:
                        continue
                    filtered.append(t)
            else:
                filtered = transactions

            # Calculate metrics
            total_income = sum(t['amount'] for t in filtered if t['amount'] > 0)
            total_expenses = abs(sum(t['amount'] for t in filtered if t['amount'] < 0))
            balance = total_income - total_expenses

            # Group by category
            expense_by_category = {}
            income_by_source = {}

            for t in filtered:
                if t['amount'] < 0:
                    category = t.get('category', 'general')
                    expense_by_category[category] = expense_by_category.get(category, 0) + abs(t['amount'])
                else:
                    source = t.get('source', 'general')
                    income_by_source[source] = income_by_source.get(source, 0) + t['amount']

            # Generate report content
            report_lines = [
                f"# Financial Report - {report_type.capitalize()}",
                f"",
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"**Period:** {start_date or 'All time'} to {end_date or 'Present'}",
                f"",
                f"---",
                f"",
                f"## Summary",
                f"",
                f"- **Total Income:** ${total_income:.2f}",
                f"- **Total Expenses:** ${total_expenses:.2f}",
                f"- **Net Balance:** ${balance:.2f}",
                f"- **Transactions:** {len(filtered)}",
                f"",
                f"---",
                f"",
                f"## Income by Source",
                f""
            ]

            if income_by_source:
                for source, amount in sorted(income_by_source.items(), key=lambda x: x[1], reverse=True):
                    report_lines.append(f"- **{source.capitalize()}:** ${amount:.2f}")
            else:
                report_lines.append("- No income recorded")

            report_lines.extend([
                f"",
                f"---",
                f"",
                f"## Expenses by Category",
                f""
            ])

            if expense_by_category:
                for category, amount in sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True):
                    report_lines.append(f"- **{category.capitalize()}:** ${amount:.2f}")
            else:
                report_lines.append("- No expenses recorded")

            report_lines.extend([
                f"",
                f"---",
                f"",
                f"*Generated by Accounting MCP Server*"
            ])

            # Save report
            report_filename = f"REPORT_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            report_path = self.reports_path / report_filename
            report_path.write_text('\n'.join(report_lines))

            logger.info(f"Generated report: {report_filename}")

            return {
                "success": True,
                "report_file": str(report_path),
                "total_income": total_income,
                "total_expenses": total_expenses,
                "balance": balance,
                "message": f"Report generated: {report_filename}"
            }

        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def list_transactions(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List recent transactions

        Args:
            limit: Number of transactions to return (default: 10)
            transaction_type: Filter by type ('income', 'expense', or 'all')
        """
        try:
            limit = int(params.get('limit', 10))
            transaction_type = params.get('transaction_type', 'all')

            transactions = self._load_transactions()

            # Filter by type
            if transaction_type != 'all':
                transactions = [t for t in transactions if t.get('type') == transaction_type]

            # Sort by date (most recent first)
            transactions.sort(key=lambda x: x.get('created_at', ''), reverse=True)

            # Limit results
            transactions = transactions[:limit]

            return {
                "success": True,
                "transactions": transactions,
                "count": len(transactions),
                "message": f"Retrieved {len(transactions)} transactions"
            }

        except Exception as e:
            logger.error(f"Failed to list transactions: {e}")
            return {
                "success": False,
                "error": str(e)
            }


async def main():
    """Test the MCP server"""
    server = AccountingMCPServer()

    print("Testing Accounting MCP Server...")
    print("=" * 60)

    # Test recording expense
    print("\n1. Recording expense...")
    result = await server.record_expense({
        'amount': 50.00,
        'description': 'Office supplies',
        'category': 'office'
    })
    print(f"Result: {result}")

    # Test recording income
    print("\n2. Recording income...")
    result = await server.record_income({
        'amount': 500.00,
        'description': 'Client payment',
        'source': 'client'
    })
    print(f"Result: {result}")

    # Test getting balance
    print("\n3. Getting balance...")
    result = await server.get_balance({})
    print(f"Result: {result}")

    # Test generating report
    print("\n4. Generating report...")
    result = await server.generate_report({
        'report_type': 'monthly'
    })
    print(f"Result: {result}")

    print("\n" + "=" * 60)
    print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
