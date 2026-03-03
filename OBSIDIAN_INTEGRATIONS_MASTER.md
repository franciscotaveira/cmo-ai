# 🔌 OBSIDIAN INTEGRATION MASTER DOCUMENT

> **Fonte**: PDF obs-app.pdf (Documentos)
> **Data**: 2026-02-25
> **Objetivo**: Mapear TODAS as integrações possíveis do Obsidian
> **Contexto**: Cérebro Adaptativo de Marketing

---

## 📊 RESUMO EXECUTIVO

O Obsidian é **muito mais que um app de notas** — é uma **plataforma extensível** com múltiplas camadas de integração:

```
┌─────────────────────────────────────────────────────────────────┐
│              CAMADAS DE INTEGRAÇÃO DO OBSIDIAN                  │
│                                                                 │
│  1. API INTERNA (Plugin Development)                            │
│  2. COMMUNITY PLUGINS (1000+ plugins prontos)                   │
│  3. LOCAL REST API (Acesso externo via HTTP)                    │
│  4. COMMAND LINE INTERFACE (CLI via scripts)                    │
│  5. URI SCHEME (obsidian:// links)                              │
│  6. FILE SYSTEM SYNC (Sync via pasta local)                     │
│  7. GIT INTEGRATION (Versionamento)                             │
│  8. WEBHOOKS (Via plugins de automação)                         │
│  9. DATABASE PLUGINS (Supabase, SQLite, etc.)                   │
│  10. AI/LLM INTEGRATIONS (GPT, Claude, local models)            │
│                                                                 │
│  TOTAL: 10+ camadas de integração                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1️⃣ API INTERNA (Plugin Development)

### O Que É

API oficial para criar plugins customizados em TypeScript.

### Documentação

- **URL**: https://docs.obsidian.md/Plugins
- **GitHub**: https://github.com/obsidianmd/obsidian-api-releases

### O Que Permite

```typescript
// 1. Acessar Vault (arquivos)
const vault = app.vault;
const file = vault.getFileByPath('Dashboard.md');
const content = await vault.read(file);
await vault.modify(file, newContent);
await vault.create('New Note.md', content);

// 2. Workspace (interface)
const workspace = app.workspace;
const leaf = workspace.getLeaf();
await leaf.openFile(file);
workspace.activeEditor;

// 3. Metadata (tags, links, frontmatter)
const metadata = app.metadataCache.getCache(file.path);
const tags = metadata.tags;
const links = metadata.links;
const frontmatter = metadata.frontmatter;

// 4. Commands (executar comandos)
app.commands.executeCommandById('editor:save');
app.commands.executeCommandById('insert-template');

// 5. Events (ouvir mudanças)
vault.on('create', (file) => console.log('File created', file));
vault.on('modify', (file) => console.log('File modified', file));
vault.on('delete', (file) => console.log('File deleted', file));

// 6. Settings (configurações do plugin)
const settings = await this.loadData();
await this.saveData(settings);

// 7. UI Components (criar interface)
new Notice('Message to user');
new Modal(app).open();

// 8. HTTP Requests (APIs externas)
fetch('https://api.example.com/data');
```

### Para Seu Cérebro de Marketing

```typescript
// Plugin "Marketing Brain"
export default class MarketingBrain extends Plugin {
    async onload() {
        // 1. Conectar ao Supabase
        this.supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
        
        // 2. Listener em tempo real
        this.supabase.channel('marketing')
            .on('postgres_changes', {...}, (payload) => {
                this.onDataChange(payload);
            });
        
        // 3. Comandos customizados
        this.addCommand({
            id: 'generate-insight',
            name: 'Generate Marketing Insight',
            callback: () => this.generateInsight()
        });
        
        // 4. View customizada (dashboard)
        this.registerView(
            'marketing-dashboard',
            (leaf) => new MarketingDashboardView(leaf)
        );
    }
    
    async onDataChange(payload: any) {
        // Atualizar notes automaticamente
        const file = this.app.vault.getFileByPath('Dashboard.md');
        const content = await this.app.vault.read(file);
        const updated = this.updateContent(content, payload);
        await this.app.vault.modify(file, updated);
    }
}
```

### Complexidade

| Nível | Tempo | Descrição |
| :---- | :---- | :-------- |
| **Plugin Básico** | 10-20h | 1-2 comandos simples |
| **Plugin Médio** | 40-60h | Views customizadas + API |
| **Plugin Complexo** | 100h+ | Multi-views + sync + API |

---

## 2️⃣ COMMUNITY PLUGINS (1000+ Prontos)

### O Que São

Plugins criados pela comunidade, instaláveis diretamente no Obsidian.

### Como Acessar

```
Settings → Community Plugins → Browse
```

### Plugins de Integração (Relevantes para Você)

| Plugin | Função | Relevância |
| :----- | :----- | :--------- |
| **Obsidian Git** | Sync com GitHub | 🟢 Alta (backup) |
| **Obsidian Sync** | Sync oficial (pago) | 🟡 Média |
| **Self-hosted LiveSync** | Sync via CouchDB | 🟢 Alta (grátis) |
| **Obsidian HTTP Request** | Fazer requisições HTTP | 🔴 ALTÍSSIMA |
| **Obsidian REST API** | Expor API REST local | 🔴 ALTÍSSIMA |
| **Templater** | Templates avançados | 🟢 Alta |
| **QuickAdd** | Captura rápida | 🟢 Alta |
| **Dataview** | Query banco de dados | 🔴 ALTÍSSIMA |
| **Obsidian AI** | Integração com IA | 🔴 ALTÍSSIMA |
| **Smart Connections** | Links automáticos | 🟢 Alta |
| **Text Generator** | Gerar texto com IA | 🟢 Alta |
| **Obsidian Copilot** | Chat com IA local | 🔴 ALTÍSSIMA |
| **Execute Code** | Rodar código (JS, Python) | 🔴 ALTÍSSIMA |
| **Advanced URI** | URI scheme avançado | 🟢 Alta |
| **Webhook** | Enviar/receive webhooks | 🔴 ALTÍSSIMA |
| **Supabase Sync** | Sync com Supabase | 🔴 ALTÍSSIMA |
| **Calendar** | Timeline de notas | 🟢 Alta |
| **Kanban** | Quadros Kanban | 🟢 Alta |
| **Excalidraw** | Diagramas | 🟢 Alta |

### Plugins CRÍTICOS para Seu Projeto

#### 1. **Obsidian REST API**

**O Que Faz**: Expõe uma API REST local para o Obsidian.

**Endpoints**:
```bash
GET    http://localhost:27123/api/vaults
GET    http://localhost:27123/api/vault/{id}/files
GET    http://localhost:27123/api/vault/{id}/files/{path}
POST   http://localhost:27123/api/vault/{id}/files/{path}
PUT    http://localhost:27123/api/vault/{id}/files/{path}
DELETE http://localhost:27123/api/vault/{id}/files/{path}
```

**Para Seu Cérebro**:
```python
# Python → Obsidian
import requests

def create_note(path, content):
    response = requests.post(
        'http://localhost:27123/api/vault/1/files/' + path,
        json={'content': content}
    )
    return response.json()

# Criar insight automático
create_note(
    'Insights/2026-02-25-Oportunidade.md',
    '# Oportunidade Detectada\n\n...'
)
```

**Setup**:
1. Instalar plugin "Obsidian REST API"
2. Configurar porta (default: 27123)
3. Habilitar autenticação (opcional)
4. Usar endpoints acima

---

#### 2. **Obsidian HTTP Request**

**O Que Faz**: Fazer requisições HTTP de dentro do Obsidian.

**Para Seu Cérebro**:
```javascript
// De dentro de uma nota ou script
const response = await fetch('http://localhost:8000/api/insights', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        tenant_id: 'salao-esposa',
        action: 'generate_insight'
    })
});

const insight = await response.json();
// Inserir insight na nota
```

**Setup**:
1. Instalar plugin "HTTP Request"
2. Criar "Request Template"
3. Usar em scripts ou commands

---

#### 3. **Dataview**

**O Que Faz**: Query SQL-like em notas Markdown.

**Para Seu Cérebro**:
```sql
-- Query em nota Markdown
```dataview
TABLE file.name as "Insight", file.mtime as "Atualizado", priority as "Prioridade"
FROM "Insights"
WHERE contains(tags, "#alerta") AND priority = "high"
SORT file.mtime DESC
LIMIT 10
```

**Resultado**: Tabela dinâmica atualizada automaticamente.

**Setup**:
1. Instalar plugin "Dataview"
2. Usar blocos ```dataview em notas
3. Query seu vault como banco de dados

---

#### 4. **Obsidian Copilot / AI**

**O Que Faz**: Chat com IA (local ou cloud) dentro do Obsidian.

**Para Seu Cérebro**:
```
Usuário: "Quais insights temos sobre CAC alto?"
Copilot: [Busca no vault + Supabase via RAG]
         "Encontrei 3 insights sobre CAC:
          1. [Insight A] - 2026-02-24
          2. [Insight B] - 2026-02-23
          3. [Insight C] - 2026-02-22
          
          Padrão: CAC subiu em campanhas com frequência > 4.0"
```

**Modelos Suportados**:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local (Ollama, LM Studio)
- Custom (via API)

**Setup**:
1. Instalar plugin "Copilot" ou "Obsidian AI"
2. Configurar API key (ou modelo local)
3. Usar Ctrl+P → "Copilot: Chat"

---

#### 5. **Execute Code**

**O Que Faz**: Rodar código (JavaScript, Python) dentro do Obsidian.

**Para Seu Cérebro**:
```python
```execute-code --language python
import requests

# Buscar dados do Supabase
response = requests.get('http://localhost:8000/api/metrics')
metrics = response.json()

# Gerar insight
print(f"CAC atual: R$ {metrics['cac']}")
print(f"Meta: R$ {metrics['cac_meta']}")

if metrics['cac'] > metrics['cac_meta'] * 1.3:
    print("🚨 ALERTA: CAC 30% acima da meta!")
```
```

**Setup**:
1. Instalar plugin "Execute Code"
2. Criar bloco de código
3. Rodar com botão "Run"

---

#### 6. **Webhook**

**O Que Faz**: Enviar e receber webhooks.

**Para Seu Cérebro**:
```yaml
# Webhook Receiver
Trigger: POST /webhook/new-insight
Action: Create note in /Insights/
Content: {{body.content}}
```

**Setup**:
1. Instalar plugin "Webhook"
2. Configurar endpoints
3. Mapear ações

---

#### 7. **Supabase Sync** (ou similar)

**O Que Faz**: Sincronizar notas com Supabase.

**Para Seu Cérebro**:
```
Nota Markdown ↔ Supabase (bidirecional)
```

**Setup**:
1. Instalar plugin "Supabase Sync" ou "Self-hosted LiveSync"
2. Configurar conexão
3. Mapear tabelas

---

## 3️⃣ LOCAL REST API (Plugins)

### Plugins que Exponham API

| Plugin | Porta | Endpoints |
| :----- | :---- | :-------- |
| **Obsidian REST API** | 27123 | CRUD de notas |
| **Obsidian Remote** | 8080 | Similar ao acima |
| **Obsidian Sync** | Varia | Sync remoto |

### Exemplo de Uso (Python → Obsidian)

```python
# engine/src/obsidian_client.py
import requests

class ObsidianClient:
    def __init__(self, base_url: str = "http://localhost:27123"):
        self.base_url = base_url
    
    def create_note(self, vault_id: str, path: str, content: str):
        """Cria nota via API REST"""
        response = requests.post(
            f"{self.base_url}/api/vault/{vault_id}/files/{path}",
            json={"content": content}
        )
        return response.json()
    
    def read_note(self, vault_id: str, path: str):
        """Lê nota via API REST"""
        response = requests.get(
            f"{self.base_url}/api/vault/{vault_id}/files/{path}"
        )
        return response.json()
    
    def update_note(self, vault_id: str, path: str, content: str):
        """Atualiza nota via API REST"""
        response = requests.put(
            f"{self.base_url}/api/vault/{vault_id}/files/{path}",
            json={"content": content}
        )
        return response.json()
    
    def delete_note(self, vault_id: str, path: str):
        """Deleta nota via API REST"""
        response = requests.delete(
            f"{self.base_url}/api/vault/{vault_id}/files/{path}"
        )
        return response.json()
    
    def list_notes(self, vault_id: str, folder: str = None):
        """Lista notas de uma pasta"""
        params = {"folder": folder} if folder else {}
        response = requests.get(
            f"{self.base_url}/api/vault/{vault_id}/files",
            params=params
        )
        return response.json()
```

---

## 4️⃣ COMMAND LINE INTERFACE (CLI)

### O Que É

Scripts que manipulam arquivos do vault diretamente.

### Exemplo (Python)

```python
# scripts/obsidian_cli.py
import os
from pathlib import Path

class ObsidianCLI:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path)
    
    def create_note(self, path: str, content: str):
        """Cria nota no vault"""
        file_path = self.vault / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path
    
    def read_note(self, path: str):
        """Lê nota do vault"""
        file_path = self.vault / path
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def update_note(self, path: str, content: str):
        """Atualiza nota"""
        return self.create_note(path, content)
    
    def search_notes(self, query: str):
        """Busca notas por conteúdo"""
        results = []
        
        for file in self.vault.rglob('*.md'):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                if query in content:
                    results.append(str(file.relative_to(self.vault)))
        
        return results
    
    def add_frontmatter(self, path: str, data: dict):
        """Adiciona frontmatter (metadata)"""
        content = self.read_note(path)
        
        frontmatter = "---\n"
        for key, value in data.items():
            frontmatter += f"{key}: {value}\n"
        frontmatter += "---\n\n"
        
        return self.update_note(path, frontmatter + content)
```

### Uso

```bash
python obsidian_cli.py create "Insights/teste.md" "# Insight\n\nConteúdo..."
python obsidian_cli.py read "Dashboard.md"
python obsidian_cli.py search "CAC alto"
```

---

## 5️⃣ URI SCHEME (obsidian://)

### O Que É

Links que abrem notas específicas no Obsidian.

### Formato

```
obsidian://open?vault=VAULT_NAME&file=FILE_PATH
obsidian://advanced-uri?vault=VAULT_NAME&file=FILE_PATH&line=LINE_NUMBER
```

### Casos de Uso

```python
# Gerar link para nota específica
def generate_note_link(vault_name: str, file_path: str):
    import urllib.parse
    
    params = urllib.parse.urlencode({
        'vault': vault_name,
        'file': file_path
    })
    
    return f"obsidian://open?{params}"

# Usar em notificações
link = generate_note_link('Marketing Brain', 'Insights/2026-02-25.md')
print(f"Clique para abrir: {link}")

# Em email/SMS
email_body = f"""
Novo insight gerado!

Clique para abrir no Obsidian:
{link}
"""
```

### Plugin: Advanced URI

Adiciona mais parâmetros:
- `line`: Linha específica
- `block`: Bloco específico
- `search`: Busca no vault
- `command`: Executar comando

---

## 6️⃣ FILE SYSTEM SYNC

### O Que É

Vault do Obsidian = pasta local no seu computador.

### Para Seu Cérebro

```python
# engine/src/obsidian_sync.py
class ObsidianFileSync:
    def __init__(self, vault_path: str):
        self.vault = Path(vault_path)
    
    def write_dashboard(self, tenant_id: str, metrics: list):
        """Escreve dashboard automático"""
        content = self._generate_markdown(metrics)
        
        filepath = self.vault / f"Dashboard_{tenant_id}.md"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def write_insight(self, insight: dict):
        """Escreve insight automático"""
        content = f"""# 💡 Insight: {insight['title']}

**Gerado em**: {insight['created_at']}
**Prioridade**: {insight['priority']}

## Contexto
{insight['context']}

## Análise
{insight['analysis']}

## Ação Sugerida
{insight['action']}
"""
        
        filepath = self.vault / f"Insights/{insight['slug']}.md"
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
```

### Vantagens

- ✅ Simples (só escrever arquivos)
- ✅ Zero dependências
- ✅ Funciona offline
- ✅ Sync via Obsidian Sync / Git / Dropbox

---

## 7️⃣ GIT INTEGRATION

### Plugin: Obsidian Git

**O Que Faz**: Versionamento de notas no Git.

**Para Seu Cérebro**:
```
Notas → Git Commit → GitHub/GitLab
       ↓
       Histórico completo de mudanças
       ↓
       Backup + Colaboração
```

**Setup**:
1. Instalar plugin "Obsidian Git"
2. Configurar repositório
3. Auto-commit (opcional)

### Python + Git

```python
# engine/src/git_sync.py
import git

class GitSync:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
    
    def commit_changes(self, message: str):
        """Commit automático de mudanças"""
        self.repo.git.add(all=True)
        self.repo.index.commit(message)
        self.repo.remote().push()
    
    def get_history(self, file_path: str):
        """Histórico de mudanças de um arquivo"""
        return list(self.repo.iter_paths(file_path))
```

---

## 8️⃣ WEBHOOKS (Via Plugins)

### Plugins de Webhook

| Plugin | Direção | Uso |
| :----- | :------ | :-- |
| **Webhook** | Enviar/Receber | Genérico |
| **HTTP Request** | Enviar | Chamadas HTTP |
| **Obsidian REST API** | Receber | API local |

### Exemplo: Receber Webhook

```yaml
# Configuração no plugin Webhook
Endpoint: POST /webhook/new-insight
Action: Create Note
Path: /Insights/{{body.slug}}.md
Content: |
  # {{body.title}}
  
  {{body.content}}
```

### Exemplo: Enviar Webhook (Python)

```python
# engine/src/webhook_sender.py
import requests

def send_to_obsidian(webhook_url: str, data: dict):
    """Envia webhook para Obsidian"""
    response = requests.post(webhook_url, json=data)
    return response.json()

# Usar: Quando insight gerado
insight = generate_insight()
send_to_obsidian(
    'http://localhost:27123/webhook/new-insight',
    {
        'title': insight['title'],
        'slug': insight['slug'],
        'content': insight['content']
    }
)
```

---

## 9️⃣ DATABASE PLUGINS

### Plugins de Banco de Dados

| Plugin | Banco | Função |
| :----- | :---- | :----- |
| **Supabase Sync** | Supabase | Sync bidirecional |
| **Self-hosted LiveSync** | CouchDB | Sync em tempo real |
| **Obsidian SQLite** | SQLite | Query SQL em notas |
| **Dataview** | "Vault" | Query tipo SQL |

### Para Seu Cérebro (Supabase)

```
┌─────────────────────────────────────────────────────────┐
│  SUPABASE ↔ OBSIDIAN (Bidirecional)                     │
│                                                         │
│  Supabase → Obsidian:                                   │
│  • Novos insights → Criar notas                         │
│  • Alertas → Criar notas de alerta                      │
│  • Dashboards → Atualizar notas                         │
│                                                         │
│  Obsidian → Supabase:                                   │
│  • Aprovações de ações → Webhook → API                  │
│  • Notas editadas → Atualizar banco                     │
│  • Tags/frontmatter → Metadados                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔟 AI/LLM INTEGRATIONS

### Plugins de IA

| Plugin | Modelos | Função |
| :----- | :------ | :----- |
| **Obsidian Copilot** | GPT, Claude, Local | Chat + RAG |
| **Obsidian AI** | OpenAI, Local | Busca semântica |
| **Text Generator** | OpenAI, Local | Gerar texto |
| **Smart Connections** | OpenAI, Local | Links automáticos |
| **AI Assistant** | Vários | Assistente geral |

### Para Seu Cérebro (LLM Local)

```
┌─────────────────────────────────────────────────────────┐
│  LLM LOCAL (Ollama) + OBSIDIAN                          │
│                                                         │
│  1. Usuário pergunta no Copilot                         │
│  2. Copilot busca no vault (RAG)                        │
│  3. Copilot busca no Supabase (via API)                 │
│  4. LLM gera resposta contextualizada                   │
│  5. Resposta aparece no chat                            │
└─────────────────────────────────────────────────────────┘
```

**Setup**:
1. Instalar Ollama (`ollama run phi3:mini`)
2. Instalar plugin "Copilot"
3. Configurar API URL: `http://localhost:11434`
4. Usar Ctrl+P → "Copilot: Chat"

---

## 📊 COMPARAÇÃO DE MÉTODOS

| Método | Complexidade | Flexibilidade | Ideal Para |
| :----- | :----------: | :-----------: | :--------- |
| **API Interna (Plugin)** | 🔴 Alta | 🟢 Alta | Plugin customizado |
| **Community Plugins** | 🟢 Baixa | 🟡 Média | Começar rápido |
| **REST API** | 🟢 Baixa | 🟡 Média | Integração externa |
| **CLI (Scripts)** | 🟡 Média | 🟢 Alta | Automações |
| **URI Scheme** | 🟢 Baixa | 🔴 Baixa | Links rápidos |
| **File System** | 🟢 Baixa | 🟡 Média | Sync simples |
| **Git** | 🟡 Média | 🟢 Alta | Versionamento |
| **Webhooks** | 🟡 Média | 🟢 Alta | Eventos em tempo real |
| **Database** | 🔴 Alta | 🟢 Alta | Sync estruturado |
| **AI/LLM** | 🟡 Média | 🟢 Alta | Chat + RAG |

---

## 🎯 RECOMENDAÇÃO PARA SEU CÉREBRO

### Arquitetura Híbrida (Melhor dos Mundos)

```
┌─────────────────────────────────────────────────────────┐
│  CÉREBRO DE MARKETING — Stack de Integração             │
│                                                         │
│  CAMADA 1: File System (Base)                           │
│  • Python escreve notas automaticamente                 │
│  • Simples, zero dependências                           │
│                                                         │
│  CAMADA 2: REST API (Interatividade)                    │
│  • Plugin "Obsidian REST API"                           │
│  • Python → Obsidian (criar/atualizar notas)            │
│  • Obsidian → Python (aprovações via webhook)           │
│                                                         │
│  CAMADA 3: Supabase Sync (Dados)                        │
│  • Plugin "Supabase Sync" ou similar                    │
│  • Notas ↔ Banco de dados                               │
│  • Frontmatter como metadados                           │
│                                                         │
│  CAMADA 4: AI/LLM (Inteligência)                        │
│  • Plugin "Copilot" + Ollama local                      │
│  • Chat com dados do vault + Supabase                   │
│  • RAG para contexto                                    │
│                                                         │
│  CAMADA 5: Dataview (Dashboards)                        │
│  • Plugin "Dataview"                                    │
│  • Queries em Markdown                                  │
│  • Dashboards dinâmicos                                 │
└─────────────────────────────────────────────────────────┘
```

### Setup Recomendado (Comece Agora)

```bash
# 1. Instalar plugins essenciais
# No Obsidian:
# - Community Plugins → Instalar:
#   • Obsidian REST API
#   • Dataview
#   • Copilot (ou Obsidian AI)
#   • Templater
#   • QuickAdd

# 2. Configurar REST API
# - Porta: 27123
# - Auth: Habilitar (opcional)

# 3. Testar integração Python
python -c "
import requests
response = requests.post(
    'http://localhost:27123/api/vault/1/files/Teste.md',
    json={'content': '# Teste\n\nFunciona!'}
)
print(response.json())
"
```

---

## 📋 ROADMAP DE IMPLEMENTAÇÃO

### Fase 1: File System (5 horas)
- [ ] Python escreve notas no vault
- [ ] Estrutura de pastas organizada
- [ ] Templates de insights

### Fase 2: REST API (10 horas)
- [ ] Instalar plugin REST API
- [ ] Python client para API
- [ ] Criar/atualizar notas via API

### Fase 3: Dataview (5 horas)
- [ ] Instalar plugin Dataview
- [ ] Criar dashboards dinâmicos
- [ ] Queries automáticas

### Fase 4: AI/LLM (10 horas)
- [ ] Instalar Copilot
- [ ] Configurar Ollama local
- [ ] Chat com dados do vault

### Fase 5: Supabase Sync (15 horas)
- [ ] Instalar plugin Supabase Sync
- [ ] Mapear tabelas ↔ notas
- [ ] Sync bidirecional

**Total**: 45 horas (~1 semana)

---

## 🏆 VEREDITO FINAL

### Obsidian é a Interface Perfeita para Seu Cérebro

```
┌─────────────────────────────────────────────────────────────────┐
│  POR QUE OBSIDIAN?                                              │
│                                                                 │
│  ✅ FLEXIBILIDADE: 10+ formas de integrar                       │
│  ✅ COMUNIDADE: 1000+ plugins prontos                           │
│  ✅ LOCAL-First: Seus dados, sua máquina                        │
│  ✅ EXTENSÍVEL: API oficial para plugins                        │
│  ✅ FUTURO-Proof: Arquivos Markdown (aberto)                    │
│  ✅ VISUAL: Interface limpa, mapas mentais                      │
│  ✅ OFFLINE: Funciona sem internet                              │
│                                                                 │
│  PARA SEU CÉREBRO DE MARKETING:                                 │
│  • Interface perfeita para usuários                             │
│  • Múltiplas formas de integrar                                 │
│  • Escala de 1 para 1000 empresas                               │
│  • Você controla os dados                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

<div align="center">

**🔌 OBSIDIAN INTEGRATION MASTER DOCUMENT**

*10+ camadas de integração • 1000+ plugins • Céu é o limite*

**45 horas para integração completa**

</div>
