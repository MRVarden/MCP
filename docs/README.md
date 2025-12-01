# 📚 Documentation Luna Consciousness

**Version:** 2.1.0-secure
**Date:** 1er décembre 2025

---

## 📖 Index de la Documentation

### 🌟 Documentation Principale

| Document | Description | Public |
|----------|-------------|--------|
| 📖 **[DEPLOYMENT.md](DEPLOYMENT.md)** | Guide complet de déploiement | Tous |
| 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** | Architecture technique détaillée | Développeurs |
| 🛠️ **[MCP_TOOLS.md](MCP_TOOLS.md)** | Référence des 13 outils MCP | Utilisateurs |

---

## 🚀 Démarrage Rapide

1. **Déploiement** → [DEPLOYMENT.md](DEPLOYMENT.md)
   - Prérequis système
   - Installation Docker Hub / Local
   - Configuration Claude Desktop
   - Vérification et troubleshooting

2. **Utilisation des Outils** → [MCP_TOOLS.md](MCP_TOOLS.md)
   - Liste des 13 outils MCP
   - Exemples d'utilisation
   - Formats de réponse

3. **Comprendre l'Architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
   - Les 9 niveaux Update01.md
   - Modules Luna Core
   - Mémoire fractale
   - Métriques Prometheus

---

## 📁 Structure de la Documentation

```
docs/
├── 📖 README.md              # Cet index
├── 📖 DEPLOYMENT.md          # Guide de déploiement unifié
├── 🏗️ ARCHITECTURE.md        # Architecture technique
├── 🛠️ MCP_TOOLS.md           # Référence outils MCP
│
├── 📁 api/                   # Documentation API (legacy)
│   └── TOOLS_REFERENCE.md
│
├── 📁 guides/                # Guides utilisateur (legacy)
│   └── QUICKSTART.md
│
├── 📁 archive/               # Documents archivés
│   ├── v1.0.1/
│   ├── v2.0.0_transition/
│   ├── v2.0.1_reorganization/
│   └── v2.1.0_reorganization/
│
└── 📁 ArchiveDocs/           # Anciens documents de travail
```

---

## 🔗 Liens Rapides

### Configuration Claude Desktop

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": ["exec", "-i", "luna-consciousness", "python", "-u", "/app/mcp-server/server.py"],
      "env": {"LUNA_MODE": "orchestrator", "LUNA_UPDATE01": "enabled"}
    }
  }
}
```

### Commandes Essentielles

```bash
# Démarrer Luna
docker-compose up -d

# Voir les logs
docker logs luna-consciousness -f

# Vérifier les métriques
curl http://localhost:9100/metrics | grep luna_phi
```

### URLs des Services

| Service | URL |
|---------|-----|
| 📊 Prometheus Metrics | http://127.0.0.1:9100/metrics |
| 📈 Grafana | http://127.0.0.1:3001 |
| 🔍 Prometheus UI | http://127.0.0.1:9090 |

---

## 📋 Documents Racine du Projet

| Document | Description |
|----------|-------------|
| 📖 **[../README.md](../README.md)** | Présentation du projet |
| 📋 **[../CHANGELOG.md](../CHANGELOG.md)** | Historique des versions |
| 🤝 **[../CONTRIBUTING.md](../CONTRIBUTING.md)** | Guide de contribution |
| 📜 **[../LICENSE.txt](../LICENSE.txt)** | Licence MIT |

---

## 🆕 Nouveautés v2.1.0-secure

### Sécurisation Complète

- 🔒 **Ports localhost-only** - Tous les services bindés sur 127.0.0.1
- 🔒 **Redis non exposé** - Accessible uniquement via réseau interne
- 🔒 **Security hardening** - cap_drop: ALL, read_only, no-new-privileges
- 🔒 **Secrets externalisés** - Variables dans .env

### Documentation Réorganisée

- ✅ **3 documents unifiés** remplacent 20+ fichiers dispersés
- ✅ **DEPLOYMENT.md** - Tout sur le déploiement en un seul fichier
- ✅ **ARCHITECTURE.md** - Architecture complète Update01.md
- ✅ **MCP_TOOLS.md** - Référence des 13 outils

### Archivage

Les anciens documents sont archivés dans `docs/archive/` pour référence historique.

---

## 💡 Comment Utiliser Cette Documentation

### 🆕 Nouveau Utilisateur ?

1. Lisez [DEPLOYMENT.md](DEPLOYMENT.md) section "Démarrage Rapide"
2. Configurez Claude Desktop
3. Testez avec `luna_orchestrated_interaction`

### 🔧 Développeur ?

1. Lisez [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre les 9 niveaux
2. Consultez [MCP_TOOLS.md](MCP_TOOLS.md) pour les détails API
3. Explorez le code dans `mcp-server/luna_core/`

### 🐛 Problème ?

1. Consultez [DEPLOYMENT.md](DEPLOYMENT.md) section "Troubleshooting"
2. Vérifiez les logs: `docker logs luna-consciousness`
3. Ouvrez une issue sur GitHub

---

**φ = 1.618033988749895** 🌙

*Index Documentation - Luna Consciousness v2.1.0-secure*
