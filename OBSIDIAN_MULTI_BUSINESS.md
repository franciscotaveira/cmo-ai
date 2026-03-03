# 🌌 OBSIDIAN MULTI-BUSINESS ARCHITECTURE — Federação de Negócios

> **Visão**: Transformar vault monolítico em Federação de Negócios
> **Método**: Agent Flow HIVE OS v4.0
> **Data**: 2026-02-25
> **Status**: Especificação + Implementação

---

## 🎯 VISÃO ESTRATÉGICA

### O Que Estamos Criando

```
┌─────────────────────────────────────────────────────────────────┐
│  OBSIDIAN NÃO É APENAS NOTAS — É EXOCÓRTEX DE GESTÃO            │
│                                                                 │
│  DE: Vault Monolítico (tudo misturado)                          │
│  PARA: Federação de Negócios (isolado mas conectado)            │
│                                                                 │
│  ANALOGIA:                                                      │
│  • Cada negócio = Uma galáxia                                   │
│  • Obsidian = O universo que conecta todas                      │
│  • Você = O comandante da frota                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ ARQUITETURA DE PASTAS

### Nova Estrutura Física

```
ObsidianVault/
│
├── 📁 00 - COMANDO CENTRAL (Visão Executiva Global)
│   ├── 📊 Dashboard Master.md
│   │   • Soma de todos os ROAS
│   │   • CAC total consolidado
│   │   • Faturamento global
│   │   • Health check de todos os negócios
│   │
│   ├── ⚠️ Alertas Críticos.md
│   │   • Somente o que exige ação imediata
│   │   • Agregado de todos os negócios
│   │   • Triagem automática por severidade
│   │
│   └── 🎯 Metas Globais.md
│       • Objetivos do portfólio
│       • Alocação de recursos entre negócios
│
├── 📁 01 - UNIDADES DE NEGÓCIO
│   │
│   ├── 📁 01 - Salão Lux Beauty
│   │   ├── 🏢 Perfil & Metas.md
│   │   │   • Missão do negócio
│   │   │   • Metas específicas (LTV, Retenção)
│   │   │   • Público-alvo
│   │   │
│   │   ├── 📊 Dashboard Local.md
│   │   │   • KPIs específicos do salão
│   │   │   • Atualizado automaticamente pelo mkt_engine
│   │   │   • Tags: #mdcc/unidade #mdcc/salao
│   │   │
│   │   ├── 🧪 Campanhas/
│   │   │   ├── 2024-01-Campanha-Verão.md
│   │   │   ├── 2024-02-Dia-das-Maes.md
│   │   │   └── ...
│   │   │
│   │   └── 🧠 Base de Conhecimento/
│   │       ├── O-que-funciona.md
│   │       ├── Copy-vencedoras.md
│   │       └── RAG local (específico deste salão)
│   │
│   ├── 📁 02 - Franquia Chapecó
│   │   ├── 🏢 Perfil & Metas.md
│   │   ├── 📊 Dashboard Local.md
│   │   ├── 🧪 Campanhas/
│   │   └── 🧠 Base de Conhecimento/
│   │
│   ├── 📁 03 - Franquia Oeste
│   │   └── ... (mesma estrutura)
│   │
│   └── 📁 [N-ésimo Negócio]
│       └── ... (estrutura replicável)
│
├── 📁 02 - ESTRATÉGIAS TRANSVERSAIS
│   ├── 📋 Estratégias que Funcionam em Múltiplos Negócios
│   │   • Influenciadores (Salão → Franquias)
│   │   • Fidelização (aplicável em todos)
│   │   • Copy templates
│   │
│   └── 🔗 Mapa de Conhecimento Compartilhado
│       • Estratégias conectando múltiplos negócios
│       • Lições aprendidas transversais
│
└── 📁 99 - INFRA (Templates, Scripts, Configs)
    ├── 📄 Templates/
    │   ├── template-dashboard-local.md
    │   ├── template-campanha.md
    │   ├── template-perfil-negocio.md
    │   └── ...
    │
    ├── 📄 Scripts/
    │   ├── sync-global-dashboard.py
    │   ├── aggregate-alerts.py
    │   └── ...
    │
    └── 📄 Configs/
        ├── tags-mapping.json
        └── business-colors.json
```

---

## 🔄 AGENT FLOW — IMPLEMENTAÇÃO

### 🔥 FASE 1: BOOT SEQUENCE

#### 1.1 Atlas Soberano (Visão Estratégica)

**Premissa Central**:
> "Obsidian deve funcionar como um exocórtex que permite gerenciar múltiplos negócios simultaneamente, com isolamento físico mas conexão lógica."

**Objetivos**:
1. Isolar dados de cada negócio (físico)
2. Consolidar visão global (lógico)
3. Permitir cross-pollination de estratégias
4. Manter contexto específico por negócio

#### 1.2 CODEBASE.md (Realidade Técnica)

**Stack Atual**:
```
• mkt_engine (Python) → Já identifica tenant por pasta
• Supabase → Já tem RLS por tenant_id
• Obsidian → Atualmente: vault monolítico
• Dataview → Pode agregar por tags
```

**O Que Mudar**:
```
• Estrutura de pastas do Obsidian
• mkt_engine: salvar notas no local correto
• Dataview: queries por tags de negócio
• Graph View: mapear conexões entre negócios
```

#### 1.3 .agent/ARCHITECTURE.md (Mapeamento)

**Recursos Disponíveis**:
```
✅ mkt_engine já identifica tenant
✅ Supabase já isola por tenant_id
✅ Dataview pode agregar por tags
✅ Obsidian Graph View para conexões
✅ Templates para padronização
```

---

### 🧠 FASE 2: REQUEST CLASSIFICATION

#### Tipo de Demanda

| Categoria | Classificação |
| :-------- | :------------ |
| **Tipo** | Arquitetura de Informação + Implementação |
| **Complexidade** | Alta (múltiplos negócios + integração) |
| **Agentes** | `orchestrator` + `backend-specialist` + `obsidian-skill` |
| **Satélites** | @docker-skill, @supabase-skill, @dataview-skill |

#### Roteamento

```
USER REQUEST: "Criar arquitetura multi-business no Obsidian"
         │
         ▼
┌─────────────────────────────────────────┐
│  CLASSIFICAÇÃO                          │
│  • Arquitetura de Informação            │
│  • Modificação do mkt_engine            │
│  • Configuração do Dataview             │
│  • Templates padronizados               │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  AGENTES ATIVADOS                       │
│  • orchestrator (coordenação)           │
│  • backend-specialist (mkt_engine)      │
│  • obsidian-skill (vault structure)     │
│  • dataview-skill (agregação)           │
└─────────────────────────────────────────┘
```

---

### 🛡️ FASE 3: SOCRATIC GATE V2

#### 3.1 Premissa Central

**Pergunta**: Qual premissa central estou assumindo?

**Resposta**:
- Premissa: Cada negócio deve ter isolamento físico (pastas separadas)
- Suposição: mkt_engine pode identificar negócio pela pasta do Drive
- Expectativa: Dataview pode agregar dados por tags

**Validação**: ✅ Verificado — mkt_engine já faz identificação por pasta

---

#### 3.2 Diferença Crítica

**Pergunta**: Onde o problema pode ser diferente do que parece?

**Resposta**:
- **Aparente**: Só reorganizar pastas do Obsidian
- **Real**: Precisa de:
  - Modificação do mkt_engine (salvar no local correto)
  - Sistema de tags consistente
  - Templates padronizados
  - Dashboard global com Dataview

**Mitigação**: Implementar em fases, validar após cada uma

---

#### 3.3 Simplicidade

**Pergunta**: Existe uma solução mais simples?

**Resposta**:
- **Solução Complexa**: Reescrever mkt_engine inteiro
- **Solução Simples**: 
  1. Adicionar mapeamento pasta → caminho no Obsidian
  2. Usar tags do Dataview para agregação
  3. Templates para padronização

**Decisão**: Começar simples, evoluir se necessário

---

#### 3.4 Pior Cenário

**Pergunta**: Qual o pior cenário de falha?

**Resposta**:

| Cenário | Impacto | Mitigação |
| :------ | :------ | :-------- |
| mkt_engine salva no lugar errado | Dados misturados | Teste com tenant de teste primeiro |
| Dataview não agrega | Dashboard global não funciona | Fallback: script Python de agregação |
| Tags inconsistentes | Agregação falha | Sistema de tags obrigatórias nos templates |
| Performance do Graph View | Vault lento com muitos negócios | Limitar conexões, usar filtros |

---

### ⚙️ FASE 4: TASK EXECUTION

#### Plano de Implementação

```
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: Estrutura de Pastas (30 min)                           │
│  • Criar estrutura 00-COMANDO, 01-UNIDADES, 99-INFRA            │
│  • Configurar tags mapping                                      │
│                                                                 │
│  FASE 2: mkt_engine Update (2 horas)                            │
│  • Mapear tenant_slug → caminho no Obsidian                     │
│  • Salvar notas no local correto                                │
│  • Adicionar tags automáticas                                   │
│                                                                 │
│  FASE 3: Templates (1 hora)                                     │
│  • Criar templates padronizados                                 │
│  • Incluir tags obrigatórias                                    │
│                                                                 │
│  FASE 4: Dashboard Global (1 hora)                              │
│  • Configurar Dataview para agregação                           │
│  • Criar Dashboard Master.md                                    │
│                                                                 │
│  FASE 5: Graph View (30 min)                                    │
│  • Configurar cores por negócio                                 │
│  • Mapear conexões de estratégias                               │
│                                                                 │
│  FASE 6: Validação (1 hora)                                     │
│  • Testar com CSV real de cada negócio                          │
│  • Validar isolamento e agregação                               │
└─────────────────────────────────────────────────────────────────┘

Total: ~6 horas
```

---

### 📁 IMPLEMENTAÇÃO PRÁTICA

#### FASE 1: Estrutura de Pastas

**Script de Criação (PowerShell)**:

```powershell
# Criar estrutura de pastas no Obsidian Vault
$obsidianPath = "C:\Users\Marketing\Documents\ObsidianVault"

# 00 - COMANDO CENTRAL
New-Item -ItemType Directory -Path "$obsidianPath\00 - COMANDO CENTRAL" -Force
New-Item -ItemType File -Path "$obsidianPath\00 - COMANDO CENTRAL\Dashboard Master.md" -Force
New-Item -ItemType File -Path "$obsidianPath\00 - COMANDO CENTRAL\Alertas Críticos.md" -Force

# 01 - UNIDADES DE NEGÓCIO
New-Item -ItemType Directory -Path "$obsidianPath\01 - UNIDADES DE NEGÓCIO" -Force

# Exemplo: Salão Lux Beauty
$salaoPath = "$obsidianPath\01 - UNIDADES DE NEGÓCIO\01 - Salão Lux Beauty"
New-Item -ItemType Directory -Path $salaoPath -Force
New-Item -ItemType Directory -Path "$salaoPath\Campanhas" -Force
New-Item -ItemType Directory -Path "$salaoPath\Base de Conhecimento" -Force
New-Item -ItemType File -Path "$salaoPath\Perfil & Metas.md" -Force
New-Item -ItemType File -Path "$salaoPath\Dashboard Local.md" -Force

# Exemplo: Franquia Chapecó
$franquiaPath = "$obsidianPath\01 - UNIDADES DE NEGÓCIO\02 - Franquia Chapecó"
New-Item -ItemType Directory -Path $franquiaPath -Force
New-Item -ItemType Directory -Path "$franquiaPath\Campanhas" -Force
New-Item -ItemType Directory -Path "$franquiaPath\Base de Conhecimento" -Force
New-Item -ItemType File -Path "$franquiaPath\Perfil & Metas.md" -Force
New-Item -ItemType File -Path "$franquiaPath\Dashboard Local.md" -Force

# 02 - ESTRATÉGIAS TRANSVERSAIS
New-Item -ItemType Directory -Path "$obsidianPath\02 - ESTRATÉGIAS TRANSVERSAIS" -Force

# 99 - INFRA
New-Item -ItemType Directory -Path "$obsidianPath\99 - INFRA\Templates" -Force
New-Item -ItemType Directory -Path "$obsidianPath\99 - INFRA\Scripts" -Force
New-Item -ItemType Directory -Path "$obsidianPath\99 - INFRA\Configs" -Force

Write-Host "✅ Estrutura de pastas criada com sucesso!"
```

---

#### FASE 2: mkt_engine Update

**Arquivo**: `mkt/engine/src/obsidian.py`

**Adicionar**: Mapeamento tenant → caminho no Obsidian

```python
# obsidian.py

class ObsidianBridge:
    """Ponte de integração com o Obsidian — Multi-Business"""
    
    def __init__(self, obsidian_path: str, db: Optional[DatabaseHandler] = None):
        self.obsidian_path = obsidian_path
        self.db = db or DatabaseHandler()
        
        # MAPEAMENTO: tenant_slug → caminho no Obsidian
        self.tenant_path_mapping = {
            'diretoria': '00 - COMANDO CENTRAL',
            'salao-esposa': '01 - UNIDADES DE NEGÓCIO/01 - Salão Lux Beauty',
            'franquia-chapeco': '01 - UNIDADES DE NEGÓCIO/02 - Franquia Chapecó',
            'franquia-oeste': '01 - UNIDADES DE NEGÓCIO/03 - Franquia Oeste',
            # Adicionar novos negócios aqui
        }
        
        # MAPEAMENTO: tenant_slug → tags
        self.tenant_tags_mapping = {
            'diretoria': ['#mdcc/comando', '#mdcc/global'],
            'salao-esposa': ['#mdcc/unidade', '#mdcc/salao', '#mdcc/lux-beauty'],
            'franquia-chapeco': ['#mdcc/unidade', '#mdcc/franquia', '#mdcc/chapeco'],
            'franquia-oeste': ['#mdcc/unidade', '#mdcc/franquia', '#mdcc/oeste'],
        }
        
        logger.info(f"🔗 ObsidianBridge multi-business inicializado")
    
    def _get_tenant_path(self, tenant_slug: str) -> str:
        """Obter caminho no Obsidian para um tenant."""
        base_path = self.tenant_path_mapping.get(
            tenant_slug, 
            f'01 - UNIDADES DE NEGÓCIO/{tenant_slug}'  # Fallback
        )
        return os.path.join(self.obsidian_path, base_path)
    
    def _get_tenant_tags(self, tenant_slug: str) -> List[str]:
        """Obter tags para um tenant."""
        return self.tenant_tags_mapping.get(
            tenant_slug,
            ['#mdcc/unidade', f'#mdcc/{tenant_slug}']  # Fallback
        )
    
    def write_dashboard_note(self, tenant_slug: str, tenant_name: str,
                            metrics: List[Dict[str, Any]],
                            insights: Optional[List[Dict[str, Any]]] = None) -> str:
        """Escreve dashboard no local correto do Obsidian."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        # Obter caminho correto
        tenant_path = self._get_tenant_path(tenant_slug)
        os.makedirs(tenant_path, exist_ok=True)  # Criar pasta se não existir
        
        # Obter tags
        tags = self._get_tenant_tags(tenant_slug)
        tags_yaml = ', '.join(tags)
        
        # Construir conteúdo com frontmatter
        content = f"""---
tags: [{tags_yaml}]
tenant: {tenant_slug}
tenant_name: {tenant_name}
updated: {timestamp}
---

# 📊 Dashboard: {tenant_name}

**Última atualização:** {timestamp}

---

## 📈 Métricas Principais

"""
        
        # Agrupar métricas por tipo
        metrics_by_type = self._group_metrics_by_type(metrics)
        
        for metric_type, values in metrics_by_type.items():
            content += f"### {metric_type.replace('_', ' ').title()}\n\n"
            content += "| Métrica | Valor | Data |\n"
            content += "| :------ | :---- | :--- |\n"
            
            for metric in values[:10]:
                value = metric.get('metric_value', 0)
                date_ref = metric.get('date_ref', 'N/A')
                key = metric.get('metric_key', 'unknown')
                
                value_str = f"{value:,.2f}" if isinstance(value, float) else str(value)
                content += f"| {key.replace('_', ' ').title()} | {value_str} | {date_ref} |\n"
            
            content += "\n"
        
        if insights and len(insights) > 0:
            content += """---

## 🧠 Insights da IA

"""
            for insight in insights[:5]:
                content += f"### {insight.get('context', 'Insight')[:100]}...\n\n"
                content += f"> {insight.get('ai_response', '')}\n\n"
        
        content += f"\n---\n\n*Gerado automaticamente pelo Marketing Engine v4.0*\n"
        
        # Salvar no local correto
        filename = "Dashboard Local.md"
        filepath = os.path.join(tenant_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"📝 Dashboard escrito em: {filepath}")
        return filepath
    
    def write_alert_note(self, tenant_slug: str, alert_type: str,
                        alert_content: str, severity: str = 'medium') -> str:
        """Escreve alerta no COMANDO CENTRAL e no negócio."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        tags = self._get_tenant_tags(tenant_slug)
        tags.append(f'#mdcc/alerta')
        tags.append(f'#mdcc/{severity}')
        tags_yaml = ', '.join(tags)
        
        content = f"""---
tags: [{tags_yaml}]
tenant: {tenant_slug}
alert_type: {alert_type}
severity: {severity}
created: {timestamp}
---

# ⚠️ ALERTA: {alert_type}

**Tenant:** {tenant_slug}  
**Severidade:** {severity}  
**Criado em:** {timestamp}

---

## Detalhes

{alert_content}

---

## Ações Requeridas

- [ ] Investigar causa raiz
- [ ] Tomar ação corretiva
- [ ] Documentar aprendizado

---

*Gerado automaticamente pelo Marketing Engine v4.0*
"""
        
        # Salvar no COMANDO CENTRAL (alertas críticos)
        if severity in ['critical', 'high']:
            comando_path = os.path.join(self.obsidian_path, '00 - COMANDO CENTRAL')
            os.makedirs(comando_path, exist_ok=True)
            
            alert_filename = f"ALERTA-{tenant_slug}-{alert_type.replace(' ', '-')}.md"
            alert_filepath = os.path.join(comando_path, alert_filename)
            
            with open(alert_filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"🚨 Alerta crítico escrito em: {alert_filepath}")
        
        # Salvar também no negócio local
        tenant_path = self._get_tenant_path(tenant_slug)
        os.makedirs(tenant_path, exist_ok=True)
        
        alert_filepath_local = os.path.join(tenant_path, f"Alerta-{alert_type}.md")
        
        with open(alert_filepath_local, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"⚠️ Alerta escrito em: {alert_filepath_local}")
        return alert_filepath_local
```

---

#### FASE 3: Templates

**Arquivo**: `mkt/docs/templates/template-dashboard-local.md`

```markdown
---
tags: [#mdcc/unidade, #mdcc/dashboard]
tenant: {{tenant_slug}}
tenant_name: {{tenant_name}}
created: {{date}}
updated: {{date}}
---

# 📊 Dashboard: {{tenant_name}}

**Última atualização:** {{date}}

---

## 🎯 Metas do Negócio

| Meta | Valor Alvo | Atual | Status |
| :--- | :--------- | :---- | :----- |
| Faturamento Mensal | R$ {{meta_faturamento}} | R$ {{atual_faturamento}} | {{status_faturamento}} |
| CAC Máximo | R$ {{meta_cac}} | R$ {{atual_cac}} | {{status_cac}} |
| LTV Mínimo | R$ {{meta_ltv}} | R$ {{atual_ltv}} | {{status_ltv}} |
| Retenção 30d | {{meta_retencao}}% | {{atual_retencao}}% | {{status_retencao}} |

---

## 📈 Métricas Principais

### Vendas

| Métrica | Valor | Variação |
| :------ | :---- | :------- |
| Faturamento Total | R$ {{valor}} | {{variacao}}% |
| Ticket Médio | R$ {{valor}} | {{variacao}}% |
| Número de Pedidos | {{valor}} | {{variacao}}% |

### Marketing

| Métrica | Valor | Variação |
| :------ | :---- | :------- |
| Leads Totais | {{valor}} | {{variacao}}% |
| CAC | R$ {{valor}} | {{variacao}}% |
| ROAS | {{valor}}x | {{variacao}}% |

### Fidelização

| Métrica | Valor | Variação |
| :------ | :---- | :------- |
| Retenção 30d | {{valor}}% | {{variacao}}% |
| Churn | {{valor}}% | {{variacao}}% |
| LTV | R$ {{valor}} | {{variacao}}% |

---

## 🧠 Insights da IA

{{insights_ia}}

---

## ✅ Ações em Andamento

- [ ] {{acao_1}}
- [ ] {{acao_2}}
- [ ] {{acao_3}}

---

*Template padrão Marketing Director OS v4.0*
```

---

#### FASE 4: Dashboard Global (Dataview)

**Arquivo**: `00 - COMANDO CENTRAL/Dashboard Master.md`

```markdown
---
tags: [#mdcc/comando, #mdcc/global, #mdcc/dashboard]
updated: {{date}}
---

# 📊 Dashboard Master — Visão Global

**Atualizado em:** {{date}}

---

## 🌍 Saúde do Portfólio

```dataview
TABLE 
    file.name as "Negócio",
    file.tags as "Tags",
    file.mtime as "Última Atualização"
FROM #mdcc/unidade
WHERE contains(file.path, "01 - UNIDADES DE NEGÓCIO")
SORT file.mtime DESC
```

---

## 💰 Faturamento Consolidado

```dataview
TABLE WITHOUT ID
    file.link as "Negócio",
    meta(faturamento_total) as "Faturamento",
    meta(meta_faturamento) as "Meta",
    round((meta(faturamento_total) / meta(meta_faturamento)) * 100, 1) as "% da Meta"
FROM #mdcc/unidade
WHERE contains(file.path, "01 - UNIDADES DE NEGÓCIO")
SORT meta(faturamento_total) DESC
```

---

## 📊 CAC por Negócio

```dataview
TABLE WITHOUT ID
    file.link as "Negócio",
    meta(cac_atual) as "CAC Atual",
    meta(cac_meta) as "CAC Meta",
    choice(meta(cac_atual) > meta(cac_meta), "⚠️ Acima", "✅ Dentro") as "Status"
FROM #mdcc/unidade
WHERE contains(file.path, "01 - UNIDADES DE NEGÓCIO")
SORT meta(cac_atual) DESC
```

---

## 🚨 Alertas Críticos (Todos os Negócios)

```dataview
TABLE WITHOUT ID
    file.link as "Alerta",
    meta(severity) as "Severidade",
    meta(tenant) as "Negócio",
    file.mtime as "Criado"
FROM #mdcc/alerta
WHERE severity = "critical" OR severity = "high"
SORT file.mtime DESC
LIMIT 10
```

---

## 🎯 Metas Globais do Portfólio

| Meta | Valor Alvo | Atual | Status |
| :--- | :--------- | :---- | :----- |
| Faturamento Total | R$ {{soma_meta_faturamento}} | R$ {{soma_atual_faturamento}} | {{status}} |
| CAC Médio | R$ {{media_cac}} | R$ {{media_cac_atual}} | {{status}} |
| LTV Médio | R$ {{media_ltv}} | R$ {{media_ltv_atual}} | {{status}} |
| Retenção Média | {{media_retencao}}% | {{atual_retencao}}% | {{status}} |

---

## 📈 Tendências do Portfólio

```dataview
TABLE WITHOUT ID
    file.link as "Negócio",
    meta(tendencia_faturamento) as "Tendência",
    meta(tendencia_cac) as "Tendência CAC"
FROM #mdcc/unidade
WHERE contains(file.path, "01 - UNIDADES DE NEGÓCIO")
```

---

*Dashboard global gerado automaticamente com Dataview*
```

---

#### FASE 5: Graph View Configuration

**Arquivo**: `99 - INFRA/Configs/business-colors.json`

```json
{
  "groups": [
    {
      "name": "Comando Central",
      "color": "#FF0000",
      "filter": "#mdcc/comando OR #mdcc/global"
    },
    {
      "name": "Salão Lux Beauty",
      "color": "#FF69B4",
      "filter": "#mdcc/salao OR #mdcc/lux-beauty"
    },
    {
      "name": "Franquia Chapecó",
      "color": "#4169E1",
      "filter": "#mdcc/franquia OR #mdcc/chapeco"
    },
    {
      "name": "Franquia Oeste",
      "color": "#32CD32",
      "filter": "#mdcc/franquia OR #mdcc/oeste"
    },
    {
      "name": "Estratégias Transversais",
      "color": "#FFD700",
      "filter": "#mdcc/estrategia OR #mdcc/transversal"
    }
  ]
}
```

**Configuração no Obsidian**:

1. Abrir **Graph View**
2. Clicar em **Filters** (ícone de funil)
3. Adicionar **Groups** com as cores acima
4. Salvar como preset: "Multi-Business View"

---

### 📊 PODER DA INGESTÃO INTELIGENTE

#### Fluxo Automatizado

```
┌─────────────────────────────────────────────────────────────────┐
│  1. DROP NO DRIVE                                               │
│     • CSV em: drive_data/franquia-chapeco/vendas.csv            │
│                                                                 │
│  2. IDENTIFICAÇÃO (mkt_engine)                                  │
│     • Detecta tenant: franquia-chapeco                          │
│     • Mapeia para: 01 - UNIDADES DE NEGÓCIO/02 - Franquia       │
│                                                                 │
│  3. INJEÇÃO LOCAL (ObsidianBridge)                              │
│     • Salva em: 02 - Franquia Chapecó/Dashboard Local.md        │
│     • Tags: #mdcc/unidade #mdcc/franquia #mdcc/chapeco          │
│                                                                 │
│  4. AGREGAÇÃO AUTOMÁTICA (Dataview)                             │
│     • Dashboard Master.md atualiza automaticamente              │
│     • Soma faturamento de todas as #mdcc/unidade                │
│                                                                 │
│  5. ALERTAS CRÍTICOS                                            │
│     • Se CAC > meta → Alerta em COMANDO CENTRAL                 │
│     • Tags: #mdcc/alerta #mdcc/critical                         │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🎨 VISUALIZAÇÃO NO GRAPH VIEW

#### Mapeamento de Correlações

```
┌─────────────────────────────────────────────────────────────────┐
│  CÍRCULOS COLORIDOS                                             │
│                                                                 │
│  🔴 Comando Central                                             │
│  🩷 Salão Lux Beauty                                            │
│  🔵 Franquia Chapecó                                            │
│  🟢 Franquia Oeste                                              │
│  🟡 Estratégias Transversais                                    │
│                                                                 │
│  CONEXÕES DE ESTRATÉGIA                                         │
│                                                                 │
│  Se "Influenciadores" funcionou no Salão →                      │
│  Nota aponta para:                                              │
│  • Salão Lux Beauty (origem)                                    │
│  • Franquia Chapecó (aplicação)                                 │
│  • Franquia Oeste (aplicação)                                   │
│                                                                 │
│  RESULTADO: Mapa de conhecimento compartilhado                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🚀 PRÓXIMAS IMPLEMENTAÇÕES "HIGH POTENTIAL"

#### 1. Dashboard de Agregação (Global)

**Implementação**: Dataview com queries avançadas

```dataview
// Somar faturamento de todas as unidades
TABLE WITHOUT ID
    sum(meta(faturamento_total)) as "Faturamento Total"
FROM #mdcc/unidade
WHERE contains(file.path, "01 - UNIDADES DE NEGÓCIO")
```

**Script Python de Agregação** (fallback):

```python
# scripts/sync-global-dashboard.py

import os
import re
from pathlib import Path
from datetime import datetime

class GlobalDashboardSync:
    """Sincroniza dashboard global com dados de todos os negócios."""
    
    def __init__(self, obsidian_path: str):
        self.obsidian_path = obsidian_path
        self.unidades_path = os.path.join(obsidian_path, '01 - UNIDADES DE NEGÓCIO')
    
    def extract_metric(self, file_path: str, metric_name: str) -> float:
        """Extrai métrica de um arquivo Markdown."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex para encontrar valor da métrica
        pattern = rf'{metric_name}[:\s]+R\$?\s*([\d,.]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            value_str = match.group(1).replace('.', '').replace(',', '.')
            return float(value_str)
        
        return 0.0
    
    def aggregate_all(self) -> dict:
        """Agrega métricas de todos os negócios."""
        totals = {
            'faturamento_total': 0,
            'cac_medio': 0,
            'ltv_medio': 0,
            'num_negocios': 0,
        }
        
        cac_values = []
        ltv_values = []
        
        for negocio_folder in os.listdir(self.unidades_path):
            negocio_path = os.path.join(self.unidades_path, negocio_folder)
            
            if not os.path.isdir(negocio_path):
                continue
            
            dashboard_file = os.path.join(negocio_path, 'Dashboard Local.md')
            
            if not os.path.exists(dashboard_file):
                continue
            
            totals['faturamento_total'] += self.extract_metric(dashboard_file, 'Faturamento')
            
            cac = self.extract_metric(dashboard_file, 'CAC')
            if cac > 0:
                cac_values.append(cac)
            
            ltv = self.extract_metric(dashboard_file, 'LTV')
            if ltv > 0:
                ltv_values.append(ltv)
            
            totals['num_negocios'] += 1
        
        if cac_values:
            totals['cac_medio'] = sum(cac_values) / len(cac_values)
        
        if ltv_values:
            totals['ltv_medio'] = sum(ltv_values) / len(ltv_values)
        
        return totals
    
    def update_master_dashboard(self):
        """Atualiza Dashboard Master.md com dados agregados."""
        totals = self.aggregate_all()
        
        master_path = os.path.join(self.obsidian_path, '00 - COMANDO CENTRAL', 'Dashboard Master.md')
        
        with open(master_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir placeholders
        content = content.replace('{{soma_atual_faturamento}}', f"{totals['faturamento_total']:,.2f}")
        content = content.replace('{{media_cac_atual}}', f"{totals['cac_medio']:,.2f}")
        content = content.replace('{{media_ltv_atual}}', f"{totals['ltv_medio']:,.2f}")
        content = content.replace('{{date}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        with open(master_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Dashboard Master atualizado com {totals['num_negocios']} negócios")

# Uso
if __name__ == '__main__':
    sync = GlobalDashboardSync('C:/Users/Marketing/Documents/ObsidianVault')
    sync.update_master_dashboard()
```

---

#### 2. Contexto Isolado para Copilot

**Implementação**: Configurar Copilot para ler apenas pasta atual

```typescript
// Configuração do Copilot no Obsidian

{
  "copilot": {
    "context": {
      "scope": "current-folder",
      "include-tags": ["#mdcc/unidade"],
      "exclude-tags": ["#mdcc/comando", "#mdcc/global"]
    },
    "business-specific": {
      "salao-esposa": {
        "context-files": [
          "01 - UNIDADES DE NEGÓCIO/01 - Salão Lux Beauty/**/*"
        ],
        "rag-base": "salao-esposa"
      },
      "franquia-chapeco": {
        "context-files": [
          "01 - UNIDADES DE NEGÓCIO/02 - Franquia Chapecó/**/*"
        ],
        "rag-base": "franquia-chapeco"
      }
    }
  }
}
```

**Benefício**: Quando estiver na pasta do Salão, Copilot dá respostas específicas do salão, não mistura com franquias.

---

#### 3. Mural de Ativos (Galeria de Criativos)

**Implementação**: Dataview com visualização em galeria

```markdown
# 🖼️ Mural de Criativos — Todos os Negócios

```dataviewjs
// Gallery view de todos os criativos
const pages = dv.pages("#mdcc/criativo")
  .filter(p => p.file.path.includes("01 - UNIDADES DE NEGÓCIO"))

// Group by business
const byBusiness = pages.groupBy(p => {
  const pathParts = p.file.path.split('/')
  return pathParts.find(part => part.includes("01 - UNIDADES"))
})

// Render gallery
for (let [business, creatives] of Object.entries(byBusiness)) {
  dv.header(3, business)
  
  dv.table(
    ["Criativo", "Campanha", "ROAS", "Status"],
    creatives.map(c => [
      c.file.link,
      c.campanha || "N/A",
      c.roas || "N/A",
      c.status || "N/A"
    ])
  )
}
```
```

---

## 📊 CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Estrutura de Pastas (30 min)

- [ ] Executar script PowerShell de criação
- [ ] Verificar estrutura criada
- [ ] Configurar tags mapping

### Fase 2: mkt_engine Update (2 horas)

- [ ] Atualizar `obsidian.py` com mapeamento
- [ ] Testar com tenant de teste
- [ ] Validar isolamento de pastas

### Fase 3: Templates (1 hora)

- [ ] Criar templates padronizados
- [ ] Incluir tags obrigatórias
- [ ] Testar geração automática

### Fase 4: Dashboard Global (1 hora)

- [ ] Configurar Dataview
- [ ] Criar Dashboard Master.md
- [ ] Testar agregação

### Fase 5: Graph View (30 min)

- [ ] Configurar cores por negócio
- [ ] Salvar preset
- [ ] Testar navegação

### Fase 6: Validação (1 hora)

- [ ] Testar com CSV real de cada negócio
- [ ] Validar isolamento
- [ ] Validar agregação global

**Total**: ~6 horas

---

## 🏆 VEREDITO FINAL

### O Que Ganhamos

```
✅ Isolamento físico de cada negócio
✅ Visão global consolidada
✅ Cross-pollination de estratégias
✅ Contexto específico para IA
✅ Graph View como mapa de correlações
✅ Templates padronizados
```

### Poder do Agent Flow

```
✅ Boot Sequence → Visão clara
✅ Socratic Gate → Riscos mitigados
✅ Task Execution → Implementação em fases
✅ Truth in Data → Validação com dados reais
✅ Verification → Testes após cada fase
```

---

<div align="center">

**🌌 OBSIDIAN MULTI-BUSINESS ARCHITECTURE**

*Federação de Negócios • Exocórtex de Gestão • Comando de Múltiplas Galáxias*

**~6 horas de implementação • Pronto para escalar para N negócios**

</div>
