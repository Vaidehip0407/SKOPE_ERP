@echo off
echo Starting Frontend (Direct Mode)...
cd frontend
node node_modules/vite/bin/vite.js --port 3001 --host 0.0.0.0
pause
