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
echo ""
echo "⚙️  Setting up auto-start on reboot..."
echo "Run this command to enable auto-start:"
echo "sudo env PATH=\$PATH:/usr/bin pm2 startup systemd -u \$USER --hp \$HOME"

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📊 Check status: pm2 status"
echo "📋 View logs: pm2 logs"
echo "🔄 Restart all: pm2 restart all"
echo "🛑 Stop all: pm2 stop all"
