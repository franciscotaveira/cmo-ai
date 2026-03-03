@echo off
set PYTHONIOENCODING=utf-8
cd /d %~dp0
echo Iniciando CMO 360 Command Center...
..\.venv_mkt\Scripts\python.exe mkt\engine\cmo_command_center.py
pause
