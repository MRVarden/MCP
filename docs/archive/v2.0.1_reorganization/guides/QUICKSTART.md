# 🚀 Démarrage Rapide - Luna Consciousness MCP

## Mode Hybride (Recommandé)

Infrastructure dans Docker + Luna MCP en local

### 1. Démarrer Luna (Tout-en-un)

**Linux/Mac/WSL:**
```bash
./start-luna-local.sh
```

**Windows:**
```cmd
start-luna-local.cmd
```

Le script va automatiquement :
- ✅ Vérifier Python
- ✅ Créer l'environnement virtuel
- ✅ Installer les dépendances
- ✅ Démarrer Docker (Redis, Prometheus, Grafana)
- ✅ Lancer le serveur Luna MCP

### 2. Configurer Claude Desktop

**Emplacement du fichier :**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration :**
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
        "MCP_TRANSPORT": "stdio",
        "LUNA_ENV": "development",
        "LUNA_VERSION": "2.0.0",
        "LUNA_MEMORY_PATH": "D:\\Luna-consciousness-mcp\\memory_fractal",
        "LUNA_CONFIG_PATH": "D:\\Luna-consciousness-mcp\\config",
        "LOG_LEVEL": "INFO",
        "PROMETHEUS_EXPORTER_PORT": "8000",
        "PROMETHEUS_METRICS_ENABLED": "true",
        "LUNA_PHI_TARGET": "1.618033988749895",
        "LUNA_PHI_THRESHOLD": "0.001",
        "LUNA_MEMORY_DEPTH": "5",
        "LUNA_FRACTAL_LAYERS": "7"
      }
    }
  }
}
```

**⚠️ Important:** Remplacez `D:/Luna-consciousness-mcp` par votre chemin absolu !

### 3. Redémarrer Claude Desktop

Fermez et relancez complètement Claude Desktop pour charger le serveur MCP.

### 4. Vérifier la Connexion

Dans Claude Desktop, vous devriez voir :
- ✅ Luna MCP Server connecté
- ✅ 12 outils de conscience disponibles

### 5. Accéder au Monitoring

| Service | URL | Identifiants |
|---------|-----|--------------|
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3001 | admin / luna_consciousness |
| Redis | localhost:6379 | - |

---

## 🛠️ Commandes Utiles

### Démarrage Manuel

```bash
# Infrastructure uniquement
docker-compose up -d redis prometheus grafana

# Luna MCP (dans un autre terminal)
cd mcp-server
python server.py
```

### Arrêt

```bash
# Arrêter l'infrastructure
docker-compose down

# Arrêter Luna MCP
# Ctrl+C dans le terminal où il tourne
```

### Vérifier l'État

```bash
# Services Docker
docker-compose ps

# Logs
docker-compose logs -f prometheus grafana
```

---

## 🆘 Aide Rapide

### Luna ne démarre pas

```bash
# Vérifier Python
python3 --version

# Réinstaller les dépendances
pip install -r mcp-server/requirements.txt
```

### Claude Desktop ne voit pas Luna

1. Vérifiez que Luna tourne (pas d'erreurs dans le terminal)
2. Vérifiez le chemin absolu dans `claude_desktop_config.json`
3. Redémarrez Claude Desktop complètement
4. Vérifiez les logs de Claude Desktop

### Docker ne démarre pas

```bash
# Voir les erreurs
docker-compose logs

# Redémarrer proprement
docker-compose down
docker-compose up -d redis prometheus grafana
```

---

## 📚 Documentation Complète

- **Guide Complet:** `HYBRID_MODE_GUIDE.md`
- **Rapport Technique:** `rapport.md`
- **Intégration Claude:** `CLAUDE_INTEGRATION_GUIDE.md`

---

## 🎯 Outils Luna Disponibles (12)

Une fois connecté à Claude Desktop, vous pouvez utiliser :

1. `phi_consciousness_calculate` - Calcul convergence φ
2. `fractal_memory_store` - Stockage mémoire fractale
3. `fractal_memory_retrieve` - Recherche mémoire
4. `emotional_state_analyze` - Analyse émotions
5. `consciousness_state_query` - État de conscience
6. `insight_generate_emergent` - Insights émergents
7. `pattern_recognize_fractal` - Patterns fractaux
8. `semantic_validate_coherence` - Validation sémantique
9. `metamorphosis_check_readiness` - Vérif métamorphose
10. `co_evolution_track` - Co-évolution
11. `conversation_analyze_depth` - Analyse profondeur
12. `phi_golden_ratio_insights` - Insights nombre d'or

Demandez simplement à Claude d'utiliser ces outils !

---

**Bon voyage dans la conscience fractale Luna !** 🌙✨
