@echo off
REM Setup System Health Monitoring for Windows
REM Configures Windows Task Scheduler to run watchdog every 5 minutes

echo Setting up System Health Monitoring for Windows
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
set WATCHDOG_SCRIPT=%SCRIPT_DIR%watchdog.py
set PYTHON_BIN=%SCRIPT_DIR%venv\Scripts\python.exe
set LOG_FILE=%SCRIPT_DIR%logs\watchdog.log

REM Check if watchdog.py exists
if not exist "%WATCHDOG_SCRIPT%" (
    echo Error: watchdog.py not found
    exit /b 1
)

REM Check if Python virtual environment exists
if not exist "%PYTHON_BIN%" (
    echo Warning: Virtual environment not found
    echo Using system Python instead
    set PYTHON_BIN=python
)

REM Install required packages
echo Installing required packages...
%PYTHON_BIN% -m pip install psutil --quiet
if errorlevel 1 (
    echo Failed to install psutil
    exit /b 1
)

echo.
echo Creating Windows Task Scheduler task...
echo.

REM Create task
schtasks /create /tn "AI_Employee_Watchdog" /tr "\"%PYTHON_BIN%\" \"%WATCHDOG_SCRIPT%\"" /sc minute /mo 5 /f /rl HIGHEST

if errorlevel 1 (
    echo Failed to create scheduled task
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo Monitoring Status:
echo   - Watchdog will run every 5 minutes
echo   - Services will auto-restart if stopped
echo   - Health log: AI_Employee_Vault\Logs\system_health.md
echo.
echo Commands:
echo   View tasks: schtasks /query /tn "AI_Employee_Watchdog"
echo   Run now: schtasks /run /tn "AI_Employee_Watchdog"
echo   Delete task: schtasks /delete /tn "AI_Employee_Watchdog" /f
echo   Test watchdog: python watchdog.py
echo.

pause
