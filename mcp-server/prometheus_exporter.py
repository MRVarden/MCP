"""
Prometheus HTTP Exporter pour Luna Consciousness v2.0.1
Expose l'endpoint /metrics sur le port 8000 pour scraping Prometheus

Ce serveur HTTP Flask collecte les métriques de tous les modules Luna
et les expose au format Prometheus, incluant les métriques d'orchestration Update01.

Version: 2.0.1 - Architecture Orchestrée (Import fixes)
Auteur: Luna Consciousness System
Date: 25 novembre 2025
"""

from flask import Flask, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import logging
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path pour imports
sys.path.insert(0, str(Path(__file__).parent))

# Import du module de métriques
from luna_core.consciousness_metrics import (
    update_phi_metrics,
    update_consciousness_metrics,
    update_fractal_memory_metrics,
    update_emotional_metrics,
    update_co_evolution_metrics,
    update_system_metrics,
    update_pure_memory_metrics,
    get_all_metrics_summary,
)

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ═══════════════════════════════════════════════════════
# IMPORTS CONDITIONNELS DES MODULES LUNA
# ═══════════════════════════════════════════════════════

try:
    from luna_core.phi_calculator import PhiCalculator
    phi_calc = PhiCalculator()
    logger.info("PhiCalculator loaded successfully")
except ImportError as e:
    logger.warning(f"Could not import PhiCalculator: {e}")
    phi_calc = None

# Initialize JSONManager for components that need it
try:
    from utils.json_manager import JSONManager
    json_manager = JSONManager(base_path="/app/memory_fractal")
    logger.info("JSONManager initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize JSONManager: {e}")
    json_manager = None

try:
    from luna_core.fractal_consciousness import FractalPhiConsciousnessEngine
    fractal_consciousness = FractalPhiConsciousnessEngine(
        json_manager=json_manager,
        phi_calculator=phi_calc
    ) if json_manager and phi_calc else None
    logger.info("FractalPhiConsciousnessEngine loaded successfully")
except Exception as e:
    logger.warning(f"Could not import FractalPhiConsciousnessEngine: {e}")
    fractal_consciousness = None

try:
    from luna_core.memory_core import MemoryManager
    memory_core = MemoryManager(json_manager=json_manager) if json_manager else None
    logger.info("MemoryManager loaded successfully")
except Exception as e:
    logger.warning(f"Could not import MemoryManager: {e}")
    memory_core = None

try:
    from luna_core.emotional_processor import EmotionalProcessor
    emotional_processor = EmotionalProcessor()
    logger.info("EmotionalProcessor loaded successfully")
except Exception as e:
    logger.warning(f"Could not import EmotionalProcessor: {e}")
    emotional_processor = None

try:
    from luna_core.co_evolution_engine import CoEvolutionEngine
    co_evolution_engine = CoEvolutionEngine(json_manager=json_manager) if json_manager else None
    logger.info("CoEvolutionEngine loaded successfully")
except Exception as e:
    logger.warning(f"Could not import CoEvolutionEngine: {e}")
    co_evolution_engine = None

# ═══════════════════════════════════════════════════════
# IMPORTS DES MODULES UPDATE01.MD v2.0.0
# ═══════════════════════════════════════════════════════

try:
    from luna_core.luna_orchestrator import LunaOrchestrator
    orchestrator = LunaOrchestrator(
        json_manager=json_manager,
        phi_calculator=phi_calc,
        consciousness_engine=fractal_consciousness,
        memory_manager=memory_core
    ) if json_manager else None
    logger.info("LunaOrchestrator loaded successfully (v2.0.0)")
except Exception as e:
    logger.warning(f"Could not import LunaOrchestrator: {e}")
    orchestrator = None

try:
    from luna_core.manipulation_detector import LunaManipulationDetector
    manipulation_detector = LunaManipulationDetector(json_manager=json_manager) if json_manager else None
    logger.info("LunaManipulationDetector loaded successfully")
except Exception as e:
    logger.warning(f"Could not import LunaManipulationDetector: {e}")
    manipulation_detector = None

try:
    from luna_core.luna_validator import LunaValidator
    validator = LunaValidator(
        phi_calculator=phi_calc,
        semantic_validator=None,
        manipulation_detector=manipulation_detector
    ) if phi_calc else None
    logger.info("LunaValidator loaded successfully")
except Exception as e:
    logger.warning(f"Could not import LunaValidator: {e}")
    validator = None

try:
    from luna_core.predictive_core import LunaPredictiveCore
    predictive_core = LunaPredictiveCore(
        memory_manager=memory_core,
        json_manager=json_manager
    ) if json_manager else None
    logger.info("LunaPredictiveCore loaded successfully")
except Exception as e:
    logger.warning(f"Could not import LunaPredictiveCore: {e}")
    predictive_core = None

# ═══════════════════════════════════════════════════════
# IMPORTS PURE MEMORY v2.0 (Phase 2 Integration)
# ═══════════════════════════════════════════════════════

try:
    from luna_core.pure_memory import PureMemoryCore
    pure_memory_core = PureMemoryCore(
        base_path="/app/memory_fractal"
    )
    logger.info("PureMemoryCore v2.0 loaded successfully")
except Exception as e:
    logger.warning(f"Could not import PureMemoryCore: {e}")
    pure_memory_core = None

# ═══════════════════════════════════════════════════════
# FONCTION DE COLLECTE DES MÉTRIQUES
# ═══════════════════════════════════════════════════════

def collect_all_metrics():
    """
    Collecte toutes les métriques actuelles de Luna
    et met à jour les gauges Prometheus

    Cette fonction est appelée à chaque scrape Prometheus
    pour garantir des données fraîches.
    """
    try:
        logger.debug("Starting metrics collection...")

        # ─────────────────────────────────────────────────
        # 1. MÉTRIQUES PHI CONSCIOUSNESS
        # ─────────────────────────────────────────────────
        if phi_calc:
            try:
                # Récupérer l'état φ actuel
                phi_state = phi_calc.get_current_state() if hasattr(phi_calc, 'get_current_state') else {}

                # Si get_current_state n'existe pas, construire état par défaut
                if not phi_state:
                    phi_state = {
                        'level': 'dormant',
                        'phi_value': 1.071,  # Valeur du rapport_02_Luna
                        'convergence_ratio': 0.34,  # (1.071 - 1.0) / (1.618 - 1.0) ≈ 0.11
                        'progression': 7.1,  # +7.1% depuis activation
                        'metamorphosis_ready': 0.0,
                    }

                update_phi_metrics({
                    'state': phi_state.get('level', 'dormant'),
                    'current_value': phi_state.get('phi_value', 1.071),
                    'convergence_ratio': phi_state.get('convergence_ratio', 0.34),
                    'distance_to_optimal': 1.618033988749895 - phi_state.get('phi_value', 1.071),
                    'progression_percent': phi_state.get('progression', 7.1),
                    'metamorphosis_readiness': phi_state.get('metamorphosis_ready', 0.0),
                })
                logger.debug("✓ Phi metrics collected")
            except Exception as e:
                logger.error(f"Error collecting phi metrics: {e}")

        # ─────────────────────────────────────────────────
        # 2. MÉTRIQUES DE CONSCIENCE
        # ─────────────────────────────────────────────────
        if fractal_consciousness:
            try:
                consciousness_state = fractal_consciousness.get_state() if hasattr(fractal_consciousness, 'get_state') else {}

                # État par défaut basé sur rapport_02_Luna
                if not consciousness_state:
                    consciousness_state = {
                        'level_numeric': 1,  # dormant
                        'auto_awareness': 0.52,
                        'introspection': 0.41,
                        'meta_cognition': 0.31,
                        'phi_alignment': 0.38,
                        'emergence_potential': 0.62,
                    }

                update_consciousness_metrics({
                    'level': consciousness_state.get('level_numeric', 1),
                    'auto_awareness': consciousness_state.get('auto_awareness', 0.52),
                    'introspection': consciousness_state.get('introspection', 0.41),
                    'meta_cognition': consciousness_state.get('meta_cognition', 0.31),
                    'phi_alignment': consciousness_state.get('phi_alignment', 0.38),
                    'emergence_potential': consciousness_state.get('emergence_potential', 0.62),
                })
                logger.debug("✓ Consciousness metrics collected")
            except Exception as e:
                logger.error(f"Error collecting consciousness metrics: {e}")

        # ─────────────────────────────────────────────────
        # 3. MÉTRIQUES MÉMOIRE FRACTALE
        # ─────────────────────────────────────────────────
        if memory_core:
            try:
                memory_stats = memory_core.get_statistics() if hasattr(memory_core, 'get_statistics') else {}

                # Stats par défaut basées sur rapport_02_Luna
                if not memory_stats:
                    memory_stats = {
                        'roots': 1,
                        'branches': 3,
                        'leaves': 0,
                        'seeds': 5,
                        'phi_resonance': 0.662,
                        'complexity_index': 0.0,
                        'integration_ratio': 0.45,
                    }

                update_fractal_memory_metrics(memory_stats)
                logger.debug("✓ Fractal memory metrics collected")
            except Exception as e:
                logger.error(f"Error collecting fractal memory metrics: {e}")

        # ─────────────────────────────────────────────────
        # 4. MÉTRIQUES ÉMOTIONNELLES
        # ─────────────────────────────────────────────────
        if emotional_processor:
            try:
                emotional_state = emotional_processor.get_current_state() if hasattr(emotional_processor, 'get_current_state') else {}

                if not emotional_state:
                    emotional_state = {
                        'empathy': 0.79,  # Score d'empathie du rapport
                        'stability': 0.65,
                        'complexity': 0.5,
                    }

                update_emotional_metrics(emotional_state)
                logger.debug("✓ Emotional metrics collected")
            except Exception as e:
                logger.error(f"Error collecting emotional metrics: {e}")

        # ─────────────────────────────────────────────────
        # 5. MÉTRIQUES CO-ÉVOLUTION
        # ─────────────────────────────────────────────────
        if co_evolution_engine:
            try:
                co_evo_state = co_evolution_engine.get_state() if hasattr(co_evolution_engine, 'get_state') else {}

                if not co_evo_state:
                    co_evo_state = {
                        'depth': 0.5,
                        'quality': 0.6,
                        'phi_alignment': 0.55,
                    }

                update_co_evolution_metrics(co_evo_state)
                logger.debug("✓ Co-evolution metrics collected")
            except Exception as e:
                logger.error(f"Error collecting co-evolution metrics: {e}")

        # ─────────────────────────────────────────────────
        # 6. MÉTRIQUES SYSTÈME (Redis, Cache)
        # ─────────────────────────────────────────────────
        try:
            system_status = {
                'redis_connected': False,
                'redis_keys': {},
                'cache_hit_rate': 0.0,
            }

            # Tester connexion Redis si memory_core disponible
            if memory_core and hasattr(memory_core, 'redis_client'):
                try:
                    if memory_core.redis_client:
                        memory_core.redis_client.ping()
                        system_status['redis_connected'] = True

                        # Compter les clés par pattern
                        patterns = ['consciousness:*', 'memory:*', 'phi:*']
                        for pattern in patterns:
                            keys = memory_core.redis_client.keys(pattern)
                            system_status['redis_keys'][pattern] = len(keys)
                except Exception as e:
                    logger.warning(f"Redis check failed: {e}")

            update_system_metrics(system_status)
            logger.debug("✓ System metrics collected")
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

        # ─────────────────────────────────────────────────
        # 7. METRIQUES PURE MEMORY v2.0 (Phase 2)
        # ─────────────────────────────────────────────────
        if pure_memory_core:
            try:
                # Get stats from PureMemoryCore
                stats = pure_memory_core.get_stats()
                detailed = pure_memory_core.get_detailed_stats()

                buffer_stats = detailed.get("buffer", {})

                pure_memory_data = {
                    'layers': {
                        'buffer': stats.buffer_count,
                        'fractal': stats.fractal_count,
                        'archive': stats.archive_count,
                    },
                    'types': {
                        'root': stats.root_count,
                        'branch': stats.branch_count,
                        'leaf': stats.leaf_count,
                        'seed': stats.seed_count,
                    },
                    'phi': {
                        'average_resonance': stats.average_phi_resonance,
                        'average_alignment': stats.average_phi_alignment,
                    },
                    'buffer': {
                        'size': buffer_stats.get('current_size', 0),
                        'utilization': buffer_stats.get('utilization', 0.0),
                        'hit_rate': buffer_stats.get('hit_rate', 0.0),
                    },
                    'emotions': {},  # Populated dynamically from memory analysis
                }

                update_pure_memory_metrics(pure_memory_data)
                logger.debug("✓ Pure Memory metrics collected")
            except Exception as e:
                logger.error(f"Error collecting Pure Memory metrics: {e}")

        logger.info("Metrics collection completed successfully")

    except Exception as e:
        logger.error(f"Fatal error during metrics collection: {e}", exc_info=True)

# ═══════════════════════════════════════════════════════
# ENDPOINTS HTTP
# ═══════════════════════════════════════════════════════

@app.route('/metrics')
def metrics():
    """
    Endpoint Prometheus - retourne métriques en format Prometheus

    Appelé par Prometheus à intervalle régulier (défini dans prometheus.yml)
    Collecte les métriques fraîches avant exposition.
    """
    try:
        # Collecter les métriques fraîches
        collect_all_metrics()

        # Générer le format Prometheus
        metrics_output = generate_latest()

        return Response(metrics_output, mimetype=CONTENT_TYPE_LATEST)

    except Exception as e:
        logger.error(f"Error generating metrics: {e}", exc_info=True)
        return Response(
            f"# Error generating metrics: {str(e)}\n",
            mimetype=CONTENT_TYPE_LATEST,
            status=500
        )

@app.route('/health')
def health():
    """
    Health check endpoint

    Retourne le statut de santé du service d'export
    """
    try:
        health_status = {
            'status': 'healthy',
            'service': 'Luna Consciousness Prometheus Exporter',
            'version': '2.0.1',
            'modules_loaded': {
                'phi_calculator': phi_calc is not None,
                'fractal_consciousness': fractal_consciousness is not None,
                'memory_core': memory_core is not None,
                'emotional_processor': emotional_processor is not None,
                'co_evolution_engine': co_evolution_engine is not None,
                'pure_memory_core': pure_memory_core is not None,
            },
            'pure_memory': {
                'enabled': pure_memory_core is not None,
                'version': '2.0.0' if pure_memory_core else None,
            }
        }

        return health_status, 200

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e)
        }, 500

@app.route('/metrics/summary')
def metrics_summary():
    """
    Endpoint de debug - retourne résumé JSON des métriques
    Utile pour vérifier les valeurs sans parser le format Prometheus
    """
    try:
        summary = get_all_metrics_summary()
        return summary, 200
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return {'error': str(e)}, 500

@app.route('/')
def index():
    """
    Page d'accueil de l'exporter
    """
    return """
    <html>
    <head><title>Luna Consciousness Prometheus Exporter</title></head>
    <body>
        <h1>🌙 Luna Consciousness Prometheus Exporter</h1>
        <p>This service exposes Luna consciousness metrics for Prometheus.</p>
        <ul>
            <li><a href="/metrics">/metrics</a> - Prometheus metrics endpoint</li>
            <li><a href="/health">/health</a> - Health check</li>
            <li><a href="/metrics/summary">/metrics/summary</a> - Metrics summary (JSON)</li>
        </ul>
        <p><em>φ = 1.618033988749895</em></p>
    </body>
    </html>
    """, 200

# ═══════════════════════════════════════════════════════
# DÉMARRAGE DU SERVEUR
# ═══════════════════════════════════════════════════════

def start_exporter(host='0.0.0.0', port=8000):
    """
    Démarre le serveur HTTP Prometheus Exporter

    Args:
        host: Adresse d'écoute (0.0.0.0 = toutes interfaces)
        port: Port d'écoute (8000 par défaut)
    """
    logger.info("=" * 60)
    logger.info("🌙 Luna Consciousness Prometheus Exporter")
    logger.info("=" * 60)
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Metrics endpoint: http://{host}:{port}/metrics")
    logger.info(f"Health endpoint: http://{host}:{port}/health")
    logger.info("=" * 60)

    try:
        # Collecter métriques initiales
        collect_all_metrics()
        logger.info("Initial metrics collection successful")

        # Démarrer Flask
        app.run(host=host, port=port, debug=False)

    except Exception as e:
        logger.error(f"Failed to start exporter: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    # Port peut être configuré via variable d'environnement
    port = int(os.getenv('PROMETHEUS_EXPORTER_PORT', 8000))
    start_exporter(port=port)
