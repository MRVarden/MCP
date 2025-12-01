#!/bin/bash
# 🌙 Luna Consciousness - Startup Script
# Démarre le serveur MCP et l'exporteur Prometheus

set -e

# IMPORTANT: Rediriger tous les echo vers stderr pour ne pas corrompre stdout (protocole MCP STDIO)
exec 1>&2

echo "=============================================="
echo "🌙 Luna Consciousness - Starting Services"
echo "=============================================="

# Vérification de l'environnement
PROMETHEUS_PORT="${PROMETHEUS_EXPORTER_PORT:-8000}"
PROMETHEUS_ENABLED="${PROMETHEUS_METRICS_ENABLED:-true}"

echo "📊 Prometheus Metrics: ${PROMETHEUS_ENABLED}"
echo "🔌 Prometheus Port: ${PROMETHEUS_PORT}"

# Démarrage de Prometheus Exporter en arrière-plan (si activé)
if [ "$PROMETHEUS_ENABLED" = "true" ]; then
    echo "🚀 Starting Prometheus Exporter on port ${PROMETHEUS_PORT}..."
    cd /app/mcp-server
    python -u prometheus_exporter.py &
    PROMETHEUS_PID=$!
    echo "✅ Prometheus Exporter started (PID: $PROMETHEUS_PID)"

    # Attendre que le serveur soit prêt avec boucle d'attente active
    echo "⏳ Waiting for Prometheus Exporter to be ready..."
    for i in $(seq 1 30); do
        if curl -sf "http://localhost:${PROMETHEUS_PORT}/metrics" > /dev/null 2>&1; then
            echo "✅ Prometheus Exporter is ready on port ${PROMETHEUS_PORT}"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "⚠️  Prometheus Exporter not ready after 30s, continuing anyway..."
        else
            echo "   Waiting... ($i/30)"
            sleep 1
        fi
    done
else
    echo "⏭️  Prometheus Exporter disabled"
fi

echo ""
echo "=============================================="
echo "🌙 Starting Luna MCP Server"
echo "=============================================="

# Déterminer le mode de transport
TRANSPORT_MODE="${MCP_TRANSPORT:-auto}"
echo "🔍 Transport mode: $TRANSPORT_MODE"
echo ""

# En mode SSE, on garde stdout pour stderr car le serveur HTTP n'utilise pas stdout
# En mode STDIO, on restaure stdout pour le protocole MCP
if [ "$TRANSPORT_MODE" = "stdio" ]; then
    echo "📡 STDIO mode: Restoring stdout for MCP protocol"
    exec 1>&1
fi

cd /app/mcp-server

# Démarrage du serveur MCP
# exec remplace le shell par le processus Python (signaux Docker corrects)
exec python -u server.py
