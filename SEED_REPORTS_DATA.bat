@echo off
title SKOPE ERP - Seed Reports Data
echo ========================================
echo   Seeding Reports Data
echo ========================================
echo.

cd /d %~dp0backend
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running seed script...
python seed_reports_data.py

echo.
echo ========================================
echo Done! Press any key to close...
pause >nul
