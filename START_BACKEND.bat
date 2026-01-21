@echo off
echo ========================================================================
echo          SKOPE ERP - Backend Server (Port 8000)
echo ========================================================================
echo.

cd backend

echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Backend Server on port 8000...
echo API will be at: http://localhost:8000
echo API Docs will be at: http://localhost:8000/docs
echo.
echo ========================================================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause



