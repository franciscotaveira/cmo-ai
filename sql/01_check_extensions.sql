-- ═══════════════════════════════════════════════════════════════════════════════
-- 01_check_extensions.sql — EXTENSÕES NECESSÁRIAS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Cria extensões necessárias para o CMO 360°
-- ═══════════════════════════════════════════════════════════════════════════════

-- Vetores para busca semântica (IA/RAG)
CREATE EXTENSION IF NOT EXISTS vector;

-- Geração de UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Funções adicionais de timestamp
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Verificar extensões instaladas
SELECT 
    '✅ EXTENSÕES INSTALADAS' AS status,
    extname AS extensao,
    extversion AS versao
FROM pg_extension
WHERE extname IN ('vector', 'uuid-ossp', 'pgcrypto')
ORDER BY extname;

-- Se alguma extensão falhar, ative manualmente no dashboard:
-- Supabase Dashboard → Database → Extensions → Enable
