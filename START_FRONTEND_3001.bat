@echo off
echo Starting Frontend (Fix Mode)...
echo [INFO] Running direct node process on Port 3001
cd frontend
call node node_modules/vite/bin/vite.js --port 3001 --host 0.0.0.0
pause
