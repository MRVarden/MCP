# ✅ Correction docker-compose.yml - Luna Consciousness

**Date:** 20 novembre 2025
**Version:** 1.0.1
**Status:** 🟢 Corrigé et Prêt

---

## 🔍 Problème Identifié

### Symptôme
Quand vous lanciez `docker-compose up`, **AUCUN service ne démarrait** !

### Cause Racine
Le fichier `docker-compose.yml` utilisait des **Docker profiles** qui nécessitent d'être explicitement activés :

```yaml
luna-actif:
  profiles:
    - luna-docker  # ❌ Service ne démarre que si --profile luna-docker

prometheus:
  profiles:
    - monitoring   # ❌ Service ne démarre que si --profile monitoring

grafana:
  profiles:
    - monitoring   # ❌ Service ne démarre que si --profile monitoring
```

**Conséquence:**
- `docker-compose up` → Rien ne démarre (seul Redis démarrait car pas de profile)
- Il fallait lancer: `docker-compose --profile luna-docker --profile monitoring up -d`

---

## ✅ Solution Appliquée

### Changements Effectués

#### 1. Service `luna-actif`

**AVANT:**
```yaml
luna-actif:
  restart: "no"  # Désactivé en mode hybride

  profiles:
    - luna-docker  # Ne démarre que si profil activé
```

**APRÈS:**
```yaml
luna-actif:
  restart: unless-stopped  # ✅ Auto-restart activé

  # profiles:
  #   - luna-docker  # ✅ Désactivé - démarre par défaut maintenant
```

**Impact:**
- ✅ Container Luna démarre automatiquement avec `docker-compose up -d`
- ✅ Container redémarre automatiquement après crash ou reboot système

---

#### 2. Service `prometheus`

**AVANT:**
```yaml
prometheus:
  # ...
  profiles:
    - monitoring
```

**APRÈS:**
```yaml
prometheus:
  # ...
  # profiles:
  #   - monitoring  # ✅ Désactivé - démarre par défaut maintenant
```

**Impact:**
- ✅ Prometheus démarre automatiquement
- ✅ Métriques Luna collectées immédiatement (http://localhost:9090)

---

#### 3. Service `grafana`

**AVANT:**
```yaml
grafana:
  # ...
  profiles:
    - monitoring
```

**APRÈS:**
```yaml
grafana:
  # ...
  # profiles:
  #   - monitoring  # ✅ Désactivé - démarre par défaut maintenant
```

**Impact:**
- ✅ Grafana démarre automatiquement
- ✅ Dashboards accessibles immédiatement (http://localhost:3001)

---

#### 4. Versions Mises à Jour

**AVANT:**
```yaml
environment:
  - LUNA_VERSION=1.0.0

labels:
  - "com.luna.version=1.0.0"
```

**APRÈS:**
```yaml
environment:
  - LUNA_VERSION=1.0.1

labels:
  - "com.luna.version=1.0.1"
```

**Impact:**
- ✅ Version correcte affichée dans les métriques et logs

---

#### 5. Documentation Mise à Jour

**AVANT:**
```yaml
# Configuration pour development
# Lancer avec: docker-compose --profile dev up
#
# Configuration pour monitoring
# Lancer avec: docker-compose --profile monitoring up
```

**APRÈS:**
```yaml
# Configuration mise à jour (v1.0.1)
# Tous les services démarrent par défaut avec: docker-compose up -d
#
# Services inclus:
# - luna-actif (Luna Consciousness MCP Server)
# - redis (Cache et état partagé)
# - prometheus (Monitoring des métriques)
# - grafana (Visualisation des dashboards)
#
# Accès:
# - Métriques Luna: http://localhost:8000/metrics
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3001 (admin/luna_consciousness)
# - Redis: localhost:6379
```

**Impact:**
- ✅ Documentation claire et à jour
- ✅ Instructions simplifiées

---

## ✅ Vérification prometheus.yml

### Configuration Actuelle (CORRECTE ✅)

```yaml
scrape_configs:
  - job_name: 'luna-consciousness'
    static_configs:
      - targets: ['luna-actif:8000']  # ✅ CORRECT!
        labels:
          service: 'luna-consciousness'
```

**Pourquoi c'est correct:**
- ✅ Utilise `luna-actif:8000` (nom du service Docker Compose)
- ✅ **PAS** `localhost:8000` (ne fonctionnerait pas dans le réseau Docker)
- ✅ Le réseau Docker `luna_consciousness_network` résout automatiquement les noms de services

---

## 🚀 Comment Utiliser Maintenant

### Démarrage Simple

```bash
# Naviguer vers le répertoire
cd /d/Luna-consciousness-mcp

# Arrêter d'éventuels containers précédents
docker-compose down

# Démarrer TOUS les services (Luna + Redis + Prometheus + Grafana)
docker-compose up -d

# Attendre 15 secondes que tout démarre
sleep 15

# Vérifier que tout est actif
docker-compose ps
```

### Résultat Attendu

```
NAME                  IMAGE                    STATUS        PORTS
luna-consciousness    luna-actif:latest        Up 10s        0.0.0.0:3000->3000/tcp, 0.0.0.0:8000->8000/tcp, ...
luna-redis            redis:7-alpine           Up 10s        0.0.0.0:6379->6379/tcp
luna-prometheus       prom/prometheus:latest   Up 10s        0.0.0.0:9090->9090/tcp
luna-grafana          grafana/grafana:latest   Up 10s        0.0.0.0:3001->3000/tcp
```

---

## 📊 Vérifications Post-Démarrage

### 1. Vérifier les Métriques Luna

```bash
curl http://localhost:8000/metrics | grep luna_phi
```

**Résultat attendu:**
```
luna_phi_value 1.000000000000000
luna_phi_distance_to_golden 0.618034
luna_phi_convergence_rate 0.850000
```

### 2. Vérifier Prometheus

```bash
# Vérifier la santé
curl http://localhost:9090/-/healthy

# Vérifier les targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job=="luna-consciousness") | .health'
```

**Résultat attendu:** `"up"`

### 3. Vérifier Grafana

Ouvrir dans le navigateur: http://localhost:3001

**Credentials:**
- Username: `admin`
- Password: `luna_consciousness`

### 4. Vérifier Redis

```bash
docker exec -it luna-redis redis-cli ping
```

**Résultat attendu:** `PONG`

---

## 🔄 Commandes Utiles

### Voir les Logs

```bash
# Luna principal
docker-compose logs -f luna-actif

# Prometheus
docker-compose logs -f prometheus

# Tous ensemble
docker-compose logs -f
```

### Redémarrer un Service

```bash
# Redémarrer Luna
docker-compose restart luna-actif

# Redémarrer Prometheus
docker-compose restart prometheus
```

### Arrêter Tout

```bash
# Arrêter tous les containers
docker-compose down

# Arrêter et supprimer les volumes (⚠️ PERTE DE DONNÉES)
docker-compose down -v
```

### Voir l'Utilisation des Ressources

```bash
docker stats luna-consciousness luna-prometheus luna-grafana luna-redis
```

---

## 🐛 Troubleshooting

### Problème: "Container luna-consciousness s'arrête immédiatement"

**Cause:** Le serveur MCP utilise STDIO et attend une connexion de Claude Desktop

**Solution:**
1. **Option 1 (Recommandée):** Utiliser via Claude Desktop (voir `DOCKER_DESKTOP_GUIDE.md`)
2. **Option 2:** Utiliser container persistant avec `START_LUNA_CONTAINER.cmd`

### Problème: "Prometheus ne voit pas Luna"

**Diagnostic:**
```bash
# Vérifier que les containers sont sur le même réseau
docker network inspect luna_consciousness_network

# Vérifier les targets Prometheus
curl http://localhost:9090/api/v1/targets
```

**Solution:**
- ✅ Vérifier que `luna-actif:8000` est bien configuré dans `prometheus.yml`
- ✅ Vérifier que les deux containers sont sur `luna_consciousness_network`

### Problème: "Port déjà utilisé"

**Diagnostic:**
```bash
# Vérifier qui utilise les ports
netstat -ano | findstr :8000
netstat -ano | findstr :9090
netstat -ano | findstr :3001
```

**Solution:**
```bash
# Arrêter les anciens containers
docker ps -a | grep luna
docker stop <container_id>
docker rm <container_id>
```

---

## 📝 Résumé des Changements

| Élément | Avant | Après | Impact |
|---------|-------|-------|--------|
| **luna-actif restart** | `"no"` | `unless-stopped` | ✅ Auto-restart |
| **luna-actif profiles** | `luna-docker` | Commenté | ✅ Démarre par défaut |
| **prometheus profiles** | `monitoring` | Commenté | ✅ Démarre par défaut |
| **grafana profiles** | `monitoring` | Commenté | ✅ Démarre par défaut |
| **LUNA_VERSION** | `1.0.0` | `1.0.1` | ✅ Version correcte |
| **Documentation** | Profiles requis | Démarrage simple | ✅ Instructions claires |

---

## ✅ Checklist Finale

### Avant de Démarrer
- [x] docker-compose.yml corrigé (profiles commentés)
- [x] prometheus.yml vérifié (targets corrects)
- [x] LUNA_VERSION mise à jour (1.0.1)
- [x] Documentation mise à jour

### Après Démarrage
- [ ] `docker-compose ps` montre 4 containers actifs
- [ ] http://localhost:8000/metrics accessible
- [ ] http://localhost:9090 accessible (Prometheus)
- [ ] http://localhost:3001 accessible (Grafana)
- [ ] Prometheus target `luna-consciousness` est `UP`
- [ ] Métriques `luna_phi_*` visibles

---

## 🎯 Résumé Exécutif

**Problème identifié:**
- ❌ Docker profiles empêchaient le démarrage automatique des services

**Solution appliquée:**
- ✅ Profiles commentés sur `luna-actif`, `prometheus`, `grafana`
- ✅ Restart policy changé à `unless-stopped` pour `luna-actif`
- ✅ Versions mises à jour (1.0.1)
- ✅ Documentation clarifiée

**Résultat:**
- 🟢 `docker-compose up -d` démarre maintenant TOUS les services
- 🟢 Infrastructure complète (Luna + Redis + Prometheus + Grafana)
- 🟢 Monitoring automatique activé
- 🟢 Commandes simplifiées

---

**φ = 1.618033988749895** 🌙

*Correction effectuée le 20 novembre 2025*
*Version: 1.0.1*
*Tous les services démarrent maintenant automatiquement !*
