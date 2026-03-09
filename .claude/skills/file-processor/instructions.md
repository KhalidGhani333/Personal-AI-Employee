# File Processor - Detailed Instructions

## Objective
Process files dropped in /Inbox, extract information, and take appropriate actions.

## Supported File Types

### PDFs
- Invoices
- Contracts
- Reports
- Documents

### Spreadsheets (CSV, XLSX)
- Bank transactions
- Expense reports
- Client lists
- Inventory data

### Images (JPG, PNG)
- Receipts
- Screenshots
- Diagrams
- Photos

## Processing Workflow

### 1. Detect File Drop
```
Input: FILE_*.md in /Needs_Action
Read: File metadata and location
Determine: File type from extension
```

### 2. Process by Type

**PDF Processing:**
```
1. Extract text using PDF parser
2. Identify document type:
   - Invoice: Extract amount, date, vendor
   - Contract: Extract parties, dates, terms
   - Report: Summarize key points
3. Create structured data file
4. Update Dashboard
```

**CSV Processing:**
```
1. Read CSV data
2. Identify columns and data types
3. If bank transactions:
   - Parse date, amount, description
   - Categorize transactions
   - Calculate totals
   - Flag unusual transactions
4. Create summary report
```

**Image Processing:**
```
1. Analyze image content
2. If receipt:
   - Extract merchant, amount, date
   - Create expense entry
3. If screenshot:
   - Extract text (OCR if needed)
   - Summarize content
4. Store in appropriate folder
```

### 3. Extract Key Information

**For Invoices:**
```markdown
---
type: invoice
vendor: {vendor_name}
amount: {total_amount}
date: {invoice_date}
due_date: {due_date}
status: unpaid
---

## Invoice Details
- Invoice #: {number}
- Items: {item_list}
- Subtotal: {subtotal}
- Tax: {tax}
- Total: {total}

## Action Required
- [ ] Verify invoice accuracy
- [ ] Approve payment
- [ ] Schedule payment
```

**For Bank Transactions:**
```markdown
---
type: bank_transactions
file: {filename}
transaction_count: {count}
total_credits: {credits}
total_debits: {debits}
date_range: {start} to {end}
---

## Summary
- Total Income: ${credits}
- Total Expenses: ${debits}
- Net: ${net}

## Flagged Transactions
- Large expense: ${amount} to {vendor}
- Unusual charge: ${amount} from {source}

## Action Required
- [ ] Review flagged transactions
- [ ] Categorize expenses
- [ ] Update accounting system
```

### 4. Create Follow-up Tasks

Based on file content, create tasks:
```
- Invoice → Task: "Pay invoice #{number} by {due_date}"
- Contract → Task: "Review contract with {party}"
- Receipt → Task: "Categorize expense: {merchant}"
```

### 5. Update Dashboard
```
- Increment files_processed_count
- Add to Recent Activity
- Update file_types_processed stats
```

### 6. Move Files
```
- Original file → /Documents or /Accounting
- Metadata file → /Done/Files
- Extracted data → Appropriate folder
```

## Special Cases

**Sensitive Documents:**
- Flag for human review
- Don't auto-process
- Create approval request

**Corrupted Files:**
- Log error
- Move to /Errors
- Notify user

**Unknown File Types:**
- Store in /Files/Unknown
- Create task for manual review

## Integration Points

- **Task Manager**: Create follow-up tasks
- **Dashboard Updater**: Update file stats
- **Accounting Integrator**: Send financial data
- **Log Manager**: Log all processing

## Success Criteria
- All files processed within 10 minutes
- Key information extracted accurately
- Appropriate tasks created
- Dashboard reflects file activity
