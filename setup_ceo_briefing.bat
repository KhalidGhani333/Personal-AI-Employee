@echo off
REM Setup Automated Weekly CEO Briefing for Windows
REM Configures Windows Task Scheduler to run every Sunday at 9 AM

echo Setting up Automated Weekly CEO Briefing for Windows
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
set CEO_BRIEFING_SCRIPT=%SCRIPT_DIR%scripts\ceo_briefing.py
set PYTHON_BIN=%SCRIPT_DIR%venv\Scripts\python.exe
set LOG_FILE=%SCRIPT_DIR%logs\ceo_briefing_cron.log

REM Check if ceo_briefing.py exists
if not exist "%CEO_BRIEFING_SCRIPT%" (
    echo Error: ceo_briefing.py not found
    exit /b 1
)

REM Check if Python virtual environment exists
if not exist "%PYTHON_BIN%" (
    echo Warning: Virtual environment not found
    echo Using system Python instead
    set PYTHON_BIN=python
)

echo.
echo Creating Windows Task Scheduler task...
echo.

REM Create task to run every Sunday at 9 AM
schtasks /create /tn "AI_Employee_CEO_Briefing" /tr "\"%PYTHON_BIN%\" \"%CEO_BRIEFING_SCRIPT%\" weekly" /sc weekly /d SUN /st 09:00 /f /rl HIGHEST

if errorlevel 1 (
    echo Failed to create scheduled task
    exit /b 1
)

echo.
echo Setup complete!
echo.
echo CEO Briefing Status:
echo   - Weekly briefing will run every Sunday at 9:00 AM
echo   - Reports saved to: AI_Employee_Vault\Briefings\
echo   - Cron log: %LOG_FILE%
echo.
echo Commands:
echo   View task: schtasks /query /tn "AI_Employee_CEO_Briefing" /v
echo   Run now: schtasks /run /tn "AI_Employee_CEO_Briefing"
echo   Delete task: schtasks /delete /tn "AI_Employee_CEO_Briefing" /f
echo   Test briefing: python scripts\ceo_briefing.py weekly
echo.
echo Next scheduled run: Next Sunday at 9:00 AM
echo.

pause
