#!/bin/bash
# ============================================
# LUNA - Vérification Sécurité
# ============================================
# Version: 2.1.0-secure
# Auteur: Varden & Luna
# ============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "========================================"
echo " LUNA CONSCIOUSNESS - Audit Sécurité"
echo " Version: 2.1.0-secure"
echo "========================================"
echo ""

ISSUES=0
WARNINGS=0

# ============================================
# CHECK 1: Fichier .env
# ============================================
echo "[1/8] Vérification fichier .env..."

if [ -f "$PROJECT_DIR/.env" ]; then
    # Vérification permissions
    if command -v stat &> /dev/null; then
        PERMS=$(stat -c %a "$PROJECT_DIR/.env" 2>/dev/null || stat -f %A "$PROJECT_DIR/.env" 2>/dev/null || echo "unknown")
        if [ "$PERMS" = "600" ]; then
            echo "      [OK] Permissions .env correctes (600)"
        elif [ "$PERMS" = "unknown" ]; then
            echo "      [WARN] Impossible de vérifier les permissions"
            ((WARNINGS++))
        else
            echo "      [ERREUR] Permissions .env incorrectes ($PERMS, devrait être 600)"
            ((ISSUES++))
        fi
    fi

    # Vérification contenu minimal
    if grep -q "REDIS_PASSWORD=" "$PROJECT_DIR/.env" && \
       grep -q "GF_ADMIN_PASSWORD=" "$PROJECT_DIR/.env" && \
       grep -q "LUNA_MASTER_KEY=" "$PROJECT_DIR/.env"; then
        echo "      [OK] Variables requises présentes"
    else
        echo "      [ERREUR] Variables manquantes dans .env"
        ((ISSUES++))
    fi
else
    echo "      [ERREUR] Fichier .env manquant"
    ((ISSUES++))
fi

echo ""

# ============================================
# CHECK 2: Redis non exposé sur 0.0.0.0
# ============================================
echo "[2/8] Vérification exposition Redis..."

if command -v ss &> /dev/null; then
    if ss -tuln 2>/dev/null | grep -q "0.0.0.0:6379"; then
        echo "      [ERREUR] Redis exposé sur 0.0.0.0:6379!"
        ((ISSUES++))
    elif ss -tuln 2>/dev/null | grep -q "127.0.0.1:6379"; then
        echo "      [WARN] Redis exposé sur localhost (127.0.0.1:6379)"
        ((WARNINGS++))
    else
        echo "      [OK] Redis non exposé publiquement"
    fi
elif command -v netstat &> /dev/null; then
    if netstat -tuln 2>/dev/null | grep -q "0.0.0.0:6379"; then
        echo "      [ERREUR] Redis exposé sur 0.0.0.0:6379!"
        ((ISSUES++))
    elif netstat -tuln 2>/dev/null | grep -q "127.0.0.1:6379"; then
        echo "      [WARN] Redis exposé sur localhost (127.0.0.1:6379)"
        ((WARNINGS++))
    else
        echo "      [OK] Redis non exposé publiquement"
    fi
else
    REDIS_PORTS=$(docker port luna-redis 2>/dev/null || echo "none")
    if [ "$REDIS_PORTS" = "none" ] || [ -z "$REDIS_PORTS" ]; then
        echo "      [OK] Redis sans port exposé (réseau interne)"
    else
        echo "      [INFO] Ports Redis: $REDIS_PORTS"
    fi
fi

echo ""

# ============================================
# CHECK 3: Authentification Redis
# ============================================
echo "[3/8] Vérification authentification Redis..."

if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "luna-redis"; then
    REDIS_NOAUTH=$(docker exec luna-redis redis-cli ping 2>&1 || true)
    if echo "$REDIS_NOAUTH" | grep -q "NOAUTH"; then
        echo "      [OK] Redis requiert authentification"
    elif echo "$REDIS_NOAUTH" | grep -q "PONG"; then
        echo "      [ERREUR] Redis accessible sans mot de passe!"
        ((ISSUES++))
    else
        echo "      [OK] Redis requiert authentification"
    fi
else
    echo "      [WARN] Container luna-redis non démarré"
    ((WARNINGS++))
fi

echo ""

# ============================================
# CHECK 4: Réseau interne Docker
# ============================================
echo "[4/8] Vérification réseau interne Docker..."

if docker network inspect luna_internal_network &>/dev/null; then
    INTERNAL=$(docker network inspect luna_internal_network --format '{{.Internal}}' 2>/dev/null)
    if [ "$INTERNAL" = "true" ]; then
        echo "      [OK] Réseau luna_internal_network isolé (internal: true)"
    else
        echo "      [ERREUR] Réseau interne non isolé (internal: false)"
        ((ISSUES++))
    fi
else
    echo "      [WARN] Réseau luna_internal_network non trouvé"
    ((WARNINGS++))
fi

echo ""

# ============================================
# CHECK 5: Ports bindés sur localhost
# ============================================
echo "[5/8] Vérification binding des ports..."

EXPOSED_EXTERNAL=$(docker ps --format '{{.Ports}}' 2>/dev/null | grep -v "127.0.0.1" | grep "0.0.0.0" || true)

if [ -z "$EXPOSED_EXTERNAL" ]; then
    echo "      [OK] Tous les ports bindés sur localhost (127.0.0.1)"
else
    echo "      [ERREUR] Ports exposés sur 0.0.0.0:"
    echo "$EXPOSED_EXTERNAL" | while read line; do
        echo "             $line"
    done
    ((ISSUES++))
fi

echo ""

# ============================================
# CHECK 6: .env dans .gitignore
# ============================================
echo "[6/8] Vérification .gitignore..."

if [ -f "$PROJECT_DIR/.gitignore" ]; then
    if grep -q "^\.env$" "$PROJECT_DIR/.gitignore" || grep -q "\.env" "$PROJECT_DIR/.gitignore"; then
        echo "      [OK] .env dans .gitignore"
    else
        echo "      [ERREUR] .env non ignoré par git!"
        ((ISSUES++))
    fi
else
    echo "      [WARN] Fichier .gitignore manquant"
    ((WARNINGS++))
fi

echo ""

# ============================================
# CHECK 7: Configuration Redis sécurisée
# ============================================
echo "[7/8] Vérification configuration Redis..."

if [ -f "$PROJECT_DIR/config/redis/redis.conf" ]; then
    REDIS_CONF="$PROJECT_DIR/config/redis/redis.conf"

    if grep -q "^protected-mode yes" "$REDIS_CONF"; then
        echo "      [OK] protected-mode activé"
    else
        echo "      [WARN] protected-mode non explicitement activé"
        ((WARNINGS++))
    fi

    if grep -q 'rename-command FLUSHALL ""' "$REDIS_CONF"; then
        echo "      [OK] Commande FLUSHALL désactivée"
    else
        echo "      [WARN] Commande FLUSHALL non désactivée"
        ((WARNINGS++))
    fi

    if grep -q 'rename-command CONFIG ""' "$REDIS_CONF"; then
        echo "      [OK] Commande CONFIG désactivée"
    else
        echo "      [WARN] Commande CONFIG non désactivée"
        ((WARNINGS++))
    fi
else
    echo "      [ERREUR] Fichier config/redis/redis.conf manquant"
    ((ISSUES++))
fi

echo ""

# ============================================
# CHECK 8: Containers security hardening
# ============================================
echo "[8/8] Vérification security hardening containers..."

if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "luna-consciousness"; then
    # Vérifier non-root
    USER=$(docker inspect luna-consciousness --format '{{.Config.User}}' 2>/dev/null)
    if [ "$USER" = "1000:1000" ] || [ "$USER" = "luna" ]; then
        echo "      [OK] Container luna-consciousness en non-root"
    else
        echo "      [WARN] Container luna-consciousness user: $USER"
        ((WARNINGS++))
    fi
    
    # Vérifier read_only
    READONLY=$(docker inspect luna-consciousness --format '{{.HostConfig.ReadonlyRootfs}}' 2>/dev/null)
    if [ "$READONLY" = "true" ]; then
        echo "      [OK] Container luna-consciousness read-only"
    else
        echo "      [WARN] Container luna-consciousness non read-only"
        ((WARNINGS++))
    fi
else
    echo "      [WARN] Container luna-consciousness non démarré"
    ((WARNINGS++))
fi

echo ""

# ============================================
# RÉSUMÉ
# ============================================
echo "========================================"
echo " RÉSUMÉ DE L'AUDIT"
echo "========================================"
echo ""

if [ $ISSUES -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo " [OK] Audit réussi - Aucun problème détecté"
    echo ""
    echo " La configuration Luna est sécurisée."
elif [ $ISSUES -eq 0 ]; then
    echo " [OK] Audit réussi avec avertissements"
    echo ""
    echo " Problèmes critiques : 0"
    echo " Avertissements      : $WARNINGS"
    echo ""
    echo " Vérifiez les avertissements pour une sécurité optimale."
else
    echo " [ERREUR] Audit échoué"
    echo ""
    echo " Problèmes critiques : $ISSUES"
    echo " Avertissements      : $WARNINGS"
    echo ""
    echo " Corrigez les problèmes avant de déployer en production."
fi

echo ""
echo "========================================"

exit $ISSUES
