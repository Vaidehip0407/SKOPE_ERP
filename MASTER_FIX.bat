@echo off
echo ===================================================
echo SKOPE ERP - MASTER FIX TOOL
echo ===================================================
echo.
echo This script will completely reset the frontend and try to fix startup issues.
echo.
pause

cd frontend
if exist node_modules (
    echo [1/5] Removing old node_modules...
    rmdir /s /q node_modules
)
if exist package-lock.json del package-lock.json

echo [2/5] Cleaning cache...
call npm cache clean --force

echo [3/5] Installing dependencies...
echo (This may take a few minutes)
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo INSTALL FAILED.
    pause
    exit /b
)

echo [4/5] Building project (Validation)...
call node node_modules/vite/bin/vite.js build
if %ERRORLEVEL% NEQ 0 (
    echo BUILD FAILED. check logs above.
    echo Proceeding to try startup anyway...
)

echo [5/5] Starting Server directly (Port 3001)...
echo.
echo Please keep this window open!
echo Open your browser to: http://localhost:3001
echo.
node node_modules/vite/bin/vite.js --port 3001 --host 0.0.0.0
pause
