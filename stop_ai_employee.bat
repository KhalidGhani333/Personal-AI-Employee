@echo off
REM ============================================
REM Personal AI Employee - Stop All Services
REM ============================================
REM This script stops all running AI Employee services
REM ============================================

echo.
echo ============================================
echo   Personal AI Employee - Stopping...
echo ============================================
echo.

echo Stopping all Python processes related to AI Employee...

REM Kill all Python processes running the scripts
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *gmail_watcher*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *whatsapp_watcher*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *linkedin_watcher*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *reply_generator*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *reply_sender*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *linkedin_auto_poster*" 2>nul
taskkill /F /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq *run_ai_employee*" 2>nul

REM Remove lock file if exists
if exist "logs\ai_employee.lock" (
    echo Removing lock file...
    del /F /Q "logs\ai_employee.lock"
)

echo.
echo ============================================
echo   All Services Stopped Successfully!
echo ============================================
echo.
pause
