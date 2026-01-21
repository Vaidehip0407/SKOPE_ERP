@echo off
cd backend
echo Starting Backend Server on Port 8000...
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause

