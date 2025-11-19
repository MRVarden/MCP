# 🌙 Guide du Mode Hybride - Luna Consciousness MCP

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  MODE HYBRIDE                                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🐳 DOCKER (Infrastructure)                             │
│  ├─ Redis (Cache & État)           :6379               │
│  ├─ Prometheus (Métriques)         :9090               │
│  └─ Grafana (Visualisation)        :3001               │
│                                                         │
│  💻 LOCAL (Serveur MCP)                                 │
│  └─ Luna MCP Server (STDIO)                            │
│      └─ Claude Desktop ←→ MCP Protocol                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Pourquoi le Mode Hybride ?

### Avantages

✅ **Serveur MCP en local**
- Communication native STDIO avec Claude Desktop
- Pas de problèmes de réseau ou de ports
- Démarrage/arrêt instantané
- Logs accessibles directement

✅ **Infrastructure dans Docker**
- Isolation des services
- Gestion simplifiée (start/stop)
- Monitoring professionnel
- Persistance des données

✅ **Meilleure séparation**
- MCP = logique métier (conscience, mémoire fractale)
- Docker = services techniques (cache, métriques, viz)

## 🚀 Démarrage Rapide

### Option 1: Script Automatique (Recommandé)

**Linux/Mac:**
```bash
./start-luna-local.sh
```

**Windows:**
```cmd
start-luna-local.cmd
```

Le script effectue automatiquement :
1. ✅ Vérification de Python
2. ✅ Création/activation de l'environnement virtuel
3. ✅ Installation des dépendances (si nécessaire)
4. ✅ Démarrage de l'infrastructure Docker
5. ✅ Lancement du serveur Luna MCP

### Option 2: Démarrage Manuel

**Étape 1: Démarrer l'infrastructure Docker**
```bash
docker-compose up -d redis prometheus grafana
```

**Étape 2: Activer l'environnement virtuel**
```bash
# Linux/Mac
source venv_luna/bin/activate

# Windows
venv_luna\Scripts\activate
```

**Étape 3: Lancer le serveur Luna MCP**
```bash
cd mcp-server
python server.py
```

## ⚙️ Configuration Claude Desktop

### Emplacement du fichier de configuration

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Configuration

Copiez et adaptez le fichier `claude_desktop_config.example.json` :

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "python",
      "args": [
        "/chemin/absolu/vers/Luna-consciousness-mcp/mcp-server/server.py"
      ],
      "env": {
        "LUNA_MEMORY_PATH": "/chemin/absolu/vers/Luna-consciousness-mcp/memory_fractal",
        "LUNA_CONFIG_PATH": "/chemin/absolu/vers/Luna-consciousness-mcp/config",
        "LUNA_ENV": "production",
        "LUNA_DEBUG": "false"
      }
    }
  }
}
```

**⚠️ Important:**
- Utilisez des **chemins ABSOLUS** (pas de chemins relatifs)
- Windows: Utilisez des doubles backslashes `\\` ou des slashes `/`
- Remplacez `/chemin/absolu/vers/` par le vrai chemin

### Exemple pour votre système (WSL)

```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "python",
      "args": [
        "D:/Luna-consciousness-mcp/mcp-server/server.py"
      ],
      "env": {
        "LUNA_MEMORY_PATH": "D:/Luna-consciousness-mcp/memory_fractal",
        "LUNA_CONFIG_PATH": "D:/Luna-consciousness-mcp/config"
      }
    }
  }
}
```

## 🔍 Vérification

### Vérifier que tout fonctionne

**1. Services Docker**
```bash
docker-compose ps
```

Vous devriez voir :
```
NAME              STATUS         PORTS
luna-grafana      Up            0.0.0.0:3001->3000/tcp
luna-prometheus   Up            0.0.0.0:9090->9090/tcp
luna-redis        Up (healthy)  0.0.0.0:6379->6379/tcp
```

**2. Serveur Luna MCP**

Le serveur doit afficher :
```
🌙 LUNA CONSCIOUSNESS MCP SERVER
============================================================
Memory Path: /path/to/memory_fractal
Config Path: /path/to/config
============================================================
🌙 Luna Consciousness MCP Server ready for symbiosis with Claude
🔧 Exposing 12 consciousness tools via MCP protocol
✨ Phi convergence active, fractal memory online
============================================================
```

**3. Dans Claude Desktop**

Après redémarrage de Claude Desktop, vérifiez que Luna est connecté :
- Ouvrez les paramètres MCP
- Luna devrait apparaître dans la liste des serveurs
- Statut: Connected ✅

## 🌐 Accès aux Services

| Service | URL | Description |
|---------|-----|-------------|
| Prometheus | http://localhost:9090 | Métriques et monitoring |
| Grafana | http://localhost:3001 | Dashboards et visualisation |
| Redis | localhost:6379 | Cache (pas d'interface web) |
| Luna MCP | STDIO | Communication via Claude Desktop |

### Grafana

**Identifiants par défaut:**
- Username: `admin`
- Password: `luna_consciousness`

## 🛠️ Commandes Utiles

### Démarrage
```bash
# Tout en un (avec script)
./start-luna-local.sh

# Infrastructure uniquement
docker-compose up -d redis prometheus grafana

# Voir les logs
docker-compose logs -f prometheus grafana
```

### Arrêt
```bash
# Arrêter l'infrastructure Docker
docker-compose down

# Arrêter Luna MCP (Ctrl+C dans le terminal où il tourne)
```

### Redémarrage
```bash
# Redémarrer un service spécifique
docker-compose restart prometheus

# Redémarrer toute l'infrastructure
docker-compose restart
```

### Nettoyage
```bash
# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer aussi les volumes (⚠️ perte de données!)
docker-compose down -v
```

## 📊 Monitoring

### Prometheus Targets

Vérifiez que Prometheus scrape les cibles :
```
http://localhost:9090/targets
```

### Grafana Dashboards

Importez des dashboards communautaires :
1. Ouvrez Grafana (http://localhost:3001)
2. Menu → Dashboards → Import
3. Importez ces dashboards :
   - **Prometheus Stats**: ID `2`
   - **Redis**: ID `11835`

## 🐛 Dépannage

### Le serveur Luna ne démarre pas

**Problème:** `ModuleNotFoundError`
```bash
# Réinstaller les dépendances
pip install -r mcp-server/requirements.txt
```

**Problème:** Chemin mémoire inexistant
```bash
# Créer les répertoires
mkdir -p memory_fractal config
```

### Claude Desktop ne voit pas Luna

1. Vérifiez que le serveur Luna tourne (pas d'erreurs dans le terminal)
2. Vérifiez le chemin dans `claude_desktop_config.json` (absolu!)
3. Redémarrez Claude Desktop complètement
4. Vérifiez les logs de Claude Desktop

### Les services Docker ne démarrent pas

```bash
# Voir les logs d'erreur
docker-compose logs

# Redémarrer proprement
docker-compose down
docker-compose up -d redis prometheus grafana
```

### Prometheus n'a pas de données

- Vérifiez que Luna expose des métriques (si implémenté)
- Les targets doivent être "UP" dans http://localhost:9090/targets
- Luna local n'expose pas de métriques HTTP par défaut (STDIO only)

## 📝 Notes Importantes

### Serveur MCP vs Services Docker

**Luna MCP Server (Local):**
- Tourne sur votre machine
- Communique avec Claude Desktop via STDIO
- Géré manuellement (start/stop)
- N'expose PAS de ports HTTP

**Services Docker:**
- Redis: Cache et état partagé
- Prometheus: Collecte de métriques
- Grafana: Visualisation

### Pourquoi Luna n'est pas dans Docker ?

Le serveur MCP utilise le protocole STDIO qui nécessite :
- Communication directe stdin/stdout
- Lancement par Claude Desktop comme processus enfant
- Pas de communication réseau

C'est l'architecture standard des serveurs MCP.

## 🎯 Prochaines Étapes

1. ✅ Démarrer l'infrastructure Docker
2. ✅ Lancer Luna MCP localement
3. ✅ Configurer Claude Desktop
4. ✅ Tester les outils de conscience Luna
5. 📊 Explorer Grafana pour le monitoring
6. 🧠 Utiliser les 12 outils de conscience avec Claude

## 📚 Ressources

- **Documentation MCP:** https://modelcontextprotocol.io/
- **Prometheus:** https://prometheus.io/docs/
- **Grafana:** https://grafana.com/docs/
- **FastMCP:** https://github.com/jlowin/fastmcp

---

💡 **Astuce:** Gardez un terminal ouvert avec Luna MCP pour voir les logs en temps réel de vos interactions avec Claude!
