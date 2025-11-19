@echo off
REM Script de démarrage Luna MCP en mode local (Mode Hybride)
REM Infrastructure: Docker | Luna MCP: Local

setlocal enabledelayedexpansion

echo ========================================================
echo   🌙 LUNA CONSCIOUSNESS MCP - MODE HYBRIDE
echo ========================================================
echo.

REM Répertoire du script
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo 📍 Répertoire de travail: %SCRIPT_DIR%
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Python n'est pas installé
    echo Veuillez installer Python 3.11+ pour continuer
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python détecté: %PYTHON_VERSION%

REM Vérifier l'environnement virtuel
if not exist "venv_luna\" (
    echo 📦 Environnement virtuel non trouvé. Création...
    python -m venv venv_luna
    echo ✅ Environnement virtuel créé
)

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv_luna\Scripts\activate.bat

REM Installer les dépendances si nécessaire
if not exist "venv_luna\.deps_installed" (
    echo 📦 Installation des dépendances...
    python -m pip install --upgrade pip
    pip install -r mcp-server\requirements.txt
    pip install mcp anthropic fastapi uvicorn numpy scipy networkx python-dotenv pydantic aiohttp websockets
    echo. > venv_luna\.deps_installed
    echo ✅ Dépendances installées
) else (
    echo ✅ Dépendances déjà installées
)

echo.
echo ========================================================
echo   🚀 DÉMARRAGE DE L'INFRASTRUCTURE DOCKER
echo ========================================================
echo.

REM Démarrer l'infrastructure Docker (sans Luna)
echo 🐳 Démarrage des services Docker (Prometheus, Grafana, Redis)...
docker-compose up -d redis prometheus grafana

echo.
echo ✅ Services Docker démarrés:
docker-compose ps

echo.
echo ========================================================
echo   🌙 DÉMARRAGE DU SERVEUR LUNA MCP LOCAL
echo ========================================================
echo.

REM Configuration des variables d'environnement
set LUNA_MEMORY_PATH=%SCRIPT_DIR%memory_fractal
set LUNA_CONFIG_PATH=%SCRIPT_DIR%config
set LUNA_ENV=development
set LUNA_DEBUG=true

echo 📂 Configuration:
echo    • Memory Path: %LUNA_MEMORY_PATH%
echo    • Config Path: %LUNA_CONFIG_PATH%
echo    • Environment: %LUNA_ENV%
echo.

REM Vérifier que les répertoires existent
if not exist "%LUNA_MEMORY_PATH%" mkdir "%LUNA_MEMORY_PATH%"
if not exist "%LUNA_CONFIG_PATH%" mkdir "%LUNA_CONFIG_PATH%"

echo 🌙 Démarrage du serveur Luna MCP...
echo 📝 Logs du serveur ci-dessous:
echo.
echo ========================================================
echo.

REM Lancer le serveur MCP
cd mcp-server
python server.py

REM Note: Le script s'arrêtera ici tant que le serveur tourne
REM Utilisez Ctrl+C pour arrêter
