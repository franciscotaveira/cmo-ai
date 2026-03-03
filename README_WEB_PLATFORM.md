# 🚀 CMO 360° — WEB PLATFORM (Docker)

> **Status**: ✅ Pronto para rodar  
> **Tempo**: 5 minutos para subir  
> **Dificuldade**: Fácil

---

## 📋 **PRÉ-REQUISITOS**

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- Conta no [Supabase](https://supabase.com) criada
- (Opcional) Conta no [Groq](https://console.groq.com/keys) para IA

---

## 🚀 **COMO RODAR (5 MINUTOS)**

### **Passo 1: Configurar .env**

```bash
# Na raiz do projeto:
copy .env.example .env

# Edite .env com:
# - SUPABASE_URL
# - SUPABASE_KEY
# - SUPABASE_ANON_KEY
# - GROQ_API_KEY (opcional)
# - SECRET_KEY
```

### **Passo 2: Subir com Docker**

```bash
# Na raiz do projeto:
docker-compose up -d

# Verificar status:
docker-compose ps

# Ver logs:
docker-compose logs -f
```

### **Passo 3: Acessar Painel**

Abra no navegador:
```
http://localhost:5173
```

**API Backend**:
```
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/api/dashboard
```

---

## 📊 **O QUE VAI RODAR**

| Serviço | URL | Finalidade |
| :------ | :-- | :--------- |
| **Frontend (React)** | http://localhost:5173 | Painel web |
| **Backend (FastAPI)** | http://localhost:8000 | API REST |
| **Redis** | localhost:6379 | Cache + WebSockets |
| **Watcher** | (background) | Monitora arquivos |
| **Nginx** | http://localhost:80 | Proxy (produção) |

---

## 🎯 **COMO USAR O PAINEL**

### **Dashboard Executivo**

Ao abrir, você verá:

1. **KPIs em Tempo Real**
   - Receita Hoje
   - CAC Médio
   - ROAS Médio
   - NPS

2. **Alertas Críticos**
   - Lista de alertas que precisam de ação
   - Severidade (🔴 crítico, 🟡 atenção)
   - Botão para ver detalhes

3. **Insights da IA**
   - Insights gerados automaticamente
   - Confiança da IA
   - Link para análise completa

4. **Performance por Canal**
   - Google Ads, Meta Ads, LinkedIn, Email
   - ROAS, CTR, Spend, Receita
   - Status (Excelente, Bom, Crítico)

---

## 🔄 **ATUALIZAR DADOS**

O painel atualiza automaticamente a cada **5 minutos**.

Para atualizar manualmente:
- Clique em **"🔄 Atualizar"** no canto superior direito

---

## 🛑 **PARAR O SISTEMA**

```bash
# Parar todos os containers:
docker-compose down

# Parar e remover volumes:
docker-compose down -v
```

---

## 📝 **COMANDOS ÚTEIS**

```bash
# Ver logs em tempo real:
docker-compose logs -f

# Ver logs de um serviço específico:
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar um serviço:
docker-compose restart backend

# Reconstruir após mudanças:
docker-compose up -d --build

# Ver status dos containers:
docker-compose ps

# Acessar terminal do backend:
docker-compose exec backend sh

# Acessar terminal do frontend:
docker-compose exec frontend sh
```

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### "Docker não encontrado"

```bash
# Instale Docker Desktop:
https://www.docker.com/products/docker-desktop/
```

### "Erro ao conectar no Supabase"

```bash
# Verifique .env:
# - SUPABASE_URL está correta?
# - SUPABASE_KEY é a service_role key?
# - Supabase está online?

# Teste no navegador:
https://SEU-PROJETO.supabase.co
```

### "Porta 5173 já em uso"

```bash
# Pare outros processos na porta:
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Ou mude a porta no docker-compose.yml
```

### "Frontend não carrega"

```bash
# Verifique logs:
docker-compose logs frontend

# Reconstrua:
docker-compose up -d --build frontend
```

### "Backend retorna erro 500"

```bash
# Verifique logs:
docker-compose logs backend

# Verifique .env:
# - SUPABASE_URL e SUPABASE_KEY corretas
# - SECRET_KEY tem 32+ caracteres
```

---

## 📊 **ESTRUTURA DO PROJETO**

```
cmo-360-platform/
├── docker-compose.yml        # Infraestrutura completa
├── .env                      # Variáveis de ambiente
├── .env.example              # Template de .env
│
├── backend/                  # API FastAPI
│   ├── main.py               # API principal
│   ├── requirements.txt      # Dependências Python
│   └── Dockerfile
│
├── frontend/                 # App React
│   ├── src/
│   │   ├── App.jsx           # Dashboard principal
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Estilos
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── drive_input/              # Arquivos para processar
└── obsidian_vault/           # Dashboards (legado)
```

---

## 🎯 **PRÓXIMOS PASSOS**

### **Semana 1: Validação**
- [ ] Subar plataforma
- [ ] Configurar Supabase
- [ ] Testar dashboard
- [ ] Coletar feedback

### **Semana 2: Features**
- [ ] Autenticação (login/senha)
- [ ] Multi-usuário
- [ ] Permissões
- [ ] Exportar PDF

### **Semana 3: Produção**
- [ ] Dominio próprio
- [ ] SSL/HTTPS
- [ ] Deploy em cloud
- [ ] Monitoramento

---

## 💰 **CUSTO DE INFRA**

| Serviço | Custo |
| :------ | :---- |
| **Docker (local)** | R$ 0 |
| **Supabase** | R$ 0 (free tier) |
| **Groq** | R$ 0 (free tier) |
| **Redis** | R$ 0 (incluso) |
| **Total** | **R$ 0/mês** |

**Em produção** (com domínio, SSL, cloud):
- VPS (DigitalOcean, AWS): R$ 50-200/mês
- Domínio: R$ 50/ano
- SSL: R$ 0 (Let's Encrypt)

---

## 📞 **SUPORTE**

Se encontrar problemas:

1. **Verifique logs**: `docker-compose logs -f`
2. **Consulte documentação**: `CMO_360_FINAL.md`
3. **Teste API**: `http://localhost:8000/health`
4. **Me informe** com erro completo + logs

---

## 🎉 **BÔNUS: API ENDPOINTS**

### **Dashboard**
```bash
curl http://localhost:8000/api/dashboard
```

### **Alertas**
```bash
curl http://localhost:8000/api/alerts
```

### **Insights**
```bash
curl http://localhost:8000/api/insights
```

### **Performance por Canal**
```bash
curl http://localhost:8000/api/channels/performance
```

### **Reconhecer Alerta**
```bash
curl -X POST http://localhost:8000/api/alerts/{alert_id}/acknowledge
```

---

<div align="center">

**🚀 CMO 360° WEB PLATFORM**

*Docker • React • FastAPI • Supabase*

**Pronto em 5 minutos • Custo R$ 0 • Escalável**

**COMO USAR: `docker-compose up -d` → http://localhost:5173**

</div>
