@echo off
title SKOPE ERP - Seed Marketing Data
echo ========================================
echo   Seeding Marketing Data
echo ========================================
echo.

cd /d %~dp0backend
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running marketing seed script...
python seed_marketing_data.py

echo.
echo ========================================
echo Done! Press any key to close...
pause >nul
