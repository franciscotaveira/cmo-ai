@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM TESTE COMPLETO — CMO 360° v5.3
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🧪 TESTE COMPLETO — CMO 360° v5.3
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    pause
    exit /b 1
)

echo ✅ Python: 
python --version
echo.

REM Ativar ambiente virtual
if exist ".venv_mkt\Scripts\activate.bat" (
    call .venv_mkt\Scripts\activate.bat
    echo ✅ Ambiente virtual ativado: .venv_mkt
) else if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo ✅ Ambiente virtual ativado: .venv
) else (
    echo ⚠️  Ambiente virtual não encontrado, tentando com Python global...
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo TESTE 1: Conexão com Supabase
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

python mkt\engine\test_supabase_connection.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Teste de conexão falhou!
    echo.
    echo Verifique:
    echo   1. Scripts SQL foram executados?
    echo   2. .env configurado com SUPABASE_URL e SUPABASE_KEY?
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo TESTE 2: Inicialização dos Módulos
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

python -c "from src.database import DatabaseHandler; db = DatabaseHandler(); print('✅ DatabaseHandler OK')"
python -c "from src.obsidian import ObsidianBridge; print('✅ ObsidianBridge OK')"
python -c "from src.growth_marketing import GrowthMarketingEngine; g = GrowthMarketingEngine(); print('✅ GrowthMarketingEngine OK')"
python -c "from src.brand_communication import BrandCommunicationEngine; b = BrandCommunicationEngine(); print('✅ BrandCommunicationEngine OK')"
python -c "from src.executive_dashboard import ExecutiveDashboard; e = ExecutiveDashboard(); print('✅ ExecutiveDashboard OK')"

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ TODOS OS TESTES PASSARAM!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Configurar PATH_TO_DRIVE e PATH_TO_OBSIDIAN no .env
echo 2. Colocar arquivos CSV/Excel na pasta do Drive
echo 3. Rodar o sistema: python -m mkt.engine.main
echo 4. Verificar dashboards no Obsidian
echo.
pause
