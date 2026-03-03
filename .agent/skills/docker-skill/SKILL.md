---
name: docker-skill
description: Docker Compose para infraestrutura MCT. Patterns de rede, volumes, variáveis de ambiente e deploy no VPS próprio.
---

# Docker — Skill MCT

## Regra Crítica de Rede

```yaml
# CORRETO: containers se comunicam pelo nome do serviço
EVOLUTION_API_URL: http://command-tower-evo-api:8080

# ERRADO: localhost não funciona entre containers
EVOLUTION_API_URL: http://localhost:8081
```

## Template Base — Stack MCT

```yaml
version: '3.8'

networks:
  mct-net:
    driver: bridge

volumes:
  postgres_data:
  redis_data:

services:
  # Evolution API — WhatsApp
  evo-api:
    image: atendai/evolution-api:latest
    container_name: command-tower-evo-api
    networks: [mct-net]
    ports: ["8081:8080"]
    environment:
      AUTHENTICATION_API_KEY: mothership_master_2026
      DATABASE_ENABLED: "true"
      DATABASE_URL: postgresql://mct:${POSTGRES_PASSWORD}@postgres:5432/evolution
    volumes:
      - ./evolution_instances:/evolution/instances
    restart: unless-stopped

  # Backend / API Node
  backend:
    build: ./backend
    container_name: command-tower-backend
    networks: [mct-net]
    ports: ["3000:3000"]
    environment:
      EVOLUTION_API_URL: http://command-tower-evo-api:8080
      EVOLUTION_API_KEY: mothership_master_2026
      SUPABASE_URL: ${SUPABASE_URL}
      SUPABASE_SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
    depends_on: [evo-api]
    restart: unless-stopped

  # Redis — Cache
  redis:
    image: redis:alpine
    container_name: command-tower-redis
    networks: [mct-net]
    volumes:
      - redis_data:/data
    restart: unless-stopped
```

## Comandos de Operação

```bash
# Subir tudo
docker compose up -d

# Ver logs em tempo real
docker compose logs -f [serviço]

# Reiniciar serviço específico
docker compose restart evo-api

# Verificar saúde dos containers
docker compose ps

# Executar comando em container
docker exec command-tower-evo-api sh -c "curl localhost:8080/health"

# Limpar cache Redis
docker exec command-tower-redis redis-cli FLUSHALL

# Rebuild de serviço específico
docker compose up -d --build backend

# Ver uso de recursos
docker stats --no-stream
```

## Debugging de Rede

```bash
# Testar conectividade entre containers
docker exec command-tower-backend \
  curl -s http://command-tower-evo-api:8080/instance/fetchInstances \
  -H "apikey: mothership_master_2026"

# Inspecionar rede
docker network inspect mct-net
```
