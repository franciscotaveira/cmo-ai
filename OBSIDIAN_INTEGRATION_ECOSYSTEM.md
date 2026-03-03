# 🔌 OBSIDIAN INTEGRATION ECOSYSTEM — Possibilidades para o Cérebro de Marketing

> **Descoberta**: `obsidian-ai-tools` (solderneer/obsidian-ai-tools)
> **Data**: 2026-02-25
> **Objetivo**: Mapear todas as formas de integrar Obsidian com ferramentas externas
> **Contexto**: Cérebro de Marketing com IA + Supabase + Automações

---

## 🎯 DESCOBERTA PRINCIPAL

### `obsidian-ai-tools` — O Que É

**Repositório**: https://github.com/solderneer/obsidian-ai-tools

**Funcionalidade**: Plugin que integra **Supabase Vector + OpenAI** diretamente no Obsidian para:
- ✅ Busca semântica nos notes
- ✅ "Conversar" com seus notes
- ✅ RAG (Retrieval-Augmented Generation) local
- ✅ Endpoint público para compartilhar notes

**Stack**:
```
Obsidian Plugin (TypeScript)
         │
         ▼
   Supabase Vector (embeddings)
         │
         ▼
   OpenAI API (LLM + Embeddings)
```

---

## 🔌 FORMAS DE INTEGRAR OBSIDIAN

### 1. **Plugins da Comunidade** (Mais Fácil)

| Plugin | Funcionalidade | Relevância para Você |
| :----- | :------------- | :------------------- |
| **obsidian-ai-tools** | Supabase + OpenAI RAG | 🔴 **ALTA** — Já faz 80% do que precisa |
| **obsidian-smart-connections** | Link automático entre notes | 🟡 Média |
| **obsidian-text-generator** | Geração de texto com IA | 🟡 Média |
| **obsidian-copilot** | Chat com IA nos notes | 🟡 Média |
| **dataview** | Query SQL-like em Markdown | 🔴 **ALTA** — Para dashboards |
| **templater** | Templates dinâmicos | 🟢 Baixa |
| **quickadd** | Automações rápidas | 🟢 Baixa |

**Vantagem**: Instala em 2 cliques, zero código  
**Desvantagem**: Limitado ao que o plugin oferece

---

### 2. **Plugin Customizado** (Seu Caso)

**Arquitetura do `obsidian-ai-tools`**:

```typescript
// src/main.ts (Estrutura simplificada)
import { Plugin } from 'obsidian';
import { SupabaseClient } from '@supabase/supabase-js';
import { Configuration, OpenAIApi } from 'openai';

export default class ObsidianAI extends Plugin {
    supabase: SupabaseClient;
    openai: OpenAIApi;
    
    async onload() {
        // 1. Carregar configurações
        const settings = await this.loadData();
        
        // 2. Inicializar clientes
        this.supabase = new SupabaseClient(
            settings.supabaseUrl,
            settings.supabaseKey
        );
        this.openai = new OpenAIApi(
            new Configuration({ apiKey: settings.openaiKey })
        );
        
        // 3. Registrar comandos
        this.addCommand({
            id: 'ai-search',
            name: 'AI Search',
            callback: () => this.aiSearch()
        });
        
        // 4. Indexar notes automaticamente
        this.registerEvent(
            this.app.vault.on('modify', (file) => {
                this.indexNote(file);
            })
        );
    }
    
    async indexNote(file: TFile) {
        // 1. Ler conteúdo do note
        const content = await this.app.vault.read(file);
        
        // 2. Gerar embedding com OpenAI
        const embedding = await this.openai.createEmbedding({
            model: 'text-embedding-ada-002',
            input: content
        });
        
        // 3. Salvar no Supabase Vector
        await this.supabase
            .from('document')
            .insert({
                file_path: file.path,
                content: content,
                embedding: embedding.data.data[0].embedding
            });
    }
    
    async aiSearch(query: string) {
        // 1. Gerar embedding da query
        const embedding = await this.openai.createEmbedding({
            model: 'text-embedding-ada-002',
            input: query
        });
        
        // 2. Busca semântica no Supabase
        const { data } = await this.supabase.rpc('match_documents', {
            query_embedding: embedding.data.data[0].embedding,
            match_threshold: 0.7
        });
        
        // 3. Mostrar resultados
        this.showResults(data);
    }
}
```

**Para Seu Caso (Cérebro de Marketing)**:

```typescript
// src/marketing-brain.ts
export default class MarketingBrain extends Plugin {
    supabase: SupabaseClient;
    decisionEngine: DecisionEngine;
    
    async onload() {
        // 1. Conectar ao Supabase do MD-OS
        this.supabase = new SupabaseClient(
            SUPABASE_URL,
            SUPABASE_KEY
        );
        
        // 2. Registrar comandos
        this.addCommand({
            id: 'generate-insight',
            name: 'Generate Marketing Insight',
            callback: () => this.generateInsight()
        });
        
        this.addCommand({
            id: 'trigger-automation',
            name: 'Trigger Automation',
            callback: () => this.triggerAutomation()
        });
        
        // 3. Listener para atualizações automáticas
        this.supabase
            .channel('marketing-changes')
            .on(
                'postgres_changes',
                {
                    event: '*',
                    schema: 'public',
                    table: 'anomaly_alerts'
                },
                (payload) => {
                    this.onNewAnomaly(payload.new);
                }
            )
            .subscribe();
    }
    
    async generateInsight() {
        // 1. Buscar dados do tenant atual
        const tenant = this.getCurrentTenant();
        
        // 2. Chamar Decision Engine
        const insight = await this.decisionEngine.generateInsight(tenant);
        
        // 3. Criar note automático
        const file = await this.app.vault.create(
            `Insights/${tenant.slug}-${Date.now()}.md`,
            this.formatInsight(insight)
        );
        
        // 4. Ativar note
        this.app.workspace.openLinkText(file.path, '');
    }
    
    async onNewAnomaly(anomaly: AnomalyAlert) {
        // 1. Criar note de alerta
        const alertNote = await this.app.vault.create(
            `Alertas/ALERT-${anomaly.metric_key}-${Date.now()}.md`,
            this.formatAlert(anomaly)
        );
        
        // 2. Notificar usuário
        this.showNotification(`🚨 Anomalia detectada: ${anomaly.metric_key}`);
        
        // 3. Sugerir ação
        const action = await this.decisionEngine.decideAction(anomaly);
        this.showActionSuggestion(action);
    }
}
```

**Vantagem**: Controle total, integra exatamente como quer  
**Desvantagem**: Requer TypeScript + conhecimento do Obsidian API

---

### 3. **Obsidian API** (Programática)

**O Que É Possível**:

```typescript
// A API do Obsidian permite:

// 1. Ler/Escrever notes
const file = app.vault.getFileByPath('Dashboard.md');
const content = await app.vault.read(file);
await app.vault.modify(file, newContent);

// 2. Criar/deletar notes
const newFile = await app.vault.create('Notes/Insight.md', content);
await app.vault.delete(newFile);

// 3. Abrir notes
const leaf = app.workspace.getLeaf();
await leaf.openFile(file);

// 4. Executar comandos
app.commands.executeCommandById('editor:save');

// 5. Registrar eventos
app.vault.on('create', (file) => console.log('File created:', file));
app.vault.on('modify', (file) => console.log('File modified:', file));
app.vault.on('delete', (file) => console.log('File deleted:', file));

// 6. Acessar metadata
const cache = app.metadataCache.getCache(file.path);
const tags = cache.tags;
const links = cache.links;

// 7. Query no Dataview (se plugin instalado)
const dv = app.plugins.plugins.dataview.api;
const results = await dv.query(`
    TABLE file.name, file.mtime
    FROM "Dashboard"
    WHERE contains(tags, "#alert")
    SORT file.mtime DESC
`);
```

**Para Seu Cérebro de Marketing**:

```typescript
// Plugin que atualiza dashboard automaticamente
this.supabase
    .channel('metrics-updates')
    .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'business_metrics'
    }, async (payload) => {
        // 1. Atualizar dashboard
        const dashboard = app.vault.getFileByPath('Dashboard.md');
        const content = await app.vault.read(dashboard);
        
        // 2. Inserir nova métrica
        const newContent = this.insertMetric(content, payload.new);
        
        // 3. Salvar
        await app.vault.modify(dashboard, newContent);
    })
    .subscribe();
```

**Vantagem**: Acesso total ao Obsidian  
**Desvantagem**: Curva de aprendizado

---

### 4. **Local REST API** (Plugin `obsidian-local-rest-api`)

**Repositório**: https://github.com/AdamCav/obsidian-local-rest-api

**Funcionalidade**: Expõe uma API REST local para o Obsidian.

**Setup**:
```bash
# Instalar plugin
# Configurar porta (default: 27123)

# API Endpoints:
GET    http://localhost:27123/api/vaults          # Listar vaults
GET    http://localhost:27123/api/vault/{id}/files  # Listar arquivos
GET    http://localhost:27123/api/vault/{id}/files/{path}  # Ler arquivo
POST   http://localhost:27123/api/vault/{id}/files/{path}  # Criar arquivo
PUT    http://localhost:27123/api/vault/{id}/files/{path}  # Atualizar arquivo
DELETE http://localhost:27123/api/vault/{id}/files/{path}  # Deletar arquivo
```

**Para Seu Cérebro**:

```python
# engine/src/obsidian_api.py
import requests

class ObsidianAPI:
    def __init__(self, base_url: str = "http://localhost:27123"):
        self.base_url = base_url
    
    def create_note(self, vault_id: str, path: str, content: str):
        """Cria note via API REST"""
        response = requests.post(
            f"{self.base_url}/api/vault/{vault_id}/files/{path}",
            json={"content": content}
        )
        return response.json()
    
    def update_note(self, vault_id: str, path: str, content: str):
        """Atualiza note via API REST"""
        response = requests.put(
            f"{self.base_url}/api/vault/{vault_id}/files/{path}",
            json={"content": content}
        )
        return response.json()
    
    def write_insight(self, insight: dict):
        """Escreve insight automaticamente"""
        path = f"Insights/{insight['tenant_slug']}-{insight['id']}.md"
        content = self._format_insight(insight)
        
        return self.create_note("marketing-brain", path, content)
```

**Vantagem**: Integra de qualquer linguagem (Python, Node, etc.)  
**Desvantagem**: API local (não funciona remoto sem tunnel)

---

### 5. **Folder Sync + Watcher** (Sua Abordagem Atual)

**Como Já Está no MD-OS**:

```python
# engine/src/obsidian_bridge.py
class ObsidianBridge:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = obsidian_path
    
    def write_dashboard(self, tenant_id: str, metrics: list):
        """Escreve dashboard via filesystem"""
        content = self._generate_markdown(metrics)
        
        filepath = os.path.join(
            self.obsidian_path,
            f"Dashboard_{tenant_id}.md"
        )
        
        with open(filepath, 'w') as f:
            f.write(content)
```

**Vantagem**: Simples, zero dependências  
**Desvantagem**: Não tem interatividade (só escreve)

---

## 🎯 COMPARAÇÃO DE ABORDAGENS

| Abordagem | Complexidade | Flexibilidade | Ideal Para |
| :-------- | :----------: | :-----------: | :--------- |
| **Plugins Comunidade** | 🟢 Baixa | 🟡 Média | Começar rápido |
| **Plugin Customizado** | 🔴 Alta | 🟢 Alta | Controle total |
| **Obsidian API** | 🟡 Média | 🟢 Alta | Automações internas |
| **Local REST API** | 🟢 Baixa | 🟡 Média | Integração externa |
| **Folder Sync** | 🟢 Baixa | 🔴 Baixa | Dashboards estáticos |

---

## 🚀 RECOMENDAÇÃO PARA SEU CASO

### Estratégia Híbrida (Melhor dos Dois Mundos)

```
┌─────────────────────────────────────────────────────────┐
│          CÉREBRO DE MARKETING COM IA                    │
│                                                         │
│  ┌───────────────────┐         ┌───────────────────┐   │
│  │  MD-OS v4.0       │         │  Obsidian Plugin  │   │
│  │  (Python/Docker)  │◄───────►│  (TypeScript)     │   │
│  │                   │         │                   │   │
│  │ - Supabase        │         │ - UI Interativa   │   │
│  │ - IA RAG          │         │ - Comandos        │   │
│  │ - Automações      │         │ - Notificações    │   │
│  └───────────────────┘         └───────────────────┘   │
│           │                            │                │
│           └────────────┬───────────────┘                │
│                        │                                │
│                        ▼                                │
│              Supabase (Real-time)                       │
│              - business_metrics                         │
│              - anomaly_alerts                           │
│              - automation_queue                         │
│              - strategic_insights                       │
└─────────────────────────────────────────────────────────┘
```

### Fase 1: Começar com Plugins Existentes (1 semana)

**Plugins para Instalar**:

1. **obsidian-ai-tools** (ou similar)
   - Já tem Supabase + OpenAI
   - Busca semântica nos insights
   - RAG sobre seus notes

2. **dataview**
   - Query dados do Supabase (via plugin `obsidian-supabase`)
   - Dashboards dinâmicos em Markdown

3. **templater**
   - Templates automáticos para insights
   - Templates de alertas

**Setup**:
```bash
# No Obsidian:
Settings > Community Plugins > Browse

1. Buscar "AI Tools" → Instalar
2. Buscar "Dataview" → Instalar
3. Buscar "Templater" → Instalar

# Configurar Supabase em cada plugin
```

---

### Fase 2: Plugin Customizado Simplificado (2-3 semanas)

**Criar Plugin "Marketing Brain"**:

```bash
# 1. Clonar template
git clone https://github.com/obsidianmd/obsidian-sample-plugin.git marketing-brain
cd marketing-brain

# 2. Instalar dependências
npm install
npm install @supabase/supabase-js openai

# 3. Editar src/main.ts (código acima)

# 4. Build
npm run build

# 5. Copiar para vault
cp main.js manifest.json styles.css /path/to/vault/.obsidian/plugins/marketing-brain/

# 6. Ativar no Obsidian
```

**Funcionalidades do Plugin**:

```typescript
// Comandos que terá:
Cmd+P → "Marketing Brain: Generate Insight"
Cmd+P → "Marketing Brain: Trigger Automation"
Cmd+P → "Marketing Brain: View Anomalies"
Cmd+P → "Marketing Brain: Executive Report"

// Notificações automáticas:
- Nova anomalia detectada → Notificação + Note criado
- Insight gerado → Note criado
- Automação completada → Relatório no note
```

---

### Fase 3: Integração Total (4-6 semanas)

**Arquitetura Final**:

```
┌─────────────────────────────────────────────────────────┐
│                    FLUXO COMPLETO                       │
│                                                         │
│  1. DADO ENTRA (CSV/API)                                │
│     └─> Supabase (business_metrics)                     │
│                                                         │
│  2. IA ANALISA (Python Engine)                          │
│     ├─> RAG (knowledge_base)                            │
│     └─> Z-score (anomaly_alerts)                        │
│                                                         │
│  3. DECISION ENGINE DECIDE                              │
│     └─> automation_queue                                │
│                                                         │
│  4. AUTOMAÇÃO DISPARA                                   │
│     ├─> WhatsApp (Evolution API)                        │
│     ├─> Meta Ads (API)                                  │
│     └─> Obsidian (Plugin) ← AQUI                        │
│                                                         │
│  5. OBSIDIAN ATUALIZA                                   │
│     ├─> Dashboard automático                            │
│     ├─> Insight note criado                             │
│     ├─> Alerta note criado                              │
│     └─> Relatório executivo                             │
│                                                         │
│  6. USUÁRIO INTERAGE                                    │
│     ├─> Cmd+P → "Generate Insight"                      │
│     ├─> Cmd+P → "View Anomalies"                        │
│     └─> Clica em link → Navega entre notes              │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 EXEMPLO PRÁTICO: Insight Automático

### Código Completo (Plugin + Python)

**Python (Decision Engine)**:
```python
# engine/src/decision_engine.py
async def generate_and_publish_insight(self, tenant_id: str):
    # 1. Gerar insight
    insight = await self.ai.generate_insight(tenant_id)
    
    # 2. Salvar no Supabase
    insight_id = self.db.insert_insight(insight)
    
    # 3. Publicar no Obsidian (via Supabase Realtime)
    await self.supabase.from_('obsidian_events').insert({
        'event_type': 'new_insight',
        'payload': insight,
        'created_at': datetime.now()
    })
```

**TypeScript (Plugin Obsidian)**:
```typescript
// src/main.ts
export default class MarketingBrain extends Plugin {
    async onload() {
        // Listener para eventos do Supabase
        this.supabase
            .channel('obsidian-events')
            .on('postgres_changes', {
                event: 'INSERT',
                schema: 'public',
                table: 'obsidian_events'
            }, async (payload) => {
                await this.handleEvent(payload.new);
            })
            .subscribe();
    }
    
    async handleEvent(event: ObsidianEvent) {
        if (event.event_type === 'new_insight') {
            // Criar note do insight
            const file = await this.app.vault.create(
                `Insights/${event.payload.tenant_slug}-${Date.now()}.md`,
                this.formatInsight(event.payload)
            );
            
            // Abrir note
            const leaf = this.app.workspace.getLeaf();
            await leaf.openFile(file);
            
            // Notificar
            this.showNotification(`💡 Insight gerado: ${event.payload.tenant_name}`);
        }
    }
}
```

---

## 🏆 VEREDITO FINAL

### Sim, Obsidian Tem API Poderosa

**O Que Você Pode Fazer**:

| Funcionalidade | Possível? | Complexidade |
| :------------- | :-------: | :----------: |
| **Ler dados do Supabase** | ✅ Sim | 🟢 Baixa |
| **Escrever notes automáticos** | ✅ Sim | 🟢 Baixa |
| **Notificações em tempo real** | ✅ Sim | 🟡 Média |
| **Comandos customizados (Cmd+P)** | ✅ Sim | 🟡 Média |
| **Busca semântica (RAG)** | ✅ Sim | 🟡 Média |
| **Integrar com WhatsApp/Ads** | ✅ Sim | 🔴 Alta |
| **Dashboard interativo** | ✅ Sim | 🟡 Média |
| **Plugin publicado na comunidade** | ✅ Sim | 🔴 Alta |

### Recomendação

**Curto Prazo (1 semana)**:
```bash
# Instalar plugins existentes
- obsidian-ai-tools (já tem Supabase + OpenAI)
- dataview (dashboards dinâmicos)
- templater (templates automáticos)
```

**Médio Prazo (2-3 semanas)**:
```bash
# Criar plugin customizado "Marketing Brain"
- Comandos: Generate Insight, Trigger Automation
- Notificações: Nova anomalia, Insight gerado
- Integração: Supabase Realtime
```

**Longo Prazo (4-6 semanas)**:
```bash
# Publicar plugin na comunidade
- open source
- outros usuários podem usar
- feedback da comunidade
```

---

## 📁 PRÓXIMOS PASSOS

### 1. Explorar `obsidian-ai-tools`
```bash
# Clonar repositório
git clone https://github.com/solderneer/obsidian-ai-tools.git

# Estudar código
cd obsidian-ai-tools
code .

# Foco em:
- src/main.ts (como conecta Supabase)
- supabase/ (migrations do banco)
```

### 2. Testar no Seu Vault
```bash
# No Obsidian:
Settings > Community Plugins > Browse
Buscar "AI Tools" → Instalar

# Configurar:
Settings > Obsidian AI
- Supabase URL: https://xxx.supabase.co
- Supabase Key: sua-chave
- OpenAI Key: sk-proj-xxx
```

### 3. Decidir Abordagem
- [ ] Usar plugins existentes (rápido)
- [ ] Criar plugin customizado (controle total)
- [ ] Híbrido (recomendado)

---

<div align="center">

**🔌 OBSIDIAN INTEGRATION ECOSYSTEM**

*Sim, Obsidian tem API poderosa e você pode plugar qualquer ferramenta!*

</div>
