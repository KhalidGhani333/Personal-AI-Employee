# Odoo Integration Skill

**Description:** Manage Odoo accounting system - record expenses, income, and generate financial reports.

**Category:** Accounting & Finance

**Version:** 1.0.0

---

## What This Skill Does

This skill integrates with your self-hosted Odoo accounting system to:
- Record business expenses with categories
- Track income from various sources
- Get real-time balance and financial summaries
- Generate detailed financial reports
- Automatically fallback to local storage if Odoo is unavailable

---

## When to Use This Skill

Use this skill when you need to:
- Record a business expense (e.g., "Record $50 expense for office supplies")
- Log income from clients (e.g., "Record $500 income from Client A")
- Check current balance (e.g., "What's my current balance?")
- Generate financial reports (e.g., "Generate monthly financial report")

---

## Prerequisites

1. **Odoo Setup (Optional):**
   - Run `scripts/setup_odoo_docker.bat` to install Odoo via Docker
   - Configure Odoo at http://localhost:8069
   - Update `.env` with Odoo credentials

2. **Environment Variables:**
   ```
   ODOO_URL=http://localhost:8069
   ODOO_DB=odoo_db
   ODOO_USERNAME=admin
   ODOO_PASSWORD=admin123
   ```

3. **Fallback Mode:**
   - If Odoo is not configured, automatically uses local JSON storage
   - No setup required for local mode

---

## How to Use

### Record Expense
```bash
claude /odoo-integration expense 50.00 "Office supplies" --category office
```

### Record Income
```bash
claude /odoo-integration income 500.00 "Client payment" --source client
```

### Check Balance
```bash
claude /odoo-integration balance
```

### Generate Report
```bash
claude /odoo-integration report monthly
```

---

## Examples

**Example 1: Record Office Expense**
```
User: "Record $75 expense for software subscription"
Skill: Records expense in Odoo (or local storage)
Output: "✅ Expense recorded: $75.00 - Software subscription"
```

**Example 2: Track Client Payment**
```
User: "Log $1,200 income from Project Alpha"
Skill: Records income in Odoo
Output: "✅ Income recorded: $1,200.00 - Project Alpha"
```

**Example 3: Financial Summary**
```
User: "What's my current balance?"
Skill: Retrieves balance from Odoo
Output: "Balance: $2,450.00 | Income: $3,500 | Expenses: $1,050"
```

---

## Integration with Other Skills

- **CEO Briefing:** Uses accounting data for weekly business reports
- **Task Manager:** Links expenses to specific projects
- **Approval Handler:** Requires approval for expenses over $100

---

## Storage Options

### Odoo Mode (Recommended for Production)
- ✅ Professional accounting system
- ✅ Multi-user support
- ✅ Advanced reporting
- ✅ Audit trails
- ⚠️ Requires Docker setup

### Local Mode (Default Fallback)
- ✅ No setup required
- ✅ Works offline
- ✅ Fast and simple
- ⚠️ Single-user only
- ⚠️ Basic features

---

## Technical Details

**MCP Server:** `accounting_mcp`
**Storage:** Odoo (primary) → Local JSON (fallback)
**Location:** `AI_Employee_Vault/Accounting/transactions.json`
**Reports:** `AI_Employee_Vault/Accounting/Reports/`

---

## Troubleshooting

**Issue:** "Odoo not connected"
- **Solution:** Run `scripts/start_odoo.bat` or use local storage

**Issue:** "Authentication failed"
- **Solution:** Check `.env` credentials match Odoo setup

**Issue:** "Docker not running"
- **Solution:** Start Docker Desktop, then run `scripts/start_odoo.bat`

---

## Gold Tier Requirement

✅ This skill fulfills Gold Tier requirement #3:
> "Create an accounting system in Odoo Community (self-hosted, local) and integrate it via an MCP server"

---

*Part of Personal AI Employee - Gold Tier Complete*
