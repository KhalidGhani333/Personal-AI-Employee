@echo off
REM Stop Odoo containers

echo Stopping Odoo containers...
docker stop odoo-app odoo-db

if %errorlevel% equ 0 (
    echo [SUCCESS] Odoo stopped successfully!
) else (
    echo [ERROR] Failed to stop Odoo.
)

echo.
pause
