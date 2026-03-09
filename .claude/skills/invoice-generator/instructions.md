# Invoice Generator - Detailed Instructions

## Objective
Generate professional invoices, send them to clients, and track payment status.

## Invoice Creation Workflow

### 1. Gather Information
```
Required Data:
- Client name and contact
- Invoice number (auto-increment)
- Invoice date
- Due date (from payment terms)
- Line items (description, quantity, rate)
- Subtotal, tax, total
- Payment instructions
```

### 2. Generate Invoice PDF
```
Template Structure:

[Company Logo/Header]

INVOICE #INV-{number}
Date: {invoice_date}
Due Date: {due_date}

Bill To:
{client_name}
{client_address}
{client_email}

Description          Qty    Rate      Amount
{item_1}            {qty}   ${rate}   ${amount}
{item_2}            {qty}   ${rate}   ${amount}

                    Subtotal:  ${subtotal}
                    Tax (10%): ${tax}
                    Total:     ${total}

Payment Instructions:
{payment_details}

Terms: {payment_terms}
```

### 3. Create Invoice Record
```markdown
---
type: invoice
invoice_number: INV-{number}
client: {client_name}
amount: {total}
date: {invoice_date}
due_date: {due_date}
status: sent|paid|overdue
payment_method: bank_transfer|paypal|stripe
---

## Line Items
- {item_1}: ${amount}
- {item_2}: ${amount}

## Payment Tracking
- Sent: {sent_date}
- Paid: {paid_date}
- Payment Method: {method}

## Follow-ups
- [ ] Send reminder 3 days before due
- [ ] Send reminder on due date
- [ ] Send overdue notice 3 days after
```

### 4. Create Email Draft
```markdown
---
type: email_draft
to: {client_email}
subject: Invoice #{number} - ${amount} Due {due_date}
attachment: /Invoices/INV-{number}.pdf
requires_approval: true
---

## Email Content

Dear {client_name},

Thank you for your business! Please find attached invoice #{number} for ${amount}.

**Invoice Details:**
- Invoice Number: INV-{number}
- Amount Due: ${amount}
- Due Date: {due_date}

**Payment Instructions:**
{payment_instructions}

Please let me know if you have any questions.

Best regards,
{your_name}
```

### 5. Request Approval
```
Move email draft to /Pending_Approval
Wait for human approval
Once approved, send via Email MCP
```

## Invoice Numbering

**Format:** INV-YYYY-NNNN
- YYYY: Year
- NNNN: Sequential number (0001, 0002, etc.)

**Example:** INV-2026-0042

**Storage:** Track last invoice number in /Accounting/invoice_counter.txt

## Payment Terms

**Standard Terms:**
- Net 15: Payment due in 15 days
- Net 30: Payment due in 30 days
- Net 60: Payment due in 60 days
- Due on Receipt: Immediate payment

**Late Fees:**
- After 30 days: 5% late fee
- After 60 days: 10% late fee

## Status Tracking

**Invoice Statuses:**
- **Draft**: Created but not sent
- **Sent**: Sent to client
- **Viewed**: Client opened email
- **Paid**: Payment received
- **Overdue**: Past due date
- **Cancelled**: Invoice cancelled

**Status Updates:**
```
Check daily:
- If current_date > due_date AND status = sent
  → Update status to overdue
  → Create follow-up task
  → Send overdue notice (if approved)
```

## Follow-up Workflow

**3 Days Before Due:**
```
Subject: Friendly Reminder - Invoice #{number} Due Soon

Hi {client_name},

This is a friendly reminder that invoice #{number} for ${amount} is due on {due_date}.

If you've already sent payment, please disregard this message.

Thank you!
```

**On Due Date:**
```
Subject: Invoice #{number} Due Today

Hi {client_name},

Invoice #{number} for ${amount} is due today.

Please let me know if you need any assistance.

Thank you!
```

**3 Days After Due:**
```
Subject: Overdue Invoice #{number} - Action Required

Hi {client_name},

Invoice #{number} for ${amount} is now 3 days overdue.

Please arrange payment at your earliest convenience.

If there's an issue, please contact me to discuss.

Thank you!
```

## Integration Points

- **Approval Handler**: Approve invoice sending
- **Email Processor**: Send invoice emails
- **Accounting Integrator**: Sync to Odoo
- **Dashboard Updater**: Update invoice stats
- **Task Manager**: Create follow-up tasks

## Reporting

**Monthly Invoice Report:**
```markdown
# Invoice Report - {month} {year}

## Summary
- Total Invoices Sent: {count}
- Total Amount Invoiced: ${total}
- Total Paid: ${paid}
- Total Outstanding: ${outstanding}
- Average Payment Time: {days} days

## Overdue Invoices
- INV-{number}: ${amount} - {days} days overdue
- INV-{number}: ${amount} - {days} days overdue

## Top Clients by Revenue
1. {client_1}: ${amount}
2. {client_2}: ${amount}
3. {client_3}: ${amount}
```

## Success Criteria
- Invoices sent within 24 hours of request
- All invoices tracked accurately
- Follow-ups sent automatically
- Payment status always current
- 90%+ collection rate
