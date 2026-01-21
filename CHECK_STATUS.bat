@echo off
echo.
echo ==========================================
echo   CHECKING PROJECT STATUS
echo ==========================================
echo.

echo [1/4] Checking Backend Server (Port 8000)...
curl -s http://localhost:8000/health > nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Backend is RUNNING on port 8000
) else (
    echo [ERROR] Backend is NOT running
)
echo.

echo [2/4] Checking Frontend Server (Port 3000)...
curl -s http://localhost:3000 > nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Frontend is RUNNING on port 3000
) else (
    echo [ERROR] Frontend is NOT running
)
echo.

echo [3/4] Checking Database...
if exist "backend\rms.db" (
    echo [OK] Database file exists
    for %%A in ("backend\rms.db") do echo     Size: %%~zA bytes
) else (
    echo [ERROR] Database file NOT found
)
echo.

echo [4/4] Checking Python Processes...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe" > nul
if %errorlevel% == 0 (
    echo [OK] Python processes running:
    tasklist /FI "IMAGENAME eq python.exe" /NH
) else (
    echo [ERROR] No Python processes found
)
echo.

echo [4/4] Checking Node Processes...
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe" > nul
if %errorlevel% == 0 (
    echo [OK] Node processes running:
    tasklist /FI "IMAGENAME eq node.exe" /NH
) else (
    echo [ERROR] No Node processes found
)
echo.

echo ==========================================
echo   STATUS CHECK COMPLETE
echo ==========================================
echo.
echo NEXT STEPS:
echo - If both servers are running, open: http://localhost:3000
echo - If servers are NOT running, use: START_BOTH_SERVERS.bat
echo - Use Incognito mode or clear browser cache!
echo.
pause

