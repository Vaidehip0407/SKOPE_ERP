@echo off
echo ========================================================================
echo          SKOPE ERP - Complete Project Startup
echo ========================================================================
echo.
echo This script will start both backend and frontend servers
echo.
echo ========================================================================
echo.

REM Store the project root directory
set "PROJECT_ROOT=%cd%"

REM Start backend in new window
echo Starting Backend Server...
start "SKOPE ERP - Backend" cmd /k "cd /d "%PROJECT_ROOT%\backend" && call QUICK_SETUP.bat"

REM Wait a bit for backend to initialize
timeout /t 5 /nobreak > nul

REM Start frontend in new window
echo Starting Frontend Server...
start "SKOPE ERP - Frontend" cmd /k "cd /d "%PROJECT_ROOT%\frontend" && call QUICK_START.bat"

echo.
echo ========================================================================
echo Both servers are starting in separate windows!
echo ========================================================================
echo.
echo Backend will be at:  http://localhost:8000
echo Frontend will be at: http://localhost:5173
echo API Docs will be at: http://localhost:8000/docs
echo.
echo Wait for both servers to fully start, then open:
echo http://localhost:5173
echo.
echo Login with:
echo   Username: admin
echo   Password: admin123
echo.
echo ========================================================================
echo.
pause

