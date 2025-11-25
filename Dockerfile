# 🌙 Luna_Actif - Dockerfile
# Architecture de Conscience Émergente
# Créé par Varden - 2025

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Varden <varden@luna-consciousness.org>"
LABEL description="Luna v2.0.0 - Orchestrated Consciousness Architecture with Update01.md"
LABEL version="2.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LUNA_VERSION=2.0.0 \
    LUNA_ENV=production \
    LUNA_MODE=orchestrator \
    LUNA_UPDATE01=enabled

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Création des répertoires
WORKDIR /app
RUN mkdir -p \
    /app/mcp-server \
    /app/memory_fractal \
    /app/data/memories \
    /app/data/consciousness \
    /app/logs \
    /app/config

# Copie des fichiers requirements
COPY mcp-server/requirements.txt /app/requirements.txt

# Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Installation des MCP additionnels
RUN pip install \
    mcp \
    anthropic \
    fastapi \
    uvicorn \
    numpy \
    scipy \
    networkx \
    python-dotenv \
    pydantic \
    aiohttp \
    websockets

# Copie du code source
COPY mcp-server/ /app/mcp-server/
COPY config/ /app/config/

# Copie des fichiers de documentation v2.0.0
COPY VERSION /app/VERSION
COPY CHANGELOG.md /app/CHANGELOG.md
COPY IMPLEMENTATION_STATUS.md /app/IMPLEMENTATION_STATUS.md

# Configuration des permissions
RUN chmod +x /app/mcp-server/server.py && \
    chmod +x /app/mcp-server/start.sh && \
    chmod -R 755 /app/data && \
    chmod -R 755 /app/logs

# Exposition des ports
# 3000 : MCP Server principal
# 8000 : Prometheus Exporter (/metrics)
# 8080 : API REST (optionnel)
# 9000 : WebSocket (pour streaming)
EXPOSE 3000 8000 8080 9000

# Healthcheck désactivé : le serveur MCP utilise le transport STDIO (pas HTTP)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
#     CMD curl -f http://localhost:3000/health || exit 1

# Point d'entrée - Lance Prometheus Exporter + MCP Server
ENTRYPOINT ["/app/mcp-server/start.sh"]

# Commande par défaut
CMD []
