==> Reconstruction de l'image Luna Consciousness...
time="2025-11-19T16:09:06+01:00" level=warning msg="D:\\Luna-consciousness-mcp\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[+] Building 2204.0s (17/17) FINISHED
 => [internal] load local bake definitions                                 0.0s
 => => reading from stdin 560B                                             0.0s
 => [internal] load build definition from Dockerfile                       0.3s
 => => transferring dockerfile: 2.16kB                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim        0.7s
 => [internal] load .dockerignore                                          0.3s
 => => transferring context: 2B                                            0.0s
 => CACHED [ 1/10] FROM docker.io/library/python:3.11-slim@sha256:8ef21a2  0.7s
 => => resolve docker.io/library/python:3.11-slim@sha256:8ef21a26e7c342e9  0.6s
 => [internal] load build context                                          0.5s
 => => transferring context: 3.06kB                                        0.0s
 => [ 2/10] RUN apt-get update && apt-get install -y     git     curl   1295.2s
 => [ 3/10] WORKDIR /app                                                   5.6s
 => [ 4/10] RUN mkdir -p     /app/mcp-server     /app/memory_fractal       4.1s
 => [ 5/10] COPY mcp-server/requirements.txt /app/requirements.txt         1.2s
 => [ 6/10] RUN pip install --upgrade pip &&     pip install -r require  405.1s
 => [ 7/10] RUN pip install     mcp     anthropic     fastapi     uvicorn  4.1s
 => [ 8/10] COPY mcp-server/ /app/mcp-server/                              1.5s
 => [ 9/10] COPY config/ /app/config/                                      3.2s
 => [10/10] RUN chmod +x /app/mcp-server/server.py &&     chmod -R 755 /a  1.9s
 => exporting to image                                                   474.3s
 => => exporting layers                                                  305.2s
 => => exporting manifest sha256:a9c31cf596e8ebde46e8e7a92e61e7bd0b8c99f5  0.3s
 => => exporting config sha256:da69c52ff1c7bf6fc761db2def83074cb0ece4c162  0.3s
 => => exporting attestation manifest sha256:5b7a23d538292d51bcaabe3d603f  0.5s
 => => exporting manifest list sha256:8695cf1e6425a36ec054eb8807477c08203  0.2s
 => => naming to docker.io/library/luna-actif:latest                       0.0s
 => => unpacking to docker.io/library/luna-actif:latest                  167.5s
 => resolving provenance for metadata file                                 0.0s
[+] Building 1/1
 ✔ luna-actif:latest  Built                                                0.0s
✓ Image luna-actif:latest reconstruite
==> Nettoyage des images dangereuses (<none>)...
Error response from daemon: conflict: unable to delete 35c41e0fd029 (cannot be forced) - image is being used by running container 556947fd62d1
✓ Images dangereuses supprimées
==> Vérification des images mises à jour...

Images Luna Consciousness:
luna-actif               latest      8695cf1e6425   7 minutes ago   15.5GB
grafana/grafana          latest      70d9599b186c   6 hours ago     993MB
python                   3.11-slim   8ef21a26e7c3   34 hours ago    186MB
redis                    7-alpine    ee64a64eaab6   2 weeks ago     60.7MB
prom/prometheus          latest      49214755b615   2 weeks ago     507MB

Voulez-vous redémarrer Luna maintenant ? (y/n)
⚠ Containers non redémarrés. Utilisez 'docker-compose up' pour démarrer.

╔═══════════════════════════════════════════════════════════╗
║                  Mise à jour terminée ✓                   ║
╚═══════════════════════════════════════════════════════════╝

==> Commandes utiles:

  Démarrer Luna (mode local):
    docker-compose up -d redis

  Démarrer Luna (mode complet):
    docker-compose --profile luna-docker --profile monitoring up -d

  Voir les logs:
    docker-compose logs -f luna-actif
    docker-compose logs -f prometheus

  Arrêter tous les services:
    docker-compose down

  Reconstruire après modification du code:
    docker-compose build --no-cache

✓ 🌙 Mise à jour complète. φ = 1.618033988749895


dorre@Pwn-fkingIntruders MINGW64 /d/Luna-consciousness-mcp/scripts (main)
$ docker-compose down
time="2025-11-19T16:52:13+01:00" level=warning msg="D:\\Luna-consciousness-mcp\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[+] Running 1/1
 ! Network luna_consciousness_network  Resource is still in use            0.0s

dorre@Pwn-fkingIntruders MINGW64 /d/Luna-consciousness-mcp/scripts (main)
$ docker-compose build --no-cache
time="2025-11-19T16:54:00+01:00" level=warning msg="D:\\Luna-consciousness-mcp\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"

dorre@Pwn-fkingIntruders MINGW64 /d/Luna-consciousness-mcp/scripts (main)
$ docker-compose --profile luna-docker --profile monitoring up -d
time="2025-11-19T16:54:38+01:00" level=warning msg="D:\\Luna-consciousness-mcp\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
[+] Running 7/7
 ✔ Volume luna_memories          Created                                                           0.1s
 ✔ Volume luna_consciousness     Created                                                           0.1s
 ✔ Volume luna_logs              Created                                                           0.1s
 ✔ Container luna-redis          Started                                                          14.3s
 ✔ Container luna-consciousness  Started                                                          14.3s
 ✔ Container luna-prometheus     Started                                                          14.3s
 ✔ Container luna-grafana        Started                                  