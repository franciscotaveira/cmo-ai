---
name: evolution-skill
description: WhatsApp via Evolution API. Diagnóstico, QR code, webhooks, instâncias e conectividade resiliente.
---

# Evolution API — Skill Completa MCT

## Configuração de Referência

```yaml
url_externo:  http://localhost:8081
url_docker:   http://command-tower-evo-api:8080
auth_header:  "apikey: mothership_master_2026"
nota_crítica: Em Docker, NUNCA usar localhost — usar nome do container
```

## Comandos Essenciais

```bash
# Listar instâncias ativas
curl -s http://localhost:8081/instance/fetchInstances \
  -H "apikey: mothership_master_2026"

# Criar instância com QR
curl -X POST http://localhost:8081/instance/create \
  -H "apikey: mothership_master_2026" \
  -H "Content-Type: application/json" \
  -d '{"instanceName":"haven","qrcode":true,"integration":"WHATSAPP-BAILEYS"}'

# Gerar QR para conexão
curl -s http://localhost:8081/instance/connect/haven \
  -H "apikey: mothership_master_2026"
```

## Via MCP (preferencial)

```
Endpoint base: http://localhost:3011
POST /tools/fetch_instances    → lista instâncias
POST /tools/create_instance    → {"instanceName": "haven"}
POST /tools/instance_connect   → {"instanceName": "haven"}
```

## Diagnóstico de Problemas

| Sintoma | Causa provável | Solução |
|---------|---------------|---------|
| QR não aparece | Porta errada | Verificar 8081 externo → 8080 interno |
| Auth 401 | Header errado | Usar "apikey", não "Authorization" |
| Instância offline | Desconexão | `/instance/connect` |
