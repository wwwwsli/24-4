@echo off
echo ========================================
echo Starting Auto Push to GitHub...
echo ========================================

:: 1. Start SSH Agent and Add Key
for /f "tokens=1-2 delims==" %%a in ('ssh-agent -s') do set %%a=%%b
ssh-add D:/github_ssh/id_rsa

:: 2. Git Operations
git add .
git commit -m "auto update"
git push origin main

echo ========================================
echo All Done!
pause