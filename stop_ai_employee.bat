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

REM Kill Python processes by command line (works for background processes)
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%gmail_watcher.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%whatsapp_watcher.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%linkedin_watcher.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%reply_generator.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%reply_sender.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%linkedin_auto_poster.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%run_ai_employee.py%%'" get processid /format:value ^| find "="') do taskkill /F /PID %%i 2>nul

echo Processes stopped.

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
