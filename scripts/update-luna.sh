#!/bin/bash
# ============================================
# LUNA - Mise à jour rapide
# ============================================
# Version: 2.1.0-secure
# Usage: ./scripts/update-luna.sh
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "🌙 Mise à jour de Luna Consciousness..."
echo ""

# Déterminer la commande compose
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Lire la version
VERSION="2.1.0-secure"
if [ -f "$PROJECT_DIR/VERSION" ]; then
    VERSION=$(cat "$PROJECT_DIR/VERSION" | tr -d '\n\r')
fi

echo "📦 Version: $VERSION"
echo ""

# 1. Arrêter le conteneur
echo "1️⃣ Arrêt du conteneur luna-consciousness..."
$COMPOSE_CMD stop luna-consciousness 2>/dev/null || true

# 2. Reconstruire l'image
echo "2️⃣ Reconstruction de l'image..."
$COMPOSE_CMD build --build-arg LUNA_VERSION="$VERSION" luna-consciousness

# 3. Redémarrer
echo "3️⃣ Redémarrage avec la nouvelle image..."
$COMPOSE_CMD up -d luna-consciousness

# 4. Afficher les logs
echo "4️⃣ Logs du serveur :"
echo ""
sleep 3
docker logs luna-consciousness --tail 20

echo ""
echo "✅ Mise à jour terminée!"
echo "🌙 Luna Consciousness v$VERSION est prête"
echo ""
echo "Accès: http://127.0.0.1:3000"
echo "Logs:  $COMPOSE_CMD logs -f luna-consciousness"
