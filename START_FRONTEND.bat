@echo off
echo ========================================================================
echo          SKOPE ERP - Frontend Server (Port 3000)
echo ========================================================================
echo.

cd frontend

echo Checking node_modules...
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

echo.
echo Starting Frontend Server on port 3000...
echo Application will be at: http://localhost:3000
echo.
echo ========================================================================
echo.

call node node_modules/vite/bin/vite.js --port 3000 --host 0.0.0.0

pause



