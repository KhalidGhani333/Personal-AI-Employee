@echo off
REM ============================================
REM Personal AI Employee - Complete Startup
REM ============================================
REM This script starts all AI Employee services
REM ============================================

echo.
echo ============================================
echo   Personal AI Employee - Starting...
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10+
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env and configure your credentials
    pause
    exit /b 1
)

echo [1/6] Starting Gmail Watcher (every 5 minutes)...
start /B python scripts/gmail_watcher.py --interval 300

echo [2/6] Starting WhatsApp Watcher (every 2 minutes)...
start /B python scripts/whatsapp_watcher.py --interval 120

echo [3/6] Starting LinkedIn Watcher (every 5 minutes)...
start /B python scripts/linkedin_watcher.py --continuous --interval 300

echo [4/6] Starting Reply Generator (every 5 minutes)...
start /B python scripts/reply_generator.py --continuous --interval 300

echo [5/6] Starting Reply Sender (every 10 minutes)...
start /B python scripts/reply_sender.py --continuous --interval 600

echo [6/6] Starting Main Orchestrator (every 5 minutes)...
start /B python scripts/run_ai_employee.py --daemon --interval 300

echo.
echo ============================================
echo   All Services Started Successfully!
echo ============================================
echo.
echo Services Running:
echo   - Gmail Watcher (5 min interval)
echo   - WhatsApp Watcher (2 min interval)
echo   - LinkedIn Watcher (5 min interval)
echo   - Reply Generator (5 min interval)
echo   - Reply Sender (10 min interval)
echo   - Main Orchestrator (5 min interval)
echo.
echo To check status: python scripts/run_ai_employee.py --status
echo To stop all services: run stop_ai_employee.bat
echo.
echo Press any key to exit (services will continue running)...
pause >nul
