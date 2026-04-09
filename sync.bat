@echo off
REM Git Vault Sync - Windows Wrapper
REM Usage: sync.bat [pull|push|status|resolve|init]

REM Check if Git Bash is available
where bash >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git Bash not found. Please install Git for Windows.
    echo Download from: https://git-scm.com/download/win
    exit /b 1
)

REM Run sync.sh with Git Bash
bash sync.sh %*
