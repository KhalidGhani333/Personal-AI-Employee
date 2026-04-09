@echo off
REM Start Odoo containers if they exist

echo Starting Odoo containers...
docker start odoo-db odoo-app

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Odoo started successfully!
    echo Access at: http://localhost:8069
    echo.
    docker ps | findstr "odoo"
) else (
    echo.
    echo [ERROR] Failed to start Odoo.
    echo Run setup_odoo_docker.bat first to install Odoo.
)

echo.
pause
