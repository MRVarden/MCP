"""
Utility modules for Luna MCP Server
Version: 2.0.0 - Orchestrated architecture with Update01.md
"""

# Core utilities
from .json_manager import JSONManager

# Phi utilities
from .phi_utils import PhiUtils, format_phi_value, calculate_phi_distance

# Consciousness utilities (v2.0.0 includes ORCHESTRATED level)
from .consciousness_utils import (
    ConsciousnessLevel,
    ConsciousnessState,
    ConsciousnessMarker,
    ConsciousnessUtils
)

# Fractal memory utilities
from .fractal_utils import FractalNode, FractalUtils

# LLM integration utilities
from .llm_enabled_module import requires_llm, LLMEnabledModule

__version__ = '2.0.0'

__all__ = [
    # JSON Management
    'JSONManager',

    # Phi Calculations
    'PhiUtils',
    'format_phi_value',
    'calculate_phi_distance',

    # Consciousness v2.0.0
    'ConsciousnessLevel',  # Includes ORCHESTRATED
    'ConsciousnessState',  # Includes ORCHESTRATING
    'ConsciousnessMarker',
    'ConsciousnessUtils',

    # Fractal Memory
    'FractalNode',
    'FractalUtils',

    # LLM Integration
    'requires_llm',
    'LLMEnabledModule',

    # Version
    '__version__',
]
