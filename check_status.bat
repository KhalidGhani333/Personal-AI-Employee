@echo off
REM ============================================
REM Personal AI Employee - Status Check
REM ============================================

echo.
echo ============================================
echo   AI Employee Status Check
echo ============================================
echo.

set FOUND=0

echo Checking for running processes...
echo.

for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%gmail_watcher.py%%'" get processid /format:value 2^>nul ^| find "="') do (
    echo [RUNNING] Gmail Watcher - PID: %%i
    set FOUND=1
)

for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%whatsapp_watcher.py%%'" get processid /format:value 2^>nul ^| find "="') do (
    echo [RUNNING] WhatsApp Watcher - PID: %%i
    set FOUND=1
)

for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%linkedin_watcher.py%%'" get processid /format:value 2^>nul ^| find "="') do (
    echo [RUNNING] LinkedIn Watcher - PID: %%i
    set FOUND=1
)

for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%reply_generator.py%%'" get processid /format:value 2^>nul ^| find "="') do (
    echo [RUNNING] Reply Generator - PID: %%i
    set FOUND=1
)

for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%reply_sender.py%%'" get processid /format:value 2^>nul ^| find "="') do (
    echo [RUNNING] Reply Sender - PID: %%i
    set FOUND=1
)

for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%run_ai_employee.py%%'" get processid /format:value 2^>nul ^| find "="') do (
    echo [RUNNING] Main Orchestrator - PID: %%i
    set FOUND=1
)

echo.
if %FOUND%==0 (
    echo [STATUS] No AI Employee processes running
) else (
    echo [STATUS] AI Employee is running
)

echo.
echo ============================================
pause
