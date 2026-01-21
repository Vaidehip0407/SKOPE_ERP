@echo off
echo ========================================== > debug_log.txt
echo DEBUG STARTED %TIME% >> debug_log.txt
echo ========================================== >> debug_log.txt

echo [CHECK] Node Version: >> debug_log.txt
node -v >> debug_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 echo Node not found! >> debug_log.txt

echo [CHECK] NPM Version: >> debug_log.txt
npm -v >> debug_log.txt 2>&1

echo [ACTION] Installing dependencies... >> debug_log.txt
call npm install >> debug_log.txt 2>&1
if %ERRORLEVEL% NEQ 0 echo NPM Install Failed! >> debug_log.txt

echo [ACTION] Starting dev server... >> debug_log.txt
echo Note: This might block if successful. >> debug_log.txt
call npm run dev >> debug_log.txt 2>&1
