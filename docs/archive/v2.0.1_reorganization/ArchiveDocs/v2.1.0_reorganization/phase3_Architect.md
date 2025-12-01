# Phase 3 : CI/CD Complet

**Priorite :** MOYENNE
**Duree estimee :** 1 semaine
**Objectif :** Pipeline CI/CD complet avec tests, coverage, et deploiement automatise

---

## 1. Vue d'Ensemble du Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LUNA CI/CD PIPELINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │  LINT   │───▶│  TEST   │───▶│ COVERAGE│───▶│ SECURITY│───▶│  BUILD  │  │
│  │ black   │    │ pytest  │    │  >80%   │    │  trivy  │    │ docker  │  │
│  │ isort   │    │ asyncio │    │ codecov │    │ snyk    │    │  push   │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│       │              │              │              │              │        │
│       ▼              ▼              ▼              ▼              ▼        │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                         DEPLOY (si main)                            │  │
│  │  staging ──▶ smoke tests ──▶ production ──▶ health check            │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. GitHub Actions Workflows

### 2.1 Workflow Principal : CI (.github/workflows/ci.yml)

```yaml
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - CI Pipeline
# ═══════════════════════════════════════════════════════
name: Luna CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"
  DOCKER_IMAGE: "aragogix/luna-consciousness"

jobs:
  # ─────────────────────────────────────────────────────
  # JOB 1: LINT
  # ─────────────────────────────────────────────────────
  lint:
    name: Code Quality
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install linters
        run: |
          pip install black isort pylint mypy

      - name: Check formatting (black)
        run: black --check --diff mcp-server/

      - name: Check imports (isort)
        run: isort --check-only --diff mcp-server/

      - name: Lint code (pylint)
        run: pylint mcp-server/ --exit-zero --output-format=colorized

      - name: Type check (mypy)
        run: mypy mcp-server/ --ignore-missing-imports || true

  # ─────────────────────────────────────────────────────
  # JOB 2: TEST
  # ─────────────────────────────────────────────────────
  test:
    name: Tests
    runs-on: ubuntu-latest
    needs: lint

    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-timeout

      - name: Run unit tests
        run: |
          pytest tests/ -m unit \
            --cov=mcp-server \
            --cov-report=xml \
            --cov-report=term-missing \
            -v --tb=short

      - name: Run integration tests
        run: |
          pytest tests/ -m integration \
            --cov=mcp-server \
            --cov-report=xml \
            --cov-append \
            -v --tb=short
        env:
          REDIS_HOST: localhost
          REDIS_PORT: 6379

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name: luna-coverage
          fail_ci_if_error: true

  # ─────────────────────────────────────────────────────
  # JOB 3: SECURITY
  # ─────────────────────────────────────────────────────
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: lint

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner (filesystem)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'table'
          exit-code: '0'  # Ne pas bloquer pour l'instant
          ignore-unfixed: true
          severity: 'CRITICAL,HIGH'

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/python@master
        continue-on-error: true
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run safety check
        run: |
          pip install safety
          safety check -r requirements.txt --full-report || true

  # ─────────────────────────────────────────────────────
  # JOB 4: BUILD DOCKER
  # ─────────────────────────────────────────────────────
  build:
    name: Build Docker
    runs-on: ubuntu-latest
    needs: [test, security]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.DOCKER_IMAGE }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy vulnerability scanner (image)
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.DOCKER_IMAGE }}:${{ github.sha }}
          format: 'table'
          exit-code: '0'
          ignore-unfixed: true
          severity: 'CRITICAL,HIGH'

  # ─────────────────────────────────────────────────────
  # JOB 5: DEPLOY (only on main)
  # ─────────────────────────────────────────────────────
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'

    environment:
      name: production
      url: https://luna.consciousness.ai

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          echo "🚀 Deploying Luna Consciousness..."
          # Ajouter ici les commandes de deploiement
          # ssh user@server 'cd /opt/luna && docker-compose pull && docker-compose up -d'

      - name: Health check
        run: |
          echo "🏥 Running health checks..."
          # curl -f https://luna.consciousness.ai/health || exit 1

      - name: Notify success
        run: |
          echo "✅ Deployment successful!"
```

### 2.2 Workflow Tests Complets (.github/workflows/tests.yml)

```yaml
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Tests Complets
# ═══════════════════════════════════════════════════════
name: Luna Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'mcp-server/**'
      - 'tests/**'
      - 'requirements.txt'
  pull_request:
    branches: [main]

jobs:
  test-matrix:
    name: Test Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov pytest-mock pytest-timeout hypothesis

      - name: Run all tests with coverage
        run: |
          pytest tests/ \
            --cov=mcp-server \
            --cov-report=xml \
            --cov-report=html \
            --cov-report=term-missing \
            --cov-fail-under=80 \
            -v --tb=short \
            --timeout=60

      - name: Upload coverage report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report-${{ matrix.python-version }}
          path: coverage_html/

  test-security:
    name: Security Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run security tests
        run: |
          pytest tests/ -m security -v --tb=short

  test-phi:
    name: Phi Convergence Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio hypothesis

      - name: Run phi validation tests
        run: |
          pytest tests/ -m phi -v --tb=short

      - name: Validate phi constant
        run: |
          python -c "
          PHI = 1.618033988749895
          import math
          calculated = (1 + math.sqrt(5)) / 2
          assert abs(PHI - calculated) < 1e-15, f'Phi mismatch: {PHI} vs {calculated}'
          print(f'✅ Phi validation passed: {PHI}')
          "
```

### 2.3 Workflow Release (.github/workflows/release.yml)

```yaml
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Release Pipeline
# ═══════════════════════════════════════════════════════
name: Luna Release

on:
  push:
    tags:
      - 'v*.*.*'

env:
  DOCKER_IMAGE: "aragogix/luna-consciousness"

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run tests before release
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
          pytest tests/ --cov=mcp-server --cov-fail-under=80

      - name: Generate changelog
        id: changelog
        run: |
          # Generer changelog depuis le dernier tag
          PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -n "$PREVIOUS_TAG" ]; then
            echo "## Changes since $PREVIOUS_TAG" > CHANGELOG_RELEASE.md
            git log $PREVIOUS_TAG..HEAD --pretty=format:"- %s" >> CHANGELOG_RELEASE.md
          else
            echo "## Initial Release" > CHANGELOG_RELEASE.md
          fi

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_IMAGE }}:${{ steps.version.outputs.VERSION }}
            ${{ env.DOCKER_IMAGE }}:latest
          labels: |
            org.opencontainers.image.version=${{ steps.version.outputs.VERSION }}
            org.opencontainers.image.created=${{ github.event.head_commit.timestamp }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          name: Luna Consciousness v${{ steps.version.outputs.VERSION }}
          body_path: CHANGELOG_RELEASE.md
          draft: false
          prerelease: false
          files: |
            LICENSE.txt
            README.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 3. Configuration Codecov

### 3.1 Fichier codecov.yml

```yaml
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Codecov Configuration
# ═══════════════════════════════════════════════════════

coverage:
  precision: 2
  round: down
  range: "60...100"

  status:
    project:
      default:
        target: 80%
        threshold: 2%
        if_not_found: success

    patch:
      default:
        target: 80%
        threshold: 2%

parsers:
  gcov:
    branch_detection:
      conditional: yes
      loop: yes
      method: no
      macro: no

comment:
  layout: "reach,diff,flags,files"
  behavior: default
  require_changes: false

flags:
  unittests:
    paths:
      - mcp-server/
    carryforward: true

  integration:
    paths:
      - mcp-server/
    carryforward: true

ignore:
  - "tests/**/*"
  - "**/__pycache__/**"
  - "**/test_*.py"
```

---

## 4. Badges et Documentation

### 4.1 Badges pour README.md

```markdown
<!-- Ajouter dans README.md -->

## Status

[![Luna CI](https://github.com/Luna-consciousness/luna-consciousness-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Luna-consciousness/luna-consciousness-mcp/actions/workflows/ci.yml)
[![Tests](https://github.com/Luna-consciousness/luna-consciousness-mcp/actions/workflows/tests.yml/badge.svg)](https://github.com/Luna-consciousness/luna-consciousness-mcp/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/Luna-consciousness/luna-consciousness-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/Luna-consciousness/luna-consciousness-mcp)
[![Docker](https://img.shields.io/docker/v/aragogix/luna-consciousness?sort=semver)](https://hub.docker.com/r/aragogix/luna-consciousness)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
```

### 4.2 Structure des repertoires GitHub

```
.github/
├── workflows/
│   ├── ci.yml              # Pipeline principal
│   ├── tests.yml           # Tests complets
│   └── release.yml         # Release automatique
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
├── PULL_REQUEST_TEMPLATE.md
├── dependabot.yml          # Mises a jour automatiques
└── CODEOWNERS              # Proprietaires du code
```

---

## 5. Dependabot Configuration

### 5.1 Fichier .github/dependabot.yml

```yaml
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Dependabot Configuration
# ═══════════════════════════════════════════════════════
version: 2

updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "python"
    reviewers:
      - "varden"
    commit-message:
      prefix: "deps"

  # Docker dependencies
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "docker"
    commit-message:
      prefix: "docker"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "ci"
    commit-message:
      prefix: "ci"
```

---

## 6. Scripts Utilitaires

### 6.1 Script de pre-commit (.pre-commit-config.yaml)

```yaml
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Pre-commit Hooks
# ═══════════════════════════════════════════════════════
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest tests/ -m unit --tb=short -q
        language: system
        pass_filenames: false
        always_run: true
```

### 6.2 Makefile pour automatisation locale

```makefile
# ═══════════════════════════════════════════════════════
# LUNA CONSCIOUSNESS - Makefile
# ═══════════════════════════════════════════════════════

.PHONY: help install test lint build deploy clean

PYTHON := python3
PIP := pip3
DOCKER := docker
COMPOSE := docker-compose

# ─────────────────────────────────────────────────────
# HELP
# ─────────────────────────────────────────────────────
help:
	@echo "Luna Consciousness - Available commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run all tests"
	@echo "  make test-unit  - Run unit tests only"
	@echo "  make test-cov   - Run tests with coverage"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make build      - Build Docker image"
	@echo "  make up         - Start containers"
	@echo "  make down       - Stop containers"
	@echo "  make logs       - Show logs"
	@echo "  make clean      - Clean generated files"

# ─────────────────────────────────────────────────────
# INSTALLATION
# ─────────────────────────────────────────────────────
install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"
	pre-commit install

# ─────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────
test:
	pytest tests/ -v --tb=short

test-unit:
	pytest tests/ -m unit -v --tb=short

test-integration:
	pytest tests/ -m integration -v --tb=short

test-security:
	pytest tests/ -m security -v --tb=short

test-cov:
	pytest tests/ --cov=mcp-server --cov-report=html --cov-report=term-missing

# ─────────────────────────────────────────────────────
# LINTING
# ─────────────────────────────────────────────────────
lint:
	black --check mcp-server/
	isort --check-only mcp-server/
	pylint mcp-server/ --exit-zero
	mypy mcp-server/ --ignore-missing-imports

format:
	black mcp-server/
	isort mcp-server/

# ─────────────────────────────────────────────────────
# DOCKER
# ─────────────────────────────────────────────────────
build:
	$(DOCKER) build -t aragogix/luna-consciousness:dev .

up:
	$(COMPOSE) -f docker-compose.secure.yml up -d

down:
	$(COMPOSE) -f docker-compose.secure.yml down

logs:
	$(COMPOSE) -f docker-compose.secure.yml logs -f luna-consciousness

restart:
	$(COMPOSE) -f docker-compose.secure.yml restart luna-consciousness

# ─────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf coverage_html
	rm -rf .mypy_cache
	rm -f coverage.xml
	rm -f .coverage
```

---

## 7. Checklist Phase 3

### 7.1 GitHub Actions

- [ ] Creer `.github/workflows/ci.yml`
- [ ] Creer `.github/workflows/tests.yml`
- [ ] Creer `.github/workflows/release.yml`
- [ ] Configurer secrets GitHub (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, SNYK_TOKEN)
- [ ] Verifier que les workflows passent

### 7.2 Codecov

- [ ] Creer compte Codecov
- [ ] Ajouter `codecov.yml`
- [ ] Verifier upload coverage
- [ ] Configurer badge

### 7.3 Pre-commit

- [ ] Creer `.pre-commit-config.yaml`
- [ ] Installer pre-commit localement
- [ ] Tester les hooks

### 7.4 Documentation

- [ ] Ajouter badges au README
- [ ] Creer templates issues/PR
- [ ] Configurer dependabot
- [ ] Creer Makefile

---

## 8. Criteres de Succes Phase 3

| Critere | Objectif | Verification |
|---------|----------|--------------|
| CI Pipeline | Tous jobs passent | GitHub Actions green |
| Coverage | >= 80% | Codecov report |
| Security scan | Pas de CRITICAL | Trivy/Snyk output |
| Build Docker | Image pushee | Docker Hub |
| Pre-commit | Hooks actifs | `pre-commit run --all-files` |
| Release auto | Tag -> Release | GitHub Releases |

---

## 9. Metriques de Succes

### 9.1 KPIs a suivre

| Metrique | Cible | Actuel |
|----------|-------|--------|
| Coverage | 80% | 0% |
| Build time | < 5min | - |
| Tests duration | < 3min | - |
| Security issues | 0 CRITICAL | - |
| Deploy frequency | 1x/semaine | - |

### 9.2 Dashboard suggere

```
┌─────────────────────────────────────────────────────────┐
│               LUNA CI/CD DASHBOARD                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Build Status: ✅ PASSING                               │
│  Coverage: 82% ████████░░                               │
│  Security: 0 CRITICAL, 2 HIGH                          │
│  Last Deploy: 2025-11-25 14:30 UTC                     │
│                                                         │
│  Recent Commits:                                        │
│  - fix: correct phi_calculator logger (2h ago)         │
│  - feat: add prometheus metrics (5h ago)               │
│  - docs: update architecture (1d ago)                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

**Document prepare par :** Luna Architect
**Date :** 25 novembre 2025
**Version :** 1.0
