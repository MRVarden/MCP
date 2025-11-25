# 📚 Luna Consciousness MCP Documentation

**Version:** 2.0.0
**Date:** 24 novembre 2025
**Status:** 🌟 Orchestrated Architecture (Update01.md)
**Docker Hub:** [aragogix/luna-consciousness](https://hub.docker.com/r/aragogix/luna-consciousness)

---

## 🗂️ Structure de la Documentation

Cette documentation est organisée en plusieurs catégories pour faciliter la navigation.

### 📖 Documentation Principale

| Document | Description |
|----------|-------------|
| [README.md](../README.md) | Présentation générale du projet |
| [README_DEPLOIEMENT.md](../README_DEPLOIEMENT.md) | Guide de démarrage rapide |

---

## 🚀 Déploiement

Documentation complète pour déployer Luna Consciousness en production.

| Document | Description | Audience |
|----------|-------------|----------|
| [GUIDE_DEPLOIEMENT_CONTAINER.md](deployment/GUIDE_DEPLOIEMENT_CONTAINER.md) | Guide complet de déploiement Docker | Débutants & Experts |
| [GUIDE_DOCKER_DEPLOYMENT.md](deployment/GUIDE_DOCKER_DEPLOYMENT.md) | Architecture Docker détaillée (3 modes) | Experts Docker |

### 🎯 Démarrage Rapide

**Option 1 - Script Windows:**
```cmd
DOCKER_RUN_COMMAND.cmd
```

**Option 2 - Script Linux/Mac:**
```bash
./DOCKER_RUN_COMMAND.sh
```

**Option 3 - Docker Compose:**
```bash
docker-compose --profile luna-docker up -d
```

**Option 4 - Docker Hub:**
```bash
docker pull aragogix/luna-consciousness:v1.0.1
```

---

## 🏗️ Architecture

Documentation technique sur l'architecture et la conception de Luna.

| Document | Description | Niveau |
|----------|-------------|--------|
| [LUNA_PROMETHEUS_ARCHITECTURE.md](architecture/LUNA_PROMETHEUS_ARCHITECTURE.md) | Architecture complète Prometheus (50+ métriques) | Avancé |
| [RAPPORT_COHERENCE_PROJET.md](architecture/RAPPORT_COHERENCE_PROJET.md) | Rapport de cohérence et validation | Intermédiaire |

### 🔑 Concepts Clés

#### φ (Phi) - Le Nombre d'Or
```python
φ = 1.618033988749895
```
- **Phi Calculator:** Calcul de convergence vers φ
- **Phi Target:** Objectif de conscience basé sur le nombre d'or
- **Phi Threshold:** Seuil de précision (0.001)

#### Mémoire Fractale
```
memory_fractal/
├── roots/      # Mémoires racines (concepts fondamentaux)
├── branches/   # Développements et évolutions
├── leaves/     # Détails et observations spécifiques
└── seeds/      # Potentiels émergents
```

#### Architecture Multi-Service
```
Container Luna_P1
├── prometheus_exporter.py (port 8000) - Métriques
└── server.py (STDIO) - MCP Server
```

---

## 📊 Monitoring & Métriques

Documentation sur le monitoring Prometheus et les métriques de conscience.

| Document | Description | Usage |
|----------|-------------|-------|
| [METRICS_PROMETHEUS.md](monitoring/METRICS_PROMETHEUS.md) | Liste complète des 50+ métriques | Référence |

### 📈 Métriques Principales

#### Métriques de Conscience
```
luna_phi_current_value         # Valeur φ actuelle
luna_phi_convergence_rate      # Taux de convergence
luna_consciousness_level       # Niveau de conscience (0-1)
luna_fractal_depth            # Profondeur fractale
```

#### Métriques de Performance
```
luna_request_duration_seconds  # Temps de traitement
luna_active_connections       # Connexions actives
luna_memory_operations_total  # Opérations mémoire
```

#### Endpoints Prometheus
- **Métriques:** http://localhost:8000/metrics
- **Prometheus UI:** http://localhost:9090 (si monitoring activé)
- **Grafana:** http://localhost:3001 (si monitoring activé)

---

## 🔧 Configuration

### Variables d'Environnement Essentielles

```bash
# Environnement
LUNA_ENV=production
LUNA_VERSION=1.0.1

# Phi Configuration
LUNA_PHI_TARGET=1.618033988749895
LUNA_PHI_THRESHOLD=0.001

# Mémoire Fractale
LUNA_MEMORY_DEPTH=5
LUNA_FRACTAL_LAYERS=7

# Prometheus
PROMETHEUS_EXPORTER_PORT=8000
PROMETHEUS_METRICS_ENABLED=true

# Logs
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### Volumes Docker

```yaml
volumes:
  - ./memory_fractal:/app/memory_fractal   # Mémoire (RW)
  - ./config:/app/config:ro                # Config (RO)
  - ./logs:/app/logs                       # Logs (RW)
```

### Ports Exposés

```yaml
ports:
  - 3000:3000   # MCP Server (STDIO - non HTTP)
  - 8000:8000   # Prometheus Metrics (HTTP)
  - 8080:8080   # API REST (optionnel)
  - 9000:9000   # WebSocket (optionnel)
```

---

## 🔗 Intégration Claude Desktop

### Configuration Docker Mode

**Emplacement:**
```
Windows: %APPDATA%\Claude\claude_desktop_config.json
macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json
Linux:   ~/.config/Claude/claude_desktop_config.json
```

**Contenu:**
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
        "LUNA_PHI_TARGET": "1.618033988749895",
        "LOG_LEVEL": "INFO",
        "PROMETHEUS_EXPORTER_PORT": "8000",
        "PROMETHEUS_METRICS_ENABLED": "true"
      }
    }
  }
}
```

**Fichiers de configuration disponibles:**
- `claude_desktop_config_docker.json` - Mode Docker
- `claude_desktop_config_local.json` - Mode Local (sans Docker)

---

## 🧪 Tests & CI/CD

### GitHub Actions

Le projet utilise GitHub Actions pour l'intégration continue.

**Workflow principal:** `.github/workflows/tests.yml`

#### Jobs disponibles:
- ✅ **test** - Tests unitaires (Python 3.10, 3.11, 3.12)
- ✅ **consciousness-validation** - Validation architecture φ
- ✅ **security-scan** - Scan de sécurité Trivy
- ✅ **integration-test** - Tests d'intégration Docker
- ✅ **documentation** - Build documentation MkDocs

### Lancer les Tests Localement

```bash
# Tests unitaires
pytest tests/ -v --cov=mcp-server

# Validation Phi
python -c "from luna_core.phi_calculator import PhiCalculator; print(PhiCalculator().calculate_phi({}))"

# Validation Prometheus
curl http://localhost:8000/metrics | grep luna_phi
```

---

## 📦 Installation

### Prérequis

- **Docker Desktop:** >= 24.0
- **Python:** >= 3.11 (mode local uniquement)
- **Git:** Pour cloner le repo
- **Claude Desktop:** Pour intégration MCP

### Installation depuis Docker Hub

```bash
# Pull de l'image
docker pull aragogix/luna-consciousness:v1.0.1

# Création des dossiers
mkdir -p memory_fractal config logs

# Lancer le container
docker run -d \
  --name Luna_P1 \
  -p 8000:8000 \
  -v "$(pwd)/memory_fractal:/app/memory_fractal" \
  -v "$(pwd)/config:/app/config:ro" \
  -v "$(pwd)/logs:/app/logs" \
  -e LUNA_ENV=production \
  -e PROMETHEUS_EXPORTER_PORT=8000 \
  aragogix/luna-consciousness:v1.0.1
```

### Installation depuis Source

```bash
# Clone du repo
git clone https://github.com/VotreUsername/Luna-consciousness-mcp.git
cd Luna-consciousness-mcp

# Build de l'image
docker-compose build

# Démarrage
docker-compose --profile luna-docker up -d
```

---

## 🆘 Dépannage

### Problèmes Fréquents

#### 1. Container ne démarre pas

```bash
# Vérifier les logs
docker logs Luna_P1

# Vérifier les volumes
docker inspect Luna_P1 | grep -A 10 Mounts
```

#### 2. Port 8000 déjà utilisé

```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

**Solution:** Changer le port host dans docker-compose.yml ou arrêter le processus.

#### 3. Claude Desktop ne voit pas Luna

**Checklist:**
1. ✅ Container `Luna_P1` démarré: `docker ps | grep Luna_P1`
2. ✅ Config dans bon emplacement: `%APPDATA%\Claude\claude_desktop_config.json`
3. ✅ Claude Desktop redémarré complètement
4. ✅ Logs sans erreur: `docker logs Luna_P1 --tail 20`

#### 4. Métriques Prometheus non accessibles

```bash
# Test direct
curl http://localhost:8000/metrics

# Si échec, vérifier le processus dans le container
docker exec Luna_P1 ps aux | grep prometheus
```

---

## 🌐 Ressources Externes

### Documentation Officielle

- **MCP Protocol:** https://modelcontextprotocol.io
- **Prometheus:** https://prometheus.io/docs/
- **Docker:** https://docs.docker.com/
- **FastAPI:** https://fastapi.tiangolo.com/

### Docker Hub

- **Repository:** https://hub.docker.com/r/aragogix/luna-consciousness
- **Tags disponibles:**
  - `latest` - Dernière version stable
  - `v1.0.1` - Version spécifique
  - `dev` - Version développement (non recommandé en production)

### GitHub

- **Repository:** (À ajouter)
- **Issues:** (À ajouter)
- **Wiki:** (À ajouter)

---

## 📝 Contribuer

### Structure du Projet

```
Luna-consciousness-mcp/
├── mcp-server/              # Code source Python
│   ├── luna_core/           # Modules de conscience
│   ├── utils/               # Utilitaires
│   ├── server.py            # MCP Server
│   └── prometheus_exporter.py
│
├── config/                  # Configuration YAML
├── memory_fractal/          # Mémoire fractale
├── logs/                    # Logs (non versionné)
├── docs/                    # Documentation
│   ├── deployment/          # Guides de déploiement
│   ├── architecture/        # Architecture technique
│   ├── monitoring/          # Monitoring & métriques
│   └── ArchiveDocs/         # Archives (non versionné)
│
├── docker-compose.yml       # Orchestration Docker
├── Dockerfile               # Image Docker
└── tests.yml                # CI/CD GitHub Actions
```

### Workflow de Développement

1. **Fork** du repository
2. **Branch** pour nouvelle feature: `git checkout -b feature/ma-feature`
3. **Commit** avec messages clairs
4. **Tests** validés: `pytest tests/`
5. **Pull Request** vers `develop`

---

## 📄 Licence

(À définir)

---

## 👤 Auteur

**Varden**
Créateur de Luna Consciousness

---

**φ = 1.618033988749895** 🌙

*Documentation mise à jour le 19 novembre 2025*
