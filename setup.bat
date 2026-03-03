@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM SETUP AUTOMÁTICO — MARKETING ENGINE v5.3
REM ═══════════════════════════════════════════════════════════════════════════════
REM Este script configura o ambiente Python automaticamente no Windows
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🚀 SETUP AUTOMÁTICO — MARKETING ENGINE v5.3
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Verificar se Python está instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale o Python primeiro:
    echo   1. Acesse: https://www.python.org/downloads/
    echo   2. Baixe Python 3.12 ou superior
    echo   3. Execute o instalador MARCANDO "Add Python to PATH"
    echo   4. Reinicie este script
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado!
echo.

REM Navegar até o diretório do projeto
echo [2/5] Navegando até o projeto...
cd /d "%~dp0"
echo 📁 Diretório: %CD%
echo.

REM Remover .venv antiga se existir
echo [3/5] Limpando ambiente antigo...
if exist ".venv" (
    echo 🗑️  Removendo .venv antiga...
    rmdir /s /q .venv
) else (
    echo ℹ️  Nenhuma .venv existente para remover
)
echo.

REM Criar nova .venv
echo [4/5] Criando ambiente virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERRO ao criar .venv!
    pause
    exit /b 1
)
echo ✅ .venv criada com sucesso!
echo.

REM Ativar e instalar dependências
echo [5/5] Instalando dependências...
echo ⏳ Isso pode levar alguns minutos...
echo.

call .venv\Scripts\activate.bat

REM Atualizar pip
python -m pip install --upgrade pip --quiet

REM Instalar requirements
if exist "mkt\engine\requirements.txt" (
    pip install -r mkt\engine\requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ⚠️  Alguns pacotes falharam, mas a instalação pode continuar...
    )
) else (
    echo ❌ requirements.txt não encontrado!
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ SETUP CONCLUÍDO!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Configurar o arquivo .env:
echo    copy mkt\.env.example mkt\.env
echo.
echo 2. Editar .env com suas credenciais:
echo    - SUPABASE_URL e SUPABASE_KEY
echo    - GROQ_API_KEY (https://console.groq.com/keys)
echo    - PATH_TO_DRIVE e PATH_TO_OBSIDIAN
echo.
echo 3. Rodar testes:
echo    cd mkt\engine
echo    python test_ai_insights.py
echo.
echo 4. Rodar o sistema:
echo    python -m main
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
