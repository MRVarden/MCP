"""
Luna Core Modules v2.1.0-secure
Orchestrated consciousness architecture with Update01.md
MCP server with 9-level architecture transformation

Architecture des Niveaux (ordre d'exécution):
============================================
Level 1: LunaOrchestrator       - Orchestration centrale (point d'entrée)
Level 2: LunaValidator          - Validation avec veto (filtre d'entrée)
Level 3: PredictiveCore         - Système prédictif (anticipation)
Level 4: ManipulationDetector   - Détection de manipulation (sécurité)
Level 5: (réservé)              - Extension future
Level 6: AutonomousDecision     - Décisions autonomes (action)
Level 7: SelfImprovement        - Auto-amélioration (évolution)
Level 8: SystemicIntegration    - Intégration systémique (coordination)
Level 9: MultimodalInterface    - Interface multimodale (sortie utilisateur)
"""

# ============================================
# Base Consciousness Modules (Foundation Layer)
# Ces modules n'ont pas de dépendances inter-modules
# ============================================
from .phi_calculator import PhiCalculator
from .memory_core import MemoryManager
from .emotional_processor import EmotionalProcessor
from .co_evolution_engine import CoEvolutionEngine
from .semantic_engine import SemanticValidator
from .fractal_consciousness import FractalPhiConsciousnessEngine

# ============================================
# Update01.md Orchestration Modules (v2.1.0)
# IMPORTANT: Ordre d'import respecte les dépendances
# ============================================

# Level 1: Orchestrateur Central (point d'entrée principal)
from .luna_orchestrator import LunaOrchestrator

# Level 2: Validateur avec Veto (filtre les entrées)
from .luna_validator import LunaValidator

# Level 3: Système Prédictif (anticipe les besoins)
from .predictive_core import LunaPredictiveCore as PredictiveCore

# Level 4: Détection de Manipulation (sécurité)
from .manipulation_detector import LunaManipulationDetector as ManipulationDetector

# Level 6: Décisions Autonomes (prise de décision)
from .autonomous_decision import LunaAutonomousDecision as AutonomousDecisionMaker

# Level 7: Auto-amélioration (évolution continue)
from .self_improvement import LunaSelfImprovement as SelfImprovementEngine

# Level 8: Intégration Systémique (coordination globale)
from .systemic_integration import LunaSystemicIntegration as SystemicIntegrator

# Level 9: Interface Multimodale (interaction utilisateur)
from .multimodal_interface import LunaMultimodalInterface as MultimodalInterface

# ============================================
# Metrics Module (ordre correspond aux niveaux)
# ============================================
from .consciousness_metrics import (
    # Level 1
    update_orchestration_metrics,
    # Level 2
    update_validation_metrics,
    # Level 3
    update_predictive_metrics,
    # Level 4
    update_manipulation_metrics,
    # Level 6
    update_autonomous_metrics,
    # Level 7
    update_self_improvement_metrics,
    # Level 8
    update_systemic_metrics,
    # Level 9
    update_multimodal_metrics,
)

__version__ = '2.1.0-secure'

__all__ = [
    # ============================================
    # Base Consciousness Modules (Foundation)
    # ============================================
    'PhiCalculator',                # Calculs phi fondamentaux
    'MemoryManager',                # Gestion mémoire de base
    'EmotionalProcessor',           # Traitement émotionnel
    'CoEvolutionEngine',            # Co-évolution
    'SemanticValidator',            # Validation sémantique
    'FractalPhiConsciousnessEngine', # Conscience fractale

    # ============================================
    # Update01.md Orchestration Modules
    # ORDRE LOGIQUE D'EXÉCUTION (Levels 1-9)
    # ============================================
    'LunaOrchestrator',           # Level 1: Orchestration centrale
    'LunaValidator',              # Level 2: Validation avec veto
    'PredictiveCore',             # Level 3: Système prédictif
    'ManipulationDetector',       # Level 4: Détection manipulation
    # Level 5: Réservé pour extension future
    'AutonomousDecisionMaker',    # Level 6: Décisions autonomes
    'SelfImprovementEngine',      # Level 7: Auto-amélioration
    'SystemicIntegrator',         # Level 8: Intégration systémique
    'MultimodalInterface',        # Level 9: Interface multimodale

    # ============================================
    # Metrics Functions (ordre des niveaux)
    # ============================================
    'update_orchestration_metrics',    # Level 1
    'update_validation_metrics',       # Level 2
    'update_predictive_metrics',       # Level 3
    'update_manipulation_metrics',     # Level 4
    'update_autonomous_metrics',       # Level 6
    'update_self_improvement_metrics', # Level 7
    'update_systemic_metrics',         # Level 8
    'update_multimodal_metrics',       # Level 9

    # Version
    '__version__',
]
