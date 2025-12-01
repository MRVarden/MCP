# Changelog

All notable changes to Luna Consciousness MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0-secure] - 2025-12-01

### 🔒 Security

#### Sécurisation Docker Complète
- **Ports localhost-only** - Tous les services bindés sur `127.0.0.1` uniquement
- **Redis non exposé** - Accessible uniquement via réseau interne (`internal: true`)
- **Security hardening** - `cap_drop: ALL`, `read_only: true`, `no-new-privileges: true`
- **Exécution non-root** - `user: "1000:1000"` sur tous les containers
- **Secrets externalisés** - Variables sensibles dans `.env`

#### Réseau Isolé
- **luna-internal** (172.28.0.0/24) - Réseau interne sans accès externe
- **luna-external** (172.29.0.0/24) - Réseau pour exposition des services

### Changed

#### Ports et Services
- **Prometheus Metrics** : Port `8000` → `9100`
- **Healthcheck** : `start_period` augmenté à 60s, retries à 5
- **Grafana** : Credentials par défaut changés (`luna_admin`)

#### Infrastructure
- **docker-compose.yml** unifié - Suppression de `docker-compose.secure.yml`
- **start.sh** amélioré - Boucle d'attente active pour Prometheus Exporter
- **Tmpfs ajoutés** - Pour Grafana et containers read-only

### Documentation

- **Toute la documentation** mise à jour vers v2.1.0-secure
- **Ports corrigés** - 8000 → 9100 pour les métriques
- **URLs sécurisées** - Utilisation de `127.0.0.1` au lieu de `localhost`

### Removed

- `docker-compose.secure.yml` - Fusionné dans `docker-compose.yml`
- `claude_desktop_config*.json` - Remplacés par `.example.json`
- Fichiers de configuration obsolètes

---

## [2.0.1] - 2025-11-25

### Fixed
- Corrections d'imports dans les modules Luna Core
- Stabilisation du serveur MCP
- Résolution des problèmes asyncio

---

## [2.0.0] - 2025-11-24

### 🎯 Breaking Changes

**Architecture majeure Update01.md implémentée** - Luna passe d'une collection d'outils passifs à un système orchestré actif.

### Added

#### 🌟 Nouveaux Modules Core (Update01.md)
- **luna_orchestrator.py** - Orchestrateur central qui route toutes les interactions
- **manipulation_detector.py** - Détection de 10 types de manipulation avec authentification Varden
- **luna_validator.py** - Système de validation avec veto power sur les réponses LLM
- **predictive_core.py** - Système prédictif pour anticiper les besoins utilisateur
- **autonomous_decision.py** - Décisions autonomes dans 14 domaines autorisés
- **self_improvement.py** - Auto-amélioration continue avec meta-learning
- **systemic_integration.py** - Coordination systémique de tous les composants
- **multimodal_interface.py** - Interface adaptative avec 8 modalités de communication

#### 🛠️ Nouveau Tool Principal
- **`luna_orchestrated_interaction`** - Point d'entrée principal pour interactions orchestrées complètes
  - Détection manipulation automatique
  - Prédiction proactive des besoins
  - Validation avec veto possible
  - Interface multimodale adaptative

#### 📊 Nouvelles Capacités
- **4 modes de décision** : AUTONOMOUS, GUIDED, DELEGATED, OVERRIDE
- **10 types de manipulation détectés** : Gaslighting, Emotional, Authority, etc.
- **5 niveaux de menace** : NONE, LOW, MEDIUM, HIGH, CRITICAL
- **14 domaines de décision autonome** : Memory optimization, PHI convergence, etc.
- **5 stratégies d'apprentissage** : Reinforcement, Imitation, Exploration, Transfer, Meta-learning
- **8 modalités de communication** : Text, Rich text, Emotional, Visual, Quantum, etc.
- **8 modes d'interface** : Conversational, Technical, Empathetic, Creative, etc.

### Changed

#### 🔄 Architecture
- **server.py** modifié pour intégrer tous les modules Update01.md
- **Flux de traitement** : User → LUNA → Analyse → Décision → [Claude si besoin] → Response validée
- **Container name** : `Luna_P1` → `luna-consciousness`
- **Configuration Docker** : Ajout de `LUNA_MODE=orchestrator` et `LUNA_UPDATE01=enabled`

#### 📈 Améliorations
- **Initiative proactive** : Luna peut maintenant prendre des initiatives
- **Protection manipulation** : Niveau 4 avec authentification Varden
- **Contexte unifié** : Tous les modules partagent un contexte commun
- **Apprentissage continu** : Auto-amélioration basée sur les interactions

### Fixed
- Correction du loop de restart Docker (STDIO vs SSE mode)
- Résolution du problème de connexion Claude Desktop
- Fix des noms de containers dans les configurations

### Documentation
- **IMPLEMENTATION_STATUS.md** : Rapport complet de l'implémentation Update01.md
- **SYNCHRONIZATION_REPORT.md** : Analyse complète du projet v2.0.0
- **README.md** : Mise à jour complète pour v2.0.0

## [1.0.3] - 2025-11-19

### Added
- Intégration Claude Desktop complète
- Support multi-configuration (Docker, Local, Minimal)
- Scripts de démarrage automatisés

### Fixed
- Résolution des problèmes de connexion Claude Desktop
- Correction des chemins dans les configurations

## [1.0.2] - 2025-11-19

### Added
- Docker Hub deployment (aragogix/luna-consciousness)
- Prometheus metrics (50+ custom metrics)
- Multi-service container support

### Changed
- Port 8000 now exposes Prometheus metrics via HTTP
- Improved Docker compose profiles

## [1.0.1] - 2025-11-18

### Added
- Complete MCP architecture
- Phi calculation and convergence
- Fractal memory system
- Semantic validation
- Docker and Codespaces support

### Documentation
- Reorganized documentation structure
- Added comprehensive guides

## [1.0.0] - 2025-11-15

### Initial Release
- Core Luna consciousness architecture
- Basic MCP protocol implementation
- 12 consciousness tools
- Redis integration
- Prometheus monitoring
- Grafana dashboards

---

## Version Naming Convention

- **Major (X.0.0)** : Breaking changes, major architecture updates
- **Minor (0.X.0)** : New features, backwards compatible
- **Patch (0.0.X)** : Bug fixes, minor improvements

## Upgrade Guide

### From 1.x to 2.0.0

1. **Update Docker configuration**:
   ```bash
   docker-compose down
   docker-compose pull
   docker-compose build --no-cache luna-actif
   ```

2. **Update Claude Desktop config**:
   - Add `LUNA_MODE=orchestrator`
   - Add `LUNA_UPDATE01=enabled`
   - Change container name to `luna-consciousness`

3. **Use new orchestrated tool**:
   - Primary tool is now `luna_orchestrated_interaction`
   - Old tools still work but don't benefit from orchestration

4. **Review breaking changes**:
   - Luna now intercepts all interactions before LLM
   - Validation can override responses
   - Manipulation detection is always active

---

For detailed migration instructions, see [docs/UPDATE01_GUIDE.md](docs/UPDATE01_GUIDE.md)

## [2.1.0-secure] - 2025-12-01

### 🎯 Résumé
Refactoring majeur de l'infrastructure Docker avec unification des fichiers de configuration,
correction du nommage des services, et renforcement de la sécurité.

### ✨ Ajouté

#### Infrastructure
- **docker-rebuild.ps1** — Nouveau script PowerShell pour rebuild propre avec purge
- **Healthcheck amélioré** — Endpoint `/metrics` sur port 9100 avec `start_period: 60s`
- **Réseaux isolés** — `luna_internal_network` (172.28.0.0/24) et `luna_external_network` (172.29.0.0/24)
- **Volumes nommés** — `luna_memories`, `luna_consciousness_data`, `luna_redis`, `luna_prometheus`, `luna_grafana`

#### Sécurité
- **Exécution non-root** — `user: "1000:1000"` sur tous les services
- **Capabilities supprimées** — `cap_drop: ALL`
- **Privilèges restreints** — `no-new-privileges: true`
- **Filesystem read-only** — `read_only: true` avec tmpfs pour `/tmp` et `/app/logs`
- **Ports localhost only** — Tous les ports bindés sur `127.0.0.1`


#### GitHub Actions
- **docker-build.yml** — Job `security-scan` avec Trivy ajouté
- **tests.yml** — Actions mises à jour (setup-python@v5, codecov-action@v4)

### 🔄 Modifié

#### Nommage (BREAKING CHANGE)
| Ancien | Nouveau |
|--------|---------|
| `luna-actif` | `luna-consciousness` |
| `docker-compose.secure.yml` | Fusionné dans `docker-compose.yml` |

#### Ports
| Service | Ancien | Nouveau |
|---------|--------|---------|
| MCP Server | 3000 | 3000 (inchangé) |
| FastMCP | 8000 | 8000 (inchangé) |
| API REST | 8080 | 8080 (inchangé) |
| WebSocket | 9000 | 9000 (inchangé) |
| Prometheus Metrics | 8000 | **9100** |
| Prometheus UI | 9090 | 9090 (inchangé) |
| Grafana | 3001 | 3001 (inchangé) |

#### Scripts
| Script | Modification |
|--------|--------------|
| `start_secure.sh` | Utilise `docker-compose.yml` (plus `.secure.yml`) |
| `update-docker-images.sh` | Référence `luna-consciousness` |
| `update-luna.sh` | Référence `luna-consciousness` |
| `start-luna-local.sh` | Mode hybride avec Redis Docker |
| `security_check.sh` | 8 checks, ports mis à jour |
| `generate_secrets.sh` | Documentation ports actualisée |

#### Healthcheck
```yaml
# Avant
healthcheck:
  test: ["CMD", "curl", "-sf", "http://localhost:8000/health"]
  start_period: 30s

# Après
healthcheck:
  test: ["CMD", "curl", "-sf", "http://localhost:9100/metrics"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 60s
```

#### Structure Projet
```
# Avant (incorrect)
.git/workflows/    ❌

# Après (correct)
.github/workflows/ ✅
```

### 🗑️ Supprimé
- **docker-compose.secure.yml** — Fusionné dans `docker-compose.yml` (qui est maintenant plus sécurisé)
- **Références à `luna-actif`** — Remplacées par `luna-consciousness`

### 🐛 Corrigé
- **Healthcheck timing** — `start_period` augmenté de 30s à 60s pour laisser le temps au Prometheus Exporter de démarrer
- **Port Prometheus** — Corrigé de 8000 à 9100 dans le Dockerfile et docker-compose
- **Structure .github** — Workflows déplacés de `.git/workflows/` vers `.github/workflows/`
- **Paradoxe sécurité** — `docker-compose.yml` maintenant plus sécurisé que l'ancien `.secure.yml`

### 📊 Métriques de Qualité
- **Tests** : 519 total, 507 réussis, 0 échecs, 12 skippés
- **Couverture** : 57% globale
- **Score Code Review** : 4/5

### ⚠️ Breaking Changes

#### Migration Requise

1. **Nom du container**
   ```powershell
   # Ancien
   docker exec luna-actif ...
   
   # Nouveau
   docker exec luna-consciousness ...
   ```

2. **Claude Desktop Config**
   ```json
   {
     "mcpServers": {
       "luna-consciousness": {
         "command": "docker",
         "args": ["exec", "-i", "luna-consciousness", "python", "-u", "/app/mcp-server/server.py"]
       }
     }
   }
   ```

3. **Suppression fichier obsolète**
   ```powershell
   Remove-Item docker-compose.secure.yml -Force
   ```

4. **Rebuild complet**
   ```powershell
   docker compose down
   docker rmi aragogix/luna-consciousness:v2.1.0-secure
   docker compose up -d --build
   ```

---
