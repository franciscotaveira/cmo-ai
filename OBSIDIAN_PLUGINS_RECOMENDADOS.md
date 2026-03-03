# 🔌 PLUGINS ESSENCIAIS DO OBSIDIAN — Para o Cérebro de Marketing

> **Foco**: Plugins para integrar com Supabase + Python + IA
> **Prioridade**: Do crítico ao "nice to have"
> **Data**: 2026-02-25

---

## 🎯 TOP 10 PLUGINS CRÍTICOS

### 1. **Obsidian REST API** 🔴 CRÍTICO
**O Que Faz**: Expõe API REST local para o Obsidian

**Por Que Você Precisa**:
```python
# Python → Obsidian (criar notas automáticas)
import requests

response = requests.post(
    'http://localhost:27123/api/vault/1/files/Insights/novo-insight.md',
    json={'content': '# Insight\n\nConteúdo...'}
)
```

**Setup**:
1. Instalar: `Settings → Community Plugins → Browse → "REST API"`
2. Configurar porta: `27123` (default)
3. Habilitar auth (recomendado)
4. Testar: `GET http://localhost:27123/api/vaults`

**Para Seu Cérebro**:
- Criar insights automáticos
- Atualizar dashboards
- Receber aprovações via webhook

**Alternativas**: Obsidian Remote, HTTP Requester

---

### 2. **Dataview** 🔴 CRÍTICO
**O Que Faz**: Query SQL-like em notas Markdown

**Por Que Você Precisa**:
```markdown
```dataview
TABLE file.name as "Insight", priority as "Prioridade", file.mtime as "Atualizado"
FROM "Insights"
WHERE contains(tags, "#alerta") AND priority = "high"
SORT file.mtime DESC
LIMIT 10
```
```

**Resultado**: Tabela dinâmica atualizada automaticamente

**Para Seu Cérebro**:
- Dashboards dinâmicos
- Listas de ações pendentes
- Relatórios automáticos

**Setup**:
1. Instalar plugin "Dataview"
2. Usar blocos ` ```dataview ` em notas
3. Query seu vault como banco de dados

---

### 3. **Obsidian Copilot** 🔴 CRÍTICO
**O Que Faz**: Chat com IA (local ou cloud) dentro do Obsidian

**Por Que Você Precisa**:
```
Usuário: "Quais insights temos sobre CAC alto?"
Copilot: [Busca no vault + Supabase via RAG]
         "Encontrei 3 insights sobre CAC..."
```

**Modelos Suportados**:
- ✅ OpenAI (GPT-4, GPT-3.5)
- ✅ Anthropic (Claude)
- ✅ Local (Ollama, LM Studio) ← **Seu caso**
- ✅ Custom (via API)

**Para Seu Cérebro**:
- Chat com dados do marketing
- RAG sobre insights históricos
- Geração de conteúdo

**Setup**:
1. Instalar plugin "Copilot"
2. Configurar API:
   - Local: `http://localhost:11434` (Ollama)
   - Cloud: API key da OpenAI
3. Ctrl+P → "Copilot: Chat"

**Alternativas**: Obsidian AI, Text Generator, Smart Connections

---

### 4. **Templater** 🟢 ALTA
**O Que Faz**: Templates avançados com variáveis dinâmicas

**Por Que Você Precisa**:
```markdown
---
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
tenant: <% tp.file.title %>
priority: high
tags: [insight, auto-generated]
---

# 💡 Insight: <% tp.file.title %>

**Gerado por**: <% tp.system.command("Marketing Brain") %>

## Contexto
<% tp.file.cursor() %>

## Ação Sugerida
- [ ] Aprovar
- [ ] Rejeitar
- [ ] Editar
```

**Para Seu Cérebro**:
- Templates de insights
- Templates de alertas
- Templates de campanhas

**Setup**:
1. Instalar plugin "Templater"
2. Criar pasta `Templates/`
3. Configurar no plugin

---

### 5. **QuickAdd** 🟢 ALTA
**O Que Faz**: Captura rápida de ideias/comandos

**Por Que Você Precisa**:
```
Ctrl+P → QuickAdd → "Novo Insight"
→ Digita insight
→ Salva automaticamente na pasta certa
```

**Para Seu Cérebro**:
- Captura rápida de insights manuais
- Comandos customizados
- Macros de automação

**Setup**:
1. Instalar plugin "QuickAdd"
2. Criar "Macros"
3. Configurar atalhos

---

### 6. **Webhook** 🟢 ALTA
**O Que Faz**: Enviar e receber webhooks

**Por Que Você Precisa**:
```yaml
# Receiver
Endpoint: POST /webhook/new-insight
Action: Create Note
Path: /Insights/{{body.slug}}.md
Content: |
  # {{body.title}}
  
  {{body.content}}
```

**Para Seu Cérebro**:
- Python → Obsidian (webhook)
- Aprovações → Python
- Notificações em tempo real

**Setup**:
1. Instalar plugin "Webhook"
2. Configurar endpoints
3. Testar com Postman/curl

**Alternativas**: HTTP Request (só envia)

---

### 7. **Self-hosted LiveSync** 🟢 ALTA
**O Que Faz**: Sync via CouchDB (grátis)

**Por Que Você Precisa**:
```
Vault Local ↔ CouchDB ↔ Outros Dispositivos
```

**Para Seu Cérebro**:
- Backup automático
- Sync entre dispositivos
- Histórico de versões

**Setup**:
1. Instalar CouchDB local ou remoto
2. Instalar plugin "Self-hosted LiveSync"
3. Configurar conexão

**Alternativas**: Obsidian Sync (pago, $8/mês), Syncthing (grátis)

---

### 8. **Obsidian Git** 🟢 ALTA
**O Que Faz**: Versionamento no Git

**Por Que Você Precisa**:
```
Notas → Git Commit → GitHub/GitLab
       ↓
       Backup + Histórico
```

**Para Seu Cérebro**:
- Backup automático
- Histórico de mudanças
- Colaboração

**Setup**:
1. Instalar plugin "Obsidian Git"
2. Configurar repositório
3. Auto-commit (opcional)

---

### 9. **Calendar** 🟢 ALTA
**O Que Faz**: Timeline de notas

**Por Que Você Precisa**:
```
Calendário visual → Clique no dia → Notas daquele dia
```

**Para Seu Cérebro**:
- Timeline de insights
- Histórico de campanhas
- Agenda de marketing

**Setup**:
1. Instalar plugin "Calendar"
2. Aparece no sidebar direito

---

### 10. **Execute Code** 🟢 ALTA
**O Que Faz**: Rodar código (JS, Python) dentro do Obsidian

**Por Que Você Precisa**:
```python
```execute-code --language python
import requests

# Buscar dados do Supabase
response = requests.get('http://localhost:8000/api/metrics')
metrics = response.json()

print(f"CAC atual: R$ {metrics['cac']}")
```
```

**Para Seu Cérebro**:
- Scripts rápidos
- Query APIs
- Automações in-note

**Setup**:
1. Instalar plugin "Execute Code"
2. Criar bloco de código
3. Botão "Run"

---

## 🟡 PLUGINS SECUNDÁRIOS (Nice to Have)

### 11. **Kanban**
**O Que Faz**: Quadros Kanban

**Para Seu Cérebro**:
- Gestão de campanhas ativas
- Pipeline de ideias
- Status de ações

**Setup**: Instalar → Criar nota → `Ctrl+P → Kanban: Create new board`

---

### 12. **Excalidraw**
**O Que Faz**: Diagramas/desenhos

**Para Seu Cérebro**:
- Mapas de estratégia
- Fluxos de campanha
- Diagramas de funnel

**Setup**: Instalar → `Ctrl+P → Excalidraw: Create new drawing`

---

### 13. **Advanced URI**
**O Que Faz**: URI scheme avançado

**Para Seu Cérebro**:
- Links profundos para notas
- Executar comandos via URL
- Integração com apps externos

**Setup**: Instalar → Configurar URIs customizados

---

### 14. **Smart Connections**
**O Que Faz**: Links automáticos entre notas relacionadas

**Para Seu Cérebro**:
- Conectar insights relacionados
- Descobrir patterns
- Navegação inteligente

**Setup**: Instalar → Configurar modelo de embedding

---

### 15. **Mind Map**
**O Que Faz**: Mapas mentais de notas

**Para Seu Cérebro**:
- Visualizar estratégias
- Conectar campanhas
- Brainstorming

**Setup**: Instalar → `Ctrl+P → Mind Map: Open current note`

---

### 16. **Supabase Sync** (ou similar)
**O Que Faz**: Sync com Supabase

**Para Seu Cérebro**:
- Notas ↔ Banco de dados
- Frontmatter como metadados
- Sync bidirecional

**Setup**: Instalar → Configurar conexão Supabase

**Alternativas**: LiveSync (CouchDB), Manual (Python scripts)

---

### 17. **Review**
**O Que Faz**: Revisão espaçada (flashcards)

**Para Seu Cérebro**:
- Revisar aprendizados
- Memorizar frameworks
- Treinar equipe

**Setup**: Instalar → Criar flashcards → Revisar diariamente

---

### 18. **Tasks**
**O Que Faz**: Gerenciamento de tarefas

**Para Seu Cérebro**:
- Ações pendentes de aprovação
- Checklist de campanhas
- Tasks por empresa

**Setup**: Instalar → Usar `- [ ]` em notas

---

### 19. **Recent Files**
**O Que Faz**: Lista de arquivos recentes

**Para Seu Cérebro**:
- Acesso rápido a insights recentes
- Histórico de navegação
- Notas mais usadas

**Setup**: Instalar → Aparece no sidebar

---

### 20. **Workspaces**
**O Que Faz**: Salvar layout de janelas

**Para Seu Cérebro**:
- Workspace por empresa
- Layouts customizados
- Troca rápida de contexto

**Setup**: Instalar → `Ctrl+P → Workspaces: Save workspace`

---

## 📊 PRIORIZAÇÃO POR FASE

### Fase 1: Essenciais (Instalar Agora, 2 horas)
```
1. Obsidian REST API
2. Dataview
3. Obsidian Copilot
4. Templater
5. QuickAdd
```

### Fase 2: Importantes (Esta Semana, 3 horas)
```
6. Webhook
7. Self-hosted LiveSync
8. Obsidian Git
9. Calendar
10. Execute Code
```

### Fase 3: Secundários (Próximo Mês, 5 horas)
```
11. Kanban
12. Excalidraw
13. Advanced URI
14. Smart Connections
15. Mind Map
```

### Fase 4: Nice to Have (Quando Precisar)
```
16. Supabase Sync
17. Review
18. Tasks
19. Recent Files
20. Workspaces
```

---

## 🚀 SETUP RÁPIDO (30 MINUTOS)

### Passo 1: Habilitar Community Plugins
```
Settings → Community Plugins → Turn on community plugins
```

### Passo 2: Instalar Top 5
```
Settings → Community Plugins → Browse

1. Buscar "REST API" → Install → Enable
2. Buscar "Dataview" → Install → Enable
3. Buscar "Copilot" → Install → Enable
4. Buscar "Templater" → Install → Enable
5. Buscar "QuickAdd" → Install → Enable
```

### Passo 3: Configurar REST API
```
Settings → Obsidian REST API
- Port: 27123
- Enable Authentication: Sim (recomendado)
- Allowed Origins: * (ou específico)
```

### Passo 4: Configurar Copilot (LLM Local)
```
Settings → Copilot
- Provider: Ollama
- API URL: http://localhost:11434
- Model: phi3:mini
```

### Passo 5: Testar
```bash
# Testar REST API
curl http://localhost:27123/api/vaults

# Testar Copilot
Ctrl+P → "Copilot: Chat"
Digitar: "Olá!"
```

---

## 💡 COMBINAÇÕES PODEROSAS

### 1. REST API + Dataview + Templater
```
Python cria nota → Template formata → Dataview exibe no dashboard
```

### 2. Copilot + QuickAdd
```
QuickAdd captura ideia → Copilot expande → Salva como insight
```

### 3. Webhook + Execute Code
```
Webhook recebe dado → Execute Code processa → Atualiza nota
```

### 4. Git + LiveSync
```
Git versiona → LiveSync sincroniza → Backup duplo
```

---

## 🏆 MINHAS RECOMENDAÇÕES PESSOAIS

### Para Começar HOJE (Não Pule Nenhum)

| Plugin | Por Que | Tempo de Setup |
| :----- | :------ | :------------- |
| **REST API** | Integração Python → Obsidian | 10 min |
| **Dataview** | Dashboards dinâmicos | 15 min |
| **Copilot** | IA local (seu caso) | 20 min |
| **Templater** | Templates automáticos | 15 min |
| **QuickAdd** | Captura rápida | 10 min |

**Total**: 70 minutos (~1 hora)

### Para Esta Semana

| Plugin | Por Que | Tempo |
| :----- | :------ | :---- |
| **Webhook** | Receber eventos do Python | 15 min |
| **LiveSync** | Backup automático | 20 min |
| **Git** | Versionamento | 15 min |
| **Calendar** | Timeline visual | 5 min |
| **Execute Code** | Scripts in-note | 15 min |

**Total**: 70 minutos (~1 hora)

---

## ⚠️ PLUGINS PARA EVITAR (Por Enquanto)

| Plugin | Por Que Evitar |
| :----- | :------------- |
| **Obsidian Sync** | Pago ($8/mês), LiveSync é grátis |
| **Text Generator** | Copilot faz o mesmo + chat |
| **AI Assistant** | Copilot é mais completo |
| **Multiple plugins de IA** | Escolha UM (Copilot) e use bem |

---

## 📋 CHECKLIST DE INSTALAÇÃO

### Hoje
- [ ] Habilitar Community Plugins
- [ ] Instalar REST API
- [ ] Instalar Dataview
- [ ] Instalar Copilot
- [ ] Instalar Templater
- [ ] Instalar QuickAdd
- [ ] Testar cada um

### Esta Semana
- [ ] Instalar Webhook
- [ ] Instalar LiveSync
- [ ] Instalar Git
- [ ] Instalar Calendar
- [ ] Instalar Execute Code
- [ ] Configurar integrações entre plugins

### Próximo Mês
- [ ] Instalar Kanban
- [ ] Instalar Excalidraw
- [ ] Instalar Advanced URI
- [ ] Instalar Smart Connections
- [ ] Instalar Mind Map

---

## 🔗 LINKS ÚTEIS

| Recurso | URL |
| :------ | :-- |
| **Obsidian Plugins** | https://obsidian.md/plugins |
| **Obsidian API** | https://docs.obsidian.md/Plugins |
| **Awesome Obsidian** | https://github.com/obsidianmd/awesome-obsidian |
| **Obsidian Forum** | https://forum.obsidian.md |

---

<div align="center">

**🔌 PLUGINS ESSENCIAIS DO OBSIDIAN**

*Top 5 críticos + 15 secundários = Cérebro de Marketing Completo*

**2 horas para setup básico • 1 semana para completo**

</div>
