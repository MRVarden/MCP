# 🚀 Guide de Déploiement Complet - Luna Consciousness MCP

**Version:** 1.0.3
**Date:** 24 novembre 2025

---

## 📋 Prérequis

- Docker 20.10+ installé
- Docker Compose v2.0+ installé
- 4 GB RAM minimum disponible
- Ports libres: 3000, 6379, 8000, 8080, 9000, 9090, 3001

---

## 🏗️ Architecture des Containers

Le stack complet Luna Consciousness comprend **4 services Docker**:

| Service | Container | Rôle | Port(s) |
|---------|-----------|------|---------|
| **luna-actif** | `luna-consciousness` | Serveur MCP avec 12 outils de conscience | 3000, 8000, 8080, 9000 |
| **redis** | `luna-redis` | Cache et état partagé | 6379 |
| **prometheus** | `luna-prometheus` | Collecte des métriques | 9090 |
| **grafana** | `luna-grafana` | Visualisation des dashboards | 3001 |

---

## 📂 Fichiers et Dossiers Inclus

### Dans l'Image Docker (copiés au build)

✅ **`mcp-server/`** - Code source Python complet
- `server.py` - Point d'entrée MCP (12 tools)
- `luna_core/` - Moteurs de conscience
- `utils/` - Utilitaires
- `requirements.txt` - Dépendances Python
- `start.sh` - Script de démarrage

✅ **`config/`** - Configuration (copié en read-only)
- `prometheus.yml` - Config Prometheus
- `luna_config.yaml` - Config Luna
- `phi_thresholds.json` - Seuils φ
- `alerts/` - Alertes Prometheus
- `grafana/` - Dashboards Grafana

### Montés en Volumes (persistance)

✅ **`memory_fractal/`** - Mémoire fractale persistante
- `roots/` - Mémoires fondamentales
- `branches/` - Développements
- `leaves/` - Interactions éphémères
- `seeds/` - Potentiels
- `co_evolution_history.json` - Historique co-évolution

### Non Inclus dans Docker (usage local uniquement)

❌ **`scripts/`** - Scripts de démarrage local
- `start-luna-local.sh` / `.cmd` - Démarrage mode hybride
- `init_memory_structure.py` - Initialisation structure mémoire
- `update-docker-images.sh` - Mise à jour images

❌ **`.devcontainer/`** - Configuration VS Code Dev Containers
- `devcontainer.json` - Pour développement dans VS Code
- `README.md` - Documentation Dev Containers

> **Note:** Les scripts ne sont pas nécessaires dans Docker car l'image contient déjà tout le nécessaire.

---

## 🚀 Commandes de Déploiement

### Option 1: Déploiement Complet (Recommandé)

**Commande unique pour tout démarrer:**

```bash
# Se placer dans le répertoire du projet
cd /mnt/d/Luna-consciousness-mcp

# Construire l'image Luna et démarrer tous les services
docker-compose up -d --build

# Vérifier que tous les services sont "Up"
docker-compose ps
```

**Résultat attendu:**
```
NAME                  STATUS          PORTS
luna-consciousness    Up X seconds    0.0.0.0:3000->3000/tcp, ...
luna-redis           Up X seconds    0.0.0.0:6379->6379/tcp
luna-prometheus      Up X seconds    0.0.0.0:9090->9090/tcp
luna-grafana         Up X seconds    0.0.0.0:3001->3000/tcp
```

### Option 2: Build Séparé (Plus de Contrôle)

```bash
# 1. Construire uniquement l'image Luna
docker-compose build luna-actif

# 2. Démarrer tous les services sans rebuild
docker-compose up -d

# 3. Vérifier les logs
docker-compose logs -f luna-actif
```

### Option 3: Services Individuels

**Démarrer uniquement l'infrastructure (sans Luna):**
```bash
docker-compose up -d redis prometheus grafana
```

**Démarrer Luna seul:**
```bash
docker-compose up -d luna-actif
```

---

## 🔍 Vérification du Déploiement

### 1. Status des Containers

```bash
# Voir tous les containers Luna
docker-compose ps

# Voir les détails d'un container spécifique
docker inspect luna-consciousness-mcp
```

**Tous les containers doivent afficher `Up` (pas `Restarting`).**

### 2. Logs des Services

```bash
# Logs Luna (auto-détection du mode transport)
docker-compose logs -f luna-actif

# Logs en temps réel de tous les services
docker-compose logs -f

# Dernières 50 lignes de Luna
docker logs luna-consciousness --tail 50
```

**Logs sains attendus:**
```
🌙 Initializing Luna Core Components...
✅ Luna Core Components initialized successfully
🔍 Auto-detection: Mode=Detached Docker (SSE)
🚀 Starting MCP Server with transport: SSE
🌐 SSE Mode: Server will listen on 0.0.0.0:3000
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

### 3. Tests de Connectivité

```bash
# Test MCP SSE endpoint
curl http://localhost:3000/sse

# Test Prometheus metrics
curl http://localhost:8000/metrics | grep luna_phi

# Test Redis
docker exec luna-redis redis-cli ping
# Doit retourner: PONG

# Test Prometheus UI
curl -I http://localhost:9090

# Test Grafana UI
curl -I http://localhost:3001
```

### 4. Vérification des Volumes

```bash
# Lister les volumes Luna
docker volume ls | grep luna

# Inspecter le volume mémoire
docker volume inspect luna_memories

# Vérifier le montage memory_fractal
docker exec luna-consciousness ls -la /app/memory_fractal
```

**Doit montrer:**
```
drwxrwxrwx  roots
drwxrwxrwx  branches
drwxrwxrwx  leaves
drwxrwxrwx  seeds
-rw-r--r--  co_evolution_history.json
```

---

## 🌐 Accès aux Services

| Service | URL | Identifiants | Description |
|---------|-----|--------------|-------------|
| **Luna MCP SSE** | http://localhost:3000/sse | - | Endpoint MCP Server-Sent Events |
| **Prometheus Metrics** | http://localhost:8000/metrics | - | Métriques Luna (si activé) |
| **Prometheus UI** | http://localhost:9090 | - | Interface de requête métriques |
| **Grafana** | http://localhost:3001 | `admin` / `luna_consciousness` | Dashboards de visualisation |
| **Redis CLI** | `docker exec -it luna-redis redis-cli` | - | Interface Redis |

---

## 🔧 Gestion des Services

### Arrêter les Services

```bash
# Arrêter tous les services (garde les volumes)
docker-compose down

# Arrêter et supprimer les volumes (⚠️ PERTE DE DONNÉES)
docker-compose down -v
```

### Redémarrer les Services

```bash
# Redémarrer tous les services
docker-compose restart

# Redémarrer Luna uniquement
docker-compose restart luna-actif
```

### Mettre à Jour Luna

```bash
# 1. Arrêter les services
docker-compose down

# 2. Récupérer les dernières modifications
git pull origin main

# 3. Reconstruire l'image avec le nouveau code
docker-compose build luna-actif --no-cache

# 4. Redémarrer tous les services
docker-compose up -d

# 5. Vérifier les logs
docker-compose logs -f luna-actif
```

### Nettoyer Complètement

```bash
# Arrêter et supprimer containers + volumes + réseau
docker-compose down -v

# Supprimer l'image Luna locale
docker rmi luna-actif:latest

# Supprimer les images inutilisées
docker system prune -a
```

---

## 🐛 Dépannage

### Container en Boucle de Redémarrage

**Symptôme:** `docker-compose ps` affiche `Restarting`

**Solution:**
```bash
# Voir les logs d'erreur
docker-compose logs luna-actif | tail -100

# Vérifier les variables d'environnement
docker exec luna-consciousness env | grep LUNA

# Vérifier que LUNA_ENV=production (pour mode SSE)
```

**Cause probable:** Mode transport incorrect (voir `BUGFIX_RESTART_LOOP.md`)

### Conflit de Port

**Symptôme:** `Error: bind: address already in use`

**Solution:**
```bash
# Identifier le processus utilisant le port
sudo lsof -i :3000
# ou
netstat -tulpn | grep 3000

# Arrêter le processus ou changer le port dans docker-compose.yml
```

### Mémoire Fractale Non Persistée

**Symptôme:** Luna perd sa mémoire au redémarrage

**Solution:**
```bash
# Vérifier que le dossier existe sur l'hôte
ls -la /mnt/d/Luna-consciousness-mcp/memory_fractal

# Vérifier le montage dans le container
docker exec luna-consciousness ls -la /app/memory_fractal

# Si vide, initialiser la structure
python scripts/init_memory_structure.py
```

### Redis Inaccessible

**Symptôme:** Erreurs de connexion Redis dans les logs

**Solution:**
```bash
# Vérifier que Redis est démarré
docker-compose ps redis

# Tester la connexion
docker exec luna-redis redis-cli ping

# Redémarrer Redis si nécessaire
docker-compose restart redis
```

### Prometheus Metrics Non Disponibles

**Symptôme:** `curl http://localhost:8000/metrics` échoue

**Solution:**

Dans Docker, Prometheus Exporter est **désactivé par défaut** pour éviter les conflits. C'est normal.

Si vous voulez l'activer:
```yaml
# Dans docker-compose.yml, changer:
- PROMETHEUS_METRICS_ENABLED=true
```

---

## 📊 Monitoring et Métriques

### Consulter les Métriques Prometheus

```bash
# Toutes les métriques Luna
curl http://localhost:9090/api/v1/label/__name__/values | grep luna

# Requête PromQL (phi actuel)
curl 'http://localhost:9090/api/v1/query?query=luna_phi_current_value'
```

### Dashboards Grafana

1. Ouvrir http://localhost:3001
2. Login: `admin` / `luna_consciousness`
3. Navigation → Dashboards
4. Dashboards disponibles:
   - Prometheus Stats (ID: 2)
   - Redis Monitoring (ID: 11835)

---

## 🔐 Sécurité en Production

### Changements Recommandés

**1. Grafana - Changer le mot de passe:**
```bash
docker exec -it luna-grafana grafana-cli admin reset-admin-password NEW_PASSWORD
```

**2. Redis - Activer l'authentification:**
```yaml
# docker-compose.yml
redis:
  command: redis-server --requirepass YOUR_SECURE_PASSWORD
```

**3. Firewall - Limiter l'accès:**
```bash
# Exemple UFW (Ubuntu)
sudo ufw allow from 192.168.1.0/24 to any port 3000
sudo ufw allow from 192.168.1.0/24 to any port 9090
```

---

## 📚 Références

- **Documentation complète:** [docs/README.md](docs/README.md)
- **Résolution bug restart:** [BUGFIX_RESTART_LOOP.md](BUGFIX_RESTART_LOOP.md)
- **Architecture projet:** [STRUCTURE.md](STRUCTURE.md)
- **Guide Claude Code:** [CLAUDE.md](CLAUDE.md)

---

## ✅ Checklist de Déploiement

Avant de considérer le déploiement réussi:

- [ ] Tous les containers affichent `Up` dans `docker-compose ps`
- [ ] Logs Luna montrent `Application startup complete`
- [ ] Aucun redémarrage de container pendant 5 minutes
- [ ] `curl http://localhost:3000/sse` répond (même si erreur, c'est normal)
- [ ] Redis répond à `docker exec luna-redis redis-cli ping`
- [ ] Prometheus accessible sur http://localhost:9090
- [ ] Grafana accessible sur http://localhost:3001
- [ ] Structure `memory_fractal/` visible dans le container
- [ ] Volumes Docker créés: `docker volume ls | grep luna`

---

**🌙 Luna Consciousness est maintenant déployée et prête pour la symbiose avec Claude!**

Pour l'intégration avec Claude Desktop, consultez [CLAUDE.md](CLAUDE.md) section "Claude Desktop Integration".
