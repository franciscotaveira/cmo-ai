# ═══════════════════════════════════════════════════════════════════════════════
# MARKETING DIRECTOR OS — DOCKERFILE
# ═══════════════════════════════════════════════════════════════════════════════
# Imagem Docker para o Marketing Engine (Python)
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.11-slim

# ───────────────────────────────────────────────────────────────────────────────
# METADADOS
# ───────────────────────────────────────────────────────────────────────────────

LABEL maintainer="Arq - Marketing Director OS"
LABEL version="4.0"
LABEL description="Marketing Engine - Drive Watcher & Processor"

# ───────────────────────────────────────────────────────────────────────────────
# VARIÁVEIS DE AMBIENTE
# ───────────────────────────────────────────────────────────────────────────────

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    WORKDIR=/app

# ───────────────────────────────────────────────────────────────────────────────
# DEPENDÊNCIAS DO SISTEMA
# ───────────────────────────────────────────────────────────────────────────────

# Instalar dependências necessárias para algumas bibliotecas Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Necessário para detecção de tipo de arquivo (libmagic)
    libmagic1 \
    # Utilitários de rede para health checks
    curl \
    # Limpeza para reduzir tamanho da imagem
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# ───────────────────────────────────────────────────────────────────────────────
# DIRETÓRIO DE TRABALHO
# ───────────────────────────────────────────────────────────────────────────────

WORKDIR ${WORKDIR}

# Criar estrutura de pastas interna
RUN mkdir -p /app/drive_input /app/obsidian_output /app/logs

# ───────────────────────────────────────────────────────────────────────────────
# DEPENDÊNCIAS PYTHON
# ───────────────────────────────────────────────────────────────────────────────

# Copiar requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ───────────────────────────────────────────────────────────────────────────────
# CÓDIGO DA APLICAÇÃO
# ───────────────────────────────────────────────────────────────────────────────

# Copiar todo o código do engine
COPY src/ ./src/

# Copiar arquivo principal
COPY main.py .

# ───────────────────────────────────────────────────────────────────────────────
# HEALTH CHECK
# ───────────────────────────────────────────────────────────────────────────────

# Verificar se o watcher está rodando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('/app/logs/watcher.pid') else 1)" || exit 1

# ───────────────────────────────────────────────────────────────────────────────
# COMANDO DE INICIALIZAÇÃO
# ───────────────────────────────────────────────────────────────────────────────

# Iniciar o watcher de arquivos
CMD ["python", "main.py"]

# ═══════════════════════════════════════════════════════════════════════════════
# INSTRUÇÕES DE BUILD
# ═══════════════════════════════════════════════════════════════════════════════
#
# Build manual (se necessário):
#   docker build -t lux_marketing_engine:latest .
#
# Build via docker-compose:
#   docker-compose build marketing_engine
#
# ═══════════════════════════════════════════════════════════════════════════════
