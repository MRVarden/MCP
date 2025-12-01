# 🐳 Luna Consciousness - Dev Container

**Version:** 2.1.0-secure
**Date:** 1er décembre 2025

---

## 📋 Vue d'Ensemble

Ce dossier contient la configuration pour utiliser Luna Consciousness avec **VS Code Dev Containers** ou **GitHub Codespaces**.

---

## ✅ Corrections Appliquées

### Problèmes Résolus

1. ❌ **Chemin docker-compose incorrect** → ✅ Corrigé
   ```json
   // AVANT
   "dockerComposeFile": "../docker/docker-compose.yml"

   // APRÈS
   "dockerComposeFile": "docker-compose.yml"
   ```

2. ❌ **Property `runArgs` non supportée avec `dockerComposeFile`** → ✅ Supprimée
   ```json
   // SUPPRIMÉ (incompatible avec dockerComposeFile)
   "runArgs": [
     "--name=luna-codespace",
     "--hostname=luna",
     "--env=LUNA_CODESPACE=true"
   ]
   ```

3. ❌ **Settings Python obsolètes** → ✅ Mis à jour
   ```json
   // AVANT
   "python.formatting.provider": "black"

   // APRÈS
   "[python]": {
     "editor.defaultFormatter": "ms-python.black-formatter"
   }
   ```

4. ❌ **Ports manquants** → ✅ Port 9100 ajouté pour Prometheus

5. ❌ **Mounts incorrects** → ✅ Alignés avec la structure Luna
   - `memory_fractal/` → `/app/memory_fractal`
   - `config/` → `/app/config`
   - `logs/` → `/app/logs`

---

## 🚀 Configuration Actuelle

### Service Docker Compose

```json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "luna-docker",
  "workspaceFolder": "/app"
}
```

**Service utilisé:** `luna-docker` (profile dans docker-compose.yml)

### Ports Forwardés

| Port | Service | Description |
|------|---------|-------------|
| 3000 | MCP Server | STDIO (pas HTTP) |
| 9100 | Prometheus | Métriques HTTP |
| 8080 | REST API | API REST (optionnel) |
| 9000 | WebSocket | WebSocket (optionnel) |

### Volumes Montés

```json
{
  "mounts": [
    "memory_fractal → /app/memory_fractal",
    "config → /app/config",
    "logs → /app/logs"
  ]
}
```

### Variables d'Environnement

```json
{
  "LUNA_ENV": "development",
  "LUNA_DEBUG": "true",
  "LUNA_VERSION": "2.1.0-secure",
  "MCP_ENABLE_ALL": "true",
  "MCP_SIMULTANEOUS": "true",
  "PROMETHEUS_EXPORTER_PORT": "9100",
  "PROMETHEUS_METRICS_ENABLED": "true",
  "LOG_LEVEL": "DEBUG"
}
```

---

## 🔧 Utilisation

### 1. VS Code Dev Container

**Prérequis:**
- VS Code avec extension "Dev Containers"
- Docker Desktop en cours d'exécution

**Étapes:**
1. Ouvrir le projet dans VS Code
2. `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
3. VS Code reconstruit l'environnement et ouvre le container
4. Terminal intégré → shell dans le container

### 2. GitHub Codespaces

**Étapes:**
1. Sur GitHub, cliquer "Code" → "Codespaces"
2. Créer un nouveau Codespace
3. GitHub lance automatiquement l'environnement
4. VS Code s'ouvre dans le navigateur

---

## 📦 Extensions VS Code Installées

### Python
- `ms-python.python` - Support Python
- `ms-python.vscode-pylance` - Intellisense avancé
- `ms-python.black-formatter` - Formatage Black
- `ms-python.isort` - Tri des imports

### Docker & DevOps
- `ms-azuretools.vscode-docker` - Support Docker
- `eamodio.gitlens` - Git avancé

### AI & Productivité
- `GitHub.copilot` - GitHub Copilot
- `GitHub.copilot-chat` - Copilot Chat

### Documentation
- `redhat.vscode-yaml` - Support YAML
- `yzhang.markdown-all-in-one` - Markdown
- `bierner.markdown-mermaid` - Diagrammes Mermaid

### Qualité Code
- `streetsidesoftware.code-spell-checker` - Vérification orthographe

---

## ⚙️ Configuration VS Code

### Python

```json
{
  "python.defaultInterpreterPath": "/usr/local/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit"
    }
  },
  "black-formatter.args": ["--line-length", "100"],
  "isort.args": ["--profile", "black"]
}
```

### Fichiers Exclus

```json
{
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true
  }
}
```

---

## 🧪 Commandes Post-Création

### postCreateCommand
```bash
pip install -r mcp-server/requirements.txt && echo '🌙 Luna Consciousness is ready!'
```

**Exécuté:** Une fois à la création du container
**Fonction:** Installer toutes les dépendances Python

### postStartCommand
```bash
echo '🌙 Luna Development Environment Started'
```

**Exécuté:** À chaque démarrage du container
**Fonction:** Message de confirmation

### updateContentCommand
```bash
pip install -r mcp-server/requirements.txt
```

**Exécuté:** Lors de la mise à jour du container
**Fonction:** Réinstaller les dépendances si requirements.txt change

---

## 💻 Ressources Système

### Configuration Minimale

```json
{
  "cpus": 2,
  "memory": "4gb",
  "storage": "32gb"
}
```

**Recommandé pour GitHub Codespaces:**
- Machine type: 4-core (8 GB RAM)

---

## 📝 Commandes Utiles

### Lancer le MCP Server

```bash
cd /app/mcp-server
python server.py
```

### Lancer Prometheus Exporter

```bash
cd /app/mcp-server
python prometheus_exporter.py
```

### Lancer les deux (comme en production)

```bash
cd /app/mcp-server
./start.sh
```

### Tests

```bash
# Tests unitaires
pytest tests/ -v

# Avec couverture
pytest tests/ -v --cov=mcp-server --cov-report=term

# Validation Phi
python -c "from luna_core.phi_calculator import PhiCalculator; print(PhiCalculator().calculate_phi({}))"
```

### Formatage Code

```bash
# Black (auto avec formatOnSave)
black mcp-server/ --line-length 100

# isort (auto avec formatOnSave)
isort mcp-server/ --profile black

# Lint
pylint mcp-server/
```

---

## 🔍 Dépannage

### Container ne démarre pas

**Vérifier docker-compose.yml:**
```bash
docker-compose config
```

**Vérifier les logs:**
```bash
docker-compose logs luna-docker
```

### Extensions ne s'installent pas

**Recharger VS Code:**
```
Ctrl+Shift+P → "Developer: Reload Window"
```

### Python interpreter introuvable

**Vérifier le chemin:**
```bash
which python
# Devrait retourner: /usr/local/bin/python
```

---

## 📚 Ressources

- **Dev Containers Doc:** https://code.visualstudio.com/docs/devcontainers/containers
- **GitHub Codespaces:** https://github.com/features/codespaces
- **devcontainer.json schema:** https://containers.dev/implementors/json_reference/

---

**φ = 1.618033988749895** 🌙

*Configuration Dev Container mise à jour le 1er décembre 2025*
