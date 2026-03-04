# 🐳 DOCKER — GUIA COMPLETO DE IMPLANTAÇÃO

> **Status**: ✅ Pronto para produção  
> **Tempo**: 15 minutos  
> **Dificuldade**: Fácil

---

## 📋 **PRÉ-REQUISITOS**

- [ ] Docker Desktop instalado
- [ ] Docker Compose instalado
- [ ] .env configurado com credenciais

---

## 🚀 **INÍCIO RÁPIDO**

### **1. Configurar .env**

```bash
# Na raiz do projeto, crie .env:
cp .env.example .env

# Edite com suas credenciais:
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
GROQ_API_KEY=gsk-your-key
SECRET_KEY=your-secret-key-min-32-chars

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=alertas@cmo360.com
EMAIL_FROM_NAME=CMO 360° Alertas
```

---

### **2. Subir Tudo (Produção)**

```bash
# Construir e subir todos os serviços
docker-compose up -d --build

# Ver status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f
```

---

### **3. Acessar**

**Frontend**: http://localhost:5173  
**Backend API**: http://localhost:8000  
**Health Check**: http://localhost:8000/health  
**Redis**: localhost:6379

---

## 🔧 **COMANDOS ÚTEIS**

### **Gerenciamento Básico**

```bash
# Iniciar tudo
docker-compose up -d

# Parar tudo
docker-compose down

# Reiniciar um serviço
docker-compose restart backend

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f watcher

# Ver status
docker-compose ps

# Ver uso de recursos
docker stats
```

---

### **Build e Rebuild**

```bash
# Construir imagens
docker-compose build

# Construir sem cache (força rebuild)
docker-compose build --no-cache

# Construir e subir apenas backend
docker-compose up -d --build backend

# Reconstruir após mudanças no código
docker-compose up -d --build
```

---

### **Acesso a Containers**

```bash
# Acessar shell do backend
docker-compose exec backend sh

# Acessar shell do frontend
docker-compose exec frontend sh

# Acessar Redis CLI
docker-compose exec redis redis-cli

# Executar comando específico
docker-compose exec backend python -c "print('Hello')"
```

---

### **Limpeza**

```bash
# Parar e remover containers
docker-compose down

# Parar, remover e volumes (cuidado!)
docker-compose down -v

# Remover imagens
docker-compose down --rmi all

# Limpar sistema Docker
docker system prune -a
```

---

## 📊 **SERVIÇOS**

| Serviço | Porta | Finalidade |
| :------ | :---- | :--------- |
| **backend** | 8000 | API FastAPI + Python |
| **frontend** | 5173 | React + Vite |
| **redis** | 6379 | Cache + WebSockets |
| **watcher** | - | Monitora arquivos |
| **nginx** | 80/443 | Reverse Proxy (prod) |

---

## 🔍 **MONITORAMENTO**

### **Health Checks**

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:5173

# Redis health
docker-compose exec redis redis-cli ping
```

---

### **Logs**

```bash
# Todos os logs
docker-compose logs -f

# Logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend

# Últimas 100 linhas
docker-compose logs --tail=100 backend

# Logs com timestamps
docker-compose logs -ft backend
```

---

### **Estatísticas**

```bash
# Uso de CPU/Memória
docker stats

# Inspecionar container
docker inspect cmo-backend

# Ver volumes
docker volume ls

# Ver redes
docker network ls
```

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### "Container não inicia"

```bash
# Ver logs de erro
docker-compose logs backend

# Verificar se porta está em uso
netstat -ano | findstr :8000

# Rebuild completo
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

### "Backend não conecta no Redis"

```bash
# Verificar se Redis está rodando
docker-compose ps redis

# Ver logs do Redis
docker-compose logs redis

# Testar conexão
docker-compose exec backend python -c "import redis; r = redis.from_url('redis://redis:6379'); print(r.ping())"
```

---

### "Frontend não carrega"

```bash
# Verificar build
docker-compose logs frontend

# Rebuild frontend
docker-compose down frontend
docker-compose build frontend
docker-compose up -d frontend
```

---

### "Erro de permissão"

```bash
# Corrigir permissões dos volumes
docker-compose down
sudo chown -R $USER:$USER ./drive_input ./obsidian_vault ./logs
docker-compose up -d
```

---

## 📈 **PRODUÇÃO**

### **1. Configurar Nginx (HTTPS)**

```bash
# Gerar certificado SSL (Let's Encrypt)
certbot certonly --standalone -d yourdomain.com

# Copiar certificados para pasta docker/nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem docker/nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem docker/nginx/ssl/

# Editar docker-compose.yml e descomentar perfil production
# docker-compose --profile production up -d
```

---

### **2. Variáveis de Ambiente (Produção)**

```env
# .env.production
SUPABASE_URL=https://projeto.supabase.co
SUPABASE_KEY=service-role-key
GROQ_API_KEY=gsk-key
SECRET_KEY=32+ chars secret

# Docker secrets (mais seguro)
# docker run --secret my_secret ...
```

---

### **3. Deploy em Cloud**

**DigitalOcean**:
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Copiar projeto
scp -r cmo-360-platform user@your-server:~/

# Acessar servidor e subir
ssh user@your-server
cd cmo-360-platform
docker-compose up -d
```

**AWS ECS**:
```bash
# Usar AWS Copilot CLI
copilot init
copilot deploy
```

**Google Cloud Run**:
```bash
# Build e push para GCR
docker build -t gcr.io/PROJECT-ID/cmo-backend .
docker push gcr.io/PROJECT-ID/cmo-backend

# Deploy
gcloud run deploy cmo-backend --image gcr.io/PROJECT-ID/cmo-backend
```

---

## 🔒 **SEGURANÇA**

### **Best Practices**

```dockerfile
# Dockerfile.backend
# ✅ Usa usuário não-root
USER app

# ✅ Não roda como root
# ✅ Scan de vulnerabilidades
docker scan cmo-backend

# ✅ Mantém imagens atualizadas
docker-compose pull
docker-compose up -d
```

---

### **Secrets**

```bash
# Nunca commitar .env no Git
# Usar Docker secrets em produção
echo "mysecret" | docker secret create my_secret -

# docker-compose.yml
secrets:
  - my_secret
```

---

## 📊 **SCALING**

### **Horizontal (Réplicas)**

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```

```bash
# Escalar backend para 3 réplicas
docker-compose up -d --scale backend=3
```

---

### **Vertical (Recursos)**

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 🎯 **CHECKLIST DE PRODUÇÃO**

- [ ] .env configurado com credenciais reais
- [ ] SECRET_KEY forte (32+ chars)
- [ ] HTTPS configurado (nginx + SSL)
- [ ] Health checks funcionando
- [ ] Logs centralizados
- [ ] Backup de volumes configurado
- [ ] Monitoramento ativo
- [ ] Auto-healing habilitado
- [ ] Rate limiting configurado
- [ ] Imagens scanadas (sem vulnerabilidades)

---

## 📚 **PRÓXIMOS PASSOS**

1. **Testar localmente**: `docker-compose up -d`
2. **Verificar health**: `curl http://localhost:8000/health`
3. **Acessar frontend**: http://localhost:5173
4. **Configurar produção**: HTTPS, domínio, etc.
5. **Monitorar**: Logs, métricas, alertas

---

<div align="center">

**🐳 DOCKER PRONTO PARA PRODUÇÃO!**

*15 minutos • 5 serviços • Custo zero*

**COMO USAR: `docker-compose up -d`**

</div>
