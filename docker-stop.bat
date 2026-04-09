@echo off
REM Docker Stop Script for Personal AI Employee (Windows)

echo ==================================================
echo   Personal AI Employee - Docker Stop
echo ==================================================
echo.

REM Check if services are running
docker-compose ps | findstr "Up" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] No services are currently running
    pause
    exit /b 0
)

echo Current running services:
docker-compose ps
echo.

REM Ask for confirmation
set /p confirm="Do you want to stop all services? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled
    pause
    exit /b 0
)

REM Ask if user wants to remove volumes
echo.
set /p remove_volumes="Do you want to remove volumes (database data will be deleted)? (y/n): "

if /i "%remove_volumes%"=="y" (
    echo.
    echo [WARNING] This will delete all database data!
    set /p confirm_delete="Are you sure? Type 'yes' to confirm: "

    if "%confirm_delete%"=="yes" (
        echo.
        echo Stopping services and removing volumes...
        docker-compose down -v
        echo [OK] Services stopped and volumes removed
    ) else (
        echo Cancelled
        pause
        exit /b 0
    )
) else (
    echo.
    echo Stopping services (keeping volumes)...
    docker-compose down
    echo [OK] Services stopped (data preserved)
)

echo.
echo ==================================================
echo   Services Stopped
echo ==================================================
echo.
echo To start again, run: docker-start.bat
echo Or: docker-compose up -d
echo.
pause
