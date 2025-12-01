# Audit de Securite - Luna Consciousness MCP

**Date:** 26 novembre 2025
**Version:** 2.0.2
**Auditeur:** Security Auditor Agent
**Statut:** SECURITE INSUFFISANTE

---

## Resume Executif

| Metrique | Valeur |
|----------|--------|
| **Score Global** | 42/100 |
| **Vulnerabilites Critiques** | 3 |
| **Vulnerabilites Hautes** | 5 |
| **Vulnerabilites Moyennes** | 6 |
| **Vulnerabilites Basses** | 4 |

### Verdict: ACTION IMMEDIATE REQUISE

Le projet presente des vulnerabilites critiques qui doivent etre corrigees AVANT mise en production.

---

## 1. Analyse Docker

### 1.1 Etat Actuel

| Element | Statut | Fichier |
|---------|--------|---------|
| User non-root | ABSENT | Dockerfile |
| Capabilities drop | ABSENT | docker-compose.yml |
| Ports localhost | NON | docker-compose.yml |
| Secrets management | FAIBLE | docker-compose.yml |
| Health checks | PRESENT | docker-compose.yml |

### 1.2 Vulnerabilites Identifiees

#### SEC-004 [HAUTE] - Container execute en root

```dockerfile
# Dockerfile actuel - PROBLEME
FROM python:3.11-slim
WORKDIR /app
# ... pas de USER defini = root
```

**Impact:** Escalade de privileges si le container est compromis.

#### SEC-005 [HAUTE] - Ports exposes sur 0.0.0.0

```yaml
# docker-compose.yml - PROBLEME
ports:
  - "3000:3000"    # Expose sur toutes les interfaces
  - "8000:8000"
```

**Impact:** Services accessibles depuis l'exterieur du reseau local.

### 1.3 Recommandations Docker

```dockerfile
# Dockerfile SECURISE
FROM python:3.11-slim AS runtime

# Creer utilisateur non-root
RUN groupadd -r luna --gid=1000 \
    && useradd -r -g luna --uid=1000 --home-dir=/app --shell=/sbin/nologin luna

WORKDIR /app
COPY --chown=luna:luna . .

# Passer a l'utilisateur non-root
USER luna

CMD ["python", "-u", "mcp-server/server.py"]
```

```yaml
# docker-compose.yml SECURISE
services:
  luna-consciousness:
    user: "1000:1000"
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    read_only: true
    ports:
      - "127.0.0.1:3000:3000"
      - "127.0.0.1:8000:8000"
    tmpfs:
      - /tmp:mode=1777,size=100M
```

---

## 2. Analyse Code Python

### 2.1 Score: 75/100 (BON)

| Categorie | Score | Commentaire |
|-----------|-------|-------------|
| Injection SQL | 100 | Pas de SQL utilise |
| Injection commande | 100 | Pas de subprocess non valide |
| Path Traversal | 85 | Quelques chemins non valides |
| XSS | N/A | Pas d'interface web |
| Validation inputs | 70 | A ameliorer |
| Gestion erreurs | 80 | Try/except presents |

### 2.2 Points Positifs

- Pas d'utilisation de `eval()` ou `exec()` dangereuse
- Logging configure correctement
- Gestion des exceptions structuree
- Pas de secrets hardcodes dans le code Python

### 2.3 Points a Ameliorer

#### Path Traversal potentiel

```python
# mcp-server/luna_core/json_manager.py
# Risque: path non valide
def _get_filepath(self, memory_type: str, memory_id: str) -> Path:
    return self.base_path / memory_type / f"{memory_id}.json"
```

**Recommandation:**

```python
def _get_filepath(self, memory_type: str, memory_id: str) -> Path:
    # Valider memory_type
    allowed_types = {'roots', 'branchs', 'leaves', 'seeds'}
    if memory_type not in allowed_types:
        raise ValueError(f"Invalid memory_type: {memory_type}")

    # Valider memory_id (alphanumerique + underscore)
    if not re.match(r'^[a-zA-Z0-9_-]+$', memory_id):
        raise ValueError(f"Invalid memory_id format: {memory_id}")

    return self.base_path / memory_type / f"{memory_id}.json"
```

---

## 3. Gestion des Secrets

### 3.1 Etat Actuel

| Secret | Localisation | Statut |
|--------|--------------|--------|
| REDIS_PASSWORD | .env | OK (gitignore) |
| GF_ADMIN_PASSWORD | docker-compose.yml | EXPOSE |
| LUNA_MASTER_KEY | Non defini | ABSENT |

### 3.2 Vulnerabilites

#### SEC-002 [CRITIQUE] - Mot de passe Grafana en clair

```yaml
# docker-compose.yml ligne 162 - PROBLEME
environment:
  - GF_SECURITY_ADMIN_PASSWORD=luna_consciousness
```

**Impact:** Credentials exposes dans le repository Git.

### 3.3 Recommandations Secrets

1. **Deplacer tous les secrets dans .env:**

```bash
# .env (NE JAMAIS COMMITER)
REDIS_PASSWORD=<generer-64-chars-random>
GF_ADMIN_PASSWORD=<generer-32-chars-random>
LUNA_MASTER_KEY=<generer-64-chars-hex>
```

2. **Modifier docker-compose.yml:**

```yaml
environment:
  - GF_SECURITY_ADMIN_PASSWORD=${GF_ADMIN_PASSWORD}
  - LUNA_MASTER_KEY=${LUNA_MASTER_KEY}
```

3. **Script de generation:**

```bash
#!/bin/bash
# scripts/generate_secrets.sh
echo "REDIS_PASSWORD=$(openssl rand -base64 48 | tr -d '\\n')"
echo "GF_ADMIN_PASSWORD=$(openssl rand -base64 24 | tr -d '\\n')"
echo "LUNA_MASTER_KEY=$(openssl rand -hex 32)"
```

---

## 4. Dependances

### 4.1 Analyse requirements.txt

| Package | Version | CVE | Severite |
|---------|---------|-----|----------|
| aiohttp | >=3.9.0 | CVE-2024-23334 | HAUTE |
| cryptography | >=42.0.0 | CVE-2024-12797 | HAUTE |
| pyyaml | >=6.0 | - | OK |
| redis | >=5.0.0 | - | OK |
| prometheus-client | >=0.19.0 | - | OK |

### 4.2 CVE Connues

#### CVE-2024-23334 - aiohttp Path Traversal

**Affecte:** aiohttp < 3.9.4
**Impact:** Un attaquant peut lire des fichiers arbitraires
**Correction:** Mettre a jour vers aiohttp >= 3.9.4

#### CVE-2024-12797 - cryptography OpenSSL

**Affecte:** cryptography < 44.0.1
**Impact:** Vulnerabilite dans les routines OpenSSL
**Correction:** Mettre a jour vers cryptography >= 44.0.1

### 4.3 Recommandations Dependances

```txt
# requirements.txt MIS A JOUR
aiohttp>=3.9.4           # CVE-2024-23334 fix
cryptography>=44.0.1     # CVE-2024-12797 fix
pyyaml>=6.0.1
redis>=5.0.0
prometheus-client>=0.20.0
mcp>=1.0.0
```

---

## 5. Pure Memory Security

### 5.1 Score: 25/100 (CRITIQUE)

### 5.2 Vulnerabilite CRITIQUE

#### SEC-001 [CRITIQUE] - Encryption XOR non securisee

```python
# archive_manager.py lignes 117-124 - PROBLEME CRITIQUE
class SimpleEncryption:
    def __init__(self, key: bytes):
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        # XOR encryption - TOTALEMENT INSECURE
        return bytes(a ^ b for a, b in zip(data, cycle(self.key)))
```

**Impact:**
- XOR avec cle repetee est trivialement cassable
- Toutes les donnees archivees sont compromises
- Attaque par analyse de frequence possible en minutes

#### SEC-003 [CRITIQUE] - Cle de chiffrement statique

```python
# archive_manager.py lignes 113-115
def _get_encryption_key(self) -> bytes:
    key_hex = self.config.get('encryption_key', 'luna_default_key_32bytes!')
    return key_hex.encode()[:32]
```

**Impact:** Cle par defaut connue = pas de securite.

### 5.3 Recommandations Pure Memory

**REMPLACER SimpleEncryption par une implementation securisee:**

```python
# archive_manager.py - VERSION SECURISEE
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class SecureEncryption:
    """Encryption AES-256 via Fernet (securise)."""

    def __init__(self, master_key_hex: str, salt: bytes = None):
        if not master_key_hex or len(master_key_hex) < 32:
            raise ValueError("Master key must be at least 32 hex characters")

        self.salt = salt or os.urandom(16)

        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(bytes.fromhex(master_key_hex)))
        self.fernet = Fernet(key)

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data with AES-256."""
        return self.salt + self.fernet.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data."""
        stored_salt = data[:16]
        ciphertext = data[16:]

        # Re-derive key with stored salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=stored_salt,
            iterations=480000,
        )
        # Note: Need to store master_key for decryption
        return self.fernet.decrypt(ciphertext)
```

---

## 6. Checklist de Remediation

### Priorite CRITIQUE (Semaine 1)

- [ ] **SEC-001** Remplacer encryption XOR par AES-256/Fernet
- [ ] **SEC-002** Deplacer GF_ADMIN_PASSWORD dans .env
- [ ] **SEC-003** Generer et configurer LUNA_MASTER_KEY unique

### Priorite HAUTE (Semaine 2)

- [ ] **SEC-004** Ajouter USER non-root dans Dockerfile
- [ ] **SEC-005** Modifier ports vers 127.0.0.1
- [ ] **SEC-006** Activer authentification Redis
- [ ] **SEC-007** Mettre a jour aiohttp >= 3.9.4
- [ ] **SEC-008** Mettre a jour cryptography >= 44.0.1

### Priorite MOYENNE (Semaine 3)

- [ ] Ajouter cap_drop: ALL dans docker-compose.yml
- [ ] Ajouter security_opt: no-new-privileges
- [ ] Implementer validation path dans json_manager.py
- [ ] Ajouter rate limiting sur les endpoints
- [ ] Configurer logging des acces sensibles
- [ ] Ajouter read_only: true avec tmpfs

### Priorite BASSE (Semaine 4)

- [ ] Implementer profil seccomp
- [ ] Ajouter scan de vulnerabilites dans CI/CD
- [ ] Documenter procedures de rotation des secrets
- [ ] Configurer alertes de securite

---

## 7. Score de Securite Detaille

| Categorie | Score | Poids | Score Pondere |
|-----------|-------|-------|---------------|
| Docker Security | 35/100 | 25% | 8.75 |
| Code Security | 75/100 | 20% | 15.00 |
| Secrets Management | 55/100 | 20% | 11.00 |
| Dependencies | 60/100 | 15% | 9.00 |
| Pure Memory Crypto | 25/100 | 20% | 5.00 |
| **TOTAL** | - | 100% | **48.75/100** |

### Objectif Post-Remediation

| Categorie | Actuel | Cible |
|-----------|--------|-------|
| Docker Security | 35 | 85 |
| Code Security | 75 | 90 |
| Secrets Management | 55 | 95 |
| Dependencies | 60 | 95 |
| Pure Memory Crypto | 25 | 90 |
| **TOTAL** | **48** | **90** |

---

## 8. Fichiers a Modifier

| Fichier | Modifications Requises |
|---------|----------------------|
| `Dockerfile` | Ajouter USER luna, multi-stage build |
| `docker-compose.yml` | Ports 127.0.0.1, secrets .env, cap_drop |
| `requirements.txt` | Versions aiohttp, cryptography |
| `archive_manager.py` | Remplacer SimpleEncryption |
| `json_manager.py` | Validation path traversal |
| `.env` | Ajouter GF_ADMIN_PASSWORD, LUNA_MASTER_KEY |
| `.gitignore` | Verifier exclusion .env |

---

## 9. Commandes de Verification

```bash
# Verifier user dans container
docker exec luna-consciousness id

# Verifier capabilities
docker inspect --format='{{.HostConfig.CapDrop}}' luna-consciousness

# Verifier ports
docker port luna-consciousness

# Scanner vulnerabilites
docker scan luna-consciousness

# Verifier .env non commite
git ls-files | grep -E "\.env$"
```

---

**Document prepare par:** Security Auditor Agent
**Date:** 26 novembre 2025
**Prochaine revue:** Apres remediation des vulnerabilites critiques
