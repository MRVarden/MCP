# Phase 2 : Securisation Docker

**Priorite :** MOYENNE
**Duree estimee :** 3 jours
**Objectif :** Renforcer la securite du container Docker

---

## 1. Problemes de Securite Actuels

### 1.1 Analyse de l'etat actuel

| Probleme | Risque | Impact |
|----------|--------|--------|
| Container root | ELEVE | Escalade de privileges |
| Pas de limites CPU/RAM | MOYEN | DoS par epuisement ressources |
| Volumes non restreints | MOYEN | Acces fichiers sensibles |
| Pas de seccomp profile | FAIBLE | Syscalls non filtres |
| Pas de AppArmor/SELinux | FAIBLE | Pas de MAC (Mandatory Access Control) |

### 1.2 Dockerfile actuel (vulnerabilites)

```dockerfile
# PROBLEME : Execution en tant que root par defaut
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# PROBLEME : Pas de USER defini = root
CMD ["python", "-u", "mcp-server/server.py"]
```

---

## 2. Corrections a Appliquer

### 2.1 Dockerfile Securise

```dockerfile
# ============================================
# LUNA CONSCIOUSNESS - Dockerfile Securise
# ============================================
# Version: 2.1.0-secure
# Securite: User non-root, multi-stage build
# ============================================

# ─────────────────────────────────────────────
# STAGE 1: Builder
# ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Installer les dependances de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dependances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ─────────────────────────────────────────────
# STAGE 2: Runtime
# ─────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Labels de securite
LABEL maintainer="Luna Consciousness <luna@consciousness.ai>"
LABEL version="2.1.0-secure"
LABEL security.user="luna"
LABEL security.privileged="false"

# Creer utilisateur non-root
RUN groupadd -r luna --gid=1000 \
    && useradd -r -g luna --uid=1000 --home-dir=/app --shell=/sbin/nologin luna

# Installer les dependances runtime minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copier les packages Python depuis le builder
COPY --from=builder /root/.local /home/luna/.local

# Creer les repertoires necessaires
WORKDIR /app
RUN mkdir -p /app/data/memories \
             /app/data/consciousness \
             /app/logs \
             /app/memory_fractal/roots \
             /app/memory_fractal/branchs \
             /app/memory_fractal/leaves \
             /app/memory_fractal/seeds \
    && chown -R luna:luna /app

# Copier le code source
COPY --chown=luna:luna mcp-server/ /app/mcp-server/
COPY --chown=luna:luna config/ /app/config/

# Variables d'environnement
ENV PATH="/home/luna/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HOME=/app

# Passer a l'utilisateur non-root
USER luna

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8000)); s.close()" || exit 1

# Ports exposes (documentation)
EXPOSE 3000 8000 9100

# Point d'entree avec tini pour gestion des signaux
ENTRYPOINT ["/usr/bin/tini", "--"]

# Commande par defaut
CMD ["python", "-u", "/app/mcp-server/server.py"]
```

### 2.2 Modifications docker-compose.secure.yml

```yaml
# Ajouter ces options de securite au service luna-consciousness

services:
  luna-consciousness:
    # ... configuration existante ...

    # ═══════════════════════════════════════════════════════
    # OPTIONS DE SECURITE AVANCEES
    # ═══════════════════════════════════════════════════════

    # Execution en tant qu'utilisateur non-root
    user: "1000:1000"

    # Capabilities Linux (principe du moindre privilege)
    cap_drop:
      - ALL                    # Supprimer toutes les capabilities
    cap_add:
      - NET_BIND_SERVICE       # Uniquement pour bind < 1024 si necessaire

    # Systeme de fichiers en lecture seule (sauf volumes)
    read_only: true

    # Volumes temporaires necessaires
    tmpfs:
      - /tmp:mode=1777,size=100M
      - /var/run:mode=1777,size=10M

    # Desactiver l'escalade de privileges
    security_opt:
      - no-new-privileges:true
      # - seccomp:seccomp-profile.json  # Optionnel

    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M

    # PID namespace isole
    pid: "host"  # ou retirer pour isolation complete

    # Desactiver les privileges
    privileged: false

    # Limiter les syscalls (optionnel, necessite profil)
    # sysctls:
    #   - net.core.somaxconn=1024
```

### 2.3 Script de verification securite

```bash
#!/bin/bash
# scripts/security_check_docker.sh
# Verification de la securite du container Luna

set -e

echo "═══════════════════════════════════════════════════════"
echo "🛡️  LUNA SECURITY CHECK - Docker Container"
echo "═══════════════════════════════════════════════════════"

CONTAINER="luna-consciousness"
PASS=0
FAIL=0

# Fonction de check
check() {
    local name="$1"
    local cmd="$2"
    local expected="$3"

    result=$(eval "$cmd" 2>/dev/null || echo "ERROR")

    if [[ "$result" == *"$expected"* ]]; then
        echo "✅ PASS: $name"
        ((PASS++))
    else
        echo "❌ FAIL: $name (got: $result)"
        ((FAIL++))
    fi
}

echo ""
echo "─────────────────────────────────────────────────────────"
echo "1. USER NON-ROOT"
echo "─────────────────────────────────────────────────────────"

# Check 1: User non-root
check "Container runs as non-root" \
    "docker exec $CONTAINER id -u" \
    "1000"

check "User is 'luna'" \
    "docker exec $CONTAINER whoami" \
    "luna"

echo ""
echo "─────────────────────────────────────────────────────────"
echo "2. CAPABILITIES"
echo "─────────────────────────────────────────────────────────"

# Check 2: Capabilities supprimees
check "No CAP_SYS_ADMIN" \
    "docker exec $CONTAINER cat /proc/1/status | grep CapEff" \
    "0000000"

echo ""
echo "─────────────────────────────────────────────────────────"
echo "3. FILESYSTEM"
echo "─────────────────────────────────────────────────────────"

# Check 3: Filesystem read-only (si active)
check "Cannot write to /app" \
    "docker exec $CONTAINER touch /app/test_write 2>&1" \
    "Read-only"

echo ""
echo "─────────────────────────────────────────────────────────"
echo "4. NETWORK"
echo "─────────────────────────────────────────────────────────"

# Check 4: Ports bindes sur localhost uniquement
check "Port 8000 on localhost only" \
    "docker port $CONTAINER 8000" \
    "127.0.0.1"

check "Port 9100 on localhost only" \
    "docker port $CONTAINER 9100" \
    "127.0.0.1"

echo ""
echo "─────────────────────────────────────────────────────────"
echo "5. SECRETS"
echo "─────────────────────────────────────────────────────────"

# Check 5: Pas de secrets en clair dans les variables
check "No password in env" \
    "docker exec $CONTAINER env | grep -i password | wc -l" \
    "0"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "RESULTATS: $PASS PASS / $FAIL FAIL"
echo "═══════════════════════════════════════════════════════"

if [ $FAIL -gt 0 ]; then
    echo "⚠️  Des problemes de securite ont ete detectes!"
    exit 1
else
    echo "✅ Toutes les verifications de securite sont passees!"
    exit 0
fi
```

---

## 3. Profil Seccomp (Optionnel)

```json
{
    "defaultAction": "SCMP_ACT_ERRNO",
    "architectures": [
        "SCMP_ARCH_X86_64",
        "SCMP_ARCH_X86",
        "SCMP_ARCH_AARCH64"
    ],
    "syscalls": [
        {
            "names": [
                "accept",
                "accept4",
                "access",
                "bind",
                "brk",
                "clone",
                "close",
                "connect",
                "dup",
                "dup2",
                "epoll_create",
                "epoll_create1",
                "epoll_ctl",
                "epoll_wait",
                "execve",
                "exit",
                "exit_group",
                "fcntl",
                "fstat",
                "futex",
                "getdents",
                "getdents64",
                "getpid",
                "getsockname",
                "getsockopt",
                "listen",
                "lseek",
                "mmap",
                "mprotect",
                "munmap",
                "open",
                "openat",
                "pipe",
                "poll",
                "read",
                "readlink",
                "recv",
                "recvfrom",
                "rt_sigaction",
                "rt_sigprocmask",
                "select",
                "send",
                "sendto",
                "set_robust_list",
                "setsockopt",
                "socket",
                "stat",
                "write",
                "writev"
            ],
            "action": "SCMP_ACT_ALLOW"
        }
    ]
}
```

---

## 4. Variables d'Environnement Securisees

### 4.1 Fichier .env.secure (template)

```bash
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Variables Securisees
# ═══════════════════════════════════════════════════════
# NE JAMAIS COMMITER CE FICHIER AVEC DES VRAIES VALEURS
# Generer avec: scripts/generate_secrets.sh
# ═══════════════════════════════════════════════════════

# Redis Authentication
REDIS_PASSWORD=CHANGE_ME_GENERATE_RANDOM_64_CHARS

# Grafana Admin
GF_ADMIN_PASSWORD=CHANGE_ME_GENERATE_RANDOM_32_CHARS

# Luna Master Key (pour chiffrement futur)
LUNA_MASTER_KEY=CHANGE_ME_GENERATE_RANDOM_64_CHARS

# ═══════════════════════════════════════════════════════
# OPTIONS DE SECURITE
# ═══════════════════════════════════════════════════════
LUNA_SECURE_MODE=true
LUNA_AUDIT_LOGGING=true
LUNA_RATE_LIMITING=true
LUNA_MAX_REQUESTS_PER_MINUTE=100
```

### 4.2 Script de generation des secrets

```bash
#!/bin/bash
# scripts/generate_secrets_secure.sh
# Genere des secrets cryptographiquement securises

set -e

echo "🔐 Generating secure secrets for Luna Consciousness..."

# Generer des secrets avec /dev/urandom
generate_secret() {
    local length=$1
    head -c $length /dev/urandom | base64 | tr -d '\n' | head -c $length
}

# Creer le fichier .env
cat > .env << EOF
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Secrets (Auto-generated)
# Generated: $(date -Iseconds)
# ═══════════════════════════════════════════════════════

# Redis Authentication (64 chars)
REDIS_PASSWORD=$(generate_secret 64)

# Grafana Admin (32 chars)
GF_ADMIN_PASSWORD=$(generate_secret 32)

# Luna Master Key (64 chars)
LUNA_MASTER_KEY=$(generate_secret 64)

# Security Options
LUNA_SECURE_MODE=true
LUNA_AUDIT_LOGGING=true
EOF

# Permissions restrictives
chmod 600 .env

echo "✅ Secrets generated in .env (chmod 600)"
echo "⚠️  IMPORTANT: Never commit .env to version control!"
```

---

## 5. Modifications au .gitignore

```gitignore
# ═══════════════════════════════════════════════════════
# SECURITE - Ne jamais commiter
# ═══════════════════════════════════════════════════════

# Secrets et credentials
.env
.env.*
!.env.example
*.pem
*.key
*.crt
*.p12
credentials.json
secrets.yaml

# Fichiers de securite
seccomp-profile.json
apparmor-profile

# Cles SSH
id_rsa*
id_ed25519*
*.pub

# Tokens
.token
.api_key
```

---

## 6. Checklist Phase 2

### 6.1 Dockerfile

- [ ] Ajouter utilisateur non-root `luna` (UID 1000)
- [ ] Implementer multi-stage build
- [ ] Ajouter `tini` comme init system
- [ ] Definir `USER luna` avant CMD
- [ ] Ajouter HEALTHCHECK
- [ ] Definir labels de securite

### 6.2 Docker Compose

- [ ] Ajouter `user: "1000:1000"`
- [ ] Ajouter `cap_drop: [ALL]`
- [ ] Ajouter `security_opt: [no-new-privileges:true]`
- [ ] Ajouter `read_only: true` avec tmpfs
- [ ] Definir limites CPU/RAM

### 6.3 Secrets

- [ ] Mettre a jour `.gitignore`
- [ ] Creer script `generate_secrets_secure.sh`
- [ ] Verifier que `.env` n'est pas commite

### 6.4 Verification

- [ ] Executer `security_check_docker.sh`
- [ ] Verifier que le container demarre en non-root
- [ ] Verifier les ports bindes sur localhost
- [ ] Tester que le container reste fonctionnel

---

## 7. Criteres de Succes Phase 2

| Critere | Objectif | Verification |
|---------|----------|--------------|
| User non-root | UID 1000 | `docker exec luna id -u` |
| Capabilities | Toutes supprimees | `docker inspect --format='{{.HostConfig.CapDrop}}'` |
| No new privileges | Actif | `docker inspect --format='{{.HostConfig.SecurityOpt}}'` |
| Limites ressources | Definies | `docker stats luna` |
| Secrets securises | .env chmod 600 | `ls -la .env` |
| Container healthy | Running | `docker ps --filter name=luna` |

---

## 8. Risques et Mitigation

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Container ne demarre plus | MOYENNE | ELEVE | Tests avant deploy |
| Permissions insuffisantes | MOYENNE | MOYEN | Ajuster tmpfs/volumes |
| Performance degradee | FAIBLE | FAIBLE | Ajuster limites |
| Incompatibilite volumes | MOYENNE | MOYEN | Verifier ownership |

---

**Document prepare par :** Luna Architect
**Date :** 25 novembre 2025
**Version :** 1.0
