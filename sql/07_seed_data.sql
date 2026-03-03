-- ═══════════════════════════════════════════════════════════════════════════════
-- 07_seed_data.sql — DADOS DE TESTE (SEED)
-- ═══════════════════════════════════════════════════════════════════════════════
-- Insere dados iniciais para teste e desenvolvimento
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TENANTS (Empresas/Unidades)
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO public.tenants (name, slug, type, settings, business_config) VALUES
    ('Diretoria Geral', 'diretoria', 'diretoria',
     '{"kpi_ouro": ["ltv", "cac", "roi", "retention", "gap"]}'::jsonb,
     '{"unidades": 60, "leads_total": 200000}'::jsonb),
    
    ('Salão Lux Beauty', 'salao-esposa', 'salao',
     '{"tom_voz": "acolhedor", "objetivo": "fidelizacao"}'::jsonb,
     '{"funcionarios": 5}'::jsonb),
    
    ('Franquia Chapecó Centro', 'franquia-chapeco-centro', 'franquia',
     '{"unidade_id": "001", "regiao": "centro"}'::jsonb,
     '{"funcionarios": 10}'::jsonb),
    
    ('Franquia Chapecó Oeste', 'franquia-chapeco-oeste', 'franquia',
     '{"unidade_id": "002", "regiao": "oeste"}'::jsonb,
     '{"funcionarios": 8}'::jsonb),
    
    ('E-commerce Exemplo', 'ecommerce-exemplo', 'ecommerce',
     '{"kpi_ouro": ["cac", "ltv", "roas", "conversion_rate"]}'::jsonb,
     '{"produtos": 500, "pedidos_mes": 1000}'::jsonb),
    
    ('SaaS Tech', 'saas-tech', 'saas',
     '{"kpi_ouro": ["mrr", "churn", "ltv", "cac"]}'::jsonb,
     '{"clientes": 200, "mrr": 50000}'::jsonb)

ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    type = EXCLUDED.type,
    settings = EXCLUDED.settings,
    business_config = EXCLUDED.business_config,
    updated_at = NOW();

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. MÉTRICAS DE EXEMPLO (Últimos 7 dias)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Métricas para Diretoria
INSERT INTO public.business_metrics (tenant_id, metric_key, metric_value, metric_unit, date_ref, period_type)
SELECT 
    t.id,
    m.metric_key,
    m.metric_value,
    m.metric_unit,
    CURRENT_DATE - d.day_offset,
    'daily'
FROM (SELECT id FROM public.tenants WHERE slug = 'diretoria') t
CROSS JOIN (
    SELECT 'cac' as metric_key, 45 + (random() * 10)::numeric as metric_value, 'BRL' as metric_unit
    UNION ALL SELECT 'ltv', 350 + (random() * 50)::numeric, 'BRL'
    UNION ALL SELECT 'roi', 3.5 + (random() * 1)::numeric, 'ratio'
    UNION ALL SELECT 'revenue', 50000 + (random() * 10000)::numeric, 'BRL'
    UNION ALL SELECT 'leads', 150 + (random() * 50)::numeric, 'count'
    UNION ALL SELECT 'conversion_rate', 2.5 + (random() * 0.5)::numeric, 'percentage'
) m
CROSS JOIN (SELECT generate_series(0, 6) as day_offset) d
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. INSIGHTS DE EXEMPLO
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO public.strategic_insights (tenant_id, context, ai_response, source_model, confidence_score, status)
SELECT 
    t.id,
    'CAC 20% acima do benchmark na última semana',
    'Recomenda-se otimizar campanhas do Meta Ads. Identificamos que o CPA subiu para R$ 65. Ações: 1) Pausar conjuntos com CPA > R$ 70, 2) Escalar Google Ads (ROAS 5.2x), 3) Implementar retargeting.',
    'llama-3.1-70b',
    0.87,
    'new'
FROM public.tenants t
WHERE t.slug = 'diretoria'
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. ALERTAS DE ANOMALIA DE EXEMPLO
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO public.anomaly_alerts (tenant_id, metric_key, metric_value, expected_value, z_score, severity, status)
SELECT 
    t.id,
    'cac',
    65.0,
    45.0,
    3.5,
    'critical',
    'new'
FROM public.tenants t
WHERE t.slug = 'diretoria'
ON CONFLICT DO NOTHING;

INSERT INTO public.anomaly_alerts (tenant_id, metric_key, metric_value, expected_value, z_score, severity, status)
SELECT 
    t.id,
    'conversion_rate',
    1.8,
    2.5,
    2.3,
    'high',
    'new'
FROM public.tenants t
WHERE t.slug = 'salao-esposa'
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. AUTOMAÇÕES NA FILA (EXEMPLO)
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO public.automation_queue (tenant_id, automation_type, trigger_source, priority, payload, status)
SELECT 
    t.id,
    'obsidian_report',
    'scheduled',
    5,
    '{"report_type": "weekly", "tenant": "diretoria"}'::jsonb,
    'pending'
FROM public.tenants t
WHERE t.slug = 'diretoria'
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- CONFIRMAÇÃO
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT '✅ Dados de teste inseridos!' AS status;

SELECT 
    '📊 RESUMO DOS DADOS' AS relatorio,
    (SELECT COUNT(*) FROM tenants) as tenants,
    (SELECT COUNT(*) FROM business_metrics) as metricas,
    (SELECT COUNT(*) FROM strategic_insights) as insights,
    (SELECT COUNT(*) FROM anomaly_alerts) as alertas,
    (SELECT COUNT(*) FROM automation_queue) as automacoes;

SELECT 
    '🏢 TENANTS CADASTRADOS' AS relatorio,
    name,
    slug,
    type,
    is_active
FROM tenants
ORDER BY created_at DESC;
