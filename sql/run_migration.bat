@echo off
REM ═══════════════════════════════════════════════════════════════════════════════
REM SQL MIGRATION EXECUTOR — CMO 360° v5.3
REM ═══════════════════════════════════════════════════════════════════════════════
REM Este script ajuda a executar todos os scripts SQL em ordem
REM ═══════════════════════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🗄️  CMO 360° — SQL Migration Executor
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo INSTRUÇÕES:
echo.
echo 1. Acesse: https://supabase.com/dashboard
echo 2. Selecione seu projeto
echo 3. Vá em: SQL Editor
echo.
echo 4. Execute os scripts NESTA ORDEM (um por vez):
echo.
echo    [1] 01_check_extensions.sql
echo    [2] 02_drop_existing.sql       ^<-- OPCIONAL ^^! Remove tabelas antigas
echo    [3] 03_create_tables.sql
echo    [4] 04_create_indexes.sql
echo    [5] 05_create_functions.sql
echo    [6] 06_enable_rls.sql
echo    [7] 07_seed_data.sql
echo    [8] 08_verify_install.sql
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📁 Scripts estão em:
echo    %CD%\sql\
echo.
echo ⏱️  Tempo estimado: 5-10 minutos
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

pause

echo.
echo 💡 DICA:
echo    - Copie TODO o conteúdo de cada arquivo .sql
echo    - Cole no SQL Editor do Supabase
echo    - Clique em RUN
echo    - Aguarde a confirmação antes de prosseguir
echo.
echo    - Se já tem tabelas, execute 02_drop_existing.sql primeiro
echo    - Se é instalação nova, pode pular o 02_drop_existing.sql
echo.
pause

echo.
echo 📂 ABRINDO PASTA SQL...
explorer "%CD%\sql"

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo ✅ Boa migração!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
