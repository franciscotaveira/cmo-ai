# 🔄 GUIA DE MIGRAÇÃO — Obsidian → Web Platform

> **Versão**: 1.0  
> **Tempo**: 1-2 horas  
> **Status**: ✅ Pronto

---

## 📋 **VISÃO GERAL**

### **O Que Está Migrando**

| De | Para | Por Quê |
| :- | :--- | :------ |
| Obsidian (local) | Web App (browser) | Acessível de qualquer lugar |
| Markdown files | Banco estruturado | Queries, filtros, exports |
| CLI (terminal) | UI (interface gráfica) | Mais intuitivo |
| Manual update | Auto refresh (5 min) | Tempo real |
| Sem login | Autenticação | Multi-usuário seguro |

---

## 🗓️ **CRONOGRAMA DE MIGRAÇÃO**

### **Fase 1: Setup (30 min)**
- [ ] Instalar Docker Desktop
- [ ] Configurar .env
- [ ] Subir plataforma
- [ ] Testar acesso

### **Fase 2: Dados (30 min)**
- [ ] Exportar dados do Obsidian
- [ ] Importar no Supabase
- [ ] Verificar integridade

### **Fase 3: Validação (30 min)**
- [ ] Comparar dashboards
- [ ] Testar funcionalidades
- [ ] Treinar usuários

### **Fase 4: Go Live (30 min)**
- [ ] Migrar tráfego
- [ ] Monitorar erros
- [ ] Coletar feedback

---

## 📝 **PASSO A PASSO**

### **Passo 1: Instalar Docker**

```bash
# Baixe Docker Desktop:
https://www.docker.com/products/docker-desktop/

# Instale e reinicie computador
# Verifique instalação:
docker --version
```

---

### **Passo 2: Configurar .env**

```bash
# Na raiz do projeto:
copy .env.example .env

# Edite .env com:
# - SUPABASE_URL (do seu projeto)
# - SUPABASE_KEY (service_role)
# - SUPABASE_ANON_KEY (anon key)
# - SECRET_KEY (32+ caracteres)
```

---

### **Passo 3: Subir Plataforma**

```bash
# Método fácil (Windows):
# Duplo clique em:
iniciar_plataforma.bat

# Método manual:
docker-compose up -d

# Verificar status:
docker-compose ps

# Ver logs:
docker-compose logs -f
```

---

### **Passo 4: Acessar Painel**

```
http://localhost:5173
```

**Você verá**:
- KPIs em tempo real
- Alertas críticos
- Insights da IA
- Performance por canal

---

### **Passo 5: Migrar Dados (Opcional)**

Se já tem dados no Obsidian:

```sql
-- No Supabase SQL Editor:

-- 1. Criar tabela de dashboards (se não existir)
CREATE TABLE IF NOT EXISTS dashboards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id),
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Importar dados do Obsidian (manual ou script Python)
-- Ver: scripts/migrate_obsidian_to_supabase.py
```

---

## 📊 **COMPARAÇÃO: ANTES VS DEPOIS**

### **Dashboard**

| Antes (Obsidian) | Depois (Web) |
| :--------------- | :----------- |
| Arquivo `.md` local | URL acessível de qualquer lugar |
| Atualização manual | Auto refresh (5 min) |
| Sem filtros | Filtros por tenant, data, tipo |
| Sem search | Busca full-text |
| Sem export | Export PDF, Excel, CSV |

---

### **Alertas**

| Antes (Obsidian) | Depois (Web) |
| :--------------- | :----------- |
| Lista em Markdown | Cards interativos |
| Sem ações | Botões: Ver, Agir, Ignorar |
| Sem notificação | Push, email, Slack |
| Sem histórico | Histórico completo |

---

### **Insights**

| Antes (Obsidian) | Depois (Web) |
| :--------------- | :----------- |
| Texto estático | Cards com confiança |
| Sem contexto | Link para análise completa |
| Sem prioridade | Ordenados por severidade |
| Sem ação | Botões: Aprovar, Rejeitar |

---

## 🎯 **TREINAMENTO DE USUÁRIOS**

### **Para C-Level (5 min)**

```
1. Abrir http://localhost:5173
2. Ver KPIs no topo
3. Clicar em alertas vermelhos
4. Clicar em "Ver Detalhes"
5. Tomar decisão
```

### **Para Analistas (15 min)**

```
1. Login (quando implementar)
2. Navegar por abas
3. Filtrar por tenant/data
4. Exportar relatórios
5. Criar tarefas
```

---

## 🔄 **PLANO DE ROLLBACK**

Se algo der errado:

### **Volta para Obsidian**

```bash
# 1. Parar plataforma:
docker-compose down

# 2. Abrir Obsidian:
# 🧠 EXOCÓRTEX/00 - Dashboards/

# 3. Usar CLI (se necessário):
cmo_command_center.bat
```

**Risco**: Baixo (dados originais intactos)

---

## 📈 **MÉTRICAS DE SUCESSO**

| Métrica | Meta | Como Medir |
| :------ | :--- | :--------- |
| **Uptime** | 95%+ | `docker-compose ps` |
| **Load Time** | < 3s | Browser DevTools |
| **User Satisfaction** | 8/10 | Survey pós-migração |
| **Features Used** | 80%+ | Analytics (futuro) |

---

## 🚨 **SOLUÇÃO DE PROBLEMAS**

### "Docker não inicia"

```bash
# Verifique:
# - Docker Desktop está rodando?
# - Portas 5173, 8000, 6379 livres?

netstat -ano | findstr :5173
netstat -ano | findstr :8000
```

### "Dados não aparecem"

```bash
# Verifique Supabase:
# - Tabelas existem?
# - Dados inseridos?
# - RLS não está bloqueando?

# No Supabase SQL Editor:
SELECT COUNT(*) FROM tenants;
SELECT COUNT(*) FROM business_metrics;
```

### "Frontend não carrega"

```bash
# Logs:
docker-compose logs frontend

# Reconstruir:
docker-compose up -d --build frontend
```

---

## 💡 **DICAS DE MIGRAÇÃO**

### **1. Migre Gradualmente**

Não desligue Obsidian de uma vez. Use ambos por 1-2 semanas.

### **2. Colete Feedback**

Após 1 semana, pergunte:
- O que funciona melhor?
- O que falta?
- O que é confuso?

### **3. Documente Issues**

Crie uma planilha:
| Data | Issue | Severidade | Status |
| :--- | :------ | :--------- | :----- |
| 02/03 | Login não funciona | Alta | Em progresso |

### **4. Tenha Rollback**

Sempre tenha um plano B (Obsidian + CLI).

---

## 🎉 **PÓS-MIGRAÇÃO**

### **Checklist Final**

- [ ] Plataforma rodando
- [ ] Dados migrados
- [ ] Usuários treinados
- [ ] Feedback coletado
- [ ] Issues documentadas
- [ ] Rollback testado (opcional)

### **Próximos Passos**

1. **Semana 2**: Implementar autenticação
2. **Semana 3**: Adicionar notificações
3. **Semana 4**: Export PDF/Excel
4. **Semana 5**: Multi-tenant (permissões)

---

## 📞 **SUPORTE**

Se precisar de ajuda:

1. **Verifique logs**: `docker-compose logs -f`
2. **Consulte docs**: `README_WEB_PLATFORM.md`
3. **Teste API**: `http://localhost:8000/health`
4. **Me informe** com erro + logs

---

<div align="center">

**🔄 MIGRAÇÃO COMPLETA**

*Obsidian → Web Platform*

**1-2 horas • Risco baixo • Rollback fácil**

**COMO COMEÇAR: `iniciar_plataforma.bat`**

</div>
