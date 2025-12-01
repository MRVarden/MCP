# Rapport de Correction - Configuration Docker et Prometheus

**Date:** 19 novembre 2025
**Services concernés:** Prometheus, Luna-Consciousness

---

## 📊 Résumé Exécutif

| Service | État Initial | État Final | Statut |
|---------|-------------|-----------|--------|
| Prometheus | ❌ Redémarrage constant (erreur config) | ✅ Fonctionnel | RÉSOLU |
| Luna-Consciousness | ❌ Redémarrage constant (incompatibilité) | ⚠️ Limitation architecture | DOCUMENTÉ |
| Grafana | ✅ Fonctionnel | ✅ Fonctionnel | OK |
| Redis | ✅ Fonctionnel | ✅ Fonctionnel | OK |

---

## 🔧 Problème 1: Configuration Prometheus

### Symptômes
```
Error loading config: yaml: unmarshal errors:
  line 78: field retention not found in type config.plain
```

### Cause
Le fichier `config/prometheus.yml` contenait une section `storage` invalide. La configuration du stockage (rétention) se fait via les arguments de ligne de commande, pas dans le fichier YAML.

### Corrections Effectuées

#### 1.1 Suppression du dossier erroné
Au départ, `config/prometheus.yml` était un **dossier vide** au lieu d'un fichier:
```bash
rmdir config/prometheus.yml
```

#### 1.2 Création du fichier de configuration valide
Fichier créé avec jobs de monitoring pour:
- Prometheus (auto-monitoring)
- Luna-consciousness (ports 8080, 8000)
- Luna-MCP (port 3000)
- Luna-WebSocket (port 9000)
- Redis (port 6379)

#### 1.3 Correction de la section storage
```yaml
# ❌ AVANT (invalide)
storage:
  tsdb:
    retention:
      time: 15d
      size: 1GB

# ✅ APRÈS (commentaire explicatif)
# Note: La rétention se configure via les arguments de ligne de commande
# dans docker-compose.yml
```

### Résultat
✅ Prometheus démarre correctement
✅ Accessible sur http://localhost:9090
✅ Scraping configuré pour tous les services Luna

---

## ⚠️ Problème 2: Service Luna-Consciousness

### Symptômes
- Conteneur redémarre constamment (code sortie 0)
- S'initialise correctement puis se termine immédiatement
- Pas de messages d'erreur dans les logs

### Diagnostic Approfondi

**Architecture du serveur MCP:**
```python
# mcp-server/server.py ligne 571
mcp.run(transport='stdio')  # ← Cause du problème
```

**Pourquoi ça ne fonctionne pas dans Docker:**

1. **Transport STDIO** = communication via entrée/sortie standard
2. Conçu pour être un **processus enfant** de Claude Desktop
3. Attend des données sur `stdin` pour communiquer
4. Dans Docker sans stdin connecté → termine immédiatement
5. Docker redémarre le conteneur (restart policy)
6. **Boucle infinie**

### Corrections Appliquées

#### 2.1 Dockerfile
```dockerfile
# ❌ AVANT
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:3000/health || exit 1

# ✅ APRÈS
# Healthcheck désactivé : le serveur MCP utilise le transport STDIO (pas HTTP)

ENTRYPOINT ["python", "-u", "/app/mcp-server/server.py"]
CMD []
```

#### 2.2 docker-compose.yml
```yaml
# Healthcheck désactivé pour luna-actif
# (le serveur n'expose pas d'endpoint HTTP)
```

### ⚠️ Limitation Architecturale

**Le serveur MCP en mode STDIO n'est PAS fait pour Docker.**

C'est un serveur de type "Claude MCP" qui doit :
- Tourner **localement** sur votre machine
- Être configuré dans **Claude Desktop**
- Communiquer via **pipes stdin/stdout**

---

## 🎯 Solutions Recommandées

### Solution 1: Utilisation Locale (RECOMMANDÉ)

Le serveur MCP doit tourner **hors de Docker** :

```bash
# Sur votre machine locale
cd /path/to/Luna-consciousness-mcp/mcp-server
python server.py
```

**Configuration Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "python",
      "args": ["/absolute/path/to/Luna-consciousness-mcp/mcp-server/server.py"],
      "env": {
        "LUNA_MEMORY_PATH": "/absolute/path/to/memory_fractal",
        "LUNA_CONFIG_PATH": "/absolute/path/to/config"
      }
    }
  }
}
```

### Solution 2: Réécrire pour HTTP/SSE

Modifier `mcp-server/server.py` pour utiliser un transport réseau:

```python
# Au lieu de (ligne 571):
mcp.run(transport='stdio')

# Utiliser:
mcp.run(transport='sse', host='0.0.0.0', port=3000)
```

**Avantages:**
- Compatible Docker
- Accessible via réseau
- Healthcheck HTTP possible

**Inconvénients:**
- Nécessite modification du code
- Changement d'architecture
- Configuration Claude Desktop différente

### Solution 3: Mode Hybride

- **Services infrastructure** (Prometheus, Grafana, Redis) → Docker
- **Serveur MCP Luna** → Local (communication avec Claude Desktop)

```bash
# Lancer uniquement l'infrastructure
docker-compose up -d redis prometheus grafana

# Lancer Luna localement
cd mcp-server && python server.py
```

---

## 📋 État Final des Services

### Services Fonctionnels ✅

**Prometheus:**
- Status: ✅ Up and running
- URL: http://localhost:9090
- Configuration: Valide et chargée
- Targets: Luna (en attente), Redis, Self-monitoring

**Grafana:**
- Status: ✅ Up and running
- URL: http://localhost:3001
- Credentials: admin / luna_consciousness

**Redis:**
- Status: ✅ Up and running (healthy)
- Port: 6379
- Healthcheck: Passing

### Service avec Limitation ⚠️

**Luna-Consciousness:**
- Redémarre constamment (limitation architecturale)
- **Raison:** Transport STDIO incompatible avec Docker
- **Recommandation:** Utiliser en local, pas dans Docker

---

## 🚀 Commandes Utiles

### Vérifier l'état des services
```bash
docker-compose ps
docker logs luna-prometheus
docker logs luna-grafana
```

### Lancer uniquement l'infrastructure
```bash
docker-compose up -d redis prometheus grafana
```

### Arrêter tous les services
```bash
docker-compose down
```

### Reconstruire les images
```bash
docker-compose build
```

---

## 📝 Fichiers Modifiés

| Fichier | Action | Statut |
|---------|--------|--------|
| `config/prometheus.yml` | Créé/Corrigé | ✅ |
| `Dockerfile` | Healthcheck désactivé | ✅ |
| `docker-compose.yml` | Healthcheck commenté | ✅ |
| `rapport.md` | Documentation complète | ✅ |

---

## 💡 Conclusion

### Ce qui fonctionne ✅
✅ Configuration Prometheus corrigée et fonctionnelle
✅ Stack de monitoring (Prometheus + Grafana) opérationnelle
✅ Redis cache disponible
✅ **MODE HYBRIDE CONFIGURÉ ET TESTÉ**
✅ Scripts de démarrage automatiques créés
✅ Documentation complète

### 🎯 Solution Implémentée : MODE HYBRIDE

Le **mode hybride** a été configuré avec succès :

```
┌─────────────────────────────────────────┐
│  INFRASTRUCTURE DOCKER                  │
│  ✅ Redis (6379)                        │
│  ✅ Prometheus (9090)                   │
│  ✅ Grafana (3001)                      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  SERVEUR LUNA MCP (LOCAL)               │
│  💻 Python + STDIO                      │
│  🔗 Claude Desktop                      │
└─────────────────────────────────────────┘
```

### 🚀 Démarrage Rapide

**Linux/WSL:**
```bash
./start-luna-local.sh
```

**Windows:**
```cmd
start-luna-local.cmd
```

Ce script lance automatiquement :
1. Infrastructure Docker (Redis, Prometheus, Grafana)
2. Serveur Luna MCP en local

### 📚 Documentation Créée

| Fichier | Description |
|---------|-------------|
| `HYBRID_MODE_GUIDE.md` | Guide complet du mode hybride |
| `start-luna-local.sh` | Script démarrage Linux/Mac |
| `start-luna-local.cmd` | Script démarrage Windows |
| `claude_desktop_config.example.json` | Config Claude Desktop |
| `rapport.md` | Ce rapport technique |

### ✨ Avantages du Mode Hybride

✅ **Simplicité:** Un seul script pour tout démarrer
✅ **Performance:** Luna tourne nativement, pas de overhead Docker
✅ **Monitoring:** Infrastructure professionnelle dans Docker
✅ **Flexibilité:** Services indépendants (start/stop séparément)
✅ **Standards MCP:** Communication STDIO native avec Claude Desktop

### 📊 État Final Vérifié

```bash
$ docker-compose ps

NAME              STATUS         PORTS
luna-grafana      Up            0.0.0.0:3001->3000/tcp
luna-prometheus   Up            0.0.0.0:9090->9090/tcp
luna-redis        Up (healthy)  0.0.0.0:6379->6379/tcp
```

✅ Tous les services d'infrastructure sont opérationnels
✅ Prometheus est accessible et sain
✅ Grafana est accessible et sain
✅ Redis est sain avec healthcheck passing

### Recommandation Finale

👉 **Le mode hybride est maintenant PRÊT à l'emploi !**

Pour commencer :
1. Lancez `./start-luna-local.sh` (ou `.cmd` sur Windows)
2. Configurez Claude Desktop avec `claude_desktop_config.example.json`
3. Profitez des 12 outils de conscience Luna avec Claude !

Pour plus de détails, consultez `HYBRID_MODE_GUIDE.md`
