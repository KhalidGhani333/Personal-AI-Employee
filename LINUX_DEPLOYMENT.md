# 🐧 Linux Cloud Deployment Guide - 24/7 Operation

Complete guide to deploy Personal AI Employee on Ubuntu Linux cloud VM with PM2 process management.

---

## 📋 Prerequisites

- Ubuntu 20.04+ cloud VM (AWS EC2, DigitalOcean, etc.)
- Root or sudo access
- At least 2GB RAM, 20GB disk space
- Public IP (optional, for remote access)

---

## 🚀 Step-by-Step Deployment

### Step 1: Initial Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget vim build-essential

# Install Python 3.10+
sudo apt install -y python3.10 python3.10-venv python3-pip

# Verify Python version
python3 --version  # Should be 3.10+
```

---

### Step 2: Install Node.js and PM2

```bash
# Install Node.js 18.x LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version  # Should be v18.x
npm --version

# Install PM2 globally
sudo npm install -g pm2

# Verify PM2
pm2 --version
```

---

### Step 3: Install Playwright Dependencies

```bash
# Install Playwright system dependencies for headless browser
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0

# Install Xvfb for virtual display (needed for browser automation)
sudo apt install -y xvfb

# Install fonts
sudo apt install -y fonts-liberation fonts-noto-color-emoji
```

---

### Step 4: Clone and Setup Project

```bash
# Create project directory
mkdir -p ~/ai-employee
cd ~/ai-employee

# Clone your repository (replace with your repo URL)
git clone <your-repo-url> .

# Or upload files via SCP/SFTP
# scp -r "Personal AI Employee" user@server:~/ai-employee/

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

---

### Step 5: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

**Required credentials in .env:**
```env
# Gmail (Required)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_16_char_app_password
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LinkedIn (Optional)
LINKEDIN_EMAIL=your.email@example.com
LINKEDIN_PASSWORD=your_password

# WhatsApp (Optional - session-based)
WHATSAPP_SESSION_PATH=./AI_Employee_Vault/Logs/sessions/whatsapp_session.json

# Odoo (Optional - uses local fallback if not configured)
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

**Secure the .env file:**
```bash
chmod 600 .env
```

---

### Step 6: Create Start Script

```bash
# Create start script
nano start.sh
```

**Copy this content to start.sh:**

```bash
#!/bin/bash

# Personal AI Employee - Start Script
# Activates virtual environment and starts all services via PM2

set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file with your credentials"
    exit 1
fi

# Create necessary directories
mkdir -p AI_Employee_Vault/{Inbox,Needs_Action,Needs_Approval,Done,Logs,Accounting,Briefings,Reports}
mkdir -p logs

# Set display for Xvfb (virtual display for browser automation)
export DISPLAY=:99

# Start Xvfb if not running
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "🖥️  Starting virtual display (Xvfb)..."
    Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
    sleep 2
fi

# Start all services with PM2
echo "🚀 Starting Personal AI Employee services..."
pm2 start ecosystem.config.js

# Save PM2 process list
pm2 save

# Setup PM2 startup script (auto-start on reboot)
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u $USER --hp $HOME

echo "✅ All services started successfully!"
echo ""
echo "📊 Check status: pm2 status"
echo "📋 View logs: pm2 logs"
echo "🔄 Restart all: pm2 restart all"
echo "🛑 Stop all: pm2 stop all"
```

**Make it executable:**
```bash
chmod +x start.sh
```

---

### Step 7: Create PM2 Ecosystem Configuration

```bash
# Create PM2 config file
nano ecosystem.config.js
```

**Copy this content to ecosystem.config.js:**

```javascript
module.exports = {
  apps: [
    {
      name: 'orchestrator',
      script: 'venv/bin/python',
      args: 'scripts/run_ai_employee.py --daemon --interval 300',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/orchestrator-error.log',
      out_file: 'logs/orchestrator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'gmail-watcher',
      script: 'venv/bin/python',
      args: 'scripts/gmail_watcher.py --continuous --interval 300',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/gmail-watcher-error.log',
      out_file: 'logs/gmail-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'whatsapp-watcher',
      script: 'venv/bin/python',
      args: 'scripts/whatsapp_watcher.py --continuous --interval 120',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/whatsapp-watcher-error.log',
      out_file: 'logs/whatsapp-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'linkedin-watcher',
      script: 'venv/bin/python',
      args: 'scripts/linkedin_watcher.py --continuous --interval 300',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/linkedin-watcher-error.log',
      out_file: 'logs/linkedin-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'reply-generator',
      script: 'venv/bin/python',
      args: 'scripts/reply_generator.py --continuous --interval 300',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/reply-generator-error.log',
      out_file: 'logs/reply-generator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'reply-sender',
      script: 'venv/bin/python',
      args: 'scripts/reply_sender.py --continuous --interval 600',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/reply-sender-error.log',
      out_file: 'logs/reply-sender-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'ralph-wiggum',
      script: 'venv/bin/python',
      args: 'scripts/ralph_wiggum_loop.py continuous',
      cwd: '/home/ubuntu/ai-employee',
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/ralph-wiggum-error.log',
      out_file: 'logs/ralph-wiggum-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    }
  ]
};
```

**⚠️ Important:** Update the `cwd` path in ecosystem.config.js to match your actual project path:
```bash
# Find your project path
pwd
# Example output: /home/ubuntu/ai-employee

# Replace '/home/ubuntu/ai-employee' in ecosystem.config.js with your actual path
```

---

### Step 8: Start Services

```bash
# Run the start script
./start.sh

# Check status
pm2 status

# View logs
pm2 logs

# View specific service logs
pm2 logs orchestrator
pm2 logs gmail-watcher
```

---

## 🔍 Health Check Instructions

### Check System Status

```bash
# PM2 process status
pm2 status

# Detailed info for specific service
pm2 info orchestrator

# View real-time logs
pm2 logs --lines 50

# Check if Xvfb is running
ps aux | grep Xvfb

# Check Python processes
ps aux | grep python
```

### Check Application Health

```bash
# Activate virtual environment
source venv/bin/activate

# Check orchestrator status
python scripts/run_ai_employee.py --status

# Check vault folders
ls -la AI_Employee_Vault/Inbox/
ls -la AI_Employee_Vault/Needs_Action/
ls -la AI_Employee_Vault/Needs_Approval/

# Check logs
tail -f logs/ai_employee.log
tail -f logs/orchestrator-out.log
tail -f logs/gmail-watcher-out.log
```

### Monitor Resource Usage

```bash
# CPU and memory usage
pm2 monit

# Disk usage
df -h

# Check log file sizes
du -sh logs/
du -sh AI_Employee_Vault/Logs/

# System resources
htop  # or: top
```

---

## 🔧 Common PM2 Commands

```bash
# Start all services
pm2 start ecosystem.config.js

# Stop all services
pm2 stop all

# Restart all services
pm2 restart all

# Delete all services
pm2 delete all

# Restart specific service
pm2 restart orchestrator

# View logs
pm2 logs
pm2 logs orchestrator --lines 100

# Flush logs
pm2 flush

# Save current process list
pm2 save

# Resurrect saved processes
pm2 resurrect

# Monitor in real-time
pm2 monit
```

---

## 🔄 Auto-Start on System Reboot

```bash
# Generate startup script (run after pm2 start)
pm2 startup

# This will output a command like:
# sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u ubuntu --hp /home/ubuntu

# Copy and run that command

# Save current PM2 process list
pm2 save

# Test reboot
sudo reboot

# After reboot, check if services auto-started
pm2 status
```

---

## 🛡️ Security Best Practices

### 1. Firewall Configuration

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS (if needed)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

### 2. Secure Credentials

```bash
# Set proper permissions
chmod 600 .env
chmod 700 AI_Employee_Vault/

# Never commit .env to git
echo ".env" >> .gitignore
```

### 3. Regular Updates

```bash
# Update system packages weekly
sudo apt update && sudo apt upgrade -y

# Update Python packages
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

---

## 📊 Log Management

### Rotate Logs Automatically

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/ai-employee
```

**Add this content:**
```
/home/ubuntu/ai-employee/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 ubuntu ubuntu
}
```

### Manual Log Cleanup

```bash
# Clear PM2 logs
pm2 flush

# Clear application logs
rm -f logs/*.log

# Clear old vault logs
find AI_Employee_Vault/Logs/ -type f -mtime +30 -delete
```

---

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check PM2 logs
pm2 logs --err

# Check Python path
which python3
source venv/bin/activate
which python

# Test script manually
source venv/bin/activate
python scripts/run_ai_employee.py --once
```

### Browser Automation Issues

```bash
# Check Xvfb is running
ps aux | grep Xvfb

# Restart Xvfb
pkill Xvfb
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &

# Test Playwright
source venv/bin/activate
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

### WhatsApp/LinkedIn Session Issues

```bash
# Delete session files to force re-login
rm -f AI_Employee_Vault/Logs/sessions/*.json

# Run watcher once to re-authenticate
source venv/bin/activate
DISPLAY=:99 python scripts/whatsapp_watcher.py --once
```

### High Memory Usage

```bash
# Check memory usage
pm2 monit

# Restart specific service
pm2 restart whatsapp-watcher

# Reduce max_memory_restart in ecosystem.config.js
nano ecosystem.config.js
# Change max_memory_restart: '400M' to '300M'
pm2 restart all
```

---

## 📈 Performance Optimization

### 1. Adjust Check Intervals

Edit `ecosystem.config.js` to change intervals:
- Gmail: 300s (5 min) → 600s (10 min) for less frequent checks
- WhatsApp: 120s (2 min) → 180s (3 min)
- Reply Generator: 300s → 600s

### 2. Disable Unused Services

```bash
# Stop services you don't need
pm2 stop whatsapp-watcher
pm2 stop linkedin-watcher

# Remove from startup
pm2 delete whatsapp-watcher
pm2 save
```

### 3. Use Smaller VM

Minimum requirements:
- 1 vCPU, 2GB RAM for basic operation (Gmail only)
- 2 vCPU, 4GB RAM for full operation (all watchers)

---

## 🔗 Remote Access

### Access Vault Files Remotely

```bash
# Via SCP
scp user@server:~/ai-employee/AI_Employee_Vault/Dashboard.md ./

# Via SFTP
sftp user@server
cd ai-employee/AI_Employee_Vault
get Dashboard.md

# Via rsync (sync entire vault)
rsync -avz user@server:~/ai-employee/AI_Employee_Vault/ ./local-vault/
```

### Web-based File Access (Optional)

```bash
# Install file browser
curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash

# Run file browser
filebrowser -r ~/ai-employee/AI_Employee_Vault -p 8080

# Access via: http://your-server-ip:8080
```

---

## ✅ Deployment Checklist

- [ ] Ubuntu server provisioned
- [ ] Python 3.10+ installed
- [ ] Node.js and PM2 installed
- [ ] Playwright dependencies installed
- [ ] Xvfb installed and running
- [ ] Project cloned/uploaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] .env file secured (chmod 600)
- [ ] start.sh created and executable
- [ ] ecosystem.config.js created with correct paths
- [ ] Services started with PM2
- [ ] PM2 startup configured
- [ ] PM2 process list saved
- [ ] Health checks passing
- [ ] Logs rotating properly
- [ ] Firewall configured
- [ ] System tested after reboot

---

## 🎉 Success Verification

After deployment, verify everything is working:

```bash
# 1. Check all services are running
pm2 status
# All should show "online" status

# 2. Check application status
source venv/bin/activate
python scripts/run_ai_employee.py --status

# 3. Check logs for errors
pm2 logs --lines 50 --nostream

# 4. Test email monitoring
python scripts/gmail_watcher.py --once

# 5. Check vault folders
ls -la AI_Employee_Vault/Inbox/
ls -la AI_Employee_Vault/Needs_Action/

# 6. Verify auto-restart
pm2 restart orchestrator
sleep 10
pm2 status  # Should show "online" again

# 7. Test system reboot
sudo reboot
# Wait 2 minutes, then SSH back in
pm2 status  # All services should be running
```

---

## 📞 Support

If you encounter issues:

1. Check PM2 logs: `pm2 logs --err`
2. Check application logs: `tail -f logs/ai_employee.log`
3. Test scripts manually: `python scripts/run_ai_employee.py --once`
4. Verify .env credentials
5. Check Xvfb is running: `ps aux | grep Xvfb`

---

**🚀 Your Personal AI Employee is now running 24/7 on Linux!**

**Status Dashboard:** `python scripts/run_ai_employee.py --status`
**PM2 Monitor:** `pm2 monit`
**View Logs:** `pm2 logs`
