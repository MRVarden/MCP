#!/bin/bash
# ============================================
# LUNA - Mise à Jour des Images Docker
# ============================================
# Version: 2.1.0-secure
# Auteur: Varden & Luna
# ============================================

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() { echo -e "${BLUE}==>${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

# Banner
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🌙 Luna Consciousness - Docker Images Update            ║"
echo "║   Version: 2.1.0-secure                                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé."
    exit 1
fi

print_success "Docker détecté"

# Répertoire du projet
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

print_step "Répertoire du projet: $PROJECT_DIR"

# Déterminer la commande compose
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# ============================================
# ÉTAPE 1: Arrêter les containers
# ============================================
print_step "Arrêt des containers Luna en cours..."
if $COMPOSE_CMD ps -q 2>/dev/null | grep -q .; then
    $COMPOSE_CMD down
    print_success "Containers arrêtés"
else
    print_warning "Aucun container en cours d'exécution"
fi

# ============================================
# ÉTAPE 2: Pull des images externes
# ============================================
print_step "Mise à jour des images externes..."

IMAGES=(
    "python:3.11-slim"
    "redis:7-alpine"
    "prom/prometheus:latest"
    "grafana/grafana:latest"
)

for image in "${IMAGES[@]}"; do
    print_step "Pull de $image..."
    if docker pull "$image"; then
        print_success "$image mise à jour"
    else
        print_warning "Échec du pull de $image (non bloquant)"
    fi
done

# ============================================
# ÉTAPE 3: Rebuild de l'image Luna
# ============================================
print_step "Reconstruction de l'image Luna Consciousness..."

# Lire la version
VERSION="2.1.0-secure"
if [ -f "$PROJECT_DIR/VERSION" ]; then
    VERSION=$(cat "$PROJECT_DIR/VERSION" | tr -d '\n\r')
fi

print_step "Version: $VERSION"

# Build sans cache
$COMPOSE_CMD build --no-cache --build-arg LUNA_VERSION="$VERSION" luna-consciousness

if [ $? -eq 0 ]; then
    print_success "Image luna-consciousness reconstruite"
else
    print_error "Échec du build de l'image Luna"
    exit 1
fi

# ============================================
# ÉTAPE 4: Nettoyage
# ============================================
print_step "Nettoyage des images dangling..."

dangling_images=$(docker images -f "dangling=true" -q)
if [ -n "$dangling_images" ]; then
    docker rmi $dangling_images 2>/dev/null || true
    print_success "Images dangling supprimées"
else
    print_warning "Aucune image dangling"
fi

# ============================================
# ÉTAPE 5: Vérification
# ============================================
print_step "Images Luna Consciousness:"
echo ""
docker images | grep -E "luna-consciousness|redis|prometheus|grafana" || true

# ============================================
# ÉTAPE 6: Redémarrage optionnel
# ============================================
echo ""
read -p "Voulez-vous redémarrer Luna maintenant ? (o/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Oo]$ ]]; then
    print_step "Démarrage des containers Luna..."
    $COMPOSE_CMD up -d
    
    if [ $? -eq 0 ]; then
        print_success "Containers démarrés"
        echo ""
        $COMPOSE_CMD ps
        echo ""
        print_success "Services accessibles (localhost uniquement):"
        echo "  • Luna MCP:    http://127.0.0.1:3000"
        echo "  • Metrics:     http://127.0.0.1:9100/metrics"
        echo "  • Prometheus:  http://127.0.0.1:9090"
        echo "  • Grafana:     http://127.0.0.1:3001"
    else
        print_error "Échec du démarrage"
    fi
else
    print_warning "Containers non redémarrés."
    echo "Utilisez '$COMPOSE_CMD up -d' pour démarrer."
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              Mise à jour terminée ✓                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
print_success "🌙 φ = 1.618033988749895"
echo ""
