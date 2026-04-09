#!/bin/bash

# Setup System Health Monitoring
# Configures cron job to run watchdog every 5 minutes

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WATCHDOG_SCRIPT="$SCRIPT_DIR/watchdog.py"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
LOG_FILE="$SCRIPT_DIR/logs/watchdog.log"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🐕 Setting up System Health Monitoring"
echo ""

# Check if watchdog.py exists
if [ ! -f "$WATCHDOG_SCRIPT" ]; then
    echo -e "${RED}❌ Error: watchdog.py not found${NC}"
    exit 1
fi

# Check if Python virtual environment exists
if [ ! -f "$PYTHON_BIN" ]; then
    echo -e "${YELLOW}⚠️  Warning: Virtual environment not found${NC}"
    echo "Using system Python instead"
    PYTHON_BIN="python3"
fi

# Install required Python package (psutil)
echo "📦 Installing required packages..."
$PYTHON_BIN -m pip install psutil --quiet || {
    echo -e "${RED}❌ Failed to install psutil${NC}"
    exit 1
}

# Create cron job entry
CRON_ENTRY="*/5 * * * * cd $SCRIPT_DIR && $PYTHON_BIN watchdog.py >> $LOG_FILE 2>&1"

echo ""
echo "📋 Cron Job Configuration:"
echo "   Frequency: Every 5 minutes"
echo "   Script: $WATCHDOG_SCRIPT"
echo "   Log: $LOG_FILE"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "watchdog.py"; then
    echo -e "${YELLOW}⚠️  Watchdog cron job already exists${NC}"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep watchdog.py
    echo ""
    read -p "Replace existing cron job? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi

    # Remove existing watchdog cron jobs
    crontab -l | grep -v "watchdog.py" | crontab -
fi

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo -e "${GREEN}✅ Cron job added successfully${NC}"
echo ""

# Verify cron job
echo "📋 Verifying cron job..."
if crontab -l | grep -q "watchdog.py"; then
    echo -e "${GREEN}✅ Cron job verified${NC}"
    echo ""
    echo "Current watchdog cron jobs:"
    crontab -l | grep watchdog.py
else
    echo -e "${RED}❌ Failed to verify cron job${NC}"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📊 Monitoring Status:"
echo "   ✅ Watchdog will run every 5 minutes"
echo "   ✅ Services will auto-restart if stopped"
echo "   ✅ Health log: AI_Employee_Vault/Logs/system_health.md"
echo "   ✅ Watchdog log: $LOG_FILE"
echo ""
echo "🔧 Commands:"
echo "   View cron jobs: crontab -l"
echo "   Remove cron job: crontab -e (then delete the line)"
echo "   Test watchdog: python watchdog.py"
echo "   View health log: cat AI_Employee_Vault/Logs/system_health.md"
echo "   View watchdog log: tail -f $LOG_FILE"
echo ""
