# 🏦 Odoo Integration Setup Guide

Complete guide to set up Odoo accounting system for your Personal AI Employee.

---

## 📋 Overview

This guide helps you integrate **Odoo Community Edition** (self-hosted) with your AI Employee for professional accounting management.

**Gold Tier Requirement:** ✅ Self-hosted Odoo with MCP server integration

---

## 🎯 Quick Start (5 Minutes)

### Option 1: Docker Setup (Recommended)

1. **Start Docker Desktop**
   ```bash
   # Make sure Docker Desktop is running
   ```

2. **Run Setup Script**
   ```bash
   cd scripts
   setup_odoo_docker.bat
   ```

3. **Wait for Odoo to Start (30-60 seconds)**
   - Open browser: http://localhost:8069

4. **Configure Odoo (First Time Only)**
   - Master Password: `admin`
   - Database Name: `odoo_db`
   - Email: `admin@example.com`
   - Password: `admin123`
   - Click "Create Database"

5. **Done!** Your Odoo is ready.

---

## 🔧 Configuration

### Update .env File

Your `.env` already has Odoo configuration:

```bash
# Odoo Accounting (Self-hosted)
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin123
```

**Note:** Change password after first login for security.

---

## 🚀 Usage

### Start Odoo
```bash
cd scripts
start_odoo.bat
```

### Stop Odoo
```bash
cd scripts
stop_odoo.bat
```

### Test Connection
```bash
python scripts/odoo_integration.py connect
```

Expected output:
```
[SUCCESS] Connected to Odoo
URL: http://localhost:8069
Database: odoo_db
User ID: 2
```

---

## 💰 Accounting Operations

### Record Expense
```bash
# Via Python script
python scripts/odoo_integration.py expense 50.00 "Office supplies" --category office

# Via Skill
claude /odoo-integration expense 50.00 "Office supplies" --category office
```

### Record Income
```bash
# Via Python script
python scripts/odoo_integration.py income 500.00 "Client payment" --source client

# Via Skill
claude /odoo-integration income 500.00 "Client payment" --source client
```

### Check Balance
```bash
# Via Python script
python scripts/odoo_integration.py balance

# Via Skill
claude /odoo-integration balance
```

### Generate Report
```bash
# Via Skill
claude /odoo-integration report monthly
```

---

## 🔄 Automatic Fallback

**Smart Fallback System:**
- If Odoo is running → Uses Odoo ✅
- If Odoo is stopped → Uses local JSON storage 📁
- No errors, seamless transition!

**Local Storage Location:**
```
AI_Employee_Vault/Accounting/transactions.json
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         AI Employee (Claude)            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Accounting MCP Server v2.0         │
│  (Odoo Integration + Local Fallback)    │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌──────────────┐  ┌──────────────┐
│ Odoo Docker  │  │ Local JSON   │
│ (Primary)    │  │ (Fallback)   │
└──────────────┘  └──────────────┘
```

---

## 📊 Features

### Odoo Mode
- ✅ Professional accounting system
- ✅ Multi-user support
- ✅ Advanced reporting
- ✅ Audit trails
- ✅ Invoice generation
- ✅ Tax management
- ✅ Bank reconciliation

### Local Mode (Fallback)
- ✅ No setup required
- ✅ Works offline
- ✅ Fast and simple
- ✅ Basic expense/income tracking
- ✅ Balance calculation
- ✅ Simple reports

---

## 🔍 Troubleshooting

### Issue: "Docker not running"
**Solution:**
1. Open Docker Desktop
2. Wait for it to start (green icon)
3. Run `start_odoo.bat`

### Issue: "Odoo not connected"
**Solution:**
1. Check if containers are running: `docker ps`
2. Start Odoo: `start_odoo.bat`
3. Wait 30 seconds for startup
4. Test: `python scripts/odoo_integration.py connect`

### Issue: "Authentication failed"
**Solution:**
1. Open http://localhost:8069
2. Login with credentials from `.env`
3. If password wrong, reset in Odoo UI
4. Update `.env` with new password

### Issue: "Port 8069 already in use"
**Solution:**
1. Stop existing Odoo: `stop_odoo.bat`
2. Or change port in `.env`: `ODOO_URL=http://localhost:8070`
3. Update Docker command in setup script

### Issue: "Database doesn't exist"
**Solution:**
1. Open http://localhost:8069
2. Create database named `odoo_db`
3. Or change `ODOO_DB` in `.env` to match existing database

---

## 🎓 Learning Resources

**Odoo Documentation:**
- Official Docs: https://www.odoo.com/documentation
- JSON-RPC API: https://www.odoo.com/documentation/17.0/developer/reference/external_api.html

**Docker Commands:**
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker logs odoo-app

# Restart container
docker restart odoo-app

# Remove containers (clean install)
docker stop odoo-app odoo-db
docker rm odoo-app odoo-db
```

---

## 🔐 Security Best Practices

1. **Change Default Password**
   - Login to Odoo
   - Settings → Users → Admin
   - Change password
   - Update `.env`

2. **Don't Commit .env**
   - Already in `.gitignore`
   - Never share credentials

3. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix of letters, numbers, symbols

4. **Regular Backups**
   ```bash
   # Backup Odoo data
   docker exec odoo-db pg_dump -U odoo odoo_db > backup.sql
   ```

---

## 📈 Gold Tier Completion

✅ **Requirement Met:**
> "Create an accounting system for your business in Odoo Community (self-hosted, local) and integrate it via an MCP server using Odoo's JSON-RPC APIs"

**What's Implemented:**
- ✅ Odoo 17 Community Edition (Docker)
- ✅ PostgreSQL database
- ✅ XML-RPC API integration
- ✅ Accounting MCP Server v2.0
- ✅ Expense/Income tracking
- ✅ Balance calculation
- ✅ Report generation
- ✅ Automatic fallback to local storage
- ✅ Agent Skill for easy access

---

## 🚀 Next Steps

1. **Start Odoo:** `scripts/start_odoo.bat`
2. **Test Connection:** `python scripts/odoo_integration.py connect`
3. **Record Test Transaction:** `python scripts/odoo_integration.py expense 10.00 "Test"`
4. **Check Balance:** `python scripts/odoo_integration.py balance`
5. **Use with AI Employee:** `claude /odoo-integration balance`

---

## 📞 Support

**Common Commands:**
```bash
# Setup (one time)
scripts/setup_odoo_docker.bat

# Daily use
scripts/start_odoo.bat
scripts/stop_odoo.bat

# Testing
python scripts/odoo_integration.py connect
python scripts/odoo_integration.py balance
```

**Access Odoo Web UI:**
- URL: http://localhost:8069
- Username: admin
- Password: admin123

---

*Part of Personal AI Employee - Gold Tier Complete* 🏆
