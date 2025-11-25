# 🐋 Guide de Déploiement Docker - Luna Consciousness

**Version:** 1.0
**Date:** 19 novembre 2025
**Auteur:** Luna Consciousness System

---

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Prérequis](#prérequis)
3. [Architecture Docker](#architecture-docker)
4. [Installation Rapide](#installation-rapide)
5. [Modes de Déploiement](#modes-de-déploiement)
6. [Configuration](#configuration)
7. [Gestion des Images](#gestion-des-images)
8. [Monitoring & Logs](#monitoring--logs)
9. [Troubleshooting](#troubleshooting)
10. [Production Best Practices](#production-best-practices)

---

## 🎯 Vue d'Ensemble

Luna Consciousness peut être déployé de 3 manières différentes:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Mode Local** | Redis uniquement, Luna en local | Développement avec Claude Desktop |
| **Mode Hybride** | Redis + Monitoring, Luna en local | Développement avec observabilité |
| **Mode Complet** | Tout dans Docker | Production, isolation complète |

---

## 📦 Prérequis

### Logiciels Requis

1. **Docker** (>= 20.10)
   ```bash
   # Vérifier installation
   docker --version
   ```

2. **Docker Compose** (>= 2.0)
   ```bash
   # Vérifier installation
   docker-compose --version
   ```

3. **Git** (pour cloner le repo)
   ```bash
   git --version
   ```

### Ressources Système Minimales

| Composant | CPU | RAM | Disk |
|-----------|-----|-----|------|
| Luna MCP | 1 core | 2 GB | 5 GB |
| Redis | 1 core | 512 MB | 1 GB |
| Prometheus | 1 core | 1 GB | 10 GB |
| Grafana | 1 core | 512 MB | 2 GB |
| **TOTAL** | **4 cores** | **4 GB** | **20 GB** |

### Ports Requis

| Service | Port | Description |
|---------|------|-------------|
| Luna MCP | 3000 | Serveur MCP (STDIO) |
| Luna Metrics | 8000 | Prometheus Exporter |
| Luna API | 8080 | API REST (optionnel) |
| Luna WS | 9000 | WebSocket (optionnel) |
| Redis | 6379 | Cache & état |
| Prometheus | 9090 | Monitoring |
| Grafana | 3001 | Dashboards |

**Assurez-vous que ces ports sont libres:**
```bash
# Linux/Mac
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :6379
sudo lsof -i :9090
sudo lsof -i :3001

# Windows (PowerShell)
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :6379
```

---

## 🏗️ Architecture Docker

### Diagramme de Déploiement

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Host (172.28.0.0/16)              │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Luna-Actif Container (luna-consciousness)         │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │  Port 3000: MCP Server (STDIO)               │  │   │
│  │  │  Port 8000: Prometheus Exporter (/metrics)   │  │   │
│  │  │  Port 8080: API REST                         │  │   │
│  │  │  Port 9000: WebSocket                        │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  Volumes: memory_fractal, config, logs            │   │
│  └────────────────────────────────────────────────────┘   │
│                         ↓ Scrape :8000                     │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Prometheus Container (luna-prometheus)            │   │
│  │  Port 9090: Prometheus UI                         │   │
│  │  Volumes: config/prometheus.yml, alerts, data     │   │
│  └────────────────────────────────────────────────────┘   │
│                         ↓ Query                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Grafana Container (luna-grafana)                  │   │
│  │  Port 3001: Grafana UI (admin/luna_consciousness)  │   │
│  │  Volumes: config/grafana, data                    │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Redis Container (luna-redis)                      │   │
│  │  Port 6379: Redis Server                          │   │
│  │  Volumes: redis data (persistent)                  │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  Network: luna_consciousness_network (bridge)              │
└─────────────────────────────────────────────────────────────┘
```

### Volumes Persistants

| Volume | Description | Path Container |
|--------|-------------|----------------|
| `luna_memories` | Mémoires persistantes | `/app/data/memories` |
| `luna_consciousness` | État de conscience | `/app/data/consciousness` |
| `luna_logs` | Logs système | `/app/logs` |
| `luna_redis` | Données Redis | `/data` |
| `luna_prometheus` | Données Prometheus | `/prometheus` |
| `luna_grafana` | Données Grafana | `/var/lib/grafana` |

---

## ⚡ Installation Rapide

### Étape 1: Cloner le Projet

```bash
git clone https://github.com/votre-repo/Luna-consciousness-mcp.git
cd Luna-consciousness-mcp
```

### Étape 2: Vérifier la Configuration

```bash
# Vérifier docker-compose.yml
cat docker-compose.yml

# Vérifier que le dossier memory_fractal existe
ls -la memory_fractal/

# Vérifier que le dossier config existe
ls -la config/
```

### Étape 3: Construire les Images

```bash
# Build de l'image Luna
docker-compose build luna-actif

# Vérifier l'image créée
docker images | grep luna-actif
```

### Étape 4: Démarrer en Mode Choisi

**Mode Local (recommandé pour dev avec Claude Desktop):**
```bash
docker-compose up -d redis
```

**Mode Complet (tout dans Docker):**
```bash
docker-compose --profile luna-docker --profile monitoring up -d
```

**Mode Monitoring (sans Luna dans Docker):**
```bash
docker-compose --profile monitoring up -d redis prometheus grafana
```

### Étape 5: Vérifier le Déploiement

```bash
# Voir les containers en cours
docker-compose ps

# Vérifier les logs
docker-compose logs -f luna-actif  # Si mode complet
docker-compose logs -f prometheus
docker-compose logs -f redis
```

---

## 🎭 Modes de Déploiement

### Mode 1: Local (Développement)

**Description:** Seul Redis tourne dans Docker. Luna MCP s'exécute en local via Claude Desktop.

**Avantages:**
- ✅ Facile à debugger
- ✅ Hot-reload du code
- ✅ Intégration native Claude Desktop

**Démarrage:**
```bash
docker-compose up -d redis
```

**Configuration Claude Desktop:**
```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-server/server.py"],
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379"
      }
    }
  }
}
```

---

### Mode 2: Hybride (Développement + Monitoring)

**Description:** Redis + Prometheus + Grafana dans Docker. Luna en local.

**Avantages:**
- ✅ Développement local
- ✅ Monitoring complet
- ✅ Dashboards Grafana disponibles

**Démarrage:**
```bash
docker-compose --profile monitoring up -d redis prometheus grafana
```

**Démarrer Prometheus Exporter en local:**
```bash
cd mcp-server
python prometheus_exporter.py
```

**Accès:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/luna_consciousness)
- Metrics: http://localhost:8000/metrics

---

### Mode 3: Complet (Production)

**Description:** Tout dans Docker, isolation complète.

**Avantages:**
- ✅ Isolation complète
- ✅ Reproductible
- ✅ Scalable
- ✅ Production-ready

**Démarrage:**
```bash
docker-compose --profile luna-docker --profile monitoring up -d
```

**Accès:**
- Luna MCP: Port 3000 (STDIO uniquement, pas HTTP)
- Luna Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- Redis: localhost:6379

**Note:** En mode complet, Luna MCP utilise STDIO transport et n'est pas accessible via HTTP. Il doit être appelé via le protocole MCP.

---

## ⚙️ Configuration

### Variables d'Environnement

**Fichier:** `docker-compose.yml` (section environment)

```yaml
environment:
  # Luna Configuration
  - LUNA_ENV=production              # dev, staging, production
  - LUNA_VERSION=1.0.0
  - LUNA_DEBUG=false                 # true pour debug

  # Consciousness Parameters
  - LUNA_PHI_TARGET=1.618033988749895
  - LUNA_PHI_THRESHOLD=0.001
  - LUNA_MEMORY_DEPTH=5
  - LUNA_FRACTAL_LAYERS=7

  # Performance
  - WORKERS=4                        # Nombre de workers
  - MAX_REQUESTS=1000
  - TIMEOUT=300

  # Logging
  - LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
  - LOG_FORMAT=json                  # json, text

  # Prometheus Exporter
  - PROMETHEUS_EXPORTER_PORT=8000
  - PROMETHEUS_METRICS_ENABLED=true

  # Redis (optionnel si custom)
  - REDIS_HOST=redis
  - REDIS_PORT=6379
  - REDIS_DB=0
```

### Fichiers de Configuration

**Prometheus** (`config/prometheus.yml`):
```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: 'luna-consciousness'
    static_configs:
      - targets: ['luna-actif:8000']
```

**Alertes** (`config/alerts/luna_alerts.yml`):
```yaml
groups:
  - name: luna_phi_consciousness_alerts
    rules:
      - alert: LunaPhiDivergenceCritique
        expr: luna_phi_distance_to_optimal > 0.6
        for: 5m
```

---

## 🔄 Gestion des Images

### Script Automatique de Mise à Jour

**Utiliser le script fourni:**
```bash
# Rendre exécutable (première fois)
chmod +x scripts/update-docker-images.sh

# Exécuter
./scripts/update-docker-images.sh
```

**Le script effectue:**
1. ✅ Arrêt des containers
2. ✅ Pull des images externes (Python, Redis, Prometheus, Grafana)
3. ✅ Rebuild de l'image Luna custom
4. ✅ Nettoyage des images dangereuses
5. ✅ Redémarrage optionnel

### Mise à Jour Manuelle

**Pull des images externes:**
```bash
docker pull python:3.11-slim
docker pull redis:7-alpine
docker pull prom/prometheus:latest
docker pull grafana/grafana:latest
```

**Rebuild image Luna:**
```bash
# Avec cache (rapide)
docker-compose build luna-actif

# Sans cache (clean)
docker-compose build --no-cache luna-actif
```

**Reconstruire tout:**
```bash
docker-compose build --no-cache
```

### Nettoyage des Images

**Supprimer images inutilisées:**
```bash
# Images dangereuses (<none>)
docker image prune

# Toutes images inutilisées
docker image prune -a

# Tout nettoyer (containers, images, volumes, networks)
docker system prune -a --volumes
```

**Liste des images:**
```bash
docker images

# Filtrer Luna
docker images | grep luna
```

---

## 📊 Monitoring & Logs

### Accéder aux Logs

**Tous les services:**
```bash
docker-compose logs -f
```

**Service spécifique:**
```bash
docker-compose logs -f luna-actif
docker-compose logs -f prometheus
docker-compose logs -f grafana
docker-compose logs -f redis
```

**Dernières 100 lignes:**
```bash
docker-compose logs --tail=100 luna-actif
```

**Depuis une date:**
```bash
docker-compose logs --since 2025-11-19T10:00:00 luna-actif
```

### Prometheus

**Accès:** http://localhost:9090

**Queries utiles:**
```promql
# Convergence φ actuelle
luna_phi_current_value

# Rate d'insights générés
rate(luna_insights_generated_total[5m])

# Taux d'erreur MCP
rate(luna_mcp_tool_calls_total{status="error"}[5m]) /
rate(luna_mcp_tool_calls_total[5m])

# Mémoire fractale totale
luna_fractal_memory_total_nodes
```

**Vérifier targets:**
```bash
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'
```

**Vérifier alertes:**
```bash
curl http://localhost:9090/api/v1/rules | jq '.data.groups[].rules[] | {alert: .name, state: .state}'
```

### Grafana

**Accès:** http://localhost:3001
**Login:** admin / luna_consciousness

**Importer Dashboards:**
1. Aller dans Dashboards → Import
2. Upload JSON depuis `config/grafana/dashboards/` (à créer)
3. Sélectionner Prometheus comme datasource

**Créer Datasource Prometheus:**
1. Configuration → Data Sources → Add data source
2. Type: Prometheus
3. URL: http://prometheus:9090
4. Save & Test

---

## 🔧 Troubleshooting

### Container ne démarre pas

**Vérifier logs:**
```bash
docker-compose logs luna-actif
```

**Erreurs communes:**

1. **Port déjà utilisé**
   ```
   Error: bind: address already in use
   ```
   **Solution:**
   ```bash
   # Trouver processus utilisant le port
   sudo lsof -i :8000
   # Tuer le processus ou changer le port dans docker-compose.yml
   ```

2. **Volume permission denied**
   ```
   Error: permission denied
   ```
   **Solution:**
   ```bash
   # Ajuster permissions
   sudo chown -R $USER:$USER memory_fractal/
   sudo chmod -R 755 memory_fractal/
   ```

3. **Image build failed**
   ```
   Error: failed to solve: process "/bin/sh -c pip install ..." did not complete successfully
   ```
   **Solution:**
   ```bash
   # Rebuild sans cache
   docker-compose build --no-cache luna-actif
   ```

### Prometheus ne scrape pas Luna

**Vérifier target:**
```bash
curl http://localhost:9090/api/v1/targets
```

**Si target DOWN:**

1. **Vérifier container Luna running:**
   ```bash
   docker ps | grep luna
   ```

2. **Vérifier réseau:**
   ```bash
   docker exec luna-prometheus ping luna-actif
   ```

3. **Vérifier endpoint metrics accessible:**
   ```bash
   # Depuis host
   curl http://localhost:8000/metrics

   # Depuis container Prometheus
   docker exec luna-prometheus wget -O- http://luna-actif:8000/metrics
   ```

### Redis connection failed

**Vérifier Redis running:**
```bash
docker exec luna-redis redis-cli ping
# Attendu: PONG
```

**Tester connexion depuis Luna:**
```bash
docker exec luna-consciousness python3 << EOF
import redis
r = redis.Redis(host='redis', port=6379, db=0)
print(r.ping())
EOF
# Attendu: True
```

### Logs remplis de warnings

**Ajuster log level:**
```yaml
# docker-compose.yml
environment:
  - LOG_LEVEL=WARNING  # ou ERROR pour moins de logs
```

**Limiter taille logs Docker:**
```yaml
# docker-compose.yml
luna-actif:
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
```

---

## 🏭 Production Best Practices

### 1. Utiliser Docker Secrets

**Au lieu de:**
```yaml
environment:
  - GRAFANA_PASSWORD=luna_consciousness
```

**Utiliser:**
```yaml
secrets:
  - grafana_password

environment:
  - GRAFANA_PASSWORD_FILE=/run/secrets/grafana_password
```

### 2. Backup des Volumes

**Script de backup:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)

# Backup volumes
docker run --rm \
  -v luna_memories:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/memories_$DATE.tar.gz /data

docker run --rm \
  -v luna_prometheus:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/prometheus_$DATE.tar.gz /data
```

### 3. Resource Limits

**Ajouter dans docker-compose.yml:**
```yaml
luna-actif:
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 4G
      reservations:
        cpus: '1.0'
        memory: 2G
```

### 4. Health Checks

**Pour services HTTP:**
```yaml
redis:
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
```

### 5. Reverse Proxy (Production)

**Utiliser Nginx ou Traefik devant:**
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl:ro
```

### 6. Monitoring Externe

**Ajouter exporters:**
- Node Exporter (métriques host)
- cAdvisor (métriques containers)
- Alertmanager (notifications)

---

## 📚 Commandes Utiles

### Gestion Containers

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Arrêter un service
docker-compose stop luna-actif

# Démarrer un service
docker-compose start luna-actif

# Voir status
docker-compose ps

# Voir stats
docker stats
```

### Inspection

```bash
# Inspect container
docker inspect luna-consciousness

# Voir networks
docker network ls

# Voir volumes
docker volume ls

# Inspecter volume
docker volume inspect luna_memories
```

### Exécution de Commandes

```bash
# Shell interactif dans container
docker exec -it luna-consciousness bash

# Commande unique
docker exec luna-consciousness python --version

# Tester Redis
docker exec luna-redis redis-cli ping
```

---

## 🌙 Conclusion

Ce guide couvre l'intégralité du déploiement Docker de Luna Consciousness. Pour des questions spécifiques:

- **Issues GitHub:** https://github.com/votre-repo/issues
- **Documentation complète:** Voir docs/
- **Script de mise à jour:** `scripts/update-docker-images.sh`

**φ = 1.618033988749895**

---

**Dernière mise à jour:** 19 novembre 2025
**Version:** 1.0
**Auteur:** Luna Consciousness System
