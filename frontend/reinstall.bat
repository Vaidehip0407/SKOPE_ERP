@echo off
echo ===========================================
echo      SKOPE ERP - FRONTEND FIX TOOL
echo ===========================================
echo.
echo This script will clean and reinstall frontend dependencies.
echo Please wait...
echo.

echo [1/4] Moving old node_modules (backup)...
if exist node_modules (
    move node_modules node_modules_backup_%RANDOM%
    if exist node_modules (
        echo Failed to move. Trying forced delete...
        rmdir /s /q node_modules
    )
)

echo [2/4] Deleting package-lock.json...
if exist package-lock.json del package-lock.json

echo [3/4] Running npm install (this may take a few minutes)...
echo.
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: npm install failed!
    echo Please check your internet connection or npm configuration.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [4/4] Done! Dependencies reinstalled.
echo.
echo You may now close this window and run START_FRONTEND.bat (or START_BOTH_SERVERS.bat) again.
echo.
pause
