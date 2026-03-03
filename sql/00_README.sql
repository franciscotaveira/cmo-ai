-- ═══════════════════════════════════════════════════════════════════════════════
-- 00_README.sql — ORDEM DE EXECUÇÃO (CMO 360° v5.3)
-- ═══════════════════════════════════════════════════════════════════════════════
-- 
-- INSTRUÇÕES:
-- Execute os scripts nesta ordem exata:
--
-- 1. 01_check_extensions.sql    — Verifica/cria extensões necessárias
-- 2. 02_drop_existing.sql       — Remove tabelas antigas (se existir)
-- 3. 03_create_tables.sql       — Cria as 8 tabelas principais
-- 4. 04_create_indexes.sql      — Cria índices para performance
-- 5. 05_create_functions.sql    — Cria funções utilitárias
-- 6. 06_enable_rls.sql          — Habilita Row Level Security
-- 7. 07_seed_data.sql           — Insere dados de teste
-- 8. 08_verify_install.sql      — Verifica se tudo foi criado
--
-- TEMPO ESTIMADO: 5-10 minutos
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '📚 CMO 360° — SQL Migration Scripts' AS info;
SELECT '=====================================' AS info;
SELECT '' AS info;
SELECT 'ORDEM DE EXECUÇÃO:' AS info;
SELECT '  1. 01_check_extensions.sql' AS passo;
SELECT '  2. 02_drop_existing.sql (opcional)' AS passo;
SELECT '  3. 03_create_tables.sql' AS passo;
SELECT '  4. 04_create_indexes.sql' AS passo;
SELECT '  5. 05_create_functions.sql' AS passo;
SELECT '  6. 06_enable_rls.sql' AS passo;
SELECT '  7. 07_seed_data.sql' AS passo;
SELECT '  8. 08_verify_install.sql' AS passo;
SELECT '' AS info;
SELECT '✅ Comece pelo script 01_check_extensions.sql' AS info;
