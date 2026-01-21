@echo off
title SKOPE ERP - Launcher
color 0A
echo ========================================================================
echo                    SKOPE ERP - Store Management System
echo                           Project Launcher
echo ========================================================================
echo.

REM Kill any existing processes
echo [Step 1/5] Cleaning up existing processes...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
echo    ✓ Cleanup complete
echo.

REM Check Backend
echo [Step 2/5] Checking Backend...
cd backend
if not exist "venv" (
    echo    ! Virtual environment not found. Creating...
    python -m venv venv
)
echo    ✓ Backend ready
cd ..
echo.

REM Check Frontend
echo [Step 3/5] Checking Frontend...
cd frontend
if not exist "node_modules" (
    echo    ! Node modules not found. Installing...
    call npm install
)
echo    ✓ Frontend ready
cd ..
echo.

REM Start Backend
echo [Step 4/5] Starting Backend Server (Port 8000)...
start "SKOPE Backend - Port 8000" cmd /k "title SKOPE Backend && cd /d %~dp0backend && call venv\Scripts\activate && echo Starting FastAPI server... && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 || (echo ERROR: Backend failed to start! && pause)"
timeout /t 3 >nul
echo    ✓ Backend window opened
echo.

REM Start Frontend
echo [Step 5/5] Starting Frontend Server (Port 3000)...
start "SKOPE Frontend - Port 3000" cmd /k "title SKOPE Frontend && cd /d %~dp0frontend && echo Starting Vite dev server... && npm run dev || (echo ERROR: Frontend failed to start! && pause)"
timeout /t 2 >nul
echo    ✓ Frontend window opened
echo.

echo ========================================================================
echo                    SERVERS LAUNCHED SUCCESSFULLY!
echo ========================================================================
echo.
echo Two new windows have been opened:
echo   1. Backend Server  - http://localhost:8000
echo   2. Frontend Server - http://localhost:3000
echo.
echo Wait 10-15 seconds for servers to fully initialize, then open:
echo   http://localhost:3000
echo.
echo Login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo ========================================================================
echo.
echo Press any key to close this launcher window...
pause >nul
