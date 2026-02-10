@echo off
chcp 936 >nul

echo Starting Auto Push...

powershell -command "Start-Service ssh-agent -ErrorAction SilentlyContinue"

ssh-add "D:\github_ssh\id_rsa"

git add .
git commit -m "Auto backup"
git push origin main

echo Done!
pause