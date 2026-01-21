@echo off
echo Starting Retail Management System - Backend Server
echo ===================================================
echo.

cd /d %~dp0
call venv\Scripts\activate.bat

echo Virtual environment activated
echo Starting FastAPI server on http://localhost:8000
echo API Documentation will be available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

pause

