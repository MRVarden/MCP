# Changelog

All notable changes to Luna Consciousness MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [V2.0.0] - 2025-11-24

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