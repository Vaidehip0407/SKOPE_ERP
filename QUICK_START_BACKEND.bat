@echo off
echo ========================================
echo   SKOPE ERP - Quick Start
echo ========================================
echo.

REM Change to the correct backend directory
cd /d C:\Users\vrajr\Desktop\Store_management\backend

echo Current directory: %CD%
echo.

echo [1/2] Seeding demo data...
python seed_demo_data.py

echo.
echo [2/2] Starting Backend Server...
echo Server will run at http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
