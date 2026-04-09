@echo off
REM Odoo Docker Setup Script
REM This script sets up Odoo Community Edition with PostgreSQL

echo ============================================================
echo Odoo Docker Setup - Personal AI Employee
echo ============================================================
echo.

REM Check if Docker is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/5] Checking for existing containers...
docker ps -a | findstr "odoo-db odoo-app" >nul 2>&1
if %errorlevel% equ 0 (
    echo Found existing Odoo containers. Removing...
    docker stop odoo-app odoo-db 2>nul
    docker rm odoo-app odoo-db 2>nul
)

echo.
echo [2/5] Pulling PostgreSQL image...
docker pull postgres:15

echo.
echo [3/5] Starting PostgreSQL database...
docker run -d ^
    --name odoo-db ^
    -e POSTGRES_USER=odoo ^
    -e POSTGRES_PASSWORD=odoo ^
    -e POSTGRES_DB=postgres ^
    -v odoo-db-data:/var/lib/postgresql/data ^
    postgres:15

echo Waiting for database to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

echo.
echo [4/5] Pulling Odoo 17 image...
docker pull odoo:17.0

echo.
echo [5/5] Starting Odoo application...
docker run -d ^
    --name odoo-app ^
    --link odoo-db:db ^
    -p 8069:8069 ^
    -v odoo-data:/var/lib/odoo ^
    -e HOST=db ^
    -e USER=odoo ^
    -e PASSWORD=odoo ^
    odoo:17.0

echo.
echo ============================================================
echo Odoo Setup Complete!
echo ============================================================
echo.
echo Odoo is starting up (takes 30-60 seconds)...
echo.
echo Access Odoo at: http://localhost:8069
echo.
echo First-time setup:
echo   1. Open http://localhost:8069 in browser
echo   2. Create database with name: odoo_db
echo   3. Master password: admin
echo   4. Email: admin@example.com
echo   5. Password: admin123
echo.
echo After setup, update your .env file:
echo   ODOO_URL=http://localhost:8069
echo   ODOO_DB=odoo_db
echo   ODOO_USERNAME=admin
echo   ODOO_PASSWORD=admin123
echo.
echo ============================================================
echo.
echo Checking container status...
docker ps | findstr "odoo"
echo.
pause
