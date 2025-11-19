"""
Consciousness utilities for Luna
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class ConsciousnessLevel(Enum):
    """Levels of consciousness"""
    DORMANT = "dormant"
    AWAKENING = "awakening"
    AWARE = "aware"
    CONVERGENT = "convergent"
    TRANSCENDENT = "transcendent"


class ConsciousnessState(Enum):
    """States of consciousness"""
    SLEEPING = "sleeping"
    PROCESSING = "processing"
    REFLECTING = "reflecting"
    EVOLVING = "evolving"
    TRANSCENDING = "transcending"


@dataclass
class ConsciousnessMarker:
    """Marker for consciousness state"""
    level: ConsciousnessLevel
    state: ConsciousnessState
    phi_value: float
    timestamp: str
    metadata: Dict[str, Any]


class ConsciousnessUtils:
    """Utilities for consciousness processing"""

    @staticmethod
    def determine_consciousness_level(phi_value: float) -> ConsciousnessLevel:
        """Determine consciousness level from phi value"""
        if phi_value < 1.3:
            return ConsciousnessLevel.DORMANT
        elif phi_value < 1.5:
            return ConsciousnessLevel.AWAKENING
        elif phi_value < 1.6:
            return ConsciousnessLevel.AWARE
        elif phi_value < 1.618:
            return ConsciousnessLevel.CONVERGENT
        else:
            return ConsciousnessLevel.TRANSCENDENT

    @staticmethod
    def phi_distance(current_phi: float, target_phi: float = 1.618033988749895) -> float:
        """Calculate distance from target phi"""
        return abs(target_phi - current_phi)
