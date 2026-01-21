@echo off
echo STARTING DIAGNOSIS > frontend_error.log
echo [CHECK] Node: >> frontend_error.log
node -v >> frontend_error.log 2>&1
echo [CHECK] NPM: >> frontend_error.log
npm -v >> frontend_error.log 2>&1
echo [ACTION] Run Dev: >> frontend_error.log
call npm run dev >> frontend_error.log 2>&1
