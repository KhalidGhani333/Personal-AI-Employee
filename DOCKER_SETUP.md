# Docker Setup Guide - Personal AI Employee

Complete guide for running your Personal AI Employee using Docker.

---

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 20GB free disk space

### 1. Initial Setup

```bash
# Clone or navigate to project directory
cd "Personal AI Employee"

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 2. Configure Secrets

Create secrets directory and add your credentials:

```bash
mkdir -p secrets

# Add Gmail credentials (from Google Cloud Console)
cp /path/to/your/gmail_credentials.json secrets/

# Add SSH keys for Git sync (Platinum tier)
mkdir -p secrets/git_ssh
cp ~/.ssh/id_rsa secrets/git_ssh/
chmod 600 secrets/git_ssh/id_rsa
```

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

---

## 📦 Services Overview

| Service | Port | Description |
|---------|------|-------------|
| postgres | 5432 | PostgreSQL database for Odoo |
| odoo | 8069 | Odoo Community Edition (Accounting) |
| ai_employee | - | Core AI Employee (Watchers + Orchestrator) |
| watchdog | - | Health monitoring & auto-restart |
| ceo_briefing | - | Weekly CEO briefing generator |
| vault_sync | - | Git-based vault synchronization |

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file with your credentials:

```bash
# Required for all tiers
ANTHROPIC_API_KEY=sk-ant-your-key-here
POSTGRES_PASSWORD=secure_password
ODOO_PASSWORD=secure_password

# Required for Silver/Gold tiers
GMAIL_CREDENTIALS_PATH=/app/secrets/gmail_credentials.json
LINKEDIN_ACCESS_TOKEN=your_token
TWITTER_API_KEY=your_key
FACEBOOK_ACCESS_TOKEN=your_token

# Required for Platinum tier
GIT_SYNC_ENABLED=true
GIT_REMOTE_URL=git@github.com:user/vault.git
CLOUD_SYNC_ENABLED=true
```

### Odoo Setup

1. Access Odoo at http://localhost:8069
2. Create database: `odoo`
3. Set master password (save in .env)
4. Install Accounting module
5. Configure company details

---

## 🎯 Usage Commands

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d odoo

# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes data)
docker-compose down -v

# Restart service
docker-compose restart ai_employee
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ai_employee

# Last 100 lines
docker-compose logs --tail=100 watchdog
```

### Execute Commands

```bash
# Run CEO briefing manually
docker-compose exec ceo_briefing python /app/scripts/ceo_briefing.py weekly

# Check vault sync status
docker-compose exec vault_sync git -C /app/AI_Employee_Vault status

# Access PostgreSQL
docker-compose exec postgres psql -U odoo -d odoo
```

---

## 🔍 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs service_name

# Rebuild image
docker-compose build --no-cache service_name
docker-compose up -d service_name
```

### Odoo Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test database connection
docker-compose exec postgres psql -U odoo -d postgres -c "SELECT 1;"
```

### Vault Sync Issues

```bash
# Manual sync
docker-compose exec vault_sync sh -c "cd /app/AI_Employee_Vault && git pull && git push"

# Check SSH keys
docker-compose exec vault_sync ls -la /root/.ssh/
```

---

## 🔐 Security Best Practices

### 1. Secrets Management

```bash
# Never commit secrets
echo "secrets/" >> .gitignore
echo ".env" >> .gitignore

# Use strong passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
```

### 2. Volume Permissions

```bash
# Ensure proper ownership
sudo chown -R 1000:1000 AI_Employee_Vault/
sudo chmod 700 secrets/
```

---

## 📊 Monitoring

### View Resource Usage

```bash
# All containers
docker stats

# Disk usage
docker system df
```

---

## 🔄 Updates & Maintenance

### Backup Data

```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U odoo odoo > backup_$(date +%Y%m%d).sql

# Backup vault
tar -czf vault_backup_$(date +%Y%m%d).tar.gz AI_Employee_Vault/
```

### Restore Data

```bash
# Restore PostgreSQL
cat backup.sql | docker-compose exec -T postgres psql -U odoo odoo

# Restore vault
tar -xzf vault_backup.tar.gz
```

---

## 🚀 Production Deployment

### Cloud VM Setup (Ubuntu)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start services
docker-compose up -d

# Enable auto-start on boot
sudo systemctl enable docker
```

---

## ✅ Verification Checklist

- [ ] Docker and Docker Compose installed
- [ ] .env file configured with all credentials
- [ ] Secrets directory created with credentials
- [ ] All services started successfully
- [ ] Odoo accessible at http://localhost:8069
- [ ] PostgreSQL connection working
- [ ] Vault folders created and accessible
- [ ] Logs showing no errors
- [ ] Health checks passing

---

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Review troubleshooting section above
3. Check GitHub issues
4. Join Wednesday Research Meeting

---

**Quick Test:**
```bash
# Start everything
docker-compose up -d

# Wait 30 seconds
sleep 30

# Check all services
docker-compose ps

# View logs
docker-compose logs --tail=50 ai_employee
```
