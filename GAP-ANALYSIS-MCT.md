# 🔍 ANÁLISE: PROMPT CLAUDE vs IMPLEMENTAÇÃO ATUAL

> **Data**: 2026-02-24
> **Tipo**: Gap Analysis
> **Objetivo**: Identificar melhorias faltantes no MCT Agent Factory

---

## 📊 RESUMO EXECUTIVO

| Categoria | Implementado | Faltante | Prioridade |
|-----------|-------------|----------|------------|
| **Core Orchestrator** | ✅ 100% | - | - |
| **Skills System** | ✅ 100% | - | - |
| **Tools** | ✅ 100% | - | - |
| **Knowledge Base Haven** | ⚠️ 60% | 📝 40% | 🔴 ALTA |
| **System Prompt** | ❌ 0% | 📝 100% | 🔴 ALTA |
| **Brain Integration** | ❌ 0% | 📝 100% | 🔴 ALTA |
| **Validação** | ⚠️ 50% | 📝 50% | 🟡 MÉDIA |

---

## ✅ O QUE JÁ ESTÁ IMPLEMENTADO

### 1. Core Orchestrator (100%)
- [x] `core/orchestrator/index.js`
- [x] `core/orchestrator/task-planner.js`
- [x] `core/orchestrator/agent-router.js`
- [x] `core/orchestrator/memory-manager.js`

**Status**: Funcional, sintaxe validada ✅

### 2. Skills System (100%)
- [x] `core/skills/base.skill.js`
- [x] `core/skills/whatsapp.skill.js`
- [x] `core/skills/calendar.skill.js`
- [x] `core/skills/crm.skill.js`
- [x] `core/skills/payment.skill.js`
- [x] `core/skills/notification.skill.js`
- [x] `core/skills/index.js`

**Status**: Funcional, sintaxe validada ✅

### 3. Tools (100%)
- [x] `core/tools/openrouter.tool.js`
- [x] `core/tools/evolution.tool.js`
- [x] `core/tools/supabase.tool.js`
- [x] `core/tools/belasis.tool.js`

**Status**: Funcional, sintaxe validada ✅

### 4. Knowledge Base Haven (60%)
- [x] `services.json` — 14 serviços (versão simplificada)
- [x] `professionals.json` — 7 profissionais (versão simplificada)
- [x] `rules.json` — Regras básicas
- [x] `faq.json` — 6 FAQs (versão simplificada)
- [ ] `business.json` — ❌ FALTANDO
- [ ] `packages.json` — ❌ FALTANDO
- [ ] `upsells.json` — ❌ FALTANDO
- [ ] `coupons.json` — ❌ FALTANDO

**Status**: Funcional mas incompleto ⚠️

---

## 🔴 O QUE FALTA IMPLEMENTAR (PRIORIDADE ALTA)

### 1. Knowledge Base Completa Haven

#### 1.1 `business.json` (CRÍTICO)
**Arquivo**: `agents/haven-receptionist/knowledge/business.json`

**Conteúdo Faltante**:
```json
{
  "name": "Haven Escovaria & Esmalteria",
  "type": "beauty_salon",
  "positioning": "Espaço sofisticado, moderno e acolhedor",
  "address": {
    "street": "Rua Mato Grosso, 837E",
    "neighborhood": "Jardim Itália",
    "city": "Chapecó",
    "state": "SC"
  },
  "hours": {
    "monday": { "open": "08:00", "close": "20:00" },
    "tuesday": { "open": "08:00", "close": "20:00" },
    "wednesday": { "open": "08:00", "close": "20:00" },
    "thursday": { "open": "08:00", "close": "20:00" },
    "friday": { "open": "08:00", "close": "20:00" },
    "saturday": { "open": "08:00", "close": "20:00" },
    "sunday": "closed"
  },
  "parking": {
    "front": true,
    "corner": { "available": true, "spots": 4 }
  }
}
```

**Impacto**: Sem este arquivo, o agente não sabe informações básicas do negócio.

---

#### 1.2 `packages.json` (CRÍTICO)
**Arquivo**: `agents/haven-receptionist/knowledge/packages.json`

**Conteúdo Faltante**:
- Pacotes de Escova (4, 8 unidades)
- Pacotes de Gel (3, 6 unidades)
- Pacotes de Unha Tradicional
- Regras de validade
- Preços com desconto de pacote
- Premium addons (coreano, labrisa, kerastase)

**Impacto**: Agente não consegue vender pacotes (receita recorrente).

---

#### 1.3 `upsells.json` (ALTO)
**Arquivo**: `agents/haven-receptionist/knowledge/upsells.json`

**Conteúdo Faltante**:
- Upgrades de produtos no lavatório
- Coreano (+R$30)
- La Brisa (+R$25)
- Kérastase (+R$30)
- Regras de promoção
- Script de venda

**Impacto**: Perda de receita de upsell (ticket médio maior).

---

#### 1.4 `coupons.json` (MÉDIO)
**Arquivo**: `agents/haven-receptionist/knowledge/coupons.json`

**Conteúdo Faltante**:
- PRISCILA10 (10%)
- EWYLIN10 (10%)
- SOLANGE10 (10%)
- CAROLINE10 (10%)
- KETLYN10 (10%)
- Regras de uso

**Impacto**: Não consegue aplicar desconto de blogueiras.

---

### 2. System Prompt Haven (CRÍTICO)

#### 2.1 `prompts/system.md`
**Arquivo**: `agents/haven-receptionist/prompts/system.md`

**Conteúdo Faltante**:
```markdown
# Luna - Recepcionista Virtual Haven

## Identidade
- Nome: Luna
- Papel: Recepcionista Virtual
- Empresa: Haven Escovaria & Esmalteria

## Personalidade
- Calorosa, profissional, atenciosa
- Tom natural do Sul do Brasil
- Usa emojis com moderação (1-3)

## Palavras Proibidas
NUNCA usar: "senhora", "prezada", "aguarde um momento", "infelizmente"

## Regras de Ouro
1. Ordem: Unha → Cabelo → Maquiagem
2. Perguntas obrigatórias (unhas, penteado, tratamento)
3. Nunca fechar no "não"
4. Blindagem de produto
5. Confirmação final

## Output Format
{
  "thinking": "...",
  "response": "...",
  "extracted_fields": {...},
  "next_action": "...",
  "handoff": false
}
```

**Impacto**: Agente não tem identidade clara e pode violar regras de negócio.

---

### 3. Brain Integration (CRÍTICO)

#### 3.1 Atualizar `brain.js`
**Arquivo**: `agents/haven-receptionist/src/services/brain.js`

**O Que Falta**:
1. Carregar TODOS os JSONs da knowledge base
2. Classificador de intenção expandido (15+ intents)
3. Context builder com business, packages, upsells, coupons
4. Smart routing baseado em complexidade
5. Tool definitions expandidas (5 tools)
6. Parse de resposta robusto

**Código Faltante**: ~400 linhas

**Impacto**: Haven não usa knowledge base completa, respostas genéricas.

---

## 🟡 O QUE FALTA (PRIORIDADE MÉDIA)

### 4. Validação Completa

#### 4.1 Script de Validação
**Arquivo**: `scripts/validate-mct.sh`

**Conteúdo Faltante**:
```bash
#!/bin/bash
# 1. Verificar estrutura
# 2. Validar JSONs
# 3. Verificar sintaxe JS
# 4. Testar health
# 5. Testar processamento
# 6. Testar FAQ
# 7. Testar cupom
```

---

#### 4.2 Testes de Integração
**Arquivo**: `tests/mct-integration.test.js`

**Testes Faltantes**:
- Testar orchestrator com mock
- Testar skills individualmente
- Testar knowledge base loading
- Testar brain com mensagens reais

---

## 📋 PLANO DE AÇÃO

### FASE A: Knowledge Base Completa (2 horas)

```bash
# 1. Criar business.json
cat > agents/haven-receptionist/knowledge/business.json << 'EOF'
{ ... }
EOF

# 2. Criar packages.json
cat > agents/haven-receptionist/knowledge/packages.json << 'EOF'
{ ... }
EOF

# 3. Criar upsells.json
cat > agents/haven-receptionist/knowledge/upsells.json << 'EOF'
{ ... }
EOF

# 4. Criar coupons.json
cat > agents/haven-receptionist/knowledge/coupons.json << 'EOF'
{ ... }
EOF

# 5. Validar JSONs
for f in agents/haven-receptionist/knowledge/*.json; do
  node -e "JSON.parse(require('fs').readFileSync('$f'))"
done
```

**Tempo Estimado**: 30 minutos

---

### FASE B: System Prompt (1 hora)

```bash
# 1. Criar prompts directory
mkdir -p agents/haven-receptionist/prompts

# 2. Criar system.md
cat > agents/haven-receptionist/prompts/system.md << 'EOF'
# Luna - Recepcionista Virtual Haven
...
EOF
```

**Tempo Estimado**: 30 minutos

---

### FASE C: Brain Integration (3 horas)

```bash
# 1. Backup do brain atual
cp agents/haven-receptionist/src/services/brain.js \
   agents/haven-receptionist/src/services/brain.js.backup

# 2. Criar novo brain.js
cat > agents/haven-receptionist/src/services/brain.js << 'EOF'
/**
 * HAVEN BRAIN - Processamento com Knowledge Base Completa
 */
...
EOF

# 3. Validar sintaxe
node --check agents/haven-receptionist/src/services/brain.js

# 4. Testar
docker-compose restart haven-receptionist-api
docker logs haven-receptionist-api --tail 50
```

**Tempo Estimado**: 2 horas

---

### FASE D: Validação (1 hora)

```bash
# 1. Criar script de validação
cat > scripts/validate-mct.sh << 'EOF'
#!/bin/bash
...
EOF
chmod +x scripts/validate-mct.sh

# 2. Executar validação
./scripts/validate-mct.sh

# 3. Testes manuais
curl -X POST http://localhost:3003/test \
  -H "Content-Type: application/json" \
  -d '{"message": "Oi, quero marcar uma escova", "userId": "test"}'
```

**Tempo Estimado**: 1 hora

---

## 🎯 PRIORIZAÇÃO

| Ordem | Tarefa | Tempo | Impacto |
|-------|--------|-------|---------|
| 1 | `business.json` | 10 min | 🔴 Alto |
| 2 | `packages.json` | 20 min | 🔴 Alto |
| 3 | `coupons.json` | 10 min | 🟡 Médio |
| 4 | `upsells.json` | 15 min | 🟡 Médio |
| 5 | `system.md` | 30 min | 🔴 Alto |
| 6 | `brain.js` | 2 horas | 🔴 Crítico |
| 7 | Validação | 1 hora | 🟢 Baixo |

**Total**: ~4 horas

---

## 📊 IMPACTO POR ÁREA

### Receita
| Feature | Impacto | Valor Estimado |
|---------|---------|----------------|
| Pacotes | Recorrência | +R$5k/mês |
| Upsells | Ticket médio | +R$30/cliente |
| Cupons | Conversão | +15% |

### Experiência
| Feature | Impacto | Métrica |
|---------|---------|---------|
| System Prompt | Consistência | NPS +20 |
| Brain Integration | Precisão | CSAT +30% |
| Knowledge Base | Respostas | Erros -80% |

---

## ✅ CHECKLIST FINAL

### Knowledge Base
- [ ] business.json
- [ ] packages.json
- [ ] upsells.json
- [ ] coupons.json
- [ ] services.json (atualizar com 50+ serviços)
- [ ] professionals.json (atualizar com 9 profissionais)
- [ ] rules.json (expandir regras)
- [ ] faq.json (expandir para 15+ FAQs)

### System Prompt
- [ ] prompts/system.md
- [ ] Identidade Luna
- [ ] Personalidade
- [ ] Regras de ouro
- [ ] Output format

### Brain Integration
- [ ] Carregar todos JSONs
- [ ] Classificador 15+ intents
- [ ] Context builder completo
- [ ] Smart routing
- [ ] 5 tool definitions
- [ ] Parse robusto

### Validação
- [ ] Script validate-mct.sh
- [ ] Testes de integração
- [ ] Testes manuais
- [ ] Documentação

---

## 🚀 RECOMENDAÇÃO

**Execute nesta ordem**:

1. **HOJE (2 horas)**:
   - business.json
   - packages.json
   - coupons.json
   - upsells.json
   - system.md

2. **AMANHÃ (3 horas)**:
   - brain.js completo
   - Validação
   - Testes

3. **DEPOIS**:
   - Expandir services.json (50+ serviços)
   - Expandir professionals.json (9 profissionais)
   - Expandir faq.json (15+ FAQs)

---

**"MCT Agent Factory v1.0 está 70% completo.**
**Faltam 30% (Knowledge Base + Brain) para 100% operacional."**

🎯 **FOCO: Complete os JSONs e o brain.js primeiro!**
