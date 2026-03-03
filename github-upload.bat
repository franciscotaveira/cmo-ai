@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM GITHUB UPLOAD SCRIPT — CMO 360° PLATFORM
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🚀 GITHUB UPLOAD — CMO 360° v6.1
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado!
    echo    Instale em: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo ✅ Git encontrado:
git --version
echo.

REM Configurar usuário (se for a primeira vez)
echo 📋 CONFIGURAÇÃO DO GIT:
echo.
git config user.name 2>nul
if %errorlevel% neq 0 (
    set /p GIT_NAME="Digite seu nome para Git: "
    git config --global user.name "%GIT_NAME%"
)

git config user.email 2>nul
if %errorlevel% neq 0 (
    set /p GIT_EMAIL="Digite seu e-mail para Git: "
    git config --global user.email "%GIT_EMAIL%"
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 1: ADICIONAR ARQUIVOS
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Adicionar arquivos
echo Adicionando arquivos...
git add .

echo ✅ Arquivos adicionados
echo.

REM Verificar status
echo 📊 STATUS:
git status --short
echo.

echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 2: COMMIT
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

set /p COMMIT_MSG="Digite a mensagem do commit (ou Enter para padrão): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=feat: CMO 360° v6.1 — Platform de Inteligência de Marketing
)

echo Fazendo commit...
git commit -m "%COMMIT_MSG%"

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Nenhum cambiamento para commitar
    echo    Ou já está tudo commitado
    echo.
    pause
    exit /b 0
)

echo ✅ Commit realizado
echo.

echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 3: CONFIGURAR REMOTE
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

set /p GITHUB_USER="Digite seu usuário do GitHub: "
set REPO_URL=https://github.com/%GITHUB_USER%/cmo-360-platform.git

echo.
echo Remote URL: %REPO_URL%
echo.

set /p CONFIRM_REMOTE="Confirmar remote? (S/N): "
if /i "%CONFIRM_REMOTE%"=="S" (
    git remote remove origin 2>nul
    git remote add origin %REPO_URL%
    echo ✅ Remote configurado
) else (
    echo ⚠️  Remote não configurado
    echo    Execute manualmente: git remote add origin %REPO_URL%
    echo.
    pause
    exit /b 0
)

echo.

echo ═══════════════════════════════════════════════════════════════════════════════
echo PASSO 4: PUSH PARA GITHUB
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📤 Enviando para GitHub...
echo.
echo ⚠️  Será solicitado:
echo    - Username: %GITHUB_USER%
echo    - Password: SEU TOKEN DO GITHUB (não é a senha!)
echo.
echo 💡  Criar token em: https://github.com/settings/tokens
echo    Marque: repo, workflow
echo.

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao fazer push!
    echo.
    echo Verifique:
    echo   1. Git token está correto
    echo   2. Repositório foi criado no GitHub
    echo   3. Permissões estão corretas
    echo.
    echo Para criar token:
    echo   https://github.com/settings/tokens
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ SUCESSO!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 🎉 Repositório enviado para GitHub!
echo.
echo 📊 URL do repositório:
echo    %REPO_URL%
echo.
echo 🌐 Acesse no navegador:
echo    https://github.com/%GITHUB_USER%/cmo-360-platform
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
