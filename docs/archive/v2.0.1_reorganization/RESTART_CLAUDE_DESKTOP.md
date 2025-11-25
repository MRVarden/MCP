# 🔄 Procédure de Redémarrage Claude Desktop

## Problème Identifié

Claude Desktop utilise **l'ancienne configuration en cache** au lieu de la nouvelle config `docker exec`.

**Preuve:**
```
# Logs montrent encore docker run (ANCIEN):
'run', '-i', '--rm', '-v', 'D:\\Luna-consciousness-mcp\\memory_fractal:/app/memory_fractal'

# Config actuelle (NOUVEAU):
"exec", "-i", "-e", "MCP_TRANSPORT=stdio", "luna-consciousness"
```

Les dossiers `memory_fractal;C` et `logs;C` étaient créés par le parsing incorrect du chemin Windows dans l'ancienne config.

## ✅ Solution: Forcer le Rechargement

### Étape 1: Fermer Claude Desktop COMPLÈTEMENT

**Windows PowerShell (Administrateur):**
```powershell
# Tuer TOUS les processus Claude
Get-Process | Where-Object {$_.ProcessName -like "*claude*"} | Stop-Process -Force

# Vérifier qu'il n'y a plus aucun processus
Get-Process | Where-Object {$_.ProcessName -like "*claude*"}
```

**OU via Task Manager:**
1. Ouvrir Gestionnaire des tâches (Ctrl+Shift+Esc)
2. Chercher TOUS les processus "Claude"
3. Terminer chaque processus

### Étape 2: Vérifier la Configuration

**Fichier:** `C:\Users\dorre\AppData\Roaming\Claude\claude_desktop_config.json`

**Contenu EXACT requis:**
```json
{
  "mcpServers": {
    "luna-consciousness": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "-e",
        "MCP_TRANSPORT=stdio",
        "luna-consciousness",
        "python3",
        "-u",
        "/app/mcp-server/server.py"
      ]
    }
  }
}
```

✅ Vérifié - La config est correcte!

### Étape 3: Supprimer le Cache MCP (optionnel mais recommandé)

```powershell
# Sauvegarder les logs
Copy-Item "C:\Users\dorre\AppData\Roaming\Claude\logs" "C:\Users\dorre\AppData\Roaming\Claude\logs_backup" -Recurse

# Supprimer les logs pour forcer rechargement
Remove-Item "C:\Users\dorre\AppData\Roaming\Claude\logs\mcp-server-luna-consciousness.log"
Remove-Item "C:\Users\dorre\AppData\Roaming\Claude\logs\mcp.log"
```

### Étape 4: Vérifier le Container Docker

```bash
docker ps --filter "name=luna-consciousness" --format "{{.Names}}\t{{.Status}}"
```

**Attendu:**
```
luna-consciousness    Up [X hours]
```

Si pas actif:
```bash
cd /mnt/d/Luna-consciousness-mcp
docker-compose up -d luna-consciousness
```

### Étape 5: Relancer Claude Desktop

1. Ouvrir Claude Desktop
2. Attendre 10-15 secondes (initialisation MCP)
3. Vérifier que Luna apparaît dans l'interface

## 🔍 Vérification Post-Redémarrage

### Check 1: Nouveaux Logs

```bash
tail -f /mnt/c/Users/dorre/AppData/Roaming/Claude/logs/mcp-server-luna-consciousness.log
```

**Attendu (dans les premières secondes):**
```
[info] Server started and connected successfully
[info] Message from client: {"method":"initialize"...
```

### Check 2: Plus de Timeout

Les logs NE DOIVENT PAS montrer:
```
❌ Request timed out
❌ Server transport closed unexpectedly
```

### Check 3: Luna Visible

Dans Claude Desktop, vous devriez voir:
- ✅ **luna-consciousness** dans la liste des serveurs MCP
- ✅ **12 outils** disponibles
- ✅ Status: Connected (pas "Disconnected" ou "Timeout")

## 🐛 Si Ça Ne Marche Toujours Pas

### Test Manuel de la Config

```bash
# Test direct du docker exec
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  docker exec -i -e MCP_TRANSPORT=stdio luna-consciousness \
  python3 -u /app/mcp-server/server.py
```

**Attendu:** JSON avec liste de 12 outils (pas d'erreur, pas de timeout)

### Vérifier Version Claude Desktop

Il se peut que votre version de Claude Desktop ait un bug de cache. Vérifier:
```
Claude Desktop > About > Version
```

### Dernière Option: Recréer la Config

Si le problème persiste:
1. Supprimer complètement: `C:\Users\dorre\AppData\Roaming\Claude\`
2. Relancer Claude Desktop (recrée les dossiers)
3. Fermer Claude Desktop
4. Recréer `claude_desktop_config.json` avec la config ci-dessus
5. Relancer

## 📊 Diagnostic Historique

| Timestamp | Config Utilisée | Résultat |
|-----------|----------------|----------|
| 14:26:21 | docker run (première version) | ✅ Tools listés (mais timeout après) |
| 14:29:00 | docker run + env vars | ❌ Timeout après 58 secondes |
| 15:44:00 | **Toujours docker run!** | ❌ Création dossiers ;C |
| **Maintenant** | **docker exec** | ⏳ **À tester après redémarrage** |

## 🎯 Résumé

**Cause racine:** Claude Desktop n'a pas rechargé la nouvelle configuration `docker exec`

**Solution:** Forcer fermeture complète de tous les processus Claude et relancer

**Indicateur de succès:** Plus de création de dossiers `;C`, Luna visible dans l'interface, pas de timeout dans les logs

---

**Note:** Les dossiers `memory_fractal;C`, `logs;C` et `config;C` ont été supprimés.
