# 🚀 PROMPT PRÓXIMOS PASSOS — Marketing Director OS v4.0

> **Para**: Antigravity (Sua IA de Desenvolvimento)
> **Contexto**: Sistema já criado e auditado (Certificação OURO 94%)
> **Objetivo**: Implementar melhorias da auditoria e preparar para produção

---

## 📋 CONTEXTO

O **Marketing Director OS v4.0** foi completamente implementado e auditado com **certificação OURO (94%)**.

**Status Atual**:
- ✅ 26 arquivos criados
- ✅ Docker rodando
- ✅ Supabase configurado
- ✅ Documentação completa

**O Que Falta** (identificado na auditoria):
- ⚠️ Security scan de dependências
- ⚠️ Testes com dados reais
- ⚠️ CI/CD pipeline
- ⚠️ Monitoramento
- ⚠️ Backup automático

---

## 🎯 SUA MISSÃO

Implementar **FASE 27-35** para levar o sistema a **nível de produção**.

Siga a ordem EXATA abaixo.

---

## 📁 ORDEM DE CRIAÇÃO

### FASE 27: Security Scan (15 min)

Crie: `mkt/scripts/security_scan.sh` (ou `.ps1` para Windows)

**Funcionalidades**:
```bash
# 1. Scan de dependências Python
pip install pip-audit
pip-audit -r engine/requirements.txt

# 2. Scan de Docker
docker scan marketing_engine

# 3. Verificar .env exposto
git ls-files | grep -i env

# 4. Relatório de vulnerabilidades
# Salvar em: logs/security_report_YYYYMMDD.md
```

**Saída esperada**: Relatório Markdown com:
- Vulnerabilidades encontradas (se houver)
- Severidade (Crítica, Alta, Média, Baixa)
- Ações corretivas
- Data do próximo scan

---

### FASE 28: Testes E2E com Dados Reais (20 min)

Crie: `mkt/tests/e2e_test.py`

**Cenários de teste**:

```python
def test_csv_reals_do_salao():
    """Testa com CSV real de vendas do salão"""
    # 1. Criar CSV com 100+ linhas de vendas reais
    # 2. Colocar em drive_data/salao-esposa/
    # 3. Aguardar processamento
    # 4. Verificar no Supabase: business_metrics
    # 5. Verificar dashboard no Obsidian
    # 6. Validar: vendas_total == soma_real
    
def test_pdf_estrategia():
    """Testa processamento de PDF de estratégia"""
    # 1. Criar PDF com estratégia de marketing
    # 2. Colocar em drive_data/diretoria/
    # 3. Aguardar processamento
    # 4. Verificar: knowledge_base tem chunks
    # 5. Fazer pergunta à IA
    # 6. Validar: resposta usa contexto do PDF
    
def test_isolamento_tenants():
    """Testa RLS: franquia não vê dados do salão"""
    # 1. Inserir métricas para salao-esposa
    # 2. Tentar buscar com tenant_id da franquia
    # 3. Validar: retorno vazio
    # 4. Log de tentativa de acesso (audit_logs)
```

**Requisitos**:
- Usar pytest
- Cobertura mínima: 80%
- Relatório HTML em `logs/coverage/`

---

### FASE 29: CI/CD Pipeline (30 min)

Crie: `.github/workflows/ci.yml`

**Jobs obrigatórios**:

```yaml
name: Marketing OS CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r mkt/engine/requirements.txt
          pip install pytest pytest-cov mypy black
      
      - name: Lint (black)
        run: black --check mkt/engine/
      
      - name: Type check (mypy)
        run: mypy mkt/engine/
      
      - name: Security scan (pip-audit)
        run: pip-audit -r mkt/engine/requirements.txt
      
      - name: Test with pytest
        run: |
          pytest mkt/tests/ --cov=mkt/engine --cov-report=html
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  docker:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Build Docker
        run: docker-compose build
      
      - name: Test Docker
        run: docker-compose up -d && sleep 30 && docker-compose ps
```

**Gatilhos**:
- Push em `main` ou `develop`
- Pull requests
- Schedule: Security scan semanal

---

### FASE 30: Monitoramento (25 min)

Crie: `mkt/monitoring/health_check.py`

**Métricas para coletar**:

```python
metrics = {
    # Engine
    'engine_status': 'up/down',
    'engine_uptime': seconds,
    'files_processed_today': count,
    'avg_processing_time': seconds,
    
    # Supabase
    'supabase_status': 'up/down',
    'db_connections': count,
    'queries_today': count,
    
    # IA
    'ia_provider': 'openai/gemini',
    'ia_status': 'up/down',
    'tokens_used_today': count,
    'insights_generated': count,
    
    # Negócio
    'tenants_active': count,
    'metrics_count': count,
    'errors_today': count
}
```

**Dashboard** (crie `mkt/monitoring/dashboard.md`):

```markdown
# 📊 Health Dashboard

**Atualizado**: 2024-01-15 10:30:00

## Status dos Serviços
| Serviço | Status | Uptime |
| :------ | :----- | :----- |
| Engine | ✅ Up | 99.9% |
| Supabase | ✅ Up | 100% |
| IA | ✅ Up | 98.5% |

## Métricas de Hoje
- Arquivos processados: 47
- Insights gerados: 12
- Erros: 0

## Alertas Ativos
- Nenhum alerta
```

**Atualização automática** a cada 5 minutos.

---

### FASE 31: Backup Automático (20 min)

Crie: `mkt/scripts/backup.py`

**Funcionalidades**:

```python
def backup_supabase():
    """Backup diário do Supabase"""
    # 1. Exportar todas tabelas (tenants, metrics, knowledge, insights)
    # 2. Salvar como JSON timestamped
    # 3. Upload para S3 ou Google Drive
    # 4. Manter últimos 30 backups
    # 5. Enviar confirmação por email/WhatsApp
    
def backup_obsidian():
    """Backup do vault do Obsidian"""
    # 1. Compactar pasta obsidian_data/
    # 2. Salvar com timestamp
    # 3. Sync para nuvem
    # 4. Manter últimos 7 backups
    
def restore_backup(backup_file):
    """Restaurar backup específico"""
    # 1. Validar arquivo
    # 2. Importar para Supabase
    # 3. Restaurar Obsidian
    # 4. Validar integridade
```

**Agendamento**:
- Backup Supabase: Diário às 03:00
- Backup Obsidian: Diário às 03:30
- Reter: 30 dias (Supabase), 7 dias (Obsidian)

---

### FASE 32: Scripts de Utilidade (15 min)

Crie em `mkt/scripts/`:

**1. `reset_system.sh`** (ou `.ps1`):
```bash
# Para tudo, limpa volumes, reinicia
docker-compose down -v
docker-compose up -d --build
```

**2. `logs_viewer.sh`**:
```bash
# Tail de todos os logs em tempo real
docker-compose logs -f --tail=100
```

**3. `db_migrate.sh`**:
```bash
# Aplica migrações de schema
psql $SUPABASE_URL < migrations/v4.1.sql
```

**4. `seed_data.py`**:
```python
# Popula banco com dados de exemplo
# Útil para testes e demonstração
```

---

### FASE 33: Documentação de Produção (20 min)

Crie em `mkt/docs/`:

**`PRODUCTION_GUIDE.md`**:
```markdown
# Guia de Produção

## Pré-requisitos
- [ ] Chaves reais no .env
- [ ] Security scan aprovado
- [ ] Testes E2E passando
- [ ] Backup configurado

## Checklist de Deploy
1. [ ] docker-compose up -d
2. [ ] docker-compose ps (todos Up)
3. [ ] Health check: http://localhost:8000/health
4. [ ] Testar processamento de arquivo
5. [ ] Validar dashboard no Obsidian

## Monitoramento
- Health dashboard: http://localhost:8080
- Logs: docker-compose logs -f
- Alertas: Configurar no monitoring/

## Rollback
Se algo der errado:
1. docker-compose down
2. Restaurar backup mais recente
3. docker-compose up -d
```

**`TROUBLESHOOTING_ADVANCED.md`**:
```markdown
# Problemas Comuns em Produção

## Engine não processa arquivos
Causas possíveis:
1. Pasta mapeada errada
2. Permissão de arquivo
3. Watcher travado

Solução:
docker-compose restart marketing_engine
docker-compose logs marketing_engine

## IA não responde
Causas:
1. Chave inválida
2. Rate limit
3. Sem créditos

Solução:
1. Verificar .env
2. Testar API manualmente
3. Verificar quota

## Supabase lento
Causas:
1. Muitas conexões
2. Queries sem índice
3. Plano gratuito limitado

Solução:
1. Connection pooling
2. Adicionar índices
3. Upgrade de plano
```

---

### FASE 34: Otimizações de Performance (20 min)

Crie: `mkt/engine/src/optimizer.py`

**Otimizações**:

```python
class PerformanceOptimizer:
    """Otimizações de performance"""
    
    def batch_insert_metrics(metrics_list):
        """Inserir 1000 métricas de uma vez"""
        # Em vez de 1000 inserts, fazer 1 bulk insert
        supabase.table('business_metrics').insert(metrics_list).execute()
    
    def cache_tenant_lookups():
        """Cache de tenant_id (evita queries repetidas)"""
        # Redis ou cache em memória
        # TTL: 1 hora
    
    def async_pdf_processing():
        """Processar PDFs em background"""
        # Usar threading ou asyncio
        # Não bloquear watcher
    
    def compress_old_data():
        """Compactar dados antigos (>90 dias)"""
        # Mover para tabela archive_
        # Reduzir custo de storage
```

**Ganhos esperados**:
- 10x mais rápido em inserts em lote
- 50% menos queries ao Supabase
- Processamento de PDF não bloqueia watcher

---

### FASE 35: Release Notes v4.1 (10 min)

Atualize: `mkt/CHANGELOG.md`

**Adicionar seção**:

```markdown
## [4.1.0] — Produção (2026-02-25)

### ✨ Adicionado
- Security scan automatizado (pip-audit)
- Testes E2E com dados reais
- CI/CD pipeline (GitHub Actions)
- Monitoring dashboard
- Backup automático diário
- Scripts de utilidade (reset, logs, migrate)
- Performance optimizations (batch inserts, cache)

### 🔒 Segurança
- Scan de vulnerabilidades em cada commit
- RLS auditado e testado
- Backup criptografado

### 📊 Performance
- 10x mais rápido em inserts em lote
- 50% menos queries ao banco
- Processamento assíncrono de PDFs

### 🐛 Corrigido
- [Listar bugs corrigidos]

### ⚠️ Breaking Changes
- Nenhum (compatível com v4.0)
```

---

## ✅ CHECKLIST DE VALIDAÇÃO (FASE 27-35)

Após criar todos os arquivos, verifique:

### Segurança
- [ ] `scripts/security_scan.sh` existe e roda
- [ ] `pip-audit` não encontrou vulnerabilidades críticas
- [ ] `.env` está no `.gitignore`
- [ ] RLS testado e funcionando

### Testes
- [ ] `tests/e2e_test.py` existe
- [ ] `pytest tests/` passa (100%)
- [ ] Cobertura > 80%
- [ ] Testes com dados reais funcionam

### CI/CD
- [ ] `.github/workflows/ci.yml` existe
- [ ] Push no GitHub dispara workflow
- [ ] Tests + Lint + Security passando
- [ ] Docker build automático

### Monitoramento
- [ ] `monitoring/health_check.py` roda
- [ ] Dashboard atualiza a cada 5 min
- [ ] Métricas corretas sendo coletadas
- [ ] Alertas configurados

### Backup
- [ ] `scripts/backup.py` existe
- [ ] Backup roda diariamente
- [ ] Restaurar backup funciona
- [ ] Backups na nuvem

### Performance
- [ ] `optimizer.py` implementado
- [ ] Batch insert funcionando
- [ ] Cache de tenants ativo
- [ ] Processamento assíncrono

### Documentação
- [ ] `docs/PRODUCTION_GUIDE.md` existe
- [ ] `docs/TROUBLESHOOTING_ADVANCED.md` existe
- [ ] `CHANGELOG.md` atualizado para v4.1
- [ ] README.md com link para produção

---

## 🎯 REGRAS DE QUALIDADE

### Código Python
- Type hints obrigatórios
- Docstrings em tudo
- Logging estruturado
- Tratamento de erros
- Comentários em português

### Scripts Bash/PowerShell
- Funcionar em Windows e Linux
- Mensagens de erro claras
- Códigos de retorno corretos

### CI/CD
- Falhar rápido (fail fast)
- Logs detalhados
- Notificações em falha

### Monitoramento
- Métricas úteis (acionáveis)
- Alertas inteligentes (sem ruído)
- Dashboard legível

---

## 🚀 INSTRUÇÕES FINAIS

1. **Siga a ordem EXATA** (Fases 27-35)
2. **Teste cada fase** após criar
3. **Valide com checklist**
4. **Documente decisões** arquiteturais

**Tempo estimado total**: 3-4 horas

**Entregável**: Sistema nível produção (v4.1.0)

---

## 📊 ENTREGÁVEIS ESPERADOS

| Arquivo | Tamanho Esperado |
| :------ | :--------------- |
| `scripts/security_scan.sh` | ~50 linhas |
| `tests/e2e_test.py` | ~200 linhas |
| `.github/workflows/ci.yml` | ~80 linhas |
| `monitoring/health_check.py` | ~150 linhas |
| `monitoring/dashboard.md` | ~50 linhas |
| `scripts/backup.py` | ~200 linhas |
| `scripts/*.sh` (4 scripts) | ~200 linhas |
| `engine/src/optimizer.py` | ~150 linhas |
| `docs/PRODUCTION_GUIDE.md` | ~100 linhas |
| `docs/TROUBLESHOOTING_ADVANCED.md` | ~150 linhas |

**Total**: ~1,330 linhas novas

---

## 🎁 BÔNUS (Se Sobrar Tempo)

### FASE 36: Webhook de Notificações

Crie: `mkt/notifications/webhook.py`

```python
# Enviar notificação quando:
# - Arquivo processado com erro
# - Insight de IA gerado (urgente)
# - Health check falhar
# - Backup completou

# Canais:
# - WhatsApp (Evolution API)
# - Email (SMTP)
# - Telegram Bot
```

### FASE 37: API REST

Crie: `mkt/api/routes.py`

```python
# endpoints:
# GET  /api/tenants          # Listar tenants
# GET  /api/metrics/:id      # Métricas de tenant
# POST /api/insights/generate # Gerar insight
# GET  /api/health           # Health check
```

### FASE 38: Mobile App (Futuro)

Planejar:
- React Native ou Flutter
- Sync offline-first
- Push notifications

---

## 📞 SUPORTE DURANTE DESENVOLVIMENTO

Se tiver dúvidas:

1. **Consulte** `AUDITORIA_HIVE_OS.md` para contexto
2. **Valide** com Socratic Gate
3. **Mantenha** Truth in Data
4. **Priorize** produção primeiro

---

## 🏆 CRITÉRIOS DE SUCESSO

Sistema em produção quando:

- [ ] Security scan: ✅ Aprovado
- [ ] Testes E2E: ✅ Passando
- [ ] CI/CD: ✅ Pipeline verde
- [ ] Monitoramento: ✅ Dashboard ativo
- [ ] Backup: ✅ Rodando diariamente
- [ ] Performance: ✅ Otimizações ativas
- [ ] Documentação: ✅ Completa e atualizada

---

<div align="center">

**🚀 Comece agora pela FASE 27: Security Scan**

*Boa implementação!*

**Versão Alvo**: v4.1.0 (Produção)

</div>
