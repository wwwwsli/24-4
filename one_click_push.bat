@echo off
chcp 936 >nul

git add .
git commit -m "update_ai_feature"
git push origin main

echo.
echo === SUCCESS ===
pause