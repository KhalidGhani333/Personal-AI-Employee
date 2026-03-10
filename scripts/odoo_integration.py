"""
Odoo Integration Script
========================
Integrates with self-hosted Odoo accounting system via XML-RPC API.
Supports expense tracking, income recording, and report generation.
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
ACCOUNTING_PATH = VAULT_PATH / "Accounting"
LOGS_PATH = VAULT_PATH / "Logs"

# Ensure directories exist
ACCOUNTING_PATH.mkdir(parents=True, exist_ok=True)
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# Setup logging
log_file = LOGS_PATH / "odoo_integration.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OdooIntegration:
    """Odoo accounting system integration"""

    def __init__(self):
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'odoo')
        self.username = os.getenv('ODOO_USERNAME', '')
        self.password = os.getenv('ODOO_PASSWORD', '')
        self.uid = None
        self.models = None
        self.connected = False

        # Try to import xmlrpc
        try:
            import xmlrpc.client
            self.xmlrpc = xmlrpc.client
        except ImportError:
            logger.warning("xmlrpc.client not available - using fallback mode")
            self.xmlrpc = None

    def connect(self) -> bool:
        """Connect to Odoo instance"""
        if not self.xmlrpc:
            logger.warning("Odoo connection not available - using local storage")
            return False

        if not self.username or not self.password:
            logger.warning("Odoo credentials not configured - using local storage")
            return False

        try:
            logger.info(f"Connecting to Odoo at {self.url}...")

            # Authenticate
            common = self.xmlrpc.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.db, self.username, self.password, {})

            if not self.uid:
                logger.error("Authentication failed")
                return False

            # Get models proxy
            self.models = self.xmlrpc.ServerProxy(f'{self.url}/xmlrpc/2/object')

            logger.info(f"Connected to Odoo as user ID: {self.uid}")
            self.connected = True
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Odoo: {e}")
            return False

    def record_expense(self, amount: float, description: str, category: str = 'general') -> Dict[str, Any]:
        """Record an expense in Odoo"""
        try:
            if not self.connected:
                logger.info("Using local storage (Odoo not connected)")
                return self._record_local_expense(amount, description, category)

            # Create expense in Odoo
            expense_data = {
                'name': description,
                'unit_amount': amount,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'employee_id': self.uid,
            }

            expense_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'hr.expense', 'create',
                [expense_data]
            )

            logger.info(f"Expense recorded in Odoo: ID {expense_id}")

            return {
                "success": True,
                "expense_id": expense_id,
                "amount": amount,
                "description": description,
                "message": f"Expense recorded in Odoo: ${amount}"
            }

        except Exception as e:
            logger.error(f"Failed to record expense in Odoo: {e}")
            logger.info("Falling back to local storage")
            return self._record_local_expense(amount, description, category)

    def record_income(self, amount: float, description: str, source: str = 'general') -> Dict[str, Any]:
        """Record income in Odoo"""
        try:
            if not self.connected:
                logger.info("Using local storage (Odoo not connected)")
                return self._record_local_income(amount, description, source)

            # Create invoice in Odoo
            invoice_data = {
                'name': description,
                'type': 'out_invoice',
                'invoice_date': datetime.now().strftime('%Y-%m-%d'),
                'amount_total': amount,
            }

            invoice_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'account.move', 'create',
                [invoice_data]
            )

            logger.info(f"Income recorded in Odoo: ID {invoice_id}")

            return {
                "success": True,
                "invoice_id": invoice_id,
                "amount": amount,
                "description": description,
                "message": f"Income recorded in Odoo: ${amount}"
            }

        except Exception as e:
            logger.error(f"Failed to record income in Odoo: {e}")
            logger.info("Falling back to local storage")
            return self._record_local_income(amount, description, source)

    def _record_local_expense(self, amount: float, description: str, category: str) -> Dict[str, Any]:
        """Record expense in local storage (fallback)"""
        transactions_file = ACCOUNTING_PATH / "transactions.json"

        # Load existing transactions
        if transactions_file.exists():
            transactions = json.loads(transactions_file.read_text())
        else:
            transactions = []

        # Create transaction
        transaction = {
            "id": f"EXP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "expense",
            "amount": -abs(amount),
            "description": description,
            "category": category,
            "date": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }

        transactions.append(transaction)
        transactions_file.write_text(json.dumps(transactions, indent=2))

        logger.info(f"Expense recorded locally: {description} - ${amount}")

        return {
            "success": True,
            "transaction_id": transaction["id"],
            "amount": amount,
            "description": description,
            "storage": "local",
            "message": f"Expense recorded locally: ${amount}"
        }

    def _record_local_income(self, amount: float, description: str, source: str) -> Dict[str, Any]:
        """Record income in local storage (fallback)"""
        transactions_file = ACCOUNTING_PATH / "transactions.json"

        # Load existing transactions
        if transactions_file.exists():
            transactions = json.loads(transactions_file.read_text())
        else:
            transactions = []

        # Create transaction
        transaction = {
            "id": f"INC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": "income",
            "amount": abs(amount),
            "description": description,
            "source": source,
            "date": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }

        transactions.append(transaction)
        transactions_file.write_text(json.dumps(transactions, indent=2))

        logger.info(f"Income recorded locally: {description} - ${amount}")

        return {
            "success": True,
            "transaction_id": transaction["id"],
            "amount": amount,
            "description": description,
            "storage": "local",
            "message": f"Income recorded locally: ${amount}"
        }

    def get_balance(self) -> Dict[str, Any]:
        """Get current balance"""
        try:
            if self.connected:
                # Get balance from Odoo
                # This would require custom Odoo queries
                logger.info("Getting balance from Odoo...")
                # For now, fall back to local
                return self._get_local_balance()
            else:
                return self._get_local_balance()

        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return self._get_local_balance()

    def _get_local_balance(self) -> Dict[str, Any]:
        """Get balance from local storage"""
        transactions_file = ACCOUNTING_PATH / "transactions.json"

        if not transactions_file.exists():
            return {
                "success": True,
                "balance": 0.0,
                "total_income": 0.0,
                "total_expenses": 0.0,
                "storage": "local"
            }

        transactions = json.loads(transactions_file.read_text())

        total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
        total_expenses = abs(sum(t['amount'] for t in transactions if t['amount'] < 0))
        balance = total_income - total_expenses

        return {
            "success": True,
            "balance": balance,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "transaction_count": len(transactions),
            "storage": "local"
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Odoo Integration - Accounting System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Connect command
    connect_parser = subparsers.add_parser('connect', help='Test Odoo connection')

    # Record expense
    expense_parser = subparsers.add_parser('expense', help='Record expense')
    expense_parser.add_argument('amount', type=float, help='Expense amount')
    expense_parser.add_argument('description', help='Expense description')
    expense_parser.add_argument('--category', default='general', help='Expense category')

    # Record income
    income_parser = subparsers.add_parser('income', help='Record income')
    income_parser.add_argument('amount', type=float, help='Income amount')
    income_parser.add_argument('description', help='Income description')
    income_parser.add_argument('--source', default='general', help='Income source')

    # Get balance
    balance_parser = subparsers.add_parser('balance', help='Get current balance')

    args = parser.parse_args()

    odoo = OdooIntegration()

    if args.command == 'connect':
        logger.info("=" * 60)
        logger.info("Testing Odoo Connection")
        logger.info("=" * 60)

        if odoo.connect():
            print("\n[SUCCESS] Connected to Odoo")
            print(f"URL: {odoo.url}")
            print(f"Database: {odoo.db}")
            print(f"User ID: {odoo.uid}")
        else:
            print("\n[INFO] Odoo not connected - using local storage")
            print("Configure ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD in .env")

    elif args.command == 'expense':
        odoo.connect()
        result = odoo.record_expense(args.amount, args.description, args.category)

        if result['success']:
            print(f"\n[SUCCESS] {result['message']}")
            print(f"Amount: ${result['amount']}")
            print(f"Description: {result['description']}")
            if 'storage' in result:
                print(f"Storage: {result['storage']}")
        else:
            print(f"\n[ERROR] Failed to record expense")

    elif args.command == 'income':
        odoo.connect()
        result = odoo.record_income(args.amount, args.description, args.source)

        if result['success']:
            print(f"\n[SUCCESS] {result['message']}")
            print(f"Amount: ${result['amount']}")
            print(f"Description: {result['description']}")
            if 'storage' in result:
                print(f"Storage: {result['storage']}")
        else:
            print(f"\n[ERROR] Failed to record income")

    elif args.command == 'balance':
        odoo.connect()
        result = odoo.get_balance()

        if result['success']:
            print(f"\n[SUCCESS] Balance Retrieved")
            print(f"Balance: ${result['balance']:.2f}")
            print(f"Total Income: ${result['total_income']:.2f}")
            print(f"Total Expenses: ${result['total_expenses']:.2f}")
            if 'storage' in result:
                print(f"Storage: {result['storage']}")
        else:
            print(f"\n[ERROR] Failed to get balance")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
