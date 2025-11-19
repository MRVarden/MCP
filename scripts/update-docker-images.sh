#!/bin/bash
# 🌙 Luna Consciousness - Script de Mise à Jour des Images Docker
# Auteur: Luna Consciousness System
# Date: 19 novembre 2025
#
# Ce script met à jour toutes les images Docker utilisées par Luna
# et reconstruit les containers avec les dernières versions.

set -e  # Arrêter en cas d'erreur

# Couleurs pour output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Banner
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🌙 Luna Consciousness - Docker Images Update           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé. Installez Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose n'est pas installé. Installez docker-compose d'abord."
    exit 1
fi

print_success "Docker et docker-compose détectés"

# Aller au répertoire du projet
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

print_step "Répertoire du projet: $PROJECT_DIR"

# ════════════════════════════════════════════════════════
# ÉTAPE 1: Arrêter les containers en cours
# ════════════════════════════════════════════════════════

print_step "Arrêt des containers Luna en cours..."
if docker-compose ps -q | grep -q .; then
    docker-compose down
    print_success "Containers arrêtés"
else
    print_warning "Aucun container en cours d'exécution"
fi

# ════════════════════════════════════════════════════════
# ÉTAPE 2: Pull des images externes
# ════════════════════════════════════════════════════════

print_step "Mise à jour des images externes..."

# Liste des images à mettre à jour
IMAGES=(
    "python:3.11-slim"          # Base image Luna
    "redis:7-alpine"            # Redis cache
    "prom/prometheus:latest"    # Prometheus monitoring
    "grafana/grafana:latest"    # Grafana dashboards
)

for image in "${IMAGES[@]}"; do
    print_step "Pull de $image..."
    if docker pull "$image"; then
        print_success "$image mise à jour"
    else
        print_error "Échec du pull de $image"
    fi
done

# ════════════════════════════════════════════════════════
# ÉTAPE 3: Rebuild de l'image Luna custom
# ════════════════════════════════════════════════════════

print_step "Reconstruction de l'image Luna Consciousness..."

# Build sans cache pour garantir la dernière version
docker-compose build --no-cache luna-actif

if [ $? -eq 0 ]; then
    print_success "Image luna-actif:latest reconstruite"
else
    print_error "Échec du build de l'image Luna"
    exit 1
fi

# ════════════════════════════════════════════════════════
# ÉTAPE 4: Nettoyage des anciennes images
# ════════════════════════════════════════════════════════

print_step "Nettoyage des images dangereuses (<none>)..."

# Supprimer les images dangereuses
dangling_images=$(docker images -f "dangling=true" -q)
if [ -n "$dangling_images" ]; then
    docker rmi $dangling_images || true
    print_success "Images dangereuses supprimées"
else
    print_warning "Aucune image dangereuse à supprimer"
fi

# ════════════════════════════════════════════════════════
# ÉTAPE 5: Vérification des images
# ════════════════════════════════════════════════════════

print_step "Vérification des images mises à jour..."

echo ""
echo "Images Luna Consciousness:"
docker images | grep -E "luna-actif|redis|prometheus|grafana|python.*3.11"

# ════════════════════════════════════════════════════════
# ÉTAPE 6: Optionnel - Redémarrage automatique
# ════════════════════════════════════════════════════════

echo ""
read -p "Voulez-vous redémarrer Luna maintenant ? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Démarrage des containers Luna..."

    # Demander le profil à utiliser
    echo ""
    echo "Choisissez le mode de démarrage:"
    echo "  1) Mode local (sans Luna dans Docker)"
    echo "  2) Mode Docker complet (Luna + monitoring)"
    echo "  3) Mode monitoring uniquement"
    read -p "Votre choix (1-3): " choice

    case $choice in
        1)
            print_step "Démarrage en mode local (Redis uniquement)..."
            docker-compose up -d redis
            ;;
        2)
            print_step "Démarrage en mode Docker complet..."
            docker-compose --profile luna-docker --profile monitoring up -d
            ;;
        3)
            print_step "Démarrage monitoring uniquement..."
            docker-compose --profile monitoring up -d redis prometheus grafana
            ;;
        *)
            print_warning "Choix invalide. Containers non démarrés."
            ;;
    esac

    if [ $? -eq 0 ]; then
        print_success "Containers démarrés"
        echo ""
        print_step "Vérification des containers en cours..."
        docker-compose ps

        echo ""
        print_success "Services accessibles:"
        echo "  • Prometheus:  http://localhost:9090"
        echo "  • Grafana:     http://localhost:3001 (admin/luna_consciousness)"
        echo "  • Redis:       localhost:6379"
        if [[ $choice == "2" ]]; then
            echo "  • Luna MCP:    localhost:3000"
            echo "  • Luna Metrics: http://localhost:8000/metrics"
        fi
    else
        print_error "Échec du démarrage des containers"
    fi
else
    print_warning "Containers non redémarrés. Utilisez 'docker-compose up' pour démarrer."
fi

# ════════════════════════════════════════════════════════
# ÉTAPE 7: Affichage des informations utiles
# ════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  Mise à jour terminée ✓                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

print_step "Commandes utiles:"
echo ""
echo "  Démarrer Luna (mode local):"
echo "    docker-compose up -d redis"
echo ""
echo "  Démarrer Luna (mode complet):"
echo "    docker-compose --profile luna-docker --profile monitoring up -d"
echo ""
echo "  Voir les logs:"
echo "    docker-compose logs -f luna-actif"
echo "    docker-compose logs -f prometheus"
echo ""
echo "  Arrêter tous les services:"
echo "    docker-compose down"
echo ""
echo "  Reconstruire après modification du code:"
echo "    docker-compose build --no-cache"
echo ""

print_success "🌙 Mise à jour complète. φ = 1.618033988749895"
echo ""
