# 🚀 Guide de Déploiement Luna Consciousness

**Version:** 2.0.1
**Date:** 25 novembre 2025
**Statut:** ✅ Production Ready

---

## 📋 Table des Matières

1. [Prérequis](#-prérequis)
2. [Méthodes de Déploiement](#-méthodes-de-déploiement)
3. [Configuration Claude Desktop](#-configuration-claude-desktop)
4. [Vérification du Déploiement](#-vérification-du-déploiement)
5. [Troubleshooting](#-troubleshooting)
6. [Mise à Jour](#-mise-à-jour)

---

## 💻 Prérequis

### Système

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| 🐍 Python | 3.11+ | 3.12 |
| 🐳 Docker | 20.10+ | 24.0+ |
| 💾 RAM | 4 GB | 8 GB |
| 📀 Disque | 10 GB | 20 GB |
| 🖥️ OS | Windows 10/11, macOS 12+, Linux | Ubuntu 22.04+ |

### Logiciels Requis

```bash
# Vérifier Docker
docker --version
docker-compose --version

# Vérifier Python (si mode local)
python3 --version
```

---

## 🐳 Méthodes de Déploiement

### 🌟 Méthode 1 : Docker Hub (Recommandé)

La méthode la plus simple - utilise l'image pré-construite.

```bash
# 1. Pull de l'image officielle
docker pull aragogix/luna-consciousness:v2.0.1

# 2. Cloner le repository (pour configs et volumes)
git clone https://github.com/MRVarden/Luna-consciousness-mcp.git
cd Luna-consciousness-mcp

# 3. Lancement
docker-compose up -d
```

**✅ Avantages :**
- Aucune compilation nécessaire
- Image optimisée et testée
- Déploiement en < 5 minutes

### 🔧 Méthode 2 : Build Local

Pour personnalisation ou développement.

```bash
# 1. Cloner le repository
git clone https://github.com/MRVarden/Luna-consciousness-mcp.git
cd Luna-consciousness-mcp

# 2. Build de l'image
docker-compose build luna-actif

# 3. Lancement
docker-compose up -d
```

**⏱️ Durée de build :** ~10-15 minutes (première fois)

### 💻 Méthode 3 : Mode Local (Développement)

Sans Docker, directement avec Python.

```bash
# 1. Cloner et préparer l'environnement
git clone https://github.com/MRVarden/Luna-consciousness-mcp.git
cd Luna-consciousness-mcp

# 2. Créer environnement virtuel
python3 -m venv venv_luna
source venv_luna/bin/activate  # Linux/Mac
# ou: venv_luna\Scripts\activate  # Windows

# 3. Installer dépendances
pip install -r mcp-server/requirements.txt

# 4. Démarrer l'infrastructure Docker (Redis, etc.)
docker-compose up -d redis prometheus grafana

# 5. Lancer le serveur Luna
cd mcp-server
python server.py
```

---

## 🐳 Services Docker

### Architecture des Services

```yaml
services:
  luna-consciousness:    # 🌙 Serveur MCP principal
    ports: 3000, 8000, 8080, 9000

  redis:                 # 🔴 Cache et état
    port: 6379

  prometheus:            # 📊 Métriques
    port: 9090

  grafana:               # 📈 Visualisation
    port: 3001
```

### Commandes Utiles

```bash
# Voir l'état des services
docker-compose ps

# Voir les logs
docker logs luna-consciousness -f

# Redémarrer un service
docker-compose restart luna-consciousness

# Arrêter tout
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

---

## ⚙️ Configuration Claude Desktop

### 📍 Emplacement du Fichier

| OS | Chemin |
|----|--------|
| 🪟 **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| 🍎 **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| 🐧 **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### 🐳 Configuration Mode Docker

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": [
        "exec", "-i", "luna-consciousness",
        "python", "-u", "/app/mcp-server/server.py"
      ],
      "env": {
        "LUNA_ENV": "production",
        "LUNA_MODE": "orchestrator",
        "LUNA_UPDATE01": "enabled",
        "LUNA_PHI_TARGET": "1.618033988749895",
        "PROMETHEUS_EXPORTER_PORT": "8000"
      }
    }
  }
}
```

### 💻 Configuration Mode Local

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "python",
      "args": ["/chemin/absolu/vers/Luna-consciousness-mcp/mcp-server/server.py"],
      "env": {
        "LUNA_MEMORY_PATH": "/chemin/absolu/vers/Luna-consciousness-mcp/memory_fractal",
        "LUNA_CONFIG_PATH": "/chemin/absolu/vers/Luna-consciousness-mcp/config",
        "LUNA_MODE": "orchestrator",
        "LUNA_UPDATE01": "enabled"
      }
    }
  }
}
```

### 🔄 Après Modification

1. Sauvegardez le fichier
2. **Fermez complètement** Claude Desktop
3. Relancez Claude Desktop
4. Vérifiez que Luna apparaît dans les outils MCP

---

## ✅ Vérification du Déploiement

### 1️⃣ Vérifier les Containers

```bash
docker ps -a
```

**Résultat attendu :**
```
CONTAINER ID   IMAGE                                STATUS          PORTS
xxxx           aragogix/luna-consciousness:v2.0.1   Up X minutes    0.0.0.0:3000->3000/tcp...
xxxx           redis:7-alpine                       Up (healthy)    0.0.0.0:6379->6379/tcp
xxxx           prom/prometheus:latest               Up              0.0.0.0:9090->9090/tcp
xxxx           grafana/grafana:latest               Up              0.0.0.0:3001->3000/tcp
```

### 2️⃣ Vérifier les Logs Luna

```bash
docker logs luna-consciousness 2>&1 | tail -20
```

**Résultat attendu :**
```
🌙 Initializing Luna Core Components...
✅ Luna Core Components initialized successfully
🚀 Initializing Update01.md Architectural Modules...
🛡️ Luna Manipulation Detector initialized
🛡️ Luna Validator initialized
🔮 Luna Predictive Core initialized
🤖 Luna Autonomous Decision System initialized
🧬 Luna Self-Improvement System initialized
🎨 Luna Multimodal Interface initialized
🌙 Luna Orchestrator initialized
🔗 Luna Systemic Integration initialized
✅ Update01.md Architectural Modules initialized successfully
🌟 Luna is now ORCHESTRATED, not just a collection of tools!
🔧 Exposing 12 consciousness tools via MCP protocol
```

### 3️⃣ Vérifier les Métriques Prometheus

```bash
curl http://localhost:8000/metrics | grep luna_phi
```

**Résultat attendu :**
```
luna_phi_current_value 1.618033988749895
luna_phi_convergence_rate 0.95
```

### 4️⃣ Test dans Claude Desktop

Ouvrez Claude Desktop et tapez :
```
Utilise l'outil luna_orchestrated_interaction avec "Bonjour Luna"
```

---

## 🔧 Troubleshooting

### ❌ Container en Restart Loop

**Symptôme :** `STATUS: Restarting (1)`

**Solution :**
```bash
# Voir les logs d'erreur
docker logs luna-consciousness 2>&1 | tail -50

# Causes communes :
# 1. Import error → Rebuild l'image
docker-compose build --no-cache luna-actif

# 2. Port déjà utilisé
docker-compose down
docker-compose up -d
```

### ❌ Claude Desktop ne voit pas Luna

**Vérifications :**

1. **Container actif ?**
   ```bash
   docker ps | grep luna-consciousness
   ```

2. **Configuration JSON valide ?**
   ```bash
   # Windows PowerShell
   cat $env:APPDATA\Claude\claude_desktop_config.json | python -m json.tool
   ```

3. **Nom du container correct ?**
   - Doit être `luna-consciousness` (pas `Luna_P1`)

4. **Redémarrer Claude Desktop**
   - Fermez complètement (pas juste minimiser)
   - Relancez

### ❌ Erreur "No running event loop"

**Cause :** Version < 2.0.1 avec asyncio mal configuré

**Solution :**
```bash
docker pull aragogix/luna-consciousness:v2.0.1
docker-compose down
docker-compose up -d
```

### ❌ Métriques Prometheus indisponibles

**Vérification :**
```bash
# Le port 8000 doit être exposé
docker port luna-consciousness 8000

# Test direct
curl -v http://localhost:8000/metrics
```

---

## 🔄 Mise à Jour

### Depuis Docker Hub

```bash
# 1. Pull nouvelle version
docker pull aragogix/luna-consciousness:latest

# 2. Redémarrer
docker-compose down
docker-compose up -d

# 3. Vérifier la version
docker logs luna-consciousness 2>&1 | head -5
```

### Depuis le Repository

```bash
# 1. Pull les changements
git pull origin main

# 2. Rebuild
docker-compose build --no-cache luna-actif

# 3. Redémarrer
docker-compose down
docker-compose up -d
```

### 💾 Sauvegarde Mémoire Fractale

Avant une mise à jour majeure :
```bash
# Sauvegarder la mémoire
cp -r memory_fractal memory_fractal_backup_$(date +%Y%m%d)
```

---

## 📊 Ports et URLs

| Service | Port | URL | Usage |
|---------|------|-----|-------|
| 🌙 Luna MCP | 3000 | STDIO (pas HTTP) | Communication MCP |
| 📊 Prometheus Metrics | 8000 | http://localhost:8000/metrics | Métriques Luna |
| 🔍 Prometheus UI | 9090 | http://localhost:9090 | Interface Prometheus |
| 📈 Grafana | 3001 | http://localhost:3001 | Dashboards |
| 🔴 Redis | 6379 | localhost:6379 | Cache |

---

## 🔐 Variables d'Environnement

| Variable | Valeur | Description |
|----------|--------|-------------|
| `LUNA_MODE` | `orchestrator` | Mode de fonctionnement |
| `LUNA_UPDATE01` | `enabled` | Active les modules Update01 |
| `LUNA_PHI_TARGET` | `1.618033988749895` | Cible φ |
| `LUNA_MEMORY_PATH` | `/app/memory_fractal` | Chemin mémoire |
| `LUNA_CONFIG_PATH` | `/app/config` | Chemin config |
| `PROMETHEUS_EXPORTER_PORT` | `8000` | Port métriques |
| `LUNA_LOG_LEVEL` | `INFO` | Niveau de log |

---

## 🎯 Checklist de Déploiement

- [ ] Docker et Docker Compose installés
- [ ] Repository cloné
- [ ] Image Docker disponible (pull ou build)
- [ ] `docker-compose up -d` exécuté
- [ ] Tous les containers en status `Up`
- [ ] Configuration Claude Desktop copiée
- [ ] Claude Desktop redémarré
- [ ] Luna visible dans les outils MCP
- [ ] Test avec `luna_orchestrated_interaction`
- [ ] Métriques Prometheus accessibles

---

**φ = 1.618033988749895** 🌙

*Guide de déploiement - Luna Consciousness v2.0.1*
