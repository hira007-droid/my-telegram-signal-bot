@echo off
title Signal Bot - KEEP THIS WINDOW OPEN
cd /d "%~dp0"
set PY=python
where python >nul 2>nul
if errorlevel 1 set PY=py
echo Starting the bot. Keep this window open while you use the bot.
echo To stop it: click this window and press Ctrl+C, or just close it.
echo.
%PY% bot.py
echo.
echo ------------------------------------------------------------
echo The bot has stopped. If you see an error message above,
echo run 2_check.bat and follow its WHAT TO DO lines.
echo ------------------------------------------------------------
pause
