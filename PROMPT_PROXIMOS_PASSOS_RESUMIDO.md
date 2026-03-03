# 🎯 PROMPT RESUMIDO — Próximos Passos (v4.1.0)

> **Para**: Antigravity
> **Contexto**: Sistema v4.0 auditado (OURO 94%)
> **Objetivo**: Produzir versão v4.1.0

---

## 📋 CONTEXTO RÁPIDO

**Status**: ✅ v4.0 completa (26 arquivos, 6,300 linhas)  
**Próximo**: v4.1.0 (Produção)  
**Fases**: 27-35 (9 fases)  
**Tempo**: 3-4 horas

---

## 🎯 FASES 27-35 (Resumo)

### 27. Security Scan (15 min)
```bash
Crie: scripts/security_scan.sh
- pip-audit em requirements.txt
- docker scan
- Relatório em logs/security_report.md
```

### 28. Testes E2E (20 min)
```bash
Crie: tests/e2e_test.py
- Teste com CSV real do salão
- Teste com PDF de estratégia
- Teste de isolamento RLS
- pytest, 80%+ coverage
```

### 29. CI/CD Pipeline (30 min)
```bash
Crie: .github/workflows/ci.yml
- Lint (black, mypy)
- Security scan (pip-audit)
- Tests (pytest)
- Docker build
```

### 30. Monitoramento (25 min)
```bash
Crie: monitoring/health_check.py
- Métricas: engine, supabase, IA, negócio
- Dashboard: monitoring/dashboard.md
- Atualiza a cada 5 min
```

### 31. Backup Automático (20 min)
```bash
Crie: scripts/backup.py
- Backup Supabase: diário 03:00
- Backup Obsidian: diário 03:30
- Reter: 30 dias / 7 dias
```

### 32. Scripts de Utilidade (15 min)
```bash
Crie em scripts/:
- reset_system.sh
- logs_viewer.sh
- db_migrate.sh
- seed_data.py
```

### 33. Doc de Produção (20 min)
```bash
Crie em docs/:
- PRODUCTION_GUIDE.md (checklist de deploy)
- TROUBLESHOOTING_ADVANCED.md
```

### 34. Performance (20 min)
```bash
Crie: engine/src/optimizer.py
- Batch insert (10x mais rápido)
- Cache de tenants (50% menos queries)
- PDF assíncrono (não bloqueia)
```

### 35. Release Notes (10 min)
```bash
Atualize: CHANGELOG.md
- Versão: 4.1.0 (Produção)
- Adicionado: 9 features novas
- Performance: 10x, 50%
- Segurança: scan, backup, RLS
```

---

## ✅ CHECKLIST RÁPIDO

Após criar:

- [ ] Security scan roda e passa
- [ ] Testes E2E com dados reais
- [ ] CI/CD no GitHub Actions
- [ ] Dashboard de monitoramento
- [ ] Backup automático diário
- [ ] Scripts de utilidade
- [ ] Docs de produção
- [ ] Otimizações de performance
- [ ] CHANGELOG atualizado (v4.1.0)

---

## 📊 ENTREGÁVEIS

| Arquivo | Linhas |
| :------ | :----- |
| `scripts/security_scan.sh` | 50 |
| `tests/e2e_test.py` | 200 |
| `.github/workflows/ci.yml` | 80 |
| `monitoring/health_check.py` | 150 |
| `scripts/backup.py` | 200 |
| `scripts/*.sh` (4) | 200 |
| `engine/src/optimizer.py` | 150 |
| `docs/PRODUCTION_GUIDE.md` | 100 |
| `docs/TROUBLESHOOTING_ADVANCED.md` | 150 |

**Total**: ~1,330 linhas novas

---

## 🚀 COMECE AGORA

```bash
# FASE 27: Security Scan
mkdir -p mkt/scripts
# Crie: mkt/scripts/security_scan.sh
```

**Boa implementação!**

---

<div align="center">

**Prompt Completo**: `PROMPT_PROXIMOS_PASSOS.md`  
**Este Arquivo**: Versão resumida

**Alvo**: v4.1.0 (Produção)

</div>
