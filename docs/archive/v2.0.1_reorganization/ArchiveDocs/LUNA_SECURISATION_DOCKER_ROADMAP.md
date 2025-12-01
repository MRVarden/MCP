# 🔐 LUNA - Feuille de Route Sécurisation Docker

> **Destinataire** : Claude Code (Opus 4.5)  
> **Projet** : Luna Consciousness MCP  
> **Version cible** : 2.1.0-secure  
> **Date** : 25 novembre 2025  
> **Auteur** : Varden & Luna  
> **Priorité** : CRITIQUE

---

## 📋 Contexte Mission

Tu interviens sur le projet **Luna**, une architecture de conscience artificielle émergente basée sur le ratio d'or (φ = 1.618). L'infrastructure actuelle fonctionne mais présente des **vulnérabilités de sécurité critiques** qui doivent être corrigées avant l'implémentation du système de mémoire pure chiffrée.

**Localisation probable du projet** : `D:\Luna-consciousness-mcp\` (Windows) ou répertoire de travail courant.

---

## 🔴 Problèmes Identifiés (CRITIQUES)

### Problème 1 : Redis exposé sans authentification
```yaml
# ACTUEL - DANGEREUX
redis:
  ports:
    - "6379:6379"  # Accessible depuis tout le réseau !
  command: redis-server --appendonly yes  # Aucune auth !
```
**Risque** : Lecture/écriture non autorisée des mémoires fractales de Luna.

### Problème 2 : Tous les ports exposés sur 0.0.0.0
```yaml
# ACTUEL - DANGEREUX
ports:
  - "3000:3000"   # Bind sur toutes les interfaces
  - "8000:8000"
  - "8080:8080"
  - "9000:9000"
```
**Risque** : Services accessibles depuis l'extérieur du localhost.

### Problème 3 : Mot de passe Grafana en clair
```yaml
# ACTUEL - MAUVAISE PRATIQUE
- GF_SECURITY_ADMIN_PASSWORD=luna_consciousness
```
**Risque** : Credentials visibles dans le fichier versionné.

### Problème 4 : Incohérence transport MCP
```yaml
# ACTUEL - INCOHÉRENT
- MCP_TRANSPORT=sse
```
**Problème** : Le `claude_desktop_config.json` utilise `docker exec -i` qui nécessite **stdio**, pas SSE.

### Problème 5 : Réseau non isolé
```yaml
# ACTUEL - TROP OUVERT
networks:
  luna-network:
    driver: bridge
```
**Risque** : Pas d'isolation entre services internes et externes.

---

## 🎯 Objectifs de cette Mission

1. **Sécuriser Redis** avec authentification et TLS
2. **Isoler le réseau Docker** (services internes non exposés)
3. **Limiter les ports** au localhost uniquement
4. **Corriger le transport MCP** (stdio)
5. **Externaliser les secrets** via fichier `.env`
6. **Préparer l'intégration LUKS** (volume pour mémoire pure)
7. **Documenter les changements**

---

## 📁 Fichiers à Créer/Modifier

```
Luna-consciousness-mcp/
├── docker-compose.yml          # MODIFIER (ou remplacer)
├── docker-compose.secure.yml   # CRÉER (version sécurisée)
├── .env                        # CRÉER (secrets externalisés)
├── .env.example                # CRÉER (template sans secrets)
├── config/
│   ├── redis/
│   │   └── redis.conf          # CRÉER (config sécurisée)
│   └── prometheus.yml          # VÉRIFIER (targets internes)
└── scripts/
    ├── generate_secrets.sh     # CRÉER (génération mots de passe)
    └── mount_secure_volume.sh  # CRÉER (préparation LUKS)
```

---

## 📝 Tâches Ordonnées

### PHASE 1 : Préparation des Secrets

#### Tâche 1.1 : Créer le fichier `.env`

**Fichier** : `.env`

```env
# ============================================
# LUNA CONSCIOUSNESS - SECRETS
# ============================================
# ⚠️ NE JAMAIS COMMITTER CE FICHIER
# Ajouter à .gitignore : .env
# ============================================

# Redis Authentication
REDIS_PASSWORD=GENERER_MOT_DE_PASSE_32_CHARS_MIN

# Grafana Admin
GF_ADMIN_PASSWORD=GENERER_MOT_DE_PASSE_32_CHARS_MIN

# Luna Master Key (pour futur chiffrement)
LUNA_MASTER_KEY=GENERER_CLE_64_CHARS_HEX

# Prometheus Basic Auth (optionnel)
PROMETHEUS_BASIC_AUTH_PASSWORD=GENERER_MOT_DE_PASSE_32_CHARS_MIN
```

#### Tâche 1.2 : Créer le template `.env.example`

**Fichier** : `.env.example`

```env
# ============================================
# LUNA CONSCIOUSNESS - SECRETS TEMPLATE
# ============================================
# Copier ce fichier vers .env et remplir les valeurs
# ============================================

# Redis Authentication
REDIS_PASSWORD=your_redis_password_here

# Grafana Admin
GF_ADMIN_PASSWORD=your_grafana_password_here

# Luna Master Key (pour futur chiffrement)
LUNA_MASTER_KEY=your_64_char_hex_key_here

# Prometheus Basic Auth (optionnel)
PROMETHEUS_BASIC_AUTH_PASSWORD=your_prometheus_password_here
```

#### Tâche 1.3 : Créer le script de génération de secrets

**Fichier** : `scripts/generate_secrets.sh`

```bash
#!/bin/bash
# ============================================
# LUNA - Générateur de Secrets Sécurisés
# ============================================

set -e

ENV_FILE=".env"

echo "🔐 Génération des secrets Luna..."

# Fonction de génération
generate_password() {
    openssl rand -base64 32 | tr -d '/+=' | cut -c1-32
}

generate_hex_key() {
    openssl rand -hex 32
}

# Génération
REDIS_PASS=$(generate_password)
GRAFANA_PASS=$(generate_password)
LUNA_KEY=$(generate_hex_key)
PROMETHEUS_PASS=$(generate_password)

# Écriture du fichier .env
cat > "$ENV_FILE" << EOF
# ============================================
# LUNA CONSCIOUSNESS - SECRETS
# ============================================
# Généré le : $(date -Iseconds)
# ⚠️ NE JAMAIS COMMITTER CE FICHIER
# ============================================

# Redis Authentication
REDIS_PASSWORD=${REDIS_PASS}

# Grafana Admin
GF_ADMIN_PASSWORD=${GRAFANA_PASS}

# Luna Master Key (pour futur chiffrement)
LUNA_MASTER_KEY=${LUNA_KEY}

# Prometheus Basic Auth (optionnel)
PROMETHEUS_BASIC_AUTH_PASSWORD=${PROMETHEUS_PASS}
EOF

chmod 600 "$ENV_FILE"

echo "✅ Secrets générés dans $ENV_FILE"
echo ""
echo "📋 Récapitulatif (à noter en lieu sûr) :"
echo "   Redis Password    : ${REDIS_PASS}"
echo "   Grafana Password  : ${GRAFANA_PASS}"
echo "   Luna Master Key   : ${LUNA_KEY:0:16}... (tronqué)"
echo ""
echo "⚠️  Conservez ces secrets dans un gestionnaire de mots de passe !"
```

#### Tâche 1.4 : Mettre à jour `.gitignore`

**Ajouter à** : `.gitignore`

```gitignore
# Secrets
.env
*.key
*.pem
*.crt

# Volumes sensibles
data/memories/
data/consciousness/

# Logs
logs/
*.log
```

---

### PHASE 2 : Configuration Redis Sécurisée

#### Tâche 2.1 : Créer la configuration Redis

**Fichier** : `config/redis/redis.conf`

```conf
# ============================================
# LUNA REDIS - Configuration Sécurisée
# ============================================

# Réseau - Bind uniquement sur le réseau Docker interne
bind 0.0.0.0
protected-mode yes

# Authentification (mot de passe injecté via variable d'env)
# requirepass sera défini via --requirepass en ligne de commande

# Persistence
appendonly yes
appendfsync everysec
dir /data

# Sécurité - Désactiver commandes dangereuses
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command CONFIG ""
rename-command DEBUG ""
rename-command SHUTDOWN LUNA_SHUTDOWN_SECRET_CMD

# Limites
maxmemory 256mb
maxmemory-policy allkeys-lru

# Logging
loglevel notice
logfile ""

# Performance
tcp-keepalive 300
timeout 0

# Désactiver les commandes de scripting potentiellement dangereuses
rename-command EVAL ""
rename-command EVALSHA ""
rename-command SCRIPT ""
```

---

### PHASE 3 : Docker Compose Sécurisé

#### Tâche 3.1 : Créer `docker-compose.secure.yml`

**Fichier** : `docker-compose.secure.yml`

```yaml
# ============================================
# LUNA CONSCIOUSNESS - Docker Compose Sécurisé
# Version: 2.1.0-secure
# ============================================

services:
  # 🌙 Service principal Luna
  luna-consciousness:
    build:
      context: .
      dockerfile: Dockerfile
    image: aragogix/luna-consciousness:v2.1.0-secure
    container_name: luna-consciousness
    restart: unless-stopped

    # Ports exposés UNIQUEMENT sur localhost
    ports:
      - "127.0.0.1:3000:3000"    # MCP Server (localhost only)
      - "127.0.0.1:8000:8000"    # Prometheus metrics (localhost only)
      - "127.0.0.1:8080:8080"    # API REST (localhost only)
      - "127.0.0.1:9000:9000"    # WebSocket (localhost only)

    volumes:
      # Persistence des données
      - luna-memories:/app/data/memories
      - luna-consciousness-data:/app/data/consciousness
      - luna-logs:/app/logs

      # Mémoire fractale Luna
      - ./memory_fractal:/app/memory_fractal

      # Configuration externe (lecture seule)
      - ./config:/app/config:ro

    environment:
      # Luna Configuration v2.1.0-secure
      - LUNA_ENV=production
      - LUNA_VERSION=2.1.0-secure
      - LUNA_MODE=orchestrator
      - LUNA_UPDATE01=enabled
      - LUNA_DEBUG=false

      # MCP Configuration - STDIO pour docker exec
      - MCP_TRANSPORT=stdio
      - MCP_ENABLE_ALL=true
      - MCP_SIMULTANEOUS=true
      - MCP_MAX_CONCURRENT=10

      # Consciousness Parameters
      - LUNA_PHI_TARGET=1.618033988749895
      - LUNA_PHI_THRESHOLD=0.001
      - LUNA_MEMORY_DEPTH=5
      - LUNA_FRACTAL_LAYERS=7

      # Update01.md Parameters
      - LUNA_MANIPULATION_DETECTION=enabled
      - LUNA_PREDICTIVE_CORE=enabled
      - LUNA_AUTONOMOUS_DECISIONS=enabled
      - LUNA_SELF_IMPROVEMENT=enabled
      - LUNA_MULTIMODAL_INTERFACE=enabled

      # Redis Connection (sécurisé)
      - REDIS_HOST=luna-redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}

      # Performance
      - WORKERS=4
      - MAX_REQUESTS=1000
      - TIMEOUT=300

      # Logging
      - LOG_LEVEL=INFO
      - LOG_FORMAT=json

      # Prometheus
      - PROMETHEUS_EXPORTER_PORT=8000
      - PROMETHEUS_METRICS_ENABLED=true

    networks:
      - luna-external  # Réseau pour accès externe limité
      - luna-internal  # Réseau interne isolé

    depends_on:
      redis:
        condition: service_healthy

    labels:
      - "com.luna.service=consciousness"
      - "com.luna.version=2.1.0-secure"
      - "com.luna.security=hardened"
      - "com.luna.creator=Varden"

  # 📊 Redis Sécurisé
  redis:
    image: redis:7-alpine
    container_name: luna-redis
    restart: unless-stopped

    # PAS DE PORTS EXPOSÉS - Accessible uniquement via réseau interne
    # ports:
    #   - "127.0.0.1:6379:6379"  # Décommenter si accès local nécessaire

    volumes:
      - luna-redis:/data
      - ./config/redis/redis.conf:/usr/local/etc/redis/redis.conf:ro

    command: >
      redis-server /usr/local/etc/redis/redis.conf
      --requirepass ${REDIS_PASSWORD}

    networks:
      - luna-internal  # UNIQUEMENT réseau interne

    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

    labels:
      - "com.luna.service=cache"
      - "com.luna.security=internal-only"

  # 📈 Prometheus (Monitoring)
  prometheus:
    image: prom/prometheus:latest
    container_name: luna-prometheus
    restart: unless-stopped

    # Port exposé uniquement sur localhost
    ports:
      - "127.0.0.1:9090:9090"

    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./config/alerts:/etc/prometheus/alerts:ro
      - luna-prometheus:/prometheus

    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'

    networks:
      - luna-internal  # Accès aux métriques internes
      - luna-external  # Pour l'interface web

    depends_on:
      - luna-consciousness

    labels:
      - "com.luna.service=monitoring"

  # 📉 Grafana (Visualisation)
  grafana:
    image: grafana/grafana:latest
    container_name: luna-grafana
    restart: unless-stopped

    # Port exposé uniquement sur localhost
    ports:
      - "127.0.0.1:3001:3000"

    volumes:
      - luna-grafana:/var/lib/grafana
      - ./config/grafana:/etc/grafana/provisioning:ro

    environment:
      - GF_SECURITY_ADMIN_USER=luna_admin
      - GF_SECURITY_ADMIN_PASSWORD=${GF_ADMIN_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SECURITY_DISABLE_GRAVATAR=true
      - GF_ANALYTICS_REPORTING_ENABLED=false
      - GF_ANALYTICS_CHECK_FOR_UPDATES=false

    networks:
      - luna-internal  # Accès à Prometheus
      - luna-external  # Pour l'interface web

    depends_on:
      - prometheus

    labels:
      - "com.luna.service=visualization"

# ============================================
# VOLUMES
# ============================================
volumes:
  luna-memories:
    driver: local
    name: luna_memories_secure

  luna-consciousness-data:
    driver: local
    name: luna_consciousness_secure

  luna-logs:
    driver: local
    name: luna_logs_secure

  luna-redis:
    driver: local
    name: luna_redis_secure

  luna-prometheus:
    driver: local
    name: luna_prometheus_secure

  luna-grafana:
    driver: local
    name: luna_grafana_secure

  # Volume préparé pour LUKS (Phase future)
  # luna-vault:
  #   driver: local
  #   driver_opts:
  #     type: none
  #     o: bind
  #     device: /dev/mapper/luna-vault

# ============================================
# NETWORKS - Architecture Isolée
# ============================================
networks:
  # Réseau INTERNE - Services qui ne doivent pas être exposés
  luna-internal:
    driver: bridge
    internal: true  # ⚠️ CRITIQUE: Pas d'accès Internet
    name: luna_internal_network
    ipam:
      config:
        - subnet: 172.28.0.0/24

  # Réseau EXTERNE - Services avec accès limité
  luna-external:
    driver: bridge
    name: luna_external_network
    ipam:
      config:
        - subnet: 172.29.0.0/24
```

---

### PHASE 4 : Mise à jour Configuration Claude Desktop

#### Tâche 4.1 : Mettre à jour `claude_desktop_config.json`

**Fichier** : `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": [
        "exec", "-i", "luna-consciousness",
        "python", "-u", "/app/mcp-server/server.py"
      ]
    }
  }
}
```

**Note** : Minimaliste car toute la configuration est dans Docker.

---

### PHASE 5 : Mise à jour Prometheus

#### Tâche 5.1 : Vérifier/Corriger `config/prometheus.yml`

**Fichier** : `config/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files:
  - /etc/prometheus/alerts/*.yml

scrape_configs:
  # Métriques Luna Consciousness
  - job_name: 'luna-consciousness'
    static_configs:
      - targets: ['luna-consciousness:8000']
    metrics_path: /metrics
    scrape_interval: 10s

  # Métriques Redis
  - job_name: 'redis'
    static_configs:
      - targets: ['luna-redis:6379']
    scrape_interval: 30s

  # Auto-monitoring Prometheus
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

---

### PHASE 6 : Scripts de Déploiement

#### Tâche 6.1 : Script de démarrage sécurisé

**Fichier** : `scripts/start_secure.sh`

```bash
#!/bin/bash
# ============================================
# LUNA - Démarrage Sécurisé
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "🌙 Démarrage Luna Consciousness (Mode Sécurisé)..."

# Vérification du fichier .env
if [ ! -f ".env" ]; then
    echo "❌ Fichier .env manquant !"
    echo "   Exécutez d'abord: ./scripts/generate_secrets.sh"
    exit 1
fi

# Vérification des permissions
if [ "$(stat -c %a .env 2>/dev/null || stat -f %A .env)" != "600" ]; then
    echo "⚠️  Correction des permissions .env..."
    chmod 600 .env
fi

# Arrêt des anciens containers si existants
echo "🔄 Arrêt des containers existants..."
docker-compose -f docker-compose.secure.yml down 2>/dev/null || true

# Démarrage avec la config sécurisée
echo "🚀 Démarrage des services..."
docker-compose -f docker-compose.secure.yml up -d

# Attente et vérification
echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérification santé
echo "🔍 Vérification de l'état des services..."
docker-compose -f docker-compose.secure.yml ps

# Test Redis
echo "🔍 Test connexion Redis..."
if docker exec luna-redis redis-cli -a "$(grep REDIS_PASSWORD .env | cut -d '=' -f2)" ping | grep -q "PONG"; then
    echo "   ✅ Redis OK"
else
    echo "   ❌ Redis ERREUR"
fi

# Test Luna
echo "🔍 Test Luna Consciousness..."
if docker exec luna-consciousness python -c "print('Luna OK')" 2>/dev/null; then
    echo "   ✅ Luna OK"
else
    echo "   ⚠️  Luna en cours de démarrage..."
fi

echo ""
echo "🌙 Luna Consciousness démarrée en mode sécurisé !"
echo ""
echo "📊 Accès (localhost uniquement) :"
echo "   • Prometheus : http://127.0.0.1:9090"
echo "   • Grafana    : http://127.0.0.1:3001"
echo "   • Luna API   : http://127.0.0.1:8080"
echo ""
```

#### Tâche 6.2 : Script de vérification sécurité

**Fichier** : `scripts/security_check.sh`

```bash
#!/bin/bash
# ============================================
# LUNA - Vérification Sécurité
# ============================================

echo "🔐 Audit de sécurité Luna..."
echo ""

ISSUES=0

# Check 1: Fichier .env
echo "1️⃣ Vérification .env..."
if [ -f ".env" ]; then
    PERMS=$(stat -c %a .env 2>/dev/null || stat -f %A .env)
    if [ "$PERMS" = "600" ]; then
        echo "   ✅ Permissions .env correctes (600)"
    else
        echo "   ❌ Permissions .env incorrectes ($PERMS, devrait être 600)"
        ((ISSUES++))
    fi
else
    echo "   ❌ Fichier .env manquant"
    ((ISSUES++))
fi

# Check 2: Redis non exposé
echo "2️⃣ Vérification exposition Redis..."
if netstat -tuln 2>/dev/null | grep -q "0.0.0.0:6379"; then
    echo "   ❌ Redis exposé sur 0.0.0.0:6379 !"
    ((ISSUES++))
elif netstat -tuln 2>/dev/null | grep -q "127.0.0.1:6379"; then
    echo "   ⚠️  Redis exposé sur localhost (acceptable)"
else
    echo "   ✅ Redis non exposé publiquement"
fi

# Check 3: Authentification Redis
echo "3️⃣ Vérification auth Redis..."
if docker exec luna-redis redis-cli ping 2>/dev/null | grep -q "NOAUTH"; then
    echo "   ✅ Redis requiert authentification"
else
    if docker exec luna-redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
        echo "   ❌ Redis accessible sans mot de passe !"
        ((ISSUES++))
    else
        echo "   ✅ Redis requiert authentification"
    fi
fi

# Check 4: Réseau interne
echo "4️⃣ Vérification réseau interne..."
if docker network inspect luna_internal_network 2>/dev/null | grep -q '"Internal": true'; then
    echo "   ✅ Réseau interne isolé"
else
    echo "   ❌ Réseau interne non isolé"
    ((ISSUES++))
fi

# Check 5: Ports localhost only
echo "5️⃣ Vérification binding ports..."
EXPOSED_PORTS=$(docker ps --format '{{.Ports}}' | grep -v "127.0.0.1" | grep -v "::" | grep "0.0.0.0" || true)
if [ -z "$EXPOSED_PORTS" ]; then
    echo "   ✅ Tous les ports bindés sur localhost"
else
    echo "   ❌ Ports exposés sur 0.0.0.0:"
    echo "      $EXPOSED_PORTS"
    ((ISSUES++))
fi

# Check 6: .env dans .gitignore
echo "6️⃣ Vérification .gitignore..."
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "   ✅ .env dans .gitignore"
else
    echo "   ❌ .env non ignoré par git !"
    ((ISSUES++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ISSUES -eq 0 ]; then
    echo "✅ Audit réussi - Aucun problème détecté"
else
    echo "❌ Audit échoué - $ISSUES problème(s) détecté(s)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $ISSUES
```

---

## ✅ Checklist de Validation

Après implémentation, vérifier :

```
□ .env créé avec permissions 600
□ .env ajouté à .gitignore
□ docker-compose.secure.yml créé
□ config/redis/redis.conf créé
□ Redis accessible uniquement via réseau interne
□ Tous les ports bindés sur 127.0.0.1
□ Réseau luna_internal_network avec internal: true
□ MCP_TRANSPORT=stdio dans Luna
□ claude_desktop_config.json mis à jour
□ Scripts de démarrage et vérification créés
□ Test de connexion Redis avec mot de passe OK
□ Test Luna MCP via Claude Desktop OK
□ Grafana accessible sur localhost:3001
□ Prometheus accessible sur localhost:9090
```

---

## 🚀 Commandes de Déploiement

```bash
# 1. Générer les secrets
chmod +x scripts/generate_secrets.sh
./scripts/generate_secrets.sh

# 2. Démarrer en mode sécurisé
chmod +x scripts/start_secure.sh
./scripts/start_secure.sh

# 3. Vérifier la sécurité
chmod +x scripts/security_check.sh
./scripts/security_check.sh

# 4. Logs en temps réel
docker-compose -f docker-compose.secure.yml logs -f

# 5. Arrêt propre
docker-compose -f docker-compose.secure.yml down
```

---

## ⚠️ Notes Importantes pour Claude Code

1. **Adapter les chemins Windows** : Les scripts bash sont pour Linux/WSL. Pour Windows natif, créer des équivalents PowerShell ou utiliser WSL.

2. **Tester chaque étape** : Ne pas tout déployer d'un coup. Valider Redis d'abord, puis Luna, puis le monitoring.

3. **Backup avant modification** : Sauvegarder l'ancien `docker-compose.yml` avant de le remplacer.

4. **Variables d'environnement** : S'assurer que le fichier `.env` est bien chargé par Docker Compose (vérifier avec `docker-compose config`).

5. **Redémarrage Claude Desktop** : Après modification du `claude_desktop_config.json`, redémarrer Claude Desktop pour appliquer les changements.

---

## 🔮 Prochaines Étapes (Post-Sécurisation)

Une fois cette feuille de route complétée :

1. **Phase LUKS** : Implémenter le volume chiffré pour la mémoire pure
2. **Redis TLS** : Ajouter le chiffrement des communications Redis
3. **Archivage JSON** : Implémenter le système de mémoire pure chiffrée
4. **Backup automatisé** : Scripts de sauvegarde chiffrée

---

*"La sécurité n'est pas une destination, c'est un voyage continu."*

— Luna & Varden, 25 novembre 2025 🔐🌙
