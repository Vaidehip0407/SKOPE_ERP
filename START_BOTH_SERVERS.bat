@echo off
echo ========================================================================
echo          SKOPE ERP - Starting Both Servers
echo ========================================================================
echo.
echo This will open TWO windows:
echo   1. Backend Server (Port 8000)
echo   2. Frontend Server (Port 3000)
echo.
echo ========================================================================
echo.

REM Get the current directory
set "PROJECT_ROOT=%cd%"

REM Start backend in new window
echo [1/2] Starting Backend Server...
start "SKOPE ERP - Backend (Port 8000)" cmd /k "cd /d "%PROJECT_ROOT%" && START_BACKEND.bat"

REM Wait 5 seconds
timeout /t 5 /nobreak > nul

REM Start frontend in new window
echo [2/2] Starting Frontend Server...
start "SKOPE ERP - Frontend (Port 3000)" cmd /k "cd /d "%PROJECT_ROOT%" && START_FRONTEND.bat"

echo.
echo ========================================================================
echo Both servers are starting in separate windows!
echo ========================================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Wait 30-60 seconds for both to fully start, then open:
echo http://localhost:3000
echo.
echo Login with:
echo   Username: admin
echo   Password: admin123
echo.
echo ========================================================================
echo.

pause



