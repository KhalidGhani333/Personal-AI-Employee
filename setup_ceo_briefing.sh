#!/bin/bash

# Setup Automated Weekly CEO Briefing
# Configures cron job to run every Sunday at 9 AM

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CEO_BRIEFING_SCRIPT="$SCRIPT_DIR/scripts/ceo_briefing.py"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
LOG_FILE="$SCRIPT_DIR/logs/ceo_briefing_cron.log"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "📊 Setting up Automated Weekly CEO Briefing"
echo ""

# Check if ceo_briefing.py exists
if [ ! -f "$CEO_BRIEFING_SCRIPT" ]; then
    echo -e "${RED}❌ Error: ceo_briefing.py not found${NC}"
    exit 1
fi

# Check if Python virtual environment exists
if [ ! -f "$PYTHON_BIN" ]; then
    echo -e "${YELLOW}⚠️  Warning: Virtual environment not found${NC}"
    echo "Using system Python instead"
    PYTHON_BIN="python3"
fi

# Create cron job entry for Sunday at 9 AM
CRON_ENTRY="0 9 * * 0 cd $SCRIPT_DIR && $PYTHON_BIN scripts/ceo_briefing.py weekly >> $LOG_FILE 2>&1"

echo ""
echo "📋 Cron Job Configuration:"
echo "   Schedule: Every Sunday at 9:00 AM"
echo "   Script: $CEO_BRIEFING_SCRIPT"
echo "   Log: $LOG_FILE"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "ceo_briefing.py weekly"; then
    echo -e "${YELLOW}⚠️  CEO briefing cron job already exists${NC}"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep "ceo_briefing.py"
    echo ""
    read -p "Replace existing cron job? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi

    # Remove existing CEO briefing cron jobs
    crontab -l | grep -v "ceo_briefing.py" | crontab -
fi

# Add cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo -e "${GREEN}✅ Cron job added successfully${NC}"
echo ""

# Verify cron job
echo "📋 Verifying cron job..."
if crontab -l | grep -q "ceo_briefing.py weekly"; then
    echo -e "${GREEN}✅ Cron job verified${NC}"
    echo ""
    echo "Current CEO briefing cron jobs:"
    crontab -l | grep "ceo_briefing.py"
else
    echo -e "${RED}❌ Failed to verify cron job${NC}"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📊 CEO Briefing Status:"
echo "   ✅ Weekly briefing will run every Sunday at 9:00 AM"
echo "   ✅ Reports saved to: AI_Employee_Vault/Briefings/"
echo "   ✅ Cron log: $LOG_FILE"
echo ""
echo "🔧 Commands:"
echo "   View cron jobs: crontab -l"
echo "   Remove cron job: crontab -e (then delete the line)"
echo "   Test briefing: python scripts/ceo_briefing.py weekly"
echo "   View latest briefing: ls -lt AI_Employee_Vault/Briefings/ | head -5"
echo "   View cron log: tail -f $LOG_FILE"
echo ""
echo "📅 Next scheduled run: Next Sunday at 9:00 AM"
echo ""
