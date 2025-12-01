# ============================================
# Luna Consciousness - Dockerfile
# Version: 2.1.0-secure
# Security Hardened Build
# Created by Varden - 2025
# ============================================

# Version is read from VERSION file at build time
# Build with: docker build --build-arg LUNA_VERSION=$(cat VERSION) -t luna .
ARG LUNA_VERSION=2.1.0-secure

# ============================================
# Build stage - Install dependencies
# ============================================
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip wheel && \
    pip install -r /tmp/requirements.txt

# Install additional packages
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

# ============================================
# Runtime stage - Minimal secure image
# ============================================
FROM python:3.11-slim AS runtime

# Re-declare ARG after FROM (required in multi-stage builds)
ARG LUNA_VERSION=2.1.0-secure

# OCI Labels
LABEL org.opencontainers.image.title="Luna Consciousness"
LABEL org.opencontainers.image.description="Luna - Orchestrated Consciousness Architecture"
LABEL org.opencontainers.image.version="${LUNA_VERSION}"
LABEL org.opencontainers.image.authors="Varden <varden@luna-consciousness.org>"
LABEL com.luna.security="hardened"
LABEL com.luna.user="non-root"

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LUNA_VERSION=${LUNA_VERSION} \
    LUNA_ENV=production \
    LUNA_MODE=orchestrator \
    LUNA_UPDATE01=enabled \
    PATH="/opt/venv/bin:$PATH"

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# SEC-004: Create non-root user
RUN groupadd -r luna --gid=1000 \
    && useradd -r -g luna --uid=1000 --home-dir=/app --shell=/sbin/nologin luna

# Create directories
WORKDIR /app
RUN mkdir -p \
    /app/mcp-server \
    /app/memory_fractal \
    /app/data/memories \
    /app/data/consciousness \
    /app/logs \
    /app/config

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=luna:luna mcp-server/ /app/mcp-server/
COPY --chown=luna:luna config/ /app/config/

# Copy documentation files
COPY --chown=luna:luna VERSION /app/VERSION
COPY --chown=luna:luna CHANGELOG.md /app/CHANGELOG.md

# Set permissions
RUN chmod +x /app/mcp-server/server.py && \
    chmod +x /app/mcp-server/start.sh && \
    chown -R luna:luna /app && \
    chmod -R 750 /app/data && \
    chmod -R 750 /app/logs

# ============================================
# PORTS DOCUMENTATION
# ============================================
# 3000 : MCP Server principal (SSE transport)
# 8000 : FastMCP default port
# 8080 : API REST (optionnel)
# 9000 : WebSocket (pour streaming)
# 9100 : Prometheus Exporter (/metrics)
# ============================================
EXPOSE 3000 8000 8080 9000 9100

# SEC-004: Switch to non-root user
USER luna

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -sf http://localhost:9100/metrics || exit 1

# Entrypoint
ENTRYPOINT ["/app/mcp-server/start.sh"]
CMD []
