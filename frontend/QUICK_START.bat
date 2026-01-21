@echo off
echo ========================================================================
echo          SKOPE ERP - Frontend Setup Script
echo ========================================================================
echo.
echo This script will:
echo   1. Install all required Node.js packages
echo   2. Start the frontend development server
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js packages...
    echo This may take a few minutes...
    echo.
    call npm install
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: npm install failed!
        echo Please make sure Node.js is installed.
        pause
        exit /b 1
    )
    
    echo.
    echo Packages installed successfully!
)

echo.
echo ========================================================================
echo Starting Frontend Development Server...
echo ========================================================================
echo.
echo The application will be available at: http://localhost:5173
echo.
echo ========================================================================
echo PRESS CTRL+C TO STOP THE SERVER
echo ========================================================================
echo.

call npm run dev

