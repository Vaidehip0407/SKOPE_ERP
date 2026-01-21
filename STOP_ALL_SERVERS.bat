@echo off
echo Stopping Store Management System...
echo.

echo Checking for processes on port 3000 (Frontend)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do (
    echo Killing Frontend process (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

echo Checking for processes on port 8000 (Backend)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Killing Backend process (PID: %%a)
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ✓ All servers stopped!
echo.
echo You can safely close this window.
pause

