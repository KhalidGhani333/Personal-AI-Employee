# Accounting Manager Skill

Maintain accounting records and generate financial summaries.

## Usage

```
/accounting-manager add-income 5000 "Client payment for Project X"
/accounting-manager add-expense 1200 "Office rent - February"
/accounting-manager weekly-summary
/accounting-manager monthly-summary
/accounting-manager balance
```

## Commands

### Add Income
```
/accounting-manager add-income <amount> "<description>"
```
Records an income transaction.

**Example:**
```
/accounting-manager add-income 5000 "Client payment for Project X"
```

### Add Expense
```
/accounting-manager add-expense <amount> "<description>"
```
Records an expense transaction.

**Example:**
```
/accounting-manager add-expense 1200 "Office rent - February"
```

### Weekly Summary
```
/accounting-manager weekly-summary
```
Generates a summary of the current week's transactions.

### Monthly Summary
```
/accounting-manager monthly-summary
```
Generates a complete summary of the current month.

### Balance
```
/accounting-manager balance
```
Shows current month's total income, expenses, and net balance.

## Features

- **Transaction Logging**: Records all income and expense transactions
- **Automatic Dating**: Timestamps all entries automatically
- **Weekly Summaries**: Generates weekly financial summaries
- **Monthly Summaries**: Complete monthly financial reports
- **Balance Tracking**: Real-time income/expense/balance calculations
- **Markdown Format**: Human-readable accounting records
- **Persistent Storage**: All data stored in `AI_Employee_Vault/Accounting/Current_Month.md`

## File Structure

All accounting data is maintained in:
```
AI_Employee_Vault/Accounting/Current_Month.md
```

Format:
```markdown
# Accounting - February 2026

## Summary
- **Total Income**: $15,000.00
- **Total Expenses**: $8,500.00
- **Net Balance**: $6,500.00

## Transactions

| Date | Type | Amount | Description |
|------|------|--------|-------------|
| 2026-02-01 | Income | $5,000.00 | Client payment for Project X |
| 2026-02-05 | Expense | $1,200.00 | Office rent - February |
| 2026-02-10 | Income | $10,000.00 | Consulting services |
| 2026-02-15 | Expense | $7,300.00 | Equipment purchase |
```

## Implementation

The skill uses `scripts/accounting_manager.py` to:
1. Maintain the Current_Month.md file
2. Add income/expense entries
3. Calculate totals and balances
4. Generate weekly and monthly summaries
5. Handle month transitions automatically

## Examples

### Recording Income
```
User: /accounting-manager add-income 5000 "Client payment"
AI: ✓ Income recorded: $5,000.00 - Client payment
    Current balance: $5,000.00
```

### Recording Expense
```
User: /accounting-manager add-expense 1200 "Office rent"
AI: ✓ Expense recorded: $1,200.00 - Office rent
    Current balance: $3,800.00
```

### Checking Balance
```
User: /accounting-manager balance
AI: Current Month Balance:
    Income:   $15,000.00
    Expenses: $8,500.00
    Net:      $6,500.00
```

### Weekly Summary
```
User: /accounting-manager weekly-summary
AI: Week of Feb 19-25, 2026:
    Income:   $5,000.00 (2 transactions)
    Expenses: $2,300.00 (3 transactions)
    Net:      $2,700.00
```

## Notes

- All amounts are in USD
- Transactions are automatically timestamped
- Monthly files are created automatically
- Previous months are archived
- Supports decimal amounts (e.g., 1234.56)
