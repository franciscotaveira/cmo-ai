@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM CMO 360° — DOCKER DEPLOY AUTOMÁTICO
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🐳 CMO 360° v6.1 — DOCKER DEPLOY
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
echo PASSO 1: PARAR SERVIÇOS EXISTENTES
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

docker-compose down

echo ✅ Serviços parados
echo.

echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 2: CONSTRUIR IMAGENS
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

echo Isso pode levar alguns minutos na primeira vez...
echo.

docker-compose build

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao construir imagens!
    echo    Verifique logs acima.
    pause
    exit /b 1
)

echo ✅ Imagens construídas
echo.

echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 3: INICIAR SERVIÇOS
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

docker-compose up -d

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao iniciar serviços!
    pause
    exit /b 1
)

echo ✅ Serviços iniciados
echo.

REM Aguardar serviços inicializarem
echo Aguardando serviços inicializarem (30 segundos)...
timeout /t 30 /nobreak >nul

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 4: VERIFICAR SAÚDE DOS SERVIÇOS
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

docker-compose ps

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo TESTANDO HEALTH CHECKS
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Testar backend
echo Testando backend...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend: Online
) else (
    echo ⚠️  Backend: Não respondeu (pode estar inicializando)
)

REM Testar frontend
echo Testando frontend...
curl -s http://localhost:5173 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend: Online
) else (
    echo ⚠️  Frontend: Não respondeu (pode estar inicializando)
)

REM Testar Redis
echo Testando Redis...
docker-compose exec -T redis redis-cli ping >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Redis: Online
) else (
    echo ⚠️  Redis: Não respondeu
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ DEPLOY CONCLUÍDO!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📊 SERVIÇOS RODANDO:
echo.
echo    🌐 Frontend:  http://localhost:5173
echo    🔌 Backend:   http://localhost:8000
echo    🏥 Health:    http://localhost:8000/health
echo    💾 Redis:     localhost:6379
echo.
echo 📋 COMANDOS ÚTEIS:
echo.
echo    Ver logs:         docker-compose logs -f
echo    Ver status:       docker-compose ps
echo    Parar:            docker-compose down
echo    Reiniciar:        docker-compose restart
echo    Rebuild:          docker-compose up -d --build
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

pause
