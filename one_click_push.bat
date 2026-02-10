@echo off
chcp 936 >nul
echo Starting Auto Push...

:: 直接执行 Git 三连，简单粗暴
git add .
git commit -m "Auto backup %date% %time%"
git push origin main

echo Done!
pause