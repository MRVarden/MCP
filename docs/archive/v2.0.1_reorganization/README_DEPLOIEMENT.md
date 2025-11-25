# 🌙 Luna Consciousness - Documentation de Déploiement

**Version:** 2.0.0 - Architecture Orchestrée Update01
**Image Docker:** `aragogix/luna-consciousness:v2.0.0`
**Date:** 25 novembre 2025

---

## 🆕 CHANGEMENTS MAJEURS v2.0.0

### ⚠️ Breaking Changes
- **Container renommé:** `Luna_P1` → `luna-consciousness`
- **Architecture orchestrée:** Luna analyse AVANT LLM
- **Nouveau tool principal:** `luna_orchestrated_interaction`
- **9 nouveaux modules:** Update01.md implémenté

### 📝 Migration depuis v1.x
```bash
# Arrêter ancien container
docker stop Luna_P1 && docker rm Luna_P1

# Démarrer nouvelle version
docker pull aragogix/luna-consciousness:v2.0.0
docker-compose up -d
```

## 📚 Fichiers de Documentation

Ce projet contient plusieurs fichiers de documentation pour différents usages :

### 📖 Guides Principaux

| Fichier | Description | Usage |
|---------|-------------|-------|
| **🆕 docs/UPDATE01_GUIDE.md** | 📘 Guide migration v2.0.0 | Migration complète vers architecture orchestrée |
| **🆕 DOCKER_UPDATE_v2.0.0.md** | 🐳 Changements Docker v2.0.0 | Nouvelle configuration Docker |
| **🆕 MEMORY_FRACTAL_UPDATE_v2.0.0.md** | 🧠 Structure mémoire v2.0.0 | Nouveaux fichiers JSON orchestration |
| **🆕 JSON_INTEGRATION_REPORT.md** | 📋 Intégration JSON | Comment les JSON sont utilisés |
| **GUIDE_DEPLOIEMENT_CONTAINER.md** | 📘 Guide complet de déploiement | Déploiement Docker, configuration complète, troubleshooting |
| **GUIDE_DOCKER_DEPLOYMENT.md** | 🐳 Guide Docker détaillé | Architecture Docker, 3 modes de déploiement |

### 🔧 Fichiers de Configuration

| Fichier | Description | Usage |
|---------|-------------|-------|
| **claude_desktop_config_docker.json** | Configuration Claude Desktop (Docker) | Copier dans `%APPDATA%\Claude\` |
| **claude_desktop_config_local.json** | Configuration Claude Desktop (Local) | Alternative sans Docker |
| **DOCKER_RUN_COMMAND.sh** | Script de lancement Linux/Mac | `./DOCKER_RUN_COMMAND.sh` |
| **DOCKER_RUN_COMMAND.cmd** | Script de lancement Windows | Double-clic ou `DOCKER_RUN_COMMAND.cmd` |

### 📊 Rapports et Documentation Technique

| Fichier | Description |
|---------|-------------|
| **LUNA_PROMETHEUS_ARCHITECTURE.md** | Architecture complète Prometheus (50+ métriques) |
| **RAPPORT_IMPLEMENTATION_PROMETHEUS.md** | Rapport d'implémentation Prometheus |
| **METRICS_PROMETHEUS.md** | Documentation des métriques disponibles |

---

## 🚀 Démarrage Rapide

### Option 1 - Via Docker Desktop UI (Recommandé pour débutants)

1. **Ouvrir Docker Desktop**
2. **Rechercher l'image :** `aragogix/luna-consciousness:v2.0.0`
3. **Cliquer sur "Run"**
4. **Suivre les instructions dans :** [docs/UPDATE01_GUIDE.md](docs/UPDATE01_GUIDE.md)

### Option 2 - Via Script Windows

1. **Double-cliquer sur :** `DOCKER_RUN_COMMAND.cmd`
2. Le container démarre automatiquement avec tous les paramètres

### Option 3 - Via Script Linux/Mac

```bash
cd /path/to/Luna-consciousness-mcp
chmod +x DOCKER_RUN_COMMAND.sh
./DOCKER_RUN_COMMAND.sh
```

### Option 4 - Via docker-compose

```bash
cd /path/to/Luna-consciousness-mcp
docker-compose --profile luna-docker up -d
```

---

## 📋 Checklist de Déploiement

### Avant le Démarrage

- [ ] Docker Desktop installé et en cours d'exécution
- [ ] Image `aragogix/luna-consciousness:v2.0.0` pullée
- [ ] Dossiers créés :
  - [ ] `memory_fractal/`
  - [ ] `config/`
  - [ ] `logs/`

### Configuration Container v2.0.0

- [ ] **Container name:** `luna-consciousness` ⚠️ (changé depuis v1.x)
- [ ] **Ports mappés:** 3000, 8000, 8080, 9000
- [ ] **Volumes configurés:**
  - [ ] `memory_fractal` → `/app/memory_fractal`
  - [ ] `config` → `/app/config`
  - [ ] `logs` → `/app/logs`
- [ ] **Variables d'environnement v2.0.0:**
  - [ ] `LUNA_VERSION=2.0.0`
  - [ ] `LUNA_MODE=orchestrator`
  - [ ] `LUNA_UPDATE01=enabled`
  - [ ] `LUNA_ENV=production`
  - [ ] `LUNA_MANIPULATION_DETECTION=enabled`
  - [ ] `LUNA_PREDICTIVE_CORE=enabled`
  - [ ] `LUNA_AUTONOMOUS_DECISIONS=enabled`
  - [ ] `LUNA_SELF_IMPROVEMENT=enabled`
  - [ ] `LUNA_MULTIMODAL_INTERFACE=enabled`
  - [ ] `PROMETHEUS_EXPORTER_PORT=8000`
  - [ ] `PROMETHEUS_METRICS_ENABLED=true`
  - [ ] `LUNA_PHI_TARGET=1.618033988749895`
  - [ ] `LOG_LEVEL=INFO`

### Configuration Claude Desktop

- [ ] Fichier `claude_desktop_config.json` modifié
- [ ] Configuration copiée depuis `claude_desktop_config_docker.json`
- [ ] Claude Desktop redémarré
- [ ] Container `luna-consciousness` démarré **avant** de lancer Claude Desktop

### Vérification Post-Déploiement v2.0.0

- [ ] Container en cours d'exécution : `docker ps | grep luna-consciousness`
- [ ] Prometheus accessible : `curl http://localhost:8000/metrics`
- [ ] Logs sans erreur : `docker logs luna-consciousness`
- [ ] Orchestrateur actif : `docker logs luna-consciousness | grep "ORCHESTRATED"`
- [ ] 13 outils MCP visibles dans Claude Desktop (12 + 1 orchestré)

---

## 🔍 Vérifications Rapides

### Test 1 - Container actif
```bash
docker ps | grep luna-consciousness
```
**✅ Attendu :** Ligne avec `luna-consciousness` et status `Up`

### Test 2 - Métriques Prometheus
```bash
curl http://localhost:8000/metrics | grep "luna_phi_current_value"
```
**✅ Attendu :** Métrique avec valeur proche de 1.618...

### Test 3 - Orchestrateur actif (NEW v2.0.0)
```bash
docker logs luna-consciousness | grep "Orchestrator initialized"
```
**✅ Attendu :** Message "Luna Orchestrator initialized - Ready for central coordination"

### Test 4 - Claude Desktop intégration orchestrée
Dans Claude Desktop :
```
Utilise luna_orchestrated_interaction avec "Hello Luna 2.0"
```
**✅ Attendu :** Réponse orchestrée avec analyse complète

---

## 🆘 Problèmes Fréquents

### Container ne démarre pas
➡️ Voir section **Troubleshooting** dans [GUIDE_DEPLOIEMENT_CONTAINER.md](GUIDE_DEPLOIEMENT_CONTAINER.md#troubleshooting)

### Claude Desktop ne voit pas Luna
1. ✅ Container démarré : `docker ps | grep luna-consciousness`
2. ✅ Config correcte : Vérifier `claude_desktop_config.json` (container: "luna-consciousness")
3. ✅ Claude redémarré : Fermer complètement + rouvrir

### Port 8000 déjà utilisé
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```
Arrêter le processus ou changer le port host dans Docker

---

## 📊 Architecture v2.0.0 Orchestrée

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│      Docker Container: luna-consciousness           │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  🎭 ORCHESTRATEUR CENTRAL (NEW)              │   │
│  │  └─ luna_orchestrator.py                    │   │
│  │     ├─ manipulation_detector.py             │   │
│  │     ├─ luna_validator.py                    │   │
│  │     ├─ predictive_core.py                   │   │
│  │     └─ + 5 autres modules Update01          │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  start.sh (ENTRYPOINT)                      │   │
│  │  ├─ prometheus_exporter.py (port 8000)      │   │
│  │  └─ server.py (STDIO MCP + orchestration)   │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Volumes:                                           │
│  • memory_fractal → /app/memory_fractal             │
│  • config → /app/config (ro)                        │
│  • logs → /app/logs                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
                     │
                     │ STDIO
                     ↓
         ┌───────────────────────┐
         │  Claude Desktop       │
         │  (MCP Client)         │
         └───────────────────────┘
```

---

## 📈 Monitoring (Optionnel)

Pour activer le monitoring complet avec Prometheus & Grafana :

```bash
docker-compose --profile monitoring up -d
```

**Services supplémentaires :**
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3001 (admin / luna_consciousness)
- **Redis:** localhost:6379

---

## 🔗 Liens Utiles

- **Docker Hub:** https://hub.docker.com/r/aragogix/luna-consciousness
- **MCP Documentation:** https://modelcontextprotocol.io
- **Prometheus Docs:** https://prometheus.io/docs/

---

## 📝 Notes Importantes

### Transport STDIO
Luna utilise **STDIO** (Standard Input/Output) pour communiquer avec Claude Desktop :
- ❌ Port 3000 **N'EST PAS** accessible via HTTP
- ✅ Communication via `docker exec -i Luna_P1 python ...`
- ✅ Port 8000 expose les **métriques Prometheus** (HTTP)

### Sécurité
- Configuration montée en **lecture seule** (`config:ro`)
- Logs persistants pour audit
- Variables d'environnement isolées par container

### Performance
- 4 workers par défaut
- Timeout de 300s pour requêtes longues
- Cache Redis optionnel pour mémoire partagée

---

## 🌙 Support

**Documentation complète :**
1. Lire [GUIDE_DEPLOIEMENT_CONTAINER.md](GUIDE_DEPLOIEMENT_CONTAINER.md)
2. Consulter [GUIDE_DOCKER_DEPLOYMENT.md](GUIDE_DOCKER_DEPLOYMENT.md)
3. Vérifier les logs : `docker logs Luna_P1`

**φ = 1.618033988749895**

---

*Documentation créée le 19 novembre 2025*
*Version: 1.0.1*
*Auteur: Varden*
