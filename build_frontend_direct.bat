@echo off
echo STARTING DIRECT BUILD %TIME% > build_log.txt
cd frontend
echo [ACTION] Running Vite Build... >> build_log.txt
node node_modules/vite/bin/vite.js build >> build_log.txt 2>&1
echo EXIT CODE: %ERRORLEVEL% >> build_log.txt
