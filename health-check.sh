#!/bin/bash

# Personal AI Employee - Health Check Script
# Monitors system health and reports status

echo "🏥 Personal AI Employee - Health Check"
echo "========================================"
echo ""

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "❌ PM2 not installed"
    exit 1
fi

# Check PM2 processes
echo "📊 PM2 Process Status:"
pm2 status

echo ""
echo "💾 Resource Usage:"
pm2 monit --no-interaction &
MONIT_PID=$!
sleep 3
kill $MONIT_PID 2>/dev/null

echo ""
echo "📁 Vault Status:"
if [ -d "AI_Employee_Vault" ]; then
    echo "✅ Vault directory exists"
    echo "   Inbox: $(ls -1 AI_Employee_Vault/Inbox/ 2>/dev/null | wc -l) files"
    echo "   Needs_Action: $(ls -1 AI_Employee_Vault/Needs_Action/ 2>/dev/null | wc -l) files"
    echo "   Needs_Approval: $(ls -1 AI_Employee_Vault/Needs_Approval/ 2>/dev/null | wc -l) files"
    echo "   Done: $(ls -1 AI_Employee_Vault/Done/ 2>/dev/null | wc -l) files"
else
    echo "❌ Vault directory not found"
fi

echo ""
echo "📋 Recent Logs (last 10 lines):"
if [ -f "logs/orchestrator-out.log" ]; then
    echo "--- Orchestrator ---"
    tail -n 5 logs/orchestrator-out.log
else
    echo "❌ No orchestrator logs found"
fi

echo ""
echo "🖥️  System Resources:"
echo "   Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "   Disk: $(df -h . | awk 'NR==2 {print $3 "/" $2 " (" $5 " used)"}')"

echo ""
echo "🔍 Xvfb Status:"
if pgrep -x "Xvfb" > /dev/null; then
    echo "✅ Xvfb is running"
else
    echo "⚠️  Xvfb is not running (needed for browser automation)"
fi

echo ""
echo "✅ Health check complete!"
echo ""
echo "Commands:"
echo "  View logs: pm2 logs"
echo "  Restart all: pm2 restart all"
echo "  Stop all: pm2 stop all"
