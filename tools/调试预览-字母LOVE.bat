@echo off
chcp 65001 >nul
title 调试预览 - 字母LOVE (不锁鼠标)
echo 正在启动 LOVE 英文字母点阵调试预览（不锁定鼠标，展示 8 秒，可按 ESC 提前退出）...
python main.py -p LOVE --no-lock -d 8
pause
