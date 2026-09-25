@echo off
title Signal Bot - checking
cd /d "%~dp0"
set PY=python
where python >nul 2>nul
if errorlevel 1 set PY=py
%PY% check_setup.py
pause
