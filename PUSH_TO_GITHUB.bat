@echo off
echo ========================================
echo Pushing Store Management to GitHub
echo Repository: https://github.com/vraj1091/SKOPE_ERP
echo ========================================
echo.

REM Initialize Git repository if not already initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Add the remote repository
echo Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/vraj1091/SKOPE_ERP.git
echo.

REM Add all files
echo Adding all files to Git...
git add .
echo.

REM Commit the changes
echo Committing changes...
git commit -m "Initial commit: Store Management System with complete features"
echo.

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main --force
echo.

echo ========================================
echo Push complete!
echo Your code is now on: https://github.com/vraj1091/SKOPE_ERP
echo ========================================
pause
