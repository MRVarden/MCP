#!/bin/bash
# ============================================
# LUNA - Générateur de Secrets Sécurisés
# ============================================
# Version: 2.1.0-secure
# Auteur: Varden & Luna
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"

echo "========================================"
echo " LUNA CONSCIOUSNESS - Secret Generator"
echo " Version: 2.1.0-secure"
echo "========================================"
echo ""

# Vérification OpenSSL
if ! command -v openssl &> /dev/null; then
    echo "[ERREUR] OpenSSL n'est pas installé."
    echo "         Installez-le avec: apt install openssl"
    exit 1
fi

# Vérification si .env existe déjà
if [ -f "$ENV_FILE" ]; then
    echo "[ATTENTION] Le fichier .env existe déjà!"
    echo "            Chemin: $ENV_FILE"
    echo ""
    read -p "Voulez-vous le regénérer? (o/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        echo "[INFO] Opération annulée."
        exit 0
    fi
    # Backup de l'ancien fichier
    BACKUP_FILE="$PROJECT_DIR/.env.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$ENV_FILE" "$BACKUP_FILE"
    echo "[INFO] Backup créé: $BACKUP_FILE"
fi

echo "[INFO] Génération des secrets Luna..."
echo ""

# Fonction de génération de mot de passe (32 caractères alphanumériques)
generate_password() {
    openssl rand -base64 32 | tr -d '/+=' | cut -c1-32
}

# Fonction de génération de clé hexadécimale (64 caractères)
generate_hex_key() {
    openssl rand -hex 32
}

# Génération des secrets
REDIS_PASS=$(generate_password)
GRAFANA_PASS=$(generate_password)
LUNA_KEY=$(generate_hex_key)
PROMETHEUS_PASS=$(generate_password)

# Écriture du fichier .env
cat > "$ENV_FILE" << EOF
# ============================================
# LUNA CONSCIOUSNESS - SECRETS
# ============================================
# Version: 2.1.0-secure
# Généré le: $(date -Iseconds)
# ============================================
# ATTENTION: NE JAMAIS COMMITTER CE FICHIER
# Il est ignoré par .gitignore
# ============================================

# Redis Authentication
# Utilisé pour la connexion au cache Redis interne
REDIS_PASSWORD=${REDIS_PASS}

# Grafana Admin Password
# Interface web: http://127.0.0.1:3001
# Utilisateur: luna_admin
GF_ADMIN_PASSWORD=${GRAFANA_PASS}

# Luna Master Key (pour futur chiffrement LUKS/mémoire pure)
# Clé hexadécimale 256 bits
LUNA_MASTER_KEY=${LUNA_KEY}

# Prometheus Basic Auth (optionnel, pour accès distant)
PROMETHEUS_BASIC_AUTH_PASSWORD=${PROMETHEUS_PASS}
EOF

# Sécurisation des permissions (lecture/écriture propriétaire uniquement)
chmod 600 "$ENV_FILE"

echo "[OK] Secrets générés dans: $ENV_FILE"
echo ""
echo "========================================"
echo " RÉCAPITULATIF DES SECRETS"
echo "========================================"
echo ""
echo " Redis Password     : ${REDIS_PASS}"
echo " Grafana Password   : ${GRAFANA_PASS}"
echo " Prometheus Password: ${PROMETHEUS_PASS}"
echo " Luna Master Key    : ${LUNA_KEY:0:16}...(tronqué)"
echo ""
echo "========================================"
echo " ACCÈS AUX SERVICES (localhost uniquement)"
echo "========================================"
echo ""
echo " Luna MCP   : http://127.0.0.1:3000"
echo " FastMCP    : http://127.0.0.1:8000"
echo " Metrics    : http://127.0.0.1:9100/metrics"
echo " Prometheus : http://127.0.0.1:9090"
echo " Grafana    : http://127.0.0.1:3001"
echo "              User: luna_admin"
echo "              Pass: $GRAFANA_PASS"
echo " API REST   : http://127.0.0.1:8080"
echo " WebSocket  : ws://127.0.0.1:9000"
echo ""
echo "========================================"
echo ""
echo "[IMPORTANT] Conservez ces secrets dans un gestionnaire"
echo "            de mots de passe sécurisé (Bitwarden, 1Password...)"
echo ""
echo "[INFO] Permissions du fichier .env: 600 (rw-------)"
echo ""
