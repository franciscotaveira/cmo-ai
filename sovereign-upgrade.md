# 🌌 Antigravity Kit v3.1: Sovereign Upgrade

Este plano detalha a fusão do conhecimento extraído na **Missão Total Recall** (consolidado no **Atlas Soberano**) com o núcleo operacional do **Antigravity Kit**. O objetivo é transformar o kit em uma ferramenta de "Soberania Total", capaz de planejar e executar projetos integrando diretamente sua infraestrutura proprietária e segredos de produção.

## 🎯 Success Criteria

- [ ] `GEMINI.md` atualizado com diretrizes de Soberania.
- [ ] `CODEBASE.md` inicializado com os "Superpoderes" (Soverign Context).
- [ ] Nova Skill `sovereign-ai` criada e funcional.
- [ ] Agentes `orchestrator` e `project-planner` evoluídos para usar o contexto soberano.

## 🛠️ Proposed Changes

### Layer 1: Foundation (Memory & Rules)

#### [NEW] `CODEBASE.md`

- **Finalidade:** Servir como "Warm Memory" do projeto.
- **Conteúdo:** Mapeamento de dependências, stack tecnológica e o **Sovereign Context** (Vertex AI, Asaas, ClickUp, PrometheusEngine).

#### [MODIFY] `.agent/rules/GEMINI.md`

- **Injeção:** Adicionar o **Atlas Soberano** como leitura obrigatória no "Session Snapshot Protocol".
- **Refino:** Atualizar o "Request Classifier" para detectar demandas "Soberanas" (migração GCP, automação financeira).

---

### Layer 2: Capability Expansion

#### [NEW] `.agent/skills/sovereign-ai/`

- **SKILL.md:** Instruções sobre como operar no ecossistema Lux (GCP/Vertex AI, Asaas API, Memória Prometheus).
- **Scripts:** Documentar como invocar os motores `world_eater.py` e `council.py` detectados no sistema.

---

### Layer 3: Agent Evolution

#### [MODIFY] `.agent/agents/orchestrator.md`

- **Update:** Adicionar `sovereign-ai` à lista de skills padrão.
- **Protocolo:** Instruir o orchestrator a cruzar tarefas com o `Atlas Soberano` antes de delegar.

#### [MODIFY] `.agent/agents/project-planner.md`

- **Update:** Incluir análise de viabilidade soberana (ex: "Isso pode rodar no Vertex AI para economizar 65%?").

---

## ✅ Phase X: Verification Plan

### Automated Tests

- Execução de `python .agent/scripts/checklist.py .` para validar a integridade dos arquivos novos/modificados.

### Manual Verification

- Simulação de um prompt "Soberano" (ex: "Planeje a migração do módulo X para o Vertex AI") e verificação se o agente utiliza o contexto do Atlas.
