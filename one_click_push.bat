@echo off
chcp 936 >nul
echo ========================================
echo Starting Auto Push to GitHub...
echo ========================================

:: 1. 强制用 Windows 方式启动管家
powershell -command "Start-Service ssh-agent -ErrorAction SilentlyContinue"

:: 2. 核心修正：注意这里用了反斜杠 \ 并且加了双引号，防止权限拦截
ssh-add "D:\github_ssh\id_rsa"

:: 3. 提交并推送
git add .
git commit -m "update %date% %time%"
git push origin main

echo ========================================
echo All Done!
pause