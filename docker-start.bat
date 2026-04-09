@echo off
REM Docker Quick Start Script for Personal AI Employee (Windows)
REM This script helps you get started with Docker deployment

echo ==================================================
echo   Personal AI Employee - Docker Quick Start
echo ==================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed
    echo Please install Docker Desktop from: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed
    echo Please install Docker Compose
    pause
    exit /b 1
)

echo [OK] Docker installed
echo [OK] Docker Compose installed
echo.

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found
    echo Creating .env from template...

    if exist .env.example (
        copy .env.example .env
        echo [OK] .env file created
        echo [WARNING] Please edit .env file with your credentials before continuing
        echo.
        pause
    ) else (
        echo [ERROR] .env.example not found
        pause
        exit /b 1
    )
) else (
    echo [OK] .env file exists
)

REM Create secrets directory
if not exist secrets (
    echo Creating secrets directory...
    mkdir secrets
    mkdir secrets\git_ssh
    echo [OK] Secrets directory created
    echo [WARNING] Please add your credentials to secrets\ directory
) else (
    echo [OK] Secrets directory exists
)

REM Create necessary vault directories
echo.
echo Creating vault directories...
if not exist AI_Employee_Vault mkdir AI_Employee_Vault
if not exist AI_Employee_Vault\Needs_Action mkdir AI_Employee_Vault\Needs_Action
if not exist AI_Employee_Vault\Needs_Approval mkdir AI_Employee_Vault\Needs_Approval
if not exist AI_Employee_Vault\Done mkdir AI_Employee_Vault\Done
if not exist AI_Employee_Vault\Approved mkdir AI_Employee_Vault\Approved
if not exist AI_Employee_Vault\Plans mkdir AI_Employee_Vault\Plans
if not exist AI_Employee_Vault\Accounting mkdir AI_Employee_Vault\Accounting
if not exist AI_Employee_Vault\Briefings mkdir AI_Employee_Vault\Briefings
if not exist AI_Employee_Vault\Logs mkdir AI_Employee_Vault\Logs
if not exist AI_Employee_Vault\Archive mkdir AI_Employee_Vault\Archive
echo [OK] Vault directories created

REM Check if Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo.
echo ==================================================
echo   Starting Docker Services
echo ==================================================
echo.

REM Pull images
echo Pulling Docker images...
docker-compose pull

REM Build custom images
echo.
echo Building custom images...
docker-compose build

REM Start services
echo.
echo Starting services...
docker-compose up -d

REM Wait for services to start
echo.
echo Waiting for services to initialize...
timeout /t 10 /nobreak >nul

REM Check service status
echo.
echo ==================================================
echo   Service Status
echo ==================================================
docker-compose ps

echo.
echo ==================================================
echo   Setup Complete!
echo ==================================================
echo.
echo [OK] All services started successfully
echo.
echo Access points:
echo   - Odoo Accounting: http://localhost:8069
echo   - Vault Location: .\AI_Employee_Vault\
echo.
echo Useful commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Restart: docker-compose restart
echo   - CEO Briefing: docker-compose exec ceo_briefing python /app/scripts/ceo_briefing.py weekly
echo.
echo For detailed documentation, see: DOCKER_SETUP.md
echo.
pause
