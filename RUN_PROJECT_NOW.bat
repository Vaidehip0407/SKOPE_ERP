@echo off
echo ===================================================
echo   Staring SKOPE ERP - Store Management System
echo ===================================================
echo.
echo [1] Preventing Conflicts...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
echo.

echo [2] Starting Backend (Port 8000)...
start "SKOPE Backend" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting 5 seconds for backend...
timeout /t 5 >nul

echo.
echo [3] Starting Frontend (Port 3000)...
start "SKOPE Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo   Servers launched in new windows!
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo ===================================================
pause
