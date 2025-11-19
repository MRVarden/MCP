#!/bin/bash
# Script de démarrage Luna MCP en mode local (Mode Hybride)
# Infrastructure: Docker | Luna MCP: Local

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  🌙 LUNA CONSCIOUSNESS MCP - MODE HYBRIDE              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}📍 Répertoire de travail:${NC} $SCRIPT_DIR"
echo ""

# Vérifier que Python est installé
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
    pip install -r mcp-server/requirements.txt
    pip install mcp anthropic fastapi uvicorn numpy scipy networkx python-dotenv pydantic aiohttp websockets
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

# Démarrer l'infrastructure Docker (sans Luna)
echo -e "${BLUE}🐳 Démarrage des services Docker (Prometheus, Grafana, Redis)...${NC}"
docker-compose up -d redis prometheus grafana

echo ""
echo -e "${GREEN}✅ Services Docker démarrés:${NC}"
docker-compose ps

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🌙 DÉMARRAGE DU SERVEUR LUNA MCP LOCAL                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Configuration des variables d'environnement
export LUNA_MEMORY_PATH="$SCRIPT_DIR/memory_fractal"
export LUNA_CONFIG_PATH="$SCRIPT_DIR/config"
export LUNA_ENV="development"
export LUNA_DEBUG="true"

echo -e "${BLUE}📂 Configuration:${NC}"
echo "   • Memory Path: $LUNA_MEMORY_PATH"
echo "   • Config Path: $LUNA_CONFIG_PATH"
echo "   • Environment: $LUNA_ENV"
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
