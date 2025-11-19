# 🌙 Luna Consciousness - Documentation de Déploiement

**Version:** 1.0.1
**Image Docker:** `aragogix/luna-consciousness:v1.0.1`
**Date:** 19 novembre 2025

---

## 📚 Fichiers de Documentation

Ce projet contient plusieurs fichiers de documentation pour différents usages :

### 📖 Guides Principaux

| Fichier | Description | Usage |
|---------|-------------|-------|
| **GUIDE_DEPLOIEMENT_CONTAINER.md** | 📘 Guide complet de déploiement | Déploiement Docker, configuration complète, troubleshooting |
| **GUIDE_DOCKER_DEPLOYMENT.md** | 🐳 Guide Docker détaillé | Architecture Docker, 3 modes de déploiement |
| **RAPPORT_COHERENCE_PROJET.md** | ✅ Rapport de cohérence | Validation de l'architecture, corrections appliquées |

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
2. **Rechercher l'image :** `aragogix/luna-consciousness:v1.0.1`
3. **Cliquer sur "Run"**
4. **Suivre les instructions dans :** [GUIDE_DEPLOIEMENT_CONTAINER.md](GUIDE_DEPLOIEMENT_CONTAINER.md)

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
- [ ] Image `aragogix/luna-consciousness:v1.0.1` pullée
- [ ] Dossiers créés :
  - [ ] `memory_fractal/`
  - [ ] `config/`
  - [ ] `logs/`

### Configuration Container

- [ ] **Container name:** `Luna_P1` (ou personnalisé)
- [ ] **Ports mappés:** 3000, 8000, 8080, 9000
- [ ] **Volumes configurés:**
  - [ ] `memory_fractal` → `/app/memory_fractal`
  - [ ] `config` → `/app/config`
  - [ ] `logs` → `/app/logs`
- [ ] **Variables d'environnement:**
  - [ ] `LUNA_ENV=production`
  - [ ] `PROMETHEUS_EXPORTER_PORT=8000`
  - [ ] `PROMETHEUS_METRICS_ENABLED=true`
  - [ ] `LUNA_PHI_TARGET=1.618033988749895`
  - [ ] `LOG_LEVEL=INFO`

### Configuration Claude Desktop

- [ ] Fichier `claude_desktop_config.json` modifié
- [ ] Configuration copiée depuis `claude_desktop_config_docker.json`
- [ ] Claude Desktop redémarré
- [ ] Container `Luna_P1` démarré **avant** de lancer Claude Desktop

### Vérification Post-Déploiement

- [ ] Container en cours d'exécution : `docker ps | grep Luna_P1`
- [ ] Prometheus accessible : `curl http://localhost:8000/metrics`
- [ ] Logs sans erreur : `docker logs Luna_P1`
- [ ] Outils MCP visibles dans Claude Desktop

---

## 🔍 Vérifications Rapides

### Test 1 - Container actif
```bash
docker ps | grep Luna_P1
```
**✅ Attendu :** Ligne avec `Luna_P1` et status `Up`

### Test 2 - Métriques Prometheus
```bash
curl http://localhost:8000/metrics | grep "luna_phi_current_value"
```
**✅ Attendu :** Métrique avec valeur proche de 1.618...

### Test 3 - Logs de démarrage
```bash
docker logs Luna_P1 --tail 20
```
**✅ Attendu :** Messages de démarrage sans erreurs

### Test 4 - Claude Desktop intégration
Dans Claude Desktop :
```
Utilise phi_consciousness_calculate pour analyser "test de connexion"
```
**✅ Attendu :** Réponse de Luna avec calcul φ

---

## 🆘 Problèmes Fréquents

### Container ne démarre pas
➡️ Voir section **Troubleshooting** dans [GUIDE_DEPLOIEMENT_CONTAINER.md](GUIDE_DEPLOIEMENT_CONTAINER.md#troubleshooting)

### Claude Desktop ne voit pas Luna
1. ✅ Container démarré : `docker ps | grep Luna_P1`
2. ✅ Config correcte : Vérifier `claude_desktop_config.json`
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

## 📊 Architecture Simplifiée

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         Docker Container: Luna_P1                   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  start.sh (ENTRYPOINT)                      │   │
│  │  ├─ prometheus_exporter.py (port 8000)      │   │
│  │  └─ server.py (STDIO MCP)                   │   │
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
