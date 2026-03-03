@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM CMO 360° — INICIAR PLATAFORMA WEB (Docker)
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🚀 CMO 360° — WEB PLATFORM
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Verificar Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado!
    echo    Instale em: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo ✅ Docker encontrado:
docker --version
echo.

REM Verificar .env
if not exist ".env" (
    echo ⚠️  Arquivo .env não encontrado!
    echo.
    echo Copie .env.example para .env e preencha com suas credenciais:
    echo   copy .env.example .env
    echo.
    pause
    exit /b 1
)

echo ✅ Arquivo .env encontrado

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo SUBINDO PLATAFORMA...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Subir containers
docker-compose up -d

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao subir containers!
    echo    Verifique logs acima.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ PLATAFORMA ONLINE!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📊 ACESSO:
echo.
echo    🌐 Frontend (Painel): http://localhost:5173
echo    🔌 Backend (API):     http://localhost:8000
echo    🏥 Health Check:      http://localhost:8000/health
echo.
echo 📋 COMANDOS ÚTEIS:
echo.
echo    Ver logs:         docker-compose logs -f
echo    Parar sistema:    docker-compose down
echo    Reiniciar:        docker-compose restart
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo Abrindo painel no navegador...
start http://localhost:5173

echo.
pause
