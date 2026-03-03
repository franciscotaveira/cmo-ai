@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM TESTE RÁPIDO — Marketing Engine v5.3
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🧪 TESTE RÁPIDO — Marketing Engine v5.3
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo    Instale em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python: 
python --version
echo.

REM Verificar se .venv existe
if not exist ".venv" (
    echo ❌ Ambiente virtual não encontrado!
    echo    Execute: setup.bat
    pause
    exit /b 1
)

echo 📦 Ambiente virtual: .venv
echo.

REM Ativar ambiente
call .venv\Scripts\activate.bat

REM Testar imports básicos
echo 🧪 Testando imports básicos...
echo.

python -c "import pandas; print('✅ pandas')"
python -c "import numpy; print('✅ numpy')"
python -c "import fastapi; print('✅ fastapi')"
python -c "import supabase; print('✅ supabase')"
python -c "import openai; print('✅ openai')"
python -c "import groq; print('✅ groq')"
python -c "import anthropic; print('✅ anthropic')"
python -c "from dotenv import load_dotenv; print('✅ python-dotenv')"

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ TESTES BÁSICOS CONCLUÍDOS!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Configurar .env (se ainda não configurou):
echo    copy mkt\.env.example mkt\.env
echo.
echo 2. Rodar teste de IA completo:
echo    cd mkt\engine
echo    python test_ai_insights.py
echo.
echo 3. Rodar o sistema:
echo    cd mkt\engine
echo    python -m main
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
