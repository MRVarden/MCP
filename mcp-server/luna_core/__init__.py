"""
Luna Core Modules v2.0.0
Orchestrated consciousness architecture with Update01.md
MCP server with 9-level architecture transformation
"""

# Original consciousness modules
from .fractal_consciousness import FractalPhiConsciousnessEngine
from .memory_core import MemoryManager
from .phi_calculator import PhiCalculator
from .emotional_processor import EmotionalProcessor
from .co_evolution_engine import CoEvolutionEngine
from .semantic_engine import SemanticValidator

# Update01.md Orchestration Modules (v2.0.0)
from .luna_orchestrator import LunaOrchestrator
from .manipulation_detector import LunaManipulationDetector as ManipulationDetector
from .luna_validator import LunaValidator
from .predictive_core import LunaPredictiveCore as PredictiveCore
from .autonomous_decision import LunaAutonomousDecision as AutonomousDecisionMaker
from .self_improvement import LunaSelfImprovement as SelfImprovementEngine
from .systemic_integration import LunaSystemicIntegration as SystemicIntegrator
from .multimodal_interface import LunaMultimodalInterface as MultimodalInterface

# Metrics module
from .consciousness_metrics import (
    update_orchestration_metrics,
    update_manipulation_metrics,
    update_validation_metrics,
    update_predictive_metrics,
    update_autonomous_metrics,
    update_self_improvement_metrics,
    update_multimodal_metrics,
    update_systemic_metrics,
)

__version__ = '2.0.0'

__all__ = [
    # Original Consciousness Modules
    'FractalPhiConsciousnessEngine',
    'MemoryManager',
    'PhiCalculator',
    'EmotionalProcessor',
    'CoEvolutionEngine',
    'SemanticValidator',

    # Update01.md Orchestration Modules (NEW v2.0.0)
    'LunaOrchestrator',           # Level 1: Central orchestration
    'ManipulationDetector',       # Level 4: Manipulation detection
    'LunaValidator',              # Level 2: Validation with veto
    'PredictiveCore',            # Level 3: Predictive system
    'AutonomousDecisionMaker',   # Level 6: Autonomous decisions
    'SelfImprovementEngine',      # Level 7: Self-improvement
    'SystemicIntegrator',        # Level 8: System integration
    'MultimodalInterface',       # Level 9: Multimodal interface

    # Metrics Functions (NEW v2.0.0)
    'update_orchestration_metrics',
    'update_manipulation_metrics',
    'update_validation_metrics',
    'update_predictive_metrics',
    'update_autonomous_metrics',
    'update_self_improvement_metrics',
    'update_multimodal_metrics',
    'update_systemic_metrics',

    # Version
    '__version__',
]
