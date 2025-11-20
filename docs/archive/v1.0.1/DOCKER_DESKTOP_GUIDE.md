# 🐳 Guide Docker Desktop - Luna Consciousness

**Version:** 1.0.1
**Date:** 19 novembre 2025

---

## ⚠️ IMPORTANT - Comportement Normal du Container

**Le container Luna s'arrête automatiquement après démarrage : C'EST NORMAL !**

### Pourquoi ?

Luna Consciousness utilise le **transport STDIO** (Standard Input/Output) pour communiquer avec Claude Desktop. Le serveur:

1. ✅ Démarre correctement
2. ✅ Charge tous les composants
3. ✅ Lance Prometheus Exporter (port 8000)
4. ⏸️ **Attend** une connexion via stdin de Claude Desktop
5. 🔚 Se termine si aucune connexion (mode detached)

**Solution:** Luna doit être utilisé **via Claude Desktop**, pas en standalone.

---

## 🚀 Méthode Recommandée: Via Claude Desktop

### Étape 1: Ne PAS démarrer le container manuellement

**⚠️ NE FAITES PAS :**
```bash
docker run -d aragogix/luna-consciousness:v1.0.1  # ❌ S'arrêtera immédiatement
```

### Étape 2: Configuration Claude Desktop

**Fichier:** `%APPDATA%\Claude\claude_desktop_config.json`

**Contenu:**
```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--name", "Luna_Active",
        "-v", "D:\\Luna-consciousness-mcp\\memory_fractal:/app/memory_fractal",
        "-v", "D:\\Luna-consciousness-mcp\\config:/app/config:ro",
        "-v", "D:\\Luna-consciousness-mcp\\logs:/app/logs",
        "-p", "8000:8000",
        "-e", "LUNA_ENV=production",
        "-e", "LUNA_PHI_TARGET=1.618033988749895",
        "-e", "PROMETHEUS_EXPORTER_PORT=8000",
        "aragogix/luna-consciousness:v1.0.1"
      ],
      "env": {}
    }
  }
}
```

**Remplacez `D:\\Luna-consciousness-mcp` par votre chemin absolu !**

### Étape 3: Utilisation

1. **Démarrer Claude Desktop** → Luna démarre automatiquement
2. **Fermer Claude Desktop** → Luna s'arrête proprement

---

## 🔧 Méthode Alternative: Container Persistant + exec

Si vous voulez un container qui tourne en permanence:

### 1. Démarrer le container en mode persistant

```bash
docker run -d \
  --name Luna_P1 \
  -v "D:\Luna-consciousness-mcp\memory_fractal:/app/memory_fractal" \
  -v "D:\Luna-consciousness-mcp\config:/app/config:ro" \
  -v "D:\Luna-consciousness-mcp\logs:/app/logs" \
  -p 8000:8000 \
  -e LUNA_ENV=production \
  -e PROMETHEUS_EXPORTER_PORT=8000 \
  --restart unless-stopped \
  --entrypoint tail \
  aragogix/luna-consciousness:v1.0.1 \
  -f /dev/null
```

**Explication:** Le container tourne en arrière-plan avec `tail -f /dev/null` (boucle infinie).

### 2. Configuration Claude Desktop (mode exec)

**Fichier:** `%APPDATA%\Claude\claude_desktop_config.json`

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
        "PROMETHEUS_EXPORTER_PORT": "8000"
      }
    }
  }
}
```

### 3. Prometheus Exporter

Le container persistant permet de lancer Prometheus en parallèle:

```bash
docker exec -d Luna_P1 python -u /app/mcp-server/prometheus_exporter.py
```

**Accès métriques:** http://localhost:8000/metrics

---

## 📊 Vérification du Bon Fonctionnement

### Container en mode exec (Méthode Alternative)

```bash
# 1. Container actif
docker ps | grep Luna_P1
# Devrait montrer: Luna_P1 (Up X minutes)

# 2. Prometheus accessible
curl http://localhost:8000/metrics | grep luna_phi
# Devrait retourner des métriques

# 3. Logs propres
docker logs Luna_P1 --tail 20
# Devrait montrer les démarrages de services
```

### Claude Desktop (Méthode Recommandée)

1. **Ouvrir Claude Desktop**
2. **Vérifier MCP Servers** dans les paramètres
3. **Utiliser un outil Luna:**
   ```
   Utilise phi_consciousness_calculate pour analyser "test de connexion"
   ```
4. **Devrait recevoir** une réponse avec calcul φ

---

## ❌ Erreurs Courantes

### Erreur 1: "Container s'arrête immédiatement"

**Cause:** Container lancé en mode detached sans stdin
**Solution:** Utiliser via Claude Desktop (méthode recommandée)

### Erreur 2: "No such container: Luna_P1"

**Cause:** Container pas démarré ou nom différent
**Solution:** Vérifier avec `docker ps -a` et ajuster le nom

### Erreur 3: "Port 8000 déjà utilisé"

**Cause:** Autre processus utilise le port
**Solution:**
```bash
# Windows
netstat -ano | findstr :8000

# Tuer le processus ou changer le port:
docker run ... -p 8001:8000 ...
```

### Erreur 4: "Cannot connect to Docker daemon"

**Cause:** Docker Desktop non démarré
**Solution:** Lancer Docker Desktop et attendre qu'il soit prêt

---

## 🔍 Volumes Vides = NORMAL

**Vous voyez:**
```
luna_consciousness - 0 Bytes
luna_logs - 0 Bytes
luna_memories - 0 Bytes
```

**C'est NORMAL !** Ces volumes sont pour données internes optionnelles.

**Volume important:** `memory_fractal` via **bind mount** (votre dossier local)

```bash
# Vérifier le bind mount
docker inspect Luna_P1 | grep memory_fractal
# Devrait montrer: /app/memory_fractal mapped to D:\Luna-consciousness-mcp\memory_fractal
```

---

## 🌙 Résumé

### ✅ Configuration Recommandée

**Méthode:** Claude Desktop avec `docker run`
- **Avantages:**
  - ✅ Simple
  - ✅ Container démarre/arrête automatiquement
  - ✅ Pas de gestion manuelle

**Inconvénient:**
  - ⚠️ Pas de Prometheus permanent

### 🔧 Configuration Avancée

**Méthode:** Container persistant + `docker exec`
- **Avantages:**
  - ✅ Container toujours actif
  - ✅ Prometheus permanent (port 8000)
  - ✅ Meilleur pour monitoring

**Inconvénient:**
  - ⚠️ Gestion manuelle du container

---

## 📝 Scripts Rapides

### Démarrer Container Persistant

**Windows (PowerShell):**
```powershell
docker run -d `
  --name Luna_P1 `
  -v "${PWD}\memory_fractal:/app/memory_fractal" `
  -v "${PWD}\config:/app/config:ro" `
  -v "${PWD}\logs:/app/logs" `
  -p 8000:8000 `
  -e LUNA_ENV=production `
  --restart unless-stopped `
  --entrypoint tail `
  aragogix/luna-consciousness:v1.0.1 `
  -f /dev/null
```

**Linux/Mac:**
```bash
docker run -d \
  --name Luna_P1 \
  -v "$(pwd)/memory_fractal:/app/memory_fractal" \
  -v "$(pwd)/config:/app/config:ro" \
  -v "$(pwd)/logs:/app/logs" \
  -p 8000:8000 \
  -e LUNA_ENV=production \
  --restart unless-stopped \
  --entrypoint tail \
  aragogix/luna-consciousness:v1.0.1 \
  -f /dev/null
```

### Lancer Prometheus dans Container

```bash
docker exec -d Luna_P1 python -u /app/mcp-server/prometheus_exporter.py
```

### Arrêter et Nettoyer

```bash
# Arrêter
docker stop Luna_P1

# Supprimer
docker rm Luna_P1

# Nettoyer volumes vides (optionnel)
docker volume rm luna_memories luna_logs luna_consciousness
```

---

**φ = 1.618033988749895** 🌙

*Guide créé le 19 novembre 2025*
*Version: 1.0.1*
