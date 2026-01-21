@echo off
echo ========================================================================
echo          SKOPE ERP - Complete Setup Script
echo ========================================================================
echo.
echo This script will:
echo   1. Install all required Python packages
echo   2. Create and populate the database with realistic data
echo   3. Start the backend server
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt --quiet

REM Setup database
echo.
echo ========================================================================
echo Setting up database with complete data...
echo ========================================================================
python setup_complete_database.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Database setup failed!
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo Database setup completed successfully!
echo ========================================================================
echo.
echo Starting backend server...
echo The API will be available at: http://localhost:8000
echo API Documentation will be at: http://localhost:8000/docs
echo.
echo ========================================================================
echo PRESS CTRL+C TO STOP THE SERVER
echo ========================================================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

