"""
Phi Metrics - Pure Memory Architecture v2.0
Extended phi calculations for memory importance and resonance.

This module extends the phi calculations to support the Pure Memory system,
providing metrics for memory importance, resonance, and promotion decisions.
"""

import math
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from .memory_types import (
    MemoryExperience,
    MemoryType,
    PhiMetrics,
    PHI,
    PHI_INVERSE,
    PHI_SQUARED
)

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Phi-based thresholds
PHI_THRESHOLD_LOW = PHI_INVERSE ** 2     # 0.382
PHI_THRESHOLD_MED = PHI_INVERSE          # 0.618
PHI_THRESHOLD_HIGH = 1.0                 # 1.0
PHI_THRESHOLD_GOLDEN = PHI               # 1.618

# Resonance decay rate (per day)
RESONANCE_DECAY_RATE = 0.01

# Maximum resonance value
MAX_RESONANCE = 1.0

# Fibonacci sequence for reference
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


# =============================================================================
# PHI CALCULATOR EXTENSIONS
# =============================================================================

class PhiMetricsCalculator:
    """
    Extended phi calculations for Pure Memory system.

    Provides:
    - Memory importance scoring
    - Resonance calculations between memories
    - Phi distance optimization
    - Promotion readiness assessment
    """

    def __init__(self):
        self.phi = PHI
        self.phi_inverse = PHI_INVERSE

        # Cache for resonance calculations
        self._resonance_cache: Dict[Tuple[str, str], float] = {}

    # =========================================================================
    # IMPORTANCE CALCULATIONS
    # =========================================================================

    def calculate_importance(
        self,
        memory: MemoryExperience,
        include_connections: bool = True
    ) -> float:
        """
        Calculate the overall importance of a memory.

        Args:
            memory: The memory to evaluate
            include_connections: Whether to include connection bonus

        Returns:
            Importance score between 0 and PHI
        """
        # Base components
        phi_component = self._calculate_phi_component(memory.phi_metrics)
        emotional_component = self._calculate_emotional_component(memory)
        temporal_component = self._calculate_temporal_component(memory)
        access_component = self._calculate_access_component(memory.phi_metrics)

        # Connection bonus
        connection_bonus = 0.0
        if include_connections:
            connection_count = len(memory.children_ids) + len(memory.related_ids)
            connection_bonus = min(connection_count * 0.05, 0.3)

        # Weighted sum with phi ratios
        importance = (
            phi_component * PHI_INVERSE +           # 0.618 weight
            emotional_component * PHI_INVERSE ** 2 + # 0.382 weight
            temporal_component * 0.1 +
            access_component * 0.1 +
            connection_bonus
        )

        return min(PHI, max(0.0, importance))

    def _calculate_phi_component(self, phi_metrics: PhiMetrics) -> float:
        """Calculate phi-based component of importance."""
        alignment = 1.0 - min(1.0, phi_metrics.phi_distance / PHI)
        resonance = phi_metrics.phi_resonance

        return (
            phi_metrics.phi_weight * 0.4 +
            alignment * 0.3 +
            resonance * 0.3
        )

    def _calculate_emotional_component(self, memory: MemoryExperience) -> float:
        """Calculate emotional component of importance."""
        context = memory.emotional_context

        # Intensity contributes directly
        intensity_score = context.intensity

        # Positive valence slightly boosts importance
        valence_bonus = max(0, context.valence) * 0.2

        # Arousal indicates memorable experiences
        arousal_score = context.arousal * 0.3

        return intensity_score * 0.5 + valence_bonus + arousal_score

    def _calculate_temporal_component(self, memory: MemoryExperience) -> float:
        """Calculate time-based component (recency matters)."""
        age_days = (datetime.now() - memory.created_at).days

        # Newer memories have higher temporal score
        # Decay follows phi ratio
        decay_factor = PHI_INVERSE ** (age_days / 30)

        return max(0.1, decay_factor)

    def _calculate_access_component(self, phi_metrics: PhiMetrics) -> float:
        """Calculate access-based component."""
        # More accesses = more important
        # Diminishing returns using phi
        access_count = phi_metrics.access_count
        return min(1.0, math.log(access_count + 1) / math.log(self.phi * 10))

    # =========================================================================
    # RESONANCE CALCULATIONS
    # =========================================================================

    def calculate_resonance(
        self,
        memory1: MemoryExperience,
        memory2: MemoryExperience
    ) -> float:
        """
        Calculate resonance between two memories.

        Args:
            memory1: First memory
            memory2: Second memory

        Returns:
            Resonance score between 0 and 1
        """
        # Check cache
        cache_key = tuple(sorted([memory1.id, memory2.id]))
        if cache_key in self._resonance_cache:
            return self._resonance_cache[cache_key]

        # Calculate components
        semantic_resonance = self._calculate_semantic_resonance(memory1, memory2)
        emotional_resonance = self._calculate_emotional_resonance(memory1, memory2)
        temporal_resonance = self._calculate_temporal_resonance(memory1, memory2)
        type_resonance = self._calculate_type_resonance(memory1, memory2)

        # Weighted combination using phi
        resonance = (
            semantic_resonance * PHI_INVERSE +      # 0.618
            emotional_resonance * PHI_INVERSE ** 2 + # 0.382
            temporal_resonance * 0.1 +
            type_resonance * 0.1
        )

        # Normalize
        resonance = min(MAX_RESONANCE, max(0.0, resonance))

        # Cache result
        self._resonance_cache[cache_key] = resonance

        return resonance

    def _calculate_semantic_resonance(
        self,
        memory1: MemoryExperience,
        memory2: MemoryExperience
    ) -> float:
        """Calculate semantic similarity based on keywords and content."""
        # Keyword overlap
        keywords1 = set(memory1.keywords)
        keywords2 = set(memory2.keywords)

        if not keywords1 or not keywords2:
            keyword_similarity = 0.0
        else:
            intersection = len(keywords1 & keywords2)
            union = len(keywords1 | keywords2)
            keyword_similarity = intersection / union if union > 0 else 0.0

        # Tag overlap
        tags1 = set(memory1.tags)
        tags2 = set(memory2.tags)

        if not tags1 or not tags2:
            tag_similarity = 0.0
        else:
            intersection = len(tags1 & tags2)
            union = len(tags1 | tags2)
            tag_similarity = intersection / union if union > 0 else 0.0

        # Simple word overlap in content
        words1 = set(memory1.content.lower().split())
        words2 = set(memory2.content.lower().split())

        intersection = len(words1 & words2)
        union = len(words1 | words2)
        content_similarity = intersection / union if union > 0 else 0.0

        return (
            keyword_similarity * 0.5 +
            tag_similarity * 0.3 +
            content_similarity * 0.2
        )

    def _calculate_emotional_resonance(
        self,
        memory1: MemoryExperience,
        memory2: MemoryExperience
    ) -> float:
        """Calculate emotional resonance between memories."""
        ctx1 = memory1.emotional_context
        ctx2 = memory2.emotional_context

        # Same primary emotion = high resonance
        if ctx1.primary_emotion == ctx2.primary_emotion:
            base_resonance = 0.8
        else:
            base_resonance = 0.3

        # Valence similarity
        valence_diff = abs(ctx1.valence - ctx2.valence)
        valence_similarity = 1.0 - (valence_diff / 2.0)

        # Arousal similarity
        arousal_diff = abs(ctx1.arousal - ctx2.arousal)
        arousal_similarity = 1.0 - arousal_diff

        return (
            base_resonance * 0.5 +
            valence_similarity * 0.3 +
            arousal_similarity * 0.2
        )

    def _calculate_temporal_resonance(
        self,
        memory1: MemoryExperience,
        memory2: MemoryExperience
    ) -> float:
        """Calculate temporal proximity resonance."""
        time_diff = abs((memory1.created_at - memory2.created_at).total_seconds())
        hours_diff = time_diff / 3600

        # Memories created close together resonate more
        # Decay using phi
        return PHI_INVERSE ** (hours_diff / 24)

    def _calculate_type_resonance(
        self,
        memory1: MemoryExperience,
        memory2: MemoryExperience
    ) -> float:
        """Calculate type-based resonance."""
        type_distances = {
            (MemoryType.ROOT, MemoryType.ROOT): 1.0,
            (MemoryType.ROOT, MemoryType.BRANCH): 0.8,
            (MemoryType.ROOT, MemoryType.LEAF): 0.6,
            (MemoryType.ROOT, MemoryType.SEED): 0.4,
            (MemoryType.BRANCH, MemoryType.BRANCH): 1.0,
            (MemoryType.BRANCH, MemoryType.LEAF): 0.8,
            (MemoryType.BRANCH, MemoryType.SEED): 0.5,
            (MemoryType.LEAF, MemoryType.LEAF): 1.0,
            (MemoryType.LEAF, MemoryType.SEED): 0.7,
            (MemoryType.SEED, MemoryType.SEED): 1.0
        }

        key = (memory1.memory_type, memory2.memory_type)
        reverse_key = (memory2.memory_type, memory1.memory_type)

        return type_distances.get(key, type_distances.get(reverse_key, 0.5))

    # =========================================================================
    # PHI DISTANCE OPTIMIZATION
    # =========================================================================

    def calculate_phi_distance(self, value: float) -> float:
        """
        Calculate distance from the golden ratio.

        Args:
            value: The value to measure

        Returns:
            Distance from phi (0 = perfect alignment)
        """
        return abs(value - self.phi)

    def optimize_phi_alignment(
        self,
        current_value: float,
        target_improvement: float = 0.1
    ) -> float:
        """
        Suggest an optimized value closer to phi.

        Args:
            current_value: Current value
            target_improvement: How much to improve by

        Returns:
            Suggested new value
        """
        distance = self.calculate_phi_distance(current_value)

        if distance < 0.001:
            return current_value  # Already optimal

        # Move toward phi
        direction = 1 if current_value < self.phi else -1
        improvement = min(target_improvement, distance)

        return current_value + (direction * improvement)

    def is_phi_aligned(self, value: float, threshold: float = 0.01) -> bool:
        """Check if a value is aligned with phi."""
        return self.calculate_phi_distance(value) < threshold

    # =========================================================================
    # PROMOTION SCORING
    # =========================================================================

    def calculate_promotion_score(self, memory: MemoryExperience) -> float:
        """
        Calculate promotion score for a memory.

        Args:
            memory: The memory to evaluate

        Returns:
            Promotion score (higher = more ready)
        """
        # Phi metrics contribution (40%)
        phi_score = memory.phi_metrics.calculate_importance()

        # Emotional significance (30%)
        emotional_score = memory.emotional_context.calculate_emotional_weight()

        # Access frequency (20%)
        access_score = min(memory.phi_metrics.access_count / 10, 1.0)

        # Age and maturity (10%)
        age_days = (datetime.now() - memory.created_at).days
        maturity_score = min(age_days / 30, 1.0)

        return (
            phi_score * 0.4 +
            emotional_score * 0.3 +
            access_score * 0.2 +
            maturity_score * 0.1
        )

    def should_promote(self, memory: MemoryExperience) -> Tuple[bool, str]:
        """
        Determine if a memory should be promoted.

        Args:
            memory: The memory to evaluate

        Returns:
            Tuple of (should_promote, reason)
        """
        score = self.calculate_promotion_score(memory)

        thresholds = {
            MemoryType.SEED: PHI_THRESHOLD_LOW,      # 0.382
            MemoryType.LEAF: PHI_THRESHOLD_MED,      # 0.618
            MemoryType.BRANCH: PHI_THRESHOLD_HIGH,   # 1.0
            MemoryType.ROOT: float('inf')            # Cannot promote
        }

        threshold = thresholds.get(memory.memory_type, float('inf'))

        if memory.memory_type == MemoryType.ROOT:
            return False, "ROOT memories cannot be promoted"

        if score >= threshold:
            return True, f"Score {score:.3f} >= threshold {threshold:.3f}"

        return False, f"Score {score:.3f} < threshold {threshold:.3f}"

    # =========================================================================
    # FIBONACCI HELPERS
    # =========================================================================

    def get_nearest_fibonacci(self, value: int) -> int:
        """Get the nearest Fibonacci number."""
        for i, fib in enumerate(FIBONACCI):
            if fib >= value:
                if i == 0:
                    return fib
                prev = FIBONACCI[i - 1]
                if value - prev < fib - value:
                    return prev
                return fib
        return FIBONACCI[-1]

    def is_fibonacci(self, value: int) -> bool:
        """Check if a value is a Fibonacci number."""
        return value in FIBONACCI

    def fibonacci_weight(self, count: int) -> float:
        """
        Get a phi-based weight for a count.
        Uses Fibonacci sequence proximity.
        """
        nearest = self.get_nearest_fibonacci(count)
        distance = abs(count - nearest) / max(nearest, 1)
        return 1.0 - min(1.0, distance)

    # =========================================================================
    # BATCH CALCULATIONS
    # =========================================================================

    def calculate_batch_metrics(
        self,
        memories: List[MemoryExperience]
    ) -> Dict[str, Any]:
        """
        Calculate aggregate metrics for a batch of memories.

        Args:
            memories: List of memories to analyze

        Returns:
            Dictionary of aggregate metrics
        """
        if not memories:
            return {
                "count": 0,
                "average_importance": 0.0,
                "average_resonance": 0.0,
                "phi_alignment": 0.0,
                "type_distribution": {}
            }

        # Calculate individual metrics
        importances = [self.calculate_importance(m) for m in memories]
        alignments = [m.phi_metrics.calculate_phi_alignment() for m in memories]

        # Type distribution
        type_counts = {}
        for m in memories:
            t = m.memory_type.value
            type_counts[t] = type_counts.get(t, 0) + 1

        # Average pairwise resonance (sample if too many)
        resonances = []
        sample_size = min(len(memories), 20)
        import random
        sample = random.sample(memories, sample_size) if len(memories) > sample_size else memories

        for i in range(len(sample)):
            for j in range(i + 1, len(sample)):
                resonances.append(self.calculate_resonance(sample[i], sample[j]))

        avg_resonance = sum(resonances) / len(resonances) if resonances else 0.0

        return {
            "count": len(memories),
            "average_importance": sum(importances) / len(importances),
            "max_importance": max(importances),
            "min_importance": min(importances),
            "average_resonance": avg_resonance,
            "phi_alignment": sum(alignments) / len(alignments),
            "type_distribution": type_counts,
            "promotion_candidates": sum(1 for m in memories if self.should_promote(m)[0])
        }

    def update_resonance_after_access(
        self,
        memory: MemoryExperience,
        related_memories: List[MemoryExperience]
    ) -> None:
        """
        Update resonance values after a memory is accessed.

        Args:
            memory: The accessed memory
            related_memories: Memories to update resonance with
        """
        for related in related_memories:
            # Calculate new resonance
            resonance = self.calculate_resonance(memory, related)

            # Update both memories' resonance scores
            # Using exponential moving average
            alpha = PHI_INVERSE  # Learning rate based on phi

            memory.phi_metrics.phi_resonance = (
                alpha * resonance +
                (1 - alpha) * memory.phi_metrics.phi_resonance
            )

            related.phi_metrics.phi_resonance = (
                alpha * resonance +
                (1 - alpha) * related.phi_metrics.phi_resonance
            )

    def decay_resonance(
        self,
        memories: List[MemoryExperience],
        days_elapsed: float = 1.0
    ) -> None:
        """
        Apply temporal decay to resonance values.

        Args:
            memories: Memories to decay
            days_elapsed: Number of days since last decay
        """
        decay_factor = 1.0 - (RESONANCE_DECAY_RATE * days_elapsed)
        decay_factor = max(0.0, decay_factor)

        for memory in memories:
            memory.phi_metrics.phi_resonance *= decay_factor

        # Clear resonance cache after decay
        self._resonance_cache.clear()


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Global calculator instance
_phi_calculator: Optional[PhiMetricsCalculator] = None


def get_phi_calculator() -> PhiMetricsCalculator:
    """Get the global phi metrics calculator instance."""
    global _phi_calculator
    if _phi_calculator is None:
        _phi_calculator = PhiMetricsCalculator()
    return _phi_calculator
