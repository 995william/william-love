@echo off
chcp 65001 >nul
title 调试预览 - 心形图案 (不锁鼠标)
echo 正在启动心形图案调试预览（不锁定鼠标，展示 8 秒，可按 ESC 提前退出）...
python main.py -p HEART --no-lock -d 8
pause
