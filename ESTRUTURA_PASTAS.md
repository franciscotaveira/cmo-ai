# 📁 ESTRUTURA DE PASTAS — Marketing Director OS v4.0

> **Nova Localização**: `C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\`
> **Objetivo**: Organização centralizada do projeto
> **Data**: 2026-02-25
> **Status**: Estrutura definida

---

## 🎯 NOVA ESTRUTURA DE PASTAS

```
C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\
│
├── 📁 01-DOCUMENTACAO/
│   ├── README.md                          # Visão geral do projeto
│   ├── VISAO_FINAL_CONSOLIDADA.md         # Visão v4.0 + v5.0 + v10.0
│   ├── CEREBRO_ADAPTATIVO_VISAO_INFINITA.md
│   ├── MARKETING_BRAIN_SEMI_AUTOMATICO.md
│   ├── MARKETING_BRAIN_HARDWARE_LIMITADO.md
│   ├── OBSIDIAN_INTEGRATIONS_MASTER.md
│   ├── OBSIDIAN_PLUGINS_RECOMENDADOS.md
│   ├── AUDITORIA_HIVE_OS.md
│   └── RELATORIO_FINAL_ENTREGA.md
│
├── 📁 02-ESPECIFICACOES/
│   ├── ESPECIFICACAO_MDCC.md              # MDCC Spec completa (13 seções)
│   ├── ARQUITETURA_UNIFICADA.md
│   └── ROADMAP_DETALHADO.md
│
├── 📁 03-CODIGO-FONTE/
│   │
│   ├── 📁 engine/                         # Python Engine
│   │   ├── main.py                        # Ponto de entrada
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   │
│   │   └── 📁 src/
│   │       ├── __init__.py
│   │       ├── database.py                # Supabase handler
│   │       ├── processor.py               # CSV/PDF parser
│   │       ├── watcher.py                 # File watcher
│   │       ├── obsidian.py                # Obsidian bridge
│   │       ├── ai_engine.py               # RAG + LLM
│   │       ├── webhook_server.py          # HTTP 8080
│   │       └── decision_engine.py         # HITL decisions
│   │
│   ├── 📁 plugins/                        # Plugins Obsidian
│   │   └── 📁 marketing-brain/
│   │       ├── main.ts
│   │       ├── manifest.json
│   │       └── styles.css
│   │
│   └── 📁 scripts/                        # Scripts utilitários
│       ├── setup.ps1                      # Setup automático Windows
│       ├── test_system.py                 # 7 testes automatizados
│       └── backup.py                      # Backup automático
│
├── 📁 04-INFRAESTRUTURA/
│   ├── docker-compose.yml                 # Orquestração Docker
│   ├── init_supabase.sql                  # Schema do banco
│   ├── .env.example                       # Modelo de configuração
│   └── .gitignore                         # Git ignore
│
├── 📁 05-DADOS/
│   │
│   ├── 📁 drive_data/                     # Simulação Google Drive
│   │   ├── 📁 salao-esposa/
│   │   ├── 📁 franquia-chapeco/
│   │   └── 📁 diretoria/
│   │
│   ├── 📁 obsidian_vault/                 # Vault do Obsidian
│   │   ├── 📁 00-Dashboard/
│   │   ├── 📁 01-Insights/
│   │   ├── 📁 02-Alertas/
│   │   ├── 📁 03-Campanhas/
│   │   ├── 📁 04-Empresas/
│   │   └── 📁 99-Arquivo/
│   │
│   └── 📁 backups/                        # Backups automáticos
│       ├── 📁 supabase/
│       └── 📁 obsidian/
│
├── 📁 06-TESTES/
│   ├── 📁 e2e/                            # Testes end-to-end
│   ├── 📁 unit/                           # Testes unitários
│   └── 📁 integration/                    # Testes de integração
│
├── 📁 07-LOGS/
│   ├── 📁 engine/                         # Logs do Python
│   ├── 📁 docker/                         # Logs do Docker
│   └── 📁 audit/                          # Logs de auditoria
│
├── 📁 08-MODELOS/
│   ├── 📁 templates-obsidian/             # Templates de notas
│   │   ├── template-insight.md
│   │   ├── template-alerta.md
│   │   ├── template-campanha.md
│   │   └── template-dashboard.md
│   │
│   ├── 📁 templates-email/                # Templates de email
│   └── 📁 templates-relatorio/            # Templates de relatório
│
├── 📁 09-INTEGRACOES/
│   ├── 📁 meta-ads/                       # Integração Meta Ads
│   ├── 📁 google-ads/                     # Integração Google Ads
│   ├── 📁 evolution-api/                  # WhatsApp
│   ├── 📁 email-api/                      # SendGrid, etc.
│   └── 📁 crm-api/                        # HubSpot, Pipedrive
│
├── 📁 10-EMPRESAS/
│   ├── 📁 001-salao-esposa/
│   │   ├── dashboard.md
│   │   ├── insights/
│   │   ├── campanhas/
│   │   └── configuracoes.json
│   │
│   ├── 📁 002-franquia-chapeco/
│   └── 📁 003-diretoria/
│
└── 📁 11-ARQUIVOS-HISTORICOS/
    ├── 📁 antigravity-kit-original/       # Pasta original (referência)
    └── 📁 versoes-anteriores/
```

---

## 🔄 MIGRAÇÃO DA PASTA ORIGINAL

### O Que Fica em `antigravity-kit/`

```
c:\Users\Marketing\Documents\Antigravity\antigravity-kit\
│
├── AGENT_FLOW.md              # ✅ Manter (workflow HIVE OS)
├── AUDITORIA_HIVE_OS.md       # ✅ Manter (auditoria)
├── RELATORIO_FINAL_ENTREGA.md # ✅ Manter (relatório)
│
└── 📁 mkt/                    # ✅ Manter (código original)
    ├── engine/
    ├── docs/
    ├── docker-compose.yml
    └── ... (26 arquivos originais)
```

**Status**: Pasta original permanece como **referência histórica**

---

### O Que Vai para Nova Pasta

```
C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\
│
├── 📁 01-DOCUMENTACAO/        # ← Copiar docs de mkt/ + novos
├── 📁 02-ESPECIFICACOES/      # ← MDCC Spec + arquitetura
├── 📁 03-CODIGO-FONTE/        # ← Copiar engine/ de mkt/
├── 📁 04-INFRAESTRUTURA/      # ← Copiar docker, SQL de mkt/
├── 📁 05-DADOS/               # ← Novo (dados reais)
├── 📁 06-TESTES/              # ← Copiar test_system.py
├── 📁 07-LOGS/                # ← Novo (logs centralizados)
├── 📁 08-MODELOS/             # ← Novo (templates)
├── 📁 09-INTEGRACOES/         # ← Novo (APIs externas)
├── 📁 10-EMPRESAS/            # ← Novo (por empresa)
└── 📁 11-ARQUIVOS-HISTORICOS/ # ← Referência original
```

---

## 📋 CHECKLIST DE MIGRAÇÃO

### Fase 1: Criar Estrutura (30 min)

```powershell
# Criar nova pasta base
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0"

# Criar subpastas
cd "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0"

mkdir 01-DOCUMENTACAO
mkdir 02-ESPECIFICACOES
mkdir 03-CODIGO-FONTE
mkdir 04-INFRAESTRUTURA
mkdir 05-DADOS
mkdir 06-TESTES
mkdir 07-LOGS
mkdir 08-MODELOS
mkdir 09-INTEGRACOES
mkdir 10-EMPRESAS
mkdir 11-ARQUIVOS-HISTORICOS
```

---

### Fase 2: Copiar Documentação (30 min)

```powershell
# Copiar documentação de mkt/
Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\README.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\CODEBASE.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\docs\*" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\" -Recurse

# Copiar documentos conceituais
Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\CEREBRO_*.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\MARKETING_*.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\OBSIDIAN_*.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\AUDITORIA_*.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\RELATORIO_*.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\VISAO_*.md" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\01-DOCUMENTACAO\"
```

---

### Fase 3: Copiar Código (30 min)

```powershell
# Copiar engine Python
Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\engine\*" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\03-CODIGO-FONTE\engine\" -Recurse

# Copiar infraestrutura
Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\docker-compose.yml" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\04-INFRAESTRUTURA\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\init_supabase.sql" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\04-INFRAESTRUTURA\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\.env.example" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\04-INFRAESTRUTURA\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\.gitignore" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\04-INFRAESTRUTURA\"
```

---

### Fase 4: Copiar Testes e Scripts (15 min)

```powershell
# Copiar testes
Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\test_system.py" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\06-TESTES\"

Copy-Item "c:\Users\Marketing\Documents\Antigravity\antigravity-kit\mkt\setup.ps1" `
          "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\06-TESTES\"
```

---

### Fase 5: Configurar Dados (30 min)

```powershell
# Criar estrutura de dados do Drive
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\drive_data\salao-esposa"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\drive_data\franquia-chapeco"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\drive_data\diretoria"

# Criar estrutura do Obsidian Vault
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\obsidian_vault\00-Dashboard"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\obsidian_vault\01-Insights"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\obsidian_vault\02-Alertas"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\obsidian_vault\03-Campanhas"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\obsidian_vault\04-Empresas"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\obsidian_vault\99-Arquivo"

# Criar pastas de backup
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\backups\supabase"
mkdir "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\05-DADOS\backups\obsidian"
```

---

### Fase 6: Criar Templates (1 hora)

```powershell
# Criar templates de notas no Obsidian
@"
---
created: {{date}}
tenant: {{tenant}}
priority: high
tags: [insight, auto-generated]
---

# 💡 Insight: {{title}}

**Gerado por**: Marketing Brain v4.0

## Contexto
{{context}}

## Análise
{{analysis}}

## Ação Sugerida
- [ ] Aprovar
- [ ] Rejeitar
- [ ] Editar

---
*Gerado automaticamente pelo Marketing Director OS*
"@ | Out-File -FilePath "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\08-MODELOS\templates-obsidian\template-insight.md" -Encoding UTF8
```

---

### Fase 7: Atualizar Configurações (30 min)

```powershell
# Criar .env na nova pasta
@"
# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-service-role

# IA
OPENAI_API_KEY=sk-proj-sua-chave
# ou
GEMINI_API_KEY=sua-chave

# Caminhos (AJUSTAR PARA NOVA PASTA)
PATH_TO_DRIVE=C:/Users/Marketing/Documents/00 - Marketing/IA/Marketing Director OS v4.0/05-DADOS/drive_data
PATH_TO_OBSIDIAN=C:/Users/Marketing/Documents/00 - Marketing/IA/Marketing Director OS v4.0/05-DADOS/obsidian_vault

# Configurações
WINDMILL_PORT=8000
DB_PASSWORD=changeme123
LOG_LEVEL=INFO
WATCHER_RECURSIVE=true
"@ | Out-File -FilePath "C:\Users\Marketing\Documents\00 - Marketing\IA\Marketing Director OS v4.0\04-INFRAESTRUTURA\.env" -Encoding UTF8
```

---

### Fase 8: Atualizar Docker (15 min)

```yaml
# Atualizar docker-compose.yml com novos caminhos
version: '3.8'

services:
  marketing_engine:
    build: ./03-CODIGO-FONTE/engine
    volumes:
      - ${PATH_TO_DRIVE}:/app/drive_input
      - ${PATH_TO_OBSIDIAN}:/app/obsidian_output
    # ... resto da configuração
```

---

## 📊 MAPA DE ARQUIVOS

### De → Para

| Original (antigravity-kit) | Novo (Marketing Director OS v4.0) |
| :------------------------- | :-------------------------------- |
| `mkt/README.md` | `01-DOCUMENTACAO/README.md` |
| `mkt/CODEBASE.md` | `01-DOCUMENTACAO/CODEBASE.md` |
| `mkt/docs/*` | `01-DOCUMENTACAO/*` |
| `mkt/engine/*` | `03-CODIGO-FONTE/engine/*` |
| `mkt/docker-compose.yml` | `04-INFRAESTRUTURA/docker-compose.yml` |
| `mkt/init_supabase.sql` | `04-INFRAESTRUTURA/init_supabase.sql` |
| `mkt/test_system.py` | `06-TESTES/test_system.py` |
| `CEREBRO_*.md` (root) | `01-DOCUMENTACAO/` |
| `MARKETING_*.md` (root) | `01-DOCUMENTACAO/` |
| `OBSIDIAN_*.md` (root) | `01-DOCUMENTACAO/` |
| `AUDITORIA_*.md` (root) | `01-DOCUMENTACAO/` |
| `VISAO_*.md` (root) | `01-DOCUMENTACAO/` |

---

## 🎯 BENEFÍCIOS DA NOVA ESTRUTURA

### 1. **Organização por Função**

```
01-DOCUMENTACAO/     → Saber o que é
02-ESPECIFICACOES/   → Saber como funciona
03-CODIGO-FONTE/     → Código fonte
04-INFRAESTRUTURA/   → Infra (Docker, SQL)
05-DADOS/            → Dados reais
06-TESTES/           → Testes automatizados
07-LOGS/             → Logs de execução
08-MODELOS/          → Templates reutilizáveis
09-INTEGRACOES/      → APIs externas
10-EMPRESAS/         → Por empresa (multi-tenant)
11-ARQUIVOS-HISTORICOS/ → Histórico
```

---

### 2. **Separação Clara**

```
✅ Código → 03-CODIGO-FONTE/
✅ Dados → 05-DADOS/
✅ Docs → 01-DOCUMENTACAO/
✅ Logs → 07-LOGS/
```

---

### 3. **Escalabilidade**

```
10-EMPRESAS/
├── 001-salao-esposa/
├── 002-franquia-chapeco/
├── 003-diretoria/
└── 004-empresa-n/  (futura)
```

---

### 4. **Versionamento**

```
11-ARQUIVOS-HISTORICOS/
├── versao-4.0/
├── versao-4.1/
└── versao-5.0/
```

---

## 📋 CHECKLIST FINAL DE MIGRAÇÃO

### Hoje (2-3 horas)

- [ ] Criar estrutura de pastas (Fase 1)
- [ ] Copiar documentação (Fase 2)
- [ ] Copiar código (Fase 3)
- [ ] Copiar testes (Fase 4)
- [ ] Configurar dados (Fase 5)

### Amanhã (1-2 horas)

- [ ] Criar templates (Fase 6)
- [ ] Atualizar configurações (Fase 7)
- [ ] Atualizar Docker (Fase 8)
- [ ] Testar nova estrutura

### Esta Semana

- [ ] Migrar dados reais para nova estrutura
- [ ] Atualizar .env com novos caminhos
- [ ] Testar end-to-end na nova estrutura
- [ ] Documentar learnings

---

## 🏆 VEREDITO

### Por Que Esta Estrutura é Melhor?

| Critério | Antiga (mkt/) | Nova (Marketing Director OS v4.0) |
| :------- | :-----------: | :-------------------------------: |
| **Organização** | 🟡 Por tipo | 🟢 Por função |
| **Escalabilidade** | 🔴 Baixa | 🟢 Alta (multi-empresa) |
| **Dados** | ❌ Misturados | 🟢 Separados (05-DADOS/) |
| **Logs** | ❌ Misturados | 🟢 Separados (07-LOGS/) |
| **Templates** | ❌ Não tinha | 🟢 08-MODELOS/ |
| **Integrações** | ❌ Não tinha | 🟢 09-INTEGRACOES/ |
| **Empresas** | ❌ Não tinha | 🟢 10-EMPRESAS/ |
| **Histórico** | ❌ Não tinha | 🟢 11-ARQUIVOS-HISTORICOS/ |

---

## 📁 ARQUIVO CRIADO

**`ESTRUTURA_PASTAS.md`**

**Local**: `c:\Users\Marketing\Documents\Antigravity\antigravity-kit\` (referência)

**Próximo**: Copiar para nova pasta e seguir checklist de migração

---

<div align="center">

**📁 ESTRUTURA DE PASTAS DEFINIDA**

*Nova organização: `00 - Marketing\IA\Marketing Director OS v4.0\`*

**2-3 horas para migrar • Organização muito melhor**

</div>
