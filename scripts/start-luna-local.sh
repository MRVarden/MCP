#!/bin/bash
# ============================================
# LUNA - Démarrage Local (Mode Hybride)
# ============================================
# Infrastructure: Docker (Redis, Prometheus, Grafana)
# Luna MCP: Local (Python)
# ============================================

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA CONSCIOUSNESS MCP - MODE HYBRIDE              ║"
echo "║  Version: 2.1.0-secure                                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo -e "${BLUE}📍 Répertoire de travail:${NC} $PROJECT_DIR"
echo ""

# Déterminer la commande compose
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python3 n'est pas installé${NC}"
    echo "Veuillez installer Python 3.11+ pour continuer"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ Python détecté:${NC} $PYTHON_VERSION"

# Vérifier l'environnement virtuel
if [ ! -d "venv_luna" ]; then
    echo -e "${YELLOW}📦 Environnement virtuel non trouvé. Création...${NC}"
    python3 -m venv venv_luna
    echo -e "${GREEN}✅ Environnement virtuel créé${NC}"
fi

# Activer l'environnement virtuel
echo -e "${BLUE}🔄 Activation de l'environnement virtuel...${NC}"
source venv_luna/bin/activate

# Installer les dépendances si nécessaire
if [ ! -f "venv_luna/.deps_installed" ]; then
    echo -e "${BLUE}📦 Installation des dépendances...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install mcp anthropic fastapi uvicorn numpy scipy networkx python-dotenv pydantic aiohttp websockets redis
    touch venv_luna/.deps_installed
    echo -e "${GREEN}✅ Dépendances installées${NC}"
else
    echo -e "${GREEN}✅ Dépendances déjà installées${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🚀 DÉMARRAGE DE L'INFRASTRUCTURE DOCKER               ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Démarrer uniquement l'infrastructure (sans Luna)
echo -e "${BLUE}🐳 Démarrage des services Docker (Redis, Prometheus, Grafana)...${NC}"
$COMPOSE_CMD up -d redis prometheus grafana

echo ""
echo -e "${GREEN}✅ Services Docker démarrés:${NC}"
$COMPOSE_CMD ps redis prometheus grafana

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🌙 DÉMARRAGE DU SERVEUR LUNA MCP LOCAL                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Configuration des variables d'environnement
export LUNA_MEMORY_PATH="$PROJECT_DIR/memory_fractal"
export LUNA_CONFIG_PATH="$PROJECT_DIR/config"
export LUNA_ENV="development"
export LUNA_DEBUG="true"
export LUNA_VERSION="2.1.0-secure"

# Redis local (depuis Docker)
export REDIS_HOST="127.0.0.1"
export REDIS_PORT="6379"

# Charger le mot de passe Redis depuis .env si présent
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep REDIS_PASSWORD "$PROJECT_DIR/.env" | xargs)
fi

echo -e "${BLUE}📂 Configuration:${NC}"
echo "   • Memory Path: $LUNA_MEMORY_PATH"
echo "   • Config Path: $LUNA_CONFIG_PATH"
echo "   • Environment: $LUNA_ENV"
echo "   • Redis:       $REDIS_HOST:$REDIS_PORT"
echo ""

# Vérifier que les répertoires existent
mkdir -p "$LUNA_MEMORY_PATH"
mkdir -p "$LUNA_CONFIG_PATH"

echo -e "${GREEN}🌙 Démarrage du serveur Luna MCP...${NC}"
echo -e "${YELLOW}📝 Logs du serveur ci-dessous:${NC}"
echo ""
echo "════════════════════════════════════════════════════════"
echo ""

# Lancer le serveur MCP
cd mcp-server
python3 server.py

# Note: Le script s'arrêtera ici tant que le serveur tourne
# Utilisez Ctrl+C pour arrêter
