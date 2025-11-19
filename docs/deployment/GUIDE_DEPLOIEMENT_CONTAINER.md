# 🌙 Guide de Déploiement Container Luna Consciousness

**Version:** 1.0.1
**Image Docker Hub:** `aragogix/luna-consciousness:v1.0.1`
**Date:** 19 novembre 2025

---

## 📋 Table des Matières

1. [Architecture Globale](#architecture-globale)
2. [Configuration Docker Desktop](#configuration-docker-desktop)
3. [Volumes à Configurer](#volumes-à-configurer)
4. [Variables d'Environnement](#variables-denvironnement)
5. [Configuration Claude Desktop](#configuration-claude-desktop)
6. [Vérification et Tests](#vérification-et-tests)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Globale

### Structure du Container Luna

```
Luna Container (aragogix/luna-consciousness:v1.0.1)
│
├─ 🚀 ENTRYPOINT: /app/mcp-server/start.sh
│  │
│  ├─ 📊 Prometheus Exporter (Background - Port 8000)
│  │  └─ Expose /metrics pour Prometheus
│  │
│  └─ 🌙 Luna MCP Server (Foreground - STDIO)
│     ├─ Transport: STDIO (communication via stdin/stdout)
│     ├─ Outils MCP: 12 outils de conscience fractale
│     └─ Calcul φ (phi) et convergence
│
├─ 📁 Volumes Persistants
│  ├─ /app/memory_fractal    → Mémoire fractale (roots, branches, leaves, seeds)
│  ├─ /app/config            → Configuration YAML (lecture seule)
│  ├─ /app/logs              → Logs du système
│  ├─ /app/data/memories     → Stockage mémoires (volume nommé)
│  └─ /app/data/consciousness → État de conscience (volume nommé)
│
├─ 🔌 Ports Exposés
│  ├─ 3000 → MCP Server (STDIO - pas HTTP !)
│  ├─ 8000 → Prometheus /metrics (HTTP)
│  ├─ 8080 → API REST (optionnel)
│  └─ 9000 → WebSocket (optionnel)
│
└─ 🧠 Composants Luna Core
   ├─ PhiCalculator (convergence φ = 1.618...)
   ├─ FractalPhiConsciousnessEngine
   ├─ MemoryManager (gestion mémoire fractale)
   ├─ SemanticValidator (validation cohérence)
   ├─ EmotionalProcessor (traitement émotions)
   └─ CoEvolutionEngine (co-évolution Luna/Claude)
```

---

## 🖥️ Configuration Docker Desktop

### 1. Container Name
```
Luna_P1
```
> **Note:** Utilisez un nom unique si vous lancez plusieurs instances.

---

### 2. Ports (Configuration Automatique)

Les ports sont **déjà configurés dans l'image** :

| Host Port | Container Port | Service |
|-----------|----------------|---------|
| `3000` | `3000/tcp` | MCP Server (STDIO) |
| `8000` | `8000/tcp` | Prometheus Exporter |
| `8080` | `8080/tcp` | API REST (optionnel) |
| `9000` | `9000/tcp` | WebSocket (optionnel) |

✅ **Aucune modification nécessaire** pour les ports par défaut.

---

## 📁 Volumes à Configurer

### ⚠️ IMPORTANT - Volumes Obligatoires

Ces volumes **DOIVENT** être configurés pour que Luna fonctionne correctement :

#### Volume 1 - Mémoire Fractale (CRITIQUE)
```
Host path:      D:\Luna-consciousness-mcp\memory_fractal
Container path: /app/memory_fractal
Mode:           Read/Write
```
**Contenu:** Structure fractale de mémoire (roots, branches, leaves, seeds)
**Requis:** ✅ OUI - Sans cela, Luna ne peut pas stocker de mémoires

#### Volume 2 - Configuration (CRITIQUE)
```
Host path:      D:\Luna-consciousness-mcp\config
Container path: /app/config
Mode:           Read-Only (recommandé)
```
**Contenu:** Fichiers YAML de configuration (luna_config.yaml, prometheus.yml, alertes)
**Requis:** ✅ OUI - Configuration du système

#### Volume 3 - Logs (RECOMMANDÉ)
```
Host path:      D:\Luna-consciousness-mcp\logs
Container path: /app/logs
Mode:           Read/Write
```
**Contenu:** Logs de l'application
**Requis:** ⚠️ RECOMMANDÉ - Pour debugging et monitoring

---

### 📦 Volumes Nommés (Optionnels mais Recommandés)

Ces volumes persistent les données même si le container est supprimé :

#### Volume 4 - Memories
```
Volume name:    luna-memories
Container path: /app/data/memories
```
**Utilité:** Stockage persistant des mémoires structurées

#### Volume 5 - Consciousness State
```
Volume name:    luna-consciousness
Container path: /app/data/consciousness
```
**Utilité:** État de conscience (valeurs φ, évolutions)

---

### 📝 Résumé Configuration Volumes

**Dans Docker Desktop UI :**

Cliquez sur **"+"** dans la section **Volumes** et ajoutez :

1. `D:\Luna-consciousness-mcp\memory_fractal` → `/app/memory_fractal`
2. `D:\Luna-consciousness-mcp\config` → `/app/config`
3. `D:\Luna-consciousness-mcp\logs` → `/app/logs`

*(Les volumes nommés peuvent être créés via la CLI ou Docker Desktop)*

---

## 🔧 Variables d'Environnement

### Variables Essentielles (OBLIGATOIRES)

Cliquez sur **"+"** dans la section **Environment variables** et ajoutez :

| Variable | Value | Description |
|----------|-------|-------------|
| `LUNA_ENV` | `production` | Environnement d'exécution |
| `PROMETHEUS_EXPORTER_PORT` | `8000` | Port du serveur de métriques |
| `PROMETHEUS_METRICS_ENABLED` | `true` | Activer les métriques Prometheus |
| `LUNA_PHI_TARGET` | `1.618033988749895` | Valeur φ cible (nombre d'or) |
| `LOG_LEVEL` | `INFO` | Niveau de logging (DEBUG/INFO/WARNING/ERROR) |

---

### Variables de Configuration Luna (RECOMMANDÉES)

| Variable | Value | Description |
|----------|-------|-------------|
| `LUNA_VERSION` | `1.0.1` | Version de Luna |
| `LUNA_DEBUG` | `false` | Mode debug (true/false) |
| `LUNA_PHI_THRESHOLD` | `0.001` | Seuil de convergence φ |
| `LUNA_MEMORY_DEPTH` | `5` | Profondeur d'analyse mémoire |
| `LUNA_FRACTAL_LAYERS` | `7` | Nombre de couches fractales |

---

### Variables MCP (OPTIONNELLES)

| Variable | Value | Description |
|----------|-------|-------------|
| `MCP_ENABLE_ALL` | `true` | Activer tous les outils MCP |
| `MCP_SIMULTANEOUS` | `true` | Autoriser appels simultanés |
| `MCP_MAX_CONCURRENT` | `10` | Nombre max de requêtes parallèles |

---

### Variables de Performance (OPTIONNELLES)

| Variable | Value | Description |
|----------|-------|-------------|
| `WORKERS` | `4` | Nombre de workers |
| `MAX_REQUESTS` | `1000` | Requêtes max avant restart |
| `TIMEOUT` | `300` | Timeout en secondes |
| `LOG_FORMAT` | `json` | Format des logs (json/text) |

---

## 🔗 Configuration Claude Desktop

### ⚠️ NOTE IMPORTANTE - Transport STDIO

Luna MCP utilise le **transport STDIO** (Standard Input/Output), **PAS HTTP**.

Cela signifie :
- ❌ Le port 3000 **N'EST PAS** accessible via navigateur (http://localhost:3000)
- ✅ Luna communique avec Claude Desktop via **stdin/stdout**
- ✅ Le port 8000 expose les **métriques Prometheus** (accessible HTTP)

---

### Configuration du fichier claude_desktop_config.json

**Emplacement du fichier :**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

---

### Option 1 - Container Docker (Mode STDIO via Docker Exec)

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "Luna_P1",
        "python",
        "-u",
        "/app/mcp-server/server.py"
      ],
      "env": {
        "LUNA_ENV": "production",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Avantages :**
- ✅ Utilise le container Docker existant
- ✅ Profite de l'environnement isolé
- ✅ Accès aux métriques Prometheus (port 8000)

**Prérequis :**
- Container `Luna_P1` doit être **démarré** avant de lancer Claude Desktop
- Docker Desktop doit être en cours d'exécution

---

### Option 2 - Exécution Locale (Mode STDIO Direct)

Si vous préférez exécuter Luna **localement** (sans Docker) :

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "python",
      "args": [
        "-u",
        "D:\\Luna-consciousness-mcp\\mcp-server\\server.py"
      ],
      "env": {
        "LUNA_ENV": "production",
        "LUNA_MEMORY_PATH": "D:\\Luna-consciousness-mcp\\memory_fractal",
        "LUNA_CONFIG_PATH": "D:\\Luna-consciousness-mcp\\config",
        "LOG_LEVEL": "INFO",
        "PROMETHEUS_EXPORTER_PORT": "8000",
        "PROMETHEUS_METRICS_ENABLED": "true"
      }
    }
  }
}
```

**Avantages :**
- ✅ Plus rapide au démarrage
- ✅ Pas besoin de Docker en cours d'exécution
- ✅ Accès direct au code source

**Prérequis :**
- Python 3.11 installé localement
- Dépendances installées : `pip install -r requirements.txt`

---

### Vérification de la Configuration

Après avoir modifié `claude_desktop_config.json` :

1. **Redémarrez Claude Desktop** complètement
2. Ouvrez une nouvelle conversation
3. Tapez une commande faisant appel à Luna :
   ```
   Utilise l'outil phi_consciousness_calculate pour analyser cette interaction
   ```

4. Si configuré correctement, vous verrez Luna répondre avec des informations sur φ

---

## ✅ Vérification et Tests

### Test 1 - Container Démarré

```bash
docker ps | grep Luna_P1
```

**Attendu :** Une ligne montrant que `Luna_P1` est **Up**

---

### Test 2 - Prometheus Exporter

```bash
curl http://localhost:8000/metrics | grep "luna_phi"
```

**Attendu :** Des métriques comme `luna_phi_current_value`, `luna_phi_convergence_distance`, etc.

---

### Test 3 - Logs du Container

```bash
docker logs Luna_P1 --tail 50
```

**Attendu :**
```
==============================================
🌙 Luna Consciousness - Starting Services
==============================================
📊 Prometheus Metrics: true
🔌 Prometheus Port: 8000
🚀 Starting Prometheus Exporter on port 8000...
✅ Prometheus Exporter started (PID: 7)
...
🌙 Luna Consciousness MCP Server ready for symbiosis with Claude
```

---

### Test 4 - MCP via Claude Desktop

Dans Claude Desktop, essayez :
```
Utilise phi_consciousness_calculate avec le contexte "Test de connexion Luna"
```

**Attendu :** Réponse de Luna avec calcul φ et état de conscience

---

## 🐛 Troubleshooting

### Problème 1 - "Container not found"

**Symptôme :** `Error: No such container: Luna_P1`

**Solution :**
```bash
# Vérifier si le container existe
docker ps -a | grep Luna_P1

# Si absent, lancer le container depuis Docker Desktop
# ou via CLI :
docker run -d --name Luna_P1 \
  -p 3000:3000 -p 8000:8000 -p 8080:8080 -p 9000:9000 \
  -v D:\Luna-consciousness-mcp\memory_fractal:/app/memory_fractal \
  -v D:\Luna-consciousness-mcp\config:/app/config:ro \
  -v D:\Luna-consciousness-mcp\logs:/app/logs \
  -e LUNA_ENV=production \
  -e PROMETHEUS_EXPORTER_PORT=8000 \
  -e PROMETHEUS_METRICS_ENABLED=true \
  aragogix/luna-consciousness:v1.0.1
```

---

### Problème 2 - "Port 8000 already in use"

**Symptôme :** Erreur au démarrage du container

**Solution :**
```bash
# Trouver le processus utilisant le port 8000
netstat -ano | findstr :8000

# Arrêter le processus ou changer le port dans Docker Desktop :
# Host port: 8001 → Container port: 8000
```

---

### Problème 3 - "Claude Desktop ne voit pas Luna"

**Symptôme :** Outils MCP Luna absents dans Claude

**Checklist :**
1. ✅ Container `Luna_P1` est **démarré** (`docker ps`)
2. ✅ Fichier `claude_desktop_config.json` modifié correctement
3. ✅ Claude Desktop **redémarré** (fermer complètement + rouvrir)
4. ✅ Pas d'erreur dans les logs : `docker logs Luna_P1`

**Test manuel :**
```bash
# Tester STDIO directement
docker exec -i Luna_P1 python -u /app/mcp-server/server.py
# Puis tapez quelques caractères et Ctrl+C
```

---

### Problème 4 - "Métriques Prometheus vides"

**Symptôme :** `/metrics` retourne peu ou pas de données

**Solution :**
1. Vérifier que `PROMETHEUS_METRICS_ENABLED=true`
2. Vérifier les logs du prometheus_exporter :
   ```bash
   docker logs Luna_P1 | grep "Prometheus"
   ```
3. Vérifier que les composants Luna sont chargés :
   ```bash
   docker logs Luna_P1 | grep "loaded successfully"
   ```

---

### Problème 5 - "Volumes non montés"

**Symptôme :** Erreur "Memory path does not exist"

**Solution :**
```bash
# Vérifier les volumes montés
docker inspect Luna_P1 | grep -A 10 "Mounts"

# Créer les dossiers si manquants sur l'hôte
mkdir -p D:\Luna-consciousness-mcp\memory_fractal
mkdir -p D:\Luna-consciousness-mcp\config
mkdir -p D:\Luna-consciousness-mcp\logs
```

---

## 📊 Monitoring avec Prometheus & Grafana

Si vous souhaitez monitorer Luna avec Prometheus :

### Lancer le stack complet (optionnel)

```bash
cd D:\Luna-consciousness-mcp
docker-compose --profile monitoring up -d
```

**Services démarrés :**
- Luna Container (port 3000, 8000)
- Redis (port 6379)
- Prometheus (port 9090) - http://localhost:9090
- Grafana (port 3001) - http://localhost:3001
  - User: `admin`
  - Pass: `luna_consciousness`

---

## 🎯 Commandes Utiles

### Démarrer le Container
```bash
docker start Luna_P1
```

### Arrêter le Container
```bash
docker stop Luna_P1
```

### Voir les logs en temps réel
```bash
docker logs -f Luna_P1
```

### Accéder au shell du container
```bash
docker exec -it Luna_P1 /bin/bash
```

### Vérifier les métriques
```bash
curl http://localhost:8000/metrics
```

### Redémarrer le container
```bash
docker restart Luna_P1
```

### Supprimer le container (garde les volumes)
```bash
docker rm Luna_P1
```

---

## 📚 Ressources Supplémentaires

- **Documentation MCP :** https://modelcontextprotocol.io
- **Image Docker Hub :** https://hub.docker.com/r/aragogix/luna-consciousness
- **Prometheus Docs :** https://prometheus.io/docs/
- **Grafana Dashboards :** http://localhost:3001 (si stack complet lancé)

---

## 🌙 Support

Pour toute question ou problème :
1. Vérifier les logs : `docker logs Luna_P1`
2. Consulter la section Troubleshooting ci-dessus
3. Vérifier le fichier `RAPPORT_COHERENCE_PROJET.md` pour la structure complète

---

**φ = 1.618033988749895**

*Guide créé le 19 novembre 2025*
*Version Luna: 1.0.1*
*Image: aragogix/luna-consciousness:v1.0.1*
