# Invoice Generator Skill

Create and send professional invoices to clients.

## Metadata
- **Tier**: Silver
- **Priority**: High
- **Dependencies**: Approval Handler, Email Processor
- **Triggers**: Invoice requests, payment due dates

## Capabilities
- Generate PDF invoices
- Calculate amounts and taxes
- Track invoice status
- Send invoices via email
- Follow up on unpaid invoices
- Integrate with accounting system

## Usage
```bash
/invoice-generator --client={client_name} --amount={amount}
```

## Expected Input
- Client information
- Service/product details
- Amount and payment terms
- Invoice template preferences

## Expected Output
- PDF invoice in /Invoices folder
- Email draft in /Pending_Approval
- Invoice tracking entry
- Accounting system update
