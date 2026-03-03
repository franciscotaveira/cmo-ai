@echo off
setlocal
color 0B
title CMO 360 - PORTAL DE COMANDO

:menu
cls
echo.
echo  ==========================================================
echo   🎯 CMO 360  -  MARKETING DATA COMMAND CENTER
echo  ==========================================================
echo.
echo   [1] ABRIR COMMAND CENTER (CLI) - Rapidez Operacional
echo   [2] ABRir DASHBOARD WEB (Next.js) - Visual e Metricas
echo   [3] ATIVAR ECOSSISTEMA DOCKER - Producao Local
echo   [4] VER DOCUMENTACAO (Obsidian/Exocortex)
echo   [5] RECARREGAR MOTOR (Watcher)
echo   [6] SAIR
echo.
echo  ==========================================================
echo.

set /p choice="Selecione uma opcao (1-6): "

if "%choice%"=="1" goto cli
if "%choice%"=="2" goto web
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto obsidian
if "%choice%"=="5" goto motor
if "%choice%"=="6" exit
goto menu

:cli
echo.
echo 🚀 Abrindo Command Center...
start "" "cmo_command_center.bat"
goto menu

:web
echo.
echo 🌐 Iniciando Servidor Web (Modo Dev)...
echo.
cd /d "web"
start cmd /k "npm run dev"
echo Servidor iniciado em: http://localhost:3000/dashboard
timeout /t 3 >nul
start "" "http://localhost:3000/dashboard"
cd /d ".."
goto menu

:docker
echo.
echo 🐳 Iniciando Ecossistema via Docker Compose...
echo.
start cmd /k "docker compose up -d --build"
echo Containers iniciando em background...
echo Verifique o Dashboard em: http://localhost:3000/dashboard
timeout /t 5 >nul
start "" "http://localhost:3000/dashboard"
goto menu

:obsidian
echo.
echo 🧠 Abrindo Exocortex no Obsidian...
set "OBSIDIAN_PATH=%CD%\🧠 EXOCÓRTEX"
explorer "%OBSIDIAN_PATH%"
goto menu

:motor
echo.
echo 🛰️  Reiniciando Motor de IA e Integracoes...
start cmd /k "setup.bat && python -m mkt.engine.main"
goto menu
