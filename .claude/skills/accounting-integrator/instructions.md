# Accounting Integrator - Detailed Instructions

## Objective
Integrate with Odoo Community Edition for comprehensive accounting and financial management.

## Odoo Setup

### 1. Odoo Installation
```bash
# Install Odoo Community Edition
# Local: http://localhost:8069
# Cloud: https://your-domain.com

Required Modules:
- Accounting
- Invoicing
- Contacts
- Sales
```

### 2. API Configuration
```python
# Odoo JSON-RPC API Configuration
ODOO_URL = "http://localhost:8069"
ODOO_DB = "ai_employee_db"
ODOO_USERNAME = "admin"
ODOO_PASSWORD = "your_password"

# Authentication
import xmlrpc.client

common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
```

## Integration Workflows

### 1. Sync Bank Transactions

**Read CSV:**
```python
import csv

transactions = []
with open('bank_statement.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        transactions.append({
            'date': row['Date'],
            'description': row['Description'],
            'amount': float(row['Amount']),
            'type': 'debit' if float(row['Amount']) < 0 else 'credit'
        })
```

**Create in Odoo:**
```python
for txn in transactions:
    # Create account.bank.statement.line
    models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.bank.statement.line', 'create',
        [{
            'date': txn['date'],
            'payment_ref': txn['description'],
            'amount': txn['amount'],
            'statement_id': statement_id
        }]
    )
```

### 2. Create Invoice in Odoo

**Invoice Data:**
```python
invoice_data = {
    'partner_id': client_id,  # Customer ID
    'move_type': 'out_invoice',  # Customer invoice
    'invoice_date': '2026-02-06',
    'invoice_date_due': '2026-03-06',
    'invoice_line_ids': [
        (0, 0, {
            'name': 'Service Description',
            'quantity': 1,
            'price_unit': 1500.00,
            'tax_ids': [(6, 0, [tax_id])]
        })
    ]
}

# Create invoice
invoice_id = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'create',
    [invoice_data]
)

# Post invoice (make it official)
models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'action_post',
    [[invoice_id]]
)
```

### 3. Record Expense

**Expense Entry:**
```python
expense_data = {
    'name': 'Software Subscription',
    'product_id': product_id,
    'unit_amount': 99.00,
    'quantity': 1,
    'employee_id': employee_id,
    'date': '2026-02-06'
}

expense_id = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'hr.expense', 'create',
    [expense_data]
)
```

### 4. Generate Financial Reports

**Profit & Loss:**
```python
# Get account.move.line records
domain = [
    ('date', '>=', '2026-01-01'),
    ('date', '<=', '2026-01-31'),
    ('account_id.internal_type', 'in', ['income', 'expense'])
]

lines = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move.line', 'search_read',
    [domain],
    {'fields': ['account_id', 'debit', 'credit', 'name']}
)

# Calculate totals
income = sum(line['credit'] for line in lines if line['account_id'][0] in income_accounts)
expenses = sum(line['debit'] for line in lines if line['account_id'][0] in expense_accounts)
profit = income - expenses
```

**Balance Sheet:**
```python
# Assets, Liabilities, Equity
domain = [
    ('date', '<=', '2026-01-31'),
    ('account_id.internal_type', 'in', ['asset', 'liability', 'equity'])
]

# Similar query and calculation
```

### 5. Reconcile Payments

**Match Invoice to Payment:**
```python
# Find invoice
invoice = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.move', 'search_read',
    [[('name', '=', 'INV/2026/0001')]],
    {'fields': ['id', 'amount_total', 'payment_state']}
)

# Find payment
payment = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'account.payment', 'search_read',
    [[('ref', '=', 'INV/2026/0001')]],
    {'fields': ['id', 'amount']}
)

# Reconcile
if invoice and payment:
    models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'account.move', 'js_assign_outstanding_line',
        [[invoice[0]['id']], payment[0]['id']]
    )
```

## Approval Workflow

**For Sensitive Operations:**
```markdown
---
type: accounting_action
action: create_invoice|record_payment|create_expense
requires_approval: true
---

## Action Details
{details}

## Odoo Impact
- Module: {module_name}
- Record Type: {record_type}
- Amount: ${amount}

## To Approve
Move to /Approved folder
```

## Data Mapping

**Client to Partner:**
```python
# Create or find partner in Odoo
partner_data = {
    'name': client_name,
    'email': client_email,
    'phone': client_phone,
    'is_company': True,
    'customer_rank': 1
}

partner_id = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'res.partner', 'create',
    [partner_data]
)
```

**Invoice to Account Move:**
```
Local Invoice → Odoo account.move
- invoice_number → name
- client → partner_id
- amount → amount_total
- line_items → invoice_line_ids
```

**Transaction to Bank Statement Line:**
```
CSV Transaction → Odoo account.bank.statement.line
- date → date
- description → payment_ref
- amount → amount
- category → account_id
```

## Error Handling

**Connection Errors:**
```python
try:
    # Odoo API call
except Exception as e:
    # Log error
    # Create retry task
    # Notify user
```

**Data Validation:**
```python
# Before syncing to Odoo
def validate_invoice(invoice_data):
    assert invoice_data['amount'] > 0
    assert invoice_data['client_id'] is not None
    assert invoice_data['date'] is valid
    return True
```

## Reporting

**Monthly Financial Report:**
```markdown
# Financial Report - {month} {year}

## Income Statement
- Revenue: ${revenue}
- Cost of Goods Sold: ${cogs}
- Gross Profit: ${gross_profit}
- Operating Expenses: ${opex}
- Net Profit: ${net_profit}

## Balance Sheet
- Assets: ${assets}
- Liabilities: ${liabilities}
- Equity: ${equity}

## Cash Flow
- Operating Activities: ${operating_cf}
- Investing Activities: ${investing_cf}
- Financing Activities: ${financing_cf}

## Key Metrics
- Profit Margin: {percentage}%
- Current Ratio: {ratio}
- Quick Ratio: {ratio}
```

## Integration Points

- **Invoice Generator**: Sync invoices to Odoo
- **Business Auditor**: Pull financial data
- **Dashboard Updater**: Update financial stats
- **Approval Handler**: Approve sensitive operations

## Success Criteria
- All transactions synced accurately
- Invoices created in Odoo
- Financial reports generated
- No data loss
- Reconciliation complete
