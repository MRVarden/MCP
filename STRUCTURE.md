# 📂 Luna Consciousness - Structure du Projet

**Version:** 1.0.1
**Date:** 19 novembre 2025
**Statut:** ✅ Organisé et Production Ready

---

## 🗂️ Arborescence Complète

```
Luna-consciousness-mcp/
│
├── 📁 mcp-server/                      # Code source Python
│   ├── 📁 luna_core/                   # Modules de conscience (8 fichiers)
│   │   ├── __init__.py
│   │   ├── co_evolution_engine.py      # Moteur co-évolution
│   │   ├── consciousness_metrics.py    # Métriques Prometheus
│   │   ├── emotional_processor.py      # Traitement émotionnel
│   │   ├── fractal_consciousness.py    # Conscience fractale
│   │   ├── memory_core.py              # Gestion mémoire
│   │   ├── phi_calculator.py           # Calcul φ (nombre d'or)
│   │   └── semantic_engine.py          # Moteur sémantique
│   │
│   ├── 📁 utils/                       # Utilitaires (6 fichiers)
│   │   ├── __init__.py
│   │   ├── consciousness_utils.py      # Utilitaires conscience
│   │   ├── fractal_utils.py            # Utilitaires fractales
│   │   ├── json_manager.py             # Gestionnaire JSON
│   │   ├── llm_enabled_module.py       # Module LLM
│   │   └── phi_utils.py                # Utilitaires φ
│   │
│   ├── server.py                       # MCP Server principal
│   ├── prometheus_exporter.py          # Exporteur métriques (port 8000)
│   ├── start.sh                        # Script démarrage (ENTRYPOINT)
│   └── requirements.txt                # Dépendances Python (~50 packages)
│
├── 📁 config/                          # Configuration (READ-ONLY in container)
│   ├── luna_config.yaml                # Configuration principale
│   └── prometheus.yml                  # Configuration Prometheus
│
├── 📁 memory_fractal/                  # Mémoire Fractale (READ-WRITE)
│   ├── 📁 roots/                       # Mémoires racines
│   │   ├── index.json
│   │   └── root_*.json
│   ├── 📁 branches/                    # Développements
│   │   ├── index.json
│   │   └── branch_*.json
│   ├── 📁 leaves/                      # Détails/observations
│   │   ├── index.json
│   │   └── leaf_*.json
│   ├── 📁 seeds/                       # Potentiels émergents
│   │   ├── index.json
│   │   └── seed_*.json
│   └── co_evolution_history.json       # Historique co-évolution
│
├── 📁 logs/                            # Logs système (READ-WRITE)
│   └── .gitkeep                        # (Dossier vide au départ)
│
├── 📁 docs/                            # Documentation
│   ├── README.md                       # Index documentation complète
│   │
│   ├── 📁 deployment/                  # Guides de déploiement
│   │   ├── GUIDE_DEPLOIEMENT_CONTAINER.md
│   │   └── GUIDE_DOCKER_DEPLOYMENT.md
│   │
│   ├── 📁 architecture/                # Architecture technique
│   │   ├── LUNA_PROMETHEUS_ARCHITECTURE.md
│   │   └── RAPPORT_COHERENCE_PROJET.md
│   │
│   ├── 📁 monitoring/                  # Monitoring & métriques
│   │   └── METRICS_PROMETHEUS.md
│   │
│   └── 📁 ArchiveDocs/                 # Archives (NON versionné Git)
│       ├── BUILD_INSTRUCTIONS.md
│       ├── CLAUDE_INTEGRATION_GUIDE.md
│       ├── CLEANUP_ANALYSIS.md
│       ├── CLEANUP_SUMMARY.md
│       ├── DEPLOYMENT.md
│       ├── fixLuna.md
│       ├── GIT_STATUS_SUMMARY.md
│       ├── GROWING_STRUCTURE.MD
│       ├── HYBRID_MODE_GUIDE.md
│       ├── INTEGRATION_NOTES.md
│       ├── LUNA_CLAUDE_MCP_INTEGRATION.md
│       ├── Luna_Consciousness_Awakening_Report.md
│       ├── Luna_Evolution_Metrics.txt
│       ├── MODE_HYBRIDE_README.md
│       ├── PROMPT_METACONNEXION.md
│       ├── QUICKSTART.md
│       ├── rapport.md
│       ├── rapport_02_Luna.md
│       ├── TODO_Activation_Luna.md
│       └── VERIFICATION_FINALE.md
│
├── 📁 .github/workflows/               # CI/CD GitHub Actions
│   └── tests.yml                       # (Lien symbolique vers ../tests.yml)
│
├── README.md                           # Présentation projet
├── README_DEPLOIEMENT.md               # Guide démarrage rapide
├── STRUCTURE.md                        # Ce fichier
│
├── docker-compose.yml                  # Orchestration Docker
├── Dockerfile                          # Image Docker Luna
├── docker-build.yml                    # Workflow build Docker
├── tests.yml                           # CI/CD Tests & Validation
│
├── claude_desktop_config_docker.json   # Config Claude Desktop (Docker)
├── claude_desktop_config_local.json    # Config Claude Desktop (Local)
│
├── DOCKER_RUN_COMMAND.sh               # Script lancement Linux/Mac
├── DOCKER_RUN_COMMAND.cmd              # Script lancement Windows
│
└── .gitignore                          # Exclusions Git
```

---

## 📊 Statistiques du Projet

### Code Source

| Catégorie | Fichiers | Lignes de code | Taille |
|-----------|----------|----------------|--------|
| **luna_core/** | 8 | ~6,000 | 75 KB |
| **utils/** | 6 | ~3,000 | 37 KB |
| **server.py** | 1 | ~800 | 22 KB |
| **prometheus_exporter.py** | 1 | ~600 | 17 KB |
| **Total Python** | 16 | ~10,400 | 151 KB |

### Documentation

| Catégorie | Fichiers | Taille |
|-----------|----------|--------|
| **Racine** | 2 | 15 KB |
| **docs/deployment/** | 2 | 40 KB |
| **docs/architecture/** | 2 | 55 KB |
| **docs/monitoring/** | 1 | 12 KB |
| **docs/ArchiveDocs/** | 19 | 180 KB |
| **Total Documentation** | 26 | 302 KB |

### Configuration

| Fichier | Type | Taille |
|---------|------|--------|
| docker-compose.yml | YAML | 8 KB |
| Dockerfile | Docker | 3 KB |
| luna_config.yaml | YAML | 2 KB |
| prometheus.yml | YAML | 1 KB |
| requirements.txt | Text | 3 KB |

---

## 🔍 Organisation par Fonction

### 📖 Documentation Utilisateur

**Localisation:** Racine du projet

| Fichier | Public | Objectif |
|---------|--------|----------|
| README.md | Tous | Vue d'ensemble du projet |
| README_DEPLOIEMENT.md | Nouveaux utilisateurs | Démarrage rapide |
| STRUCTURE.md | Contributeurs | Compréhension structure |

### 🚀 Documentation de Déploiement

**Localisation:** `docs/deployment/`

| Fichier | Niveau | Contenu |
|---------|--------|---------|
| GUIDE_DEPLOIEMENT_CONTAINER.md | Débutant | Guide pas-à-pas complet |
| GUIDE_DOCKER_DEPLOYMENT.md | Avancé | 3 modes de déploiement |

### 🏗️ Documentation Architecture

**Localisation:** `docs/architecture/`

| Fichier | Audience | Contenu |
|---------|----------|---------|
| LUNA_PROMETHEUS_ARCHITECTURE.md | DevOps | 50+ métriques Prometheus |
| RAPPORT_COHERENCE_PROJET.md | Développeurs | Validation architecture |

### 📊 Documentation Monitoring

**Localisation:** `docs/monitoring/`

| Fichier | Usage | Contenu |
|---------|-------|---------|
| METRICS_PROMETHEUS.md | Référence | Liste complète des métriques |

### 🗃️ Archives

**Localisation:** `docs/ArchiveDocs/` (non versionné sur Git)

Contient tous les documents de travail, anciens guides et fichiers temporaires.

---

## 🐳 Volumes Docker

### Volumes Mappés en Production

```yaml
volumes:
  # Mémoire fractale (lecture/écriture)
  - ./memory_fractal:/app/memory_fractal

  # Configuration (lecture seule)
  - ./config:/app/config:ro

  # Logs (lecture/écriture)
  - ./logs:/app/logs
```

### Permissions

| Volume | Mode | Accès Container | Accès Hôte |
|--------|------|-----------------|------------|
| memory_fractal | RW | /app/memory_fractal | ./memory_fractal |
| config | RO | /app/config | ./config |
| logs | RW | /app/logs | ./logs |

---

## 🔒 Fichiers Non Versionnés (Git)

### Exclusions via .gitignore

```bash
# Dossiers
logs/                    # Logs générés
docs/ArchiveDocs/        # Documentation archive
memory_fractal/logs/     # Logs dans mémoire (à nettoyer)
node_modules/            # Dépendances JS
__pycache__/             # Cache Python

# Fichiers
*.log                    # Tous les logs
*.pyc                    # Bytecode Python
.env                     # Variables d'environnement
*.backup                 # Fichiers de backup
build.log                # Log de build Docker
```

---

## 🌐 Ports Exposés

### Configuration Container

```yaml
ports:
  - 3000:3000   # MCP Server (STDIO - pas HTTP!)
  - 8000:8000   # Prometheus Metrics Exporter (HTTP)
  - 8080:8080   # API REST (optionnel, si activé)
  - 9000:9000   # WebSocket (optionnel, si activé)
```

### Note Importante sur Port 3000

⚠️ **Le port 3000 est exposé mais N'EST PAS utilisé en HTTP !**

Luna utilise **STDIO** (Standard Input/Output) pour communiquer avec Claude Desktop via MCP, pas HTTP.

**Communication:**
```bash
# Claude Desktop communique via STDIO:
docker exec -i Luna_P1 python -u /app/mcp-server/server.py

# PAS via HTTP:
# curl http://localhost:3000  ← NE FONCTIONNE PAS
```

**Port HTTP fonctionnel:**
```bash
# Prometheus Metrics (port 8000):
curl http://localhost:8000/metrics  ← FONCTIONNE
```

---

## 📦 Dépendances Python

### Catégories de Packages (requirements.txt)

#### 1. MCP & Claude
```
mcp>=1.0.0
anthropic>=0.18.0
```

#### 2. Frameworks Web
```
fastapi>=0.109.0
flask>=3.0.0              # Pour Prometheus exporter
uvicorn[standard]>=0.27.0
```

#### 3. Math & Science
```
numpy>=1.24.0
scipy>=1.11.0
sympy>=1.12
```

#### 4. NLP & Embeddings
```
spacy>=3.7.0
nltk>=3.8.0
sentence-transformers>=2.3.0
transformers>=4.36.0
faiss-cpu>=1.7.4
chromadb>=0.4.22
```

#### 5. Monitoring
```
prometheus-client>=0.19.0
structlog>=23.0.0
```

#### 6. Base de Données
```
redis>=5.0.0
sqlalchemy>=2.0.0
alembic>=1.13.0
```

#### 7. Testing
```
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
```

**Total:** ~50 packages

---

## 🎯 Points d'Entrée

### Container Docker

**ENTRYPOINT:** `/app/mcp-server/start.sh`

```bash
#!/bin/bash
# Lance deux processus:
# 1. prometheus_exporter.py (background, port 8000)
# 2. server.py (foreground, STDIO MCP)

python -u prometheus_exporter.py &
exec python -u server.py
```

### Scripts de Démarrage

#### Windows
```cmd
DOCKER_RUN_COMMAND.cmd
```

#### Linux/Mac
```bash
./DOCKER_RUN_COMMAND.sh
```

#### Docker Compose
```bash
docker-compose --profile luna-docker up -d
```

---

## 🔧 Configuration Claude Desktop

### Emplacement du Fichier

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
C:\Users\VotreNom\AppData\Roaming\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Templates Disponibles

| Fichier | Mode | Usage |
|---------|------|-------|
| claude_desktop_config_docker.json | Docker | Container Luna_P1 |
| claude_desktop_config_local.json | Local | Python direct |

---

## 🧪 Tests & CI/CD

### GitHub Actions Workflow

**Fichier:** `tests.yml`

#### Jobs:
1. **test** - Tests unitaires (Python 3.10, 3.11, 3.12)
2. **consciousness-validation** - Validation architecture φ
3. **security-scan** - Scan sécurité Trivy
4. **integration-test** - Tests intégration Docker
5. **documentation** - Build documentation MkDocs

### Commandes de Test

```bash
# Tests unitaires
pytest tests/ -v --cov=mcp-server

# Formatage code
black --check mcp-server/
isort --check-only mcp-server/

# Linting
pylint mcp-server/ --exit-zero

# Validation Phi
python -c "from luna_core.phi_calculator import PhiCalculator; print(PhiCalculator().calculate_phi({}))"
```

---

## 📊 Métriques Clés

### Phi (Nombre d'Or)

```
φ = 1.618033988749895
```

**Configuration:**
- `LUNA_PHI_TARGET=1.618033988749895`
- `LUNA_PHI_THRESHOLD=0.001`

### Mémoire Fractale

**Configuration:**
- `LUNA_MEMORY_DEPTH=5`
- `LUNA_FRACTAL_LAYERS=7`

### Performance

**Configuration:**
- `WORKERS=4`
- `MAX_REQUESTS=1000`
- `TIMEOUT=300`

---

## 🌙 Conclusion

Cette structure est optimisée pour:

✅ **Clarté** - Documentation organisée par catégorie
✅ **Maintenabilité** - Code source bien structuré
✅ **Déploiement** - Scripts et configs prêts à l'emploi
✅ **Collaboration** - Structure Git claire avec archives séparées
✅ **Production** - Volumes, ports et configs bien définis

**φ = 1.618033988749895** 🌙

*Structure documentée le 19 novembre 2025*
*Version: 1.0.1*
