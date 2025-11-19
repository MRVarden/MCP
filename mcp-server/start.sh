#!/bin/bash
# 🌙 Luna Consciousness - Startup Script
# Démarre le serveur MCP et l'exporteur Prometheus

set -e

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

    # Attendre que le serveur soit prêt
    sleep 3
    echo "✅ Prometheus Exporter should be listening on port ${PROMETHEUS_PORT}"
else
    echo "⏭️  Prometheus Exporter disabled"
fi

echo ""
echo "=============================================="
echo "🌙 Starting Luna MCP Server (STDIO mode)"
echo "=============================================="

# Démarrage du serveur MCP (en premier plan)
cd /app/mcp-server
exec python -u server.py

# Note: exec remplace le shell par le processus Python
# Cela permet à Docker de recevoir les signaux correctement
