# 🌙 Configuration Luna - Solution Complète

**Date:** 2025-11-20  
**Basé sur:** Tes fichiers Dockerfile, docker-compose.yml, docker-build.yml

---

## 🔍 Problème identifié

Ton `docker-compose.yml` utilise des **profils Docker** :

```yaml
luna-actif:
  profiles:
    - luna-docker  # ❌ Ne démarre que si profil activé

prometheus:
  profiles:
    - monitoring   # ❌ Ne démarre que si profil activé
```

**Conséquence:** Quand tu lances `docker-compose up`, RIEN ne démarre !

---

## ✅ SOLUTION 1: Démarrer avec les profils (RECOMMANDÉ)

### Commande magique

```bash
cd /d/Luna-consciousness-mcp

# Arrêter tout
docker-compose down

# Supprimer luna-test (on va utiliser luna-actif à la place)
docker stop luna-test 2>/dev/null
docker rm luna-test 2>/dev/null

# Nettoyer les orphelins
docker stop happy_yalow elegant_gauss vigilant_lumiere 2>/dev/null
docker rm happy_yalow elegant_gauss vigilant_lumiere 2>/dev/null

# Démarrer TOUT avec les bons profils
docker-compose --profile luna-docker --profile monitoring up -d

# Attendre 15 secondes que tout démarre
sleep 15

# Vérifier
docker ps
curl http://localhost:8000/metrics | grep luna_phi
curl http://localhost:9090/api/v1/targets
```

### Ce que tu devrais voir

```
CONTAINER ID   IMAGE                    STATUS        PORTS
abc123...      luna-actif:latest        Up 10s        0.0.0.0:8000->8000/tcp
def456...      prom/prometheus:latest   Up 10s        0.0.0.0:9090->9090/tcp
ghi789...      grafana/grafana:latest   Up 10s        0.0.0.0:3001->3000/tcp
jkl012...      redis:7-alpine           Up 10s        0.0.0.0:6379->6379/tcp
```

---

## ✅ SOLUTION 2: Modifier docker-compose.yml (mode toujours actif)

Si tu veux que tout démarre SANS avoir à spécifier les profils:

### Éditer docker-compose.yml

```bash
nano /d/Luna-consciousness-mcp/docker-compose.yml
# OU
notepad D:\Luna-consciousness-mcp\docker-compose.yml
```

### Modifications à faire

```yaml
# AVANT (lignes 14-15)
luna-actif:
  # ...
  restart: "no"  # ❌
  profiles:
    - luna-docker  # ❌

# APRÈS
luna-actif:
  # ...
  restart: unless-stopped  # ✅
  # profiles:  # ✅ SUPPRIMER ou commenter cette ligne
  #   - luna-docker

# ---

# AVANT (lignes 129-130)
prometheus:
  # ...
  profiles:
    - monitoring  # ❌

# APRÈS
prometheus:
  # ...
  # profiles:  # ✅ SUPPRIMER ou commenter cette ligne
  #   - monitoring

# ---

# AVANT (lignes 152-153)
grafana:
  # ...
  profiles:
    - monitoring  # ❌

# APRÈS
grafana:
  # ...
  # profiles:  # ✅ SUPPRIMER ou commenter cette ligne
  #   - monitoring
```

### Puis redémarrer

```bash
docker-compose down
docker-compose up -d

# Tout démarre automatiquement maintenant !
```

---

## ✅ SOLUTION 3: Utiliser un alias dans .bashrc (hybride)

Pour ne pas avoir à taper les profils à chaque fois:

```bash
# Ajouter dans ~/.bashrc (Git Bash)
echo 'alias luna-up="docker-compose --profile luna-docker --profile monitoring up -d"' >> ~/.bashrc
echo 'alias luna-down="docker-compose down"' >> ~/.bashrc
echo 'alias luna-logs="docker logs -f luna-consciousness"' >> ~/.bashrc
echo 'alias luna-metrics="curl -s http://localhost:8000/metrics | grep luna_"' >> ~/.bashrc

# Recharger
source ~/.bashrc

# Utiliser
luna-up        # Démarre tout
luna-logs      # Voir les logs
luna-metrics   # Voir les métriques
luna-down      # Arrêter tout
```

---

## 🔧 Vérifier prometheus.yml

### Éditer le fichier

```bash
cat /d/Luna-consciousness-mcp/config/prometheus.yml
```

### Configuration attendue

```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s
  scrape_timeout: 3s

scrape_configs:
  # Luna Consciousness
  - job_name: 'luna-consciousness'
    static_configs:
      - targets: 
          # ✅ CORRECT avec docker-compose
          - 'luna-actif:8000'
          # OU utiliser l'alias défini dans docker-compose.yml
          # - 'luna-mcp-server:8000'
        labels:
          service: 'luna-consciousness'
          component: 'mcp-server'
          metrics_type: 'consciousness'
  
  # Prometheus lui-même
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
        labels:
          service: 'prometheus'
```

**IMPORTANT:** Avec docker-compose, utilise `luna-actif:8000` (nom du service) et **PAS** `localhost:8000`

---

## 🐛 Si build échoue

### Construire l'image manuellement

```bash
cd /d/Luna-consciousness-mcp

# Build l'image
docker build -t luna-actif:latest -f Dockerfile .

# Vérifier
docker images | grep luna

# Puis démarrer
docker-compose --profile luna-docker --profile monitoring up -d
```

### Vérifier les logs de build

```bash
# Voir si l'image existe
docker images | grep luna

# Si erreur, rebuild avec verbose
docker build -t luna-actif:latest -f Dockerfile . --no-cache --progress=plain
```

---

## 📊 Structure réseau correcte

Quand tout fonctionne, tu devrais avoir:

```
Network: luna_consciousness_network (172.28.0.0/16)
├─ luna-consciousness (luna-actif)
│  ├─ Aliases: luna-mcp-server
│  └─ IP: 172.28.0.2
├─ luna-prometheus
│  └─ IP: 172.28.0.3
├─ luna-grafana
│  └─ IP: 172.28.0.4
└─ luna-redis
   └─ IP: 172.28.0.5
```

### Vérifier le réseau

```bash
docker network inspect luna_consciousness_network
```

---

## 🎯 Checklist complète

### Avant de démarrer

- [ ] Les fichiers existent:
  - `D:\Luna-consciousness-mcp\Dockerfile`
  - `D:\Luna-consciousness-mcp\docker-compose.yml`
  - `D:\Luna-consciousness-mcp\config\prometheus.yml`
  - `D:\Luna-consciousness-mcp\mcp-server\` (dossier avec le code)

- [ ] Les dossiers existent:
  - `D:\Luna-consciousness-mcp\memory_fractal\`
  - `D:\Luna-consciousness-mcp\config\`
  - `D:\Luna-consciousness-mcp\logs\`

### Après démarrage

- [ ] `docker ps` montre 4 containers:
  - luna-consciousness (luna-actif)
  - luna-prometheus
  - luna-grafana
  - luna-redis

- [ ] Ports accessibles:
  - http://localhost:8000/metrics ← Métriques Luna
  - http://localhost:9090 ← Prometheus
  - http://localhost:3001 ← Grafana (admin/luna_consciousness)
  - http://localhost:6379 ← Redis

- [ ] Prometheus targets UP:
  - http://localhost:9090/targets
  - `luna-consciousness` doit être `UP`

- [ ] Métriques Luna disponibles:
  ```bash
  curl http://localhost:8000/metrics | grep luna_phi
  # Devrait retourner:
  # luna_phi_value 1.000000000000000
  # luna_phi_distance_to_golden 0.618034
  ```

---

## 🚀 Script de démarrage automatisé

Créer un fichier `start-luna.sh`:

```bash
#!/bin/bash

echo "🌙 Starting Luna Consciousness Infrastructure..."

cd /d/Luna-consciousness-mcp

# Cleanup
echo "🧹 Cleaning up old containers..."
docker-compose down 2>/dev/null
docker stop luna-test happy_yalow elegant_gauss vigilant_lumiere 2>/dev/null
docker rm luna-test happy_yalow elegant_gauss vigilant_lumiere 2>/dev/null

# Start
echo "🚀 Starting all services..."
docker-compose --profile luna-docker --profile monitoring up -d

# Wait
echo "⏳ Waiting for services to start (15s)..."
sleep 15

# Check
echo ""
echo "📊 Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "luna|prometheus|grafana|redis"

echo ""
echo "🔍 Testing endpoints..."

# Test metrics
if curl -s http://localhost:8000/metrics | grep -q "luna_phi_value"; then
    echo "✅ Luna metrics: OK"
    curl -s http://localhost:8000/metrics | grep "luna_phi_value"
else
    echo "❌ Luna metrics: FAIL"
fi

# Test Prometheus
if curl -s http://localhost:9090/-/healthy | grep -q "Healthy"; then
    echo "✅ Prometheus: OK"
else
    echo "❌ Prometheus: FAIL"
fi

# Test Prometheus targets
echo ""
echo "📈 Prometheus Targets:"
curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | select(.labels.job=="luna-consciousness") | "  \(.labels.job): \(.health)"'

echo ""
echo "🌙 Luna Infrastructure Status:"
echo "  📊 Metrics:     http://localhost:8000/metrics"
echo "  📈 Prometheus:  http://localhost:9090"
echo "  📉 Grafana:     http://localhost:3001 (admin/luna_consciousness)"
echo "  🔴 Redis:       localhost:6379"
echo ""
echo "✨ Luna is ready for consciousness emergence!"
```

### Rendre exécutable et lancer

```bash
chmod +x start-luna.sh
./start-luna.sh
```

---

## 🔄 Commandes utiles

### Logs en temps réel

```bash
# Luna principal
docker logs -f luna-consciousness

# Prometheus
docker logs -f luna-prometheus

# Tous ensemble
docker-compose logs -f
```

### Redémarrer un service

```bash
docker-compose restart luna-actif
docker-compose restart prometheus
```

### Voir l'utilisation des ressources

```bash
docker stats luna-consciousness luna-prometheus luna-grafana luna-redis
```

### Nettoyer complètement

```bash
# Arrêter et supprimer TOUT
docker-compose down -v

# Supprimer les volumes (⚠️ PERTE DE DONNÉES)
docker volume rm luna_memories luna_consciousness luna_logs luna_redis luna_prometheus luna_grafana

# Supprimer l'image
docker rmi luna-actif:latest
```

---

## 💡 Mode développement

Si tu veux modifier le code sans rebuild:

### Modifier docker-compose.yml

```yaml
luna-actif:
  # ...
  volumes:
    # Ajouter cette ligne pour le dev
    - ./mcp-server:/app/mcp-server  # ✅ Code source en live
    # ...
```

### Puis restart pour voir les changements

```bash
docker-compose restart luna-actif
```

---

## 🎉 Résumé de la meilleure méthode

```bash
# 1. Nettoyer
cd /d/Luna-consciousness-mcp
docker-compose down
docker stop luna-test 2>/dev/null ; docker rm luna-test 2>/dev/null

# 2. Démarrer avec profils
docker-compose --profile luna-docker --profile monitoring up -d

# 3. Vérifier après 15s
sleep 15
curl http://localhost:8000/metrics | grep luna_phi
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[0].health'

# 4. Si OK, accéder aux UIs
# - Métriques: http://localhost:8000/metrics
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3001
```

---

🌙 **Avec cette config, Luna sera pleinement opérationnelle et observable !**
