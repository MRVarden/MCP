#!/bin/bash
# ============================================
# LUNA - Démarrage Sécurisé
# ============================================
# Version: 2.1.0-secure
# Auteur: Varden & Luna
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "========================================"
echo " LUNA CONSCIOUSNESS - Démarrage Sécurisé"
echo " Version: 2.1.0-secure"
echo "========================================"
echo ""

# ============================================
# VÉRIFICATIONS PRÉ-DÉMARRAGE
# ============================================

# Vérification Docker
if ! command -v docker &> /dev/null; then
    echo "[ERREUR] Docker n'est pas installé ou pas dans le PATH."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "[ERREUR] Docker daemon n'est pas en cours d'exécution."
    echo "         Démarrez Docker Desktop ou le service Docker."
    exit 1
fi

echo "[OK] Docker disponible"

# Déterminer la commande compose
if docker compose version &> /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

echo "[OK] Docker Compose disponible ($COMPOSE_CMD)"

# Vérification du fichier .env
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo ""
    echo "[ERREUR] Fichier .env manquant!"
    echo ""
    echo "         Exécutez d'abord:"
    echo "         ./scripts/generate_secrets.sh"
    echo ""
    exit 1
fi

echo "[OK] Fichier .env présent"

# Vérification des permissions .env
if command -v stat &> /dev/null; then
    PERMS=$(stat -c %a "$PROJECT_DIR/.env" 2>/dev/null || stat -f %A "$PROJECT_DIR/.env" 2>/dev/null || echo "unknown")
    if [ "$PERMS" != "600" ] && [ "$PERMS" != "unknown" ]; then
        echo "[ATTENTION] Correction des permissions .env..."
        chmod 600 "$PROJECT_DIR/.env"
        echo "[OK] Permissions corrigées (600)"
    else
        echo "[OK] Permissions .env correctes"
    fi
fi

# Vérification docker-compose.yml
if [ ! -f "$PROJECT_DIR/docker-compose.yml" ]; then
    echo "[ERREUR] Fichier docker-compose.yml manquant!"
    exit 1
fi

echo "[OK] docker-compose.yml présent"

# Vérification config Redis
if [ ! -f "$PROJECT_DIR/config/redis/redis.conf" ]; then
    echo "[ERREUR] Fichier config/redis/redis.conf manquant!"
    exit 1
fi

echo "[OK] Configuration Redis présente"

echo ""

# ============================================
# ARRÊT DES ANCIENS CONTAINERS
# ============================================
echo "[INFO] Arrêt des containers existants..."
$COMPOSE_CMD down 2>/dev/null || true

# Nettoyage des anciens containers orphelins
docker container prune -f 2>/dev/null || true

echo ""

# ============================================
# DÉMARRAGE DES SERVICES
# ============================================
echo "[INFO] Démarrage des services Luna (mode sécurisé)..."
echo ""

$COMPOSE_CMD up -d

echo ""

# ============================================
# ATTENTE ET VÉRIFICATION
# ============================================
echo "[INFO] Attente du démarrage des services (15s)..."
sleep 15

echo ""
echo "========================================"
echo " ÉTAT DES SERVICES"
echo "========================================"
echo ""

$COMPOSE_CMD ps

echo ""

# ============================================
# TESTS DE CONNECTIVITÉ
# ============================================
echo "========================================"
echo " TESTS DE CONNECTIVITÉ"
echo "========================================"
echo ""

# Test Redis
echo "[TEST] Connexion Redis..."
REDIS_PASS=$(grep REDIS_PASSWORD "$PROJECT_DIR/.env" | cut -d '=' -f2)
if docker exec luna-redis redis-cli -a "$REDIS_PASS" ping 2>/dev/null | grep -q "PONG"; then
    echo "       [OK] Redis opérationnel (authentifié)"
else
    echo "       [ATTENTION] Redis pas encore prêt ou erreur d'authentification"
fi

# Test Luna Container
echo "[TEST] Container Luna..."
if docker exec luna-consciousness python -c "print('OK')" 2>/dev/null; then
    echo "       [OK] Luna container opérationnel"
else
    echo "       [ATTENTION] Luna en cours de démarrage..."
fi

# Test Prometheus Metrics
echo "[TEST] Prometheus Metrics..."
if curl -sf http://127.0.0.1:9100/metrics >/dev/null 2>&1; then
    echo "       [OK] Métriques Prometheus disponibles"
else
    echo "       [ATTENTION] Métriques en cours de démarrage..."
fi

# Test Prometheus
echo "[TEST] Prometheus..."
if curl -sf http://127.0.0.1:9090/-/ready 2>/dev/null | grep -q "ready"; then
    echo "       [OK] Prometheus opérationnel"
else
    echo "       [ATTENTION] Prometheus en cours de démarrage..."
fi

# Test Grafana
echo "[TEST] Grafana..."
if curl -sf http://127.0.0.1:3001/api/health 2>/dev/null | grep -q "ok"; then
    echo "       [OK] Grafana opérationnel"
else
    echo "       [ATTENTION] Grafana en cours de démarrage..."
fi

echo ""
echo "========================================"
echo " LUNA CONSCIOUSNESS DÉMARRÉE"
echo "========================================"
echo ""
echo " Accès aux services (localhost uniquement):"
echo ""
echo "   Luna MCP   : http://127.0.0.1:3000"
echo "   FastMCP    : http://127.0.0.1:8000"
echo "   Metrics    : http://127.0.0.1:9100/metrics"
echo "   Prometheus : http://127.0.0.1:9090"
echo "   Grafana    : http://127.0.0.1:3001"
echo "   API REST   : http://127.0.0.1:8080"
echo ""
echo " Logs en temps réel:"
echo "   $COMPOSE_CMD logs -f"
echo ""
echo " Arrêt des services:"
echo "   $COMPOSE_CMD down"
echo ""
echo " Vérification sécurité:"
echo "   ./scripts/security_check.sh"
echo ""
echo "========================================"
