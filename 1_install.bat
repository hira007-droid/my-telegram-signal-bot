@echo off
title Signal Bot - installing
cd /d "%~dp0"
set PY=python
where python >nul 2>nul
if errorlevel 1 set PY=py
echo Installing the two small libraries the bot needs. Please wait...
echo.
%PY% -m pip install --upgrade python-telegram-bot tzdata requests
echo.
echo ------------------------------------------------------------
echo Finished. If you see "Successfully installed" or
echo "Requirement already satisfied" above, it worked.
echo If you see a red ERROR, check your internet and run this again.
echo ------------------------------------------------------------
pause
