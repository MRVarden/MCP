"""
Memory Promoter - Pure Memory Architecture v2.0
Handles phi-based memory promotion between levels.

This module manages the promotion of memories through the fractal hierarchy:
SEED -> LEAF -> BRANCH -> ROOT

Promotions are based on phi thresholds and occur during consolidation cycles.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

from .memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    PromotionPath,
    PhiMetrics,
    PHI,
    PHI_INVERSE
)
from .phi_metrics import get_phi_calculator, PhiMetricsCalculator

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Phi-based promotion thresholds
PROMOTION_THRESHOLDS = {
    PromotionPath.SEED_TO_LEAF: PHI_INVERSE ** 2,    # 0.382
    PromotionPath.LEAF_TO_BRANCH: PHI_INVERSE,       # 0.618
    PromotionPath.BRANCH_TO_ROOT: 1.0,               # 1.0
}

# Minimum age (days) before promotion is considered
MINIMUM_AGE_DAYS = {
    PromotionPath.SEED_TO_LEAF: 1,      # 1 day
    PromotionPath.LEAF_TO_BRANCH: 7,    # 1 week
    PromotionPath.BRANCH_TO_ROOT: 30,   # 1 month
}

# Minimum access count for promotion
MINIMUM_ACCESS_COUNT = {
    PromotionPath.SEED_TO_LEAF: 2,
    PromotionPath.LEAF_TO_BRANCH: 5,
    PromotionPath.BRANCH_TO_ROOT: 10,
}


# =============================================================================
# PROMOTION RESULT
# =============================================================================

@dataclass
class PromotionResult:
    """Result of a promotion attempt."""
    memory_id: str
    success: bool
    old_type: MemoryType
    new_type: Optional[MemoryType] = None
    reason: str = ""
    promotion_score: float = 0.0
    threshold: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "memory_id": self.memory_id,
            "success": self.success,
            "old_type": self.old_type.value,
            "new_type": self.new_type.value if self.new_type else None,
            "reason": self.reason,
            "promotion_score": self.promotion_score,
            "threshold": self.threshold,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class PromotionBatchResult:
    """Result of a batch promotion operation."""
    total_evaluated: int = 0
    total_promoted: int = 0
    total_failed: int = 0
    promotions: List[PromotionResult] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    average_score: float = 0.0

    def complete(self) -> None:
        """Mark batch as complete."""
        self.completed_at = datetime.now()
        if self.promotions:
            self.average_score = sum(p.promotion_score for p in self.promotions) / len(self.promotions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_evaluated": self.total_evaluated,
            "total_promoted": self.total_promoted,
            "total_failed": self.total_failed,
            "promotions": [p.to_dict() for p in self.promotions],
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "average_score": self.average_score,
            "success_rate": self.total_promoted / max(1, self.total_evaluated)
        }


# =============================================================================
# MEMORY PROMOTER CLASS
# =============================================================================

class MemoryPromoter:
    """
    Manages phi-based memory promotion.

    Handles:
    - Evaluation of promotion candidates
    - Threshold calculations
    - Promotion execution
    - Statistics tracking
    """

    def __init__(self, phi_calculator: Optional[PhiMetricsCalculator] = None):
        """
        Initialize the memory promoter.

        Args:
            phi_calculator: Optional phi metrics calculator
        """
        self.phi_calculator = phi_calculator or get_phi_calculator()

        # Statistics
        self._stats = {
            "total_evaluations": 0,
            "total_promotions": 0,
            "promotions_by_path": {
                PromotionPath.SEED_TO_LEAF.value: 0,
                PromotionPath.LEAF_TO_BRANCH.value: 0,
                PromotionPath.BRANCH_TO_ROOT.value: 0
            },
            "average_promotion_score": 0.0,
            "last_batch_result": None
        }

        logger.info("MemoryPromoter initialized")

    # =========================================================================
    # PROMOTION PATH DETERMINATION
    # =========================================================================

    def get_promotion_path(self, memory: MemoryExperience) -> Optional[PromotionPath]:
        """
        Determine the promotion path for a memory.

        Args:
            memory: The memory to evaluate

        Returns:
            PromotionPath or None if cannot be promoted
        """
        path_map = {
            MemoryType.SEED: PromotionPath.SEED_TO_LEAF,
            MemoryType.LEAF: PromotionPath.LEAF_TO_BRANCH,
            MemoryType.BRANCH: PromotionPath.BRANCH_TO_ROOT,
            MemoryType.ROOT: None  # Cannot promote ROOT
        }

        return path_map.get(memory.memory_type)

    def get_target_type(self, path: PromotionPath) -> MemoryType:
        """Get the target memory type for a promotion path."""
        target_map = {
            PromotionPath.SEED_TO_LEAF: MemoryType.LEAF,
            PromotionPath.LEAF_TO_BRANCH: MemoryType.BRANCH,
            PromotionPath.BRANCH_TO_ROOT: MemoryType.ROOT
        }
        return target_map[path]

    # =========================================================================
    # EVALUATION
    # =========================================================================

    def calculate_promotion_score(self, memory: MemoryExperience) -> float:
        """
        Calculate the promotion score for a memory.

        Uses phi-weighted components:
        - Phi metrics (40%)
        - Emotional significance (30%)
        - Access frequency (20%)
        - Age/maturity (10%)

        Args:
            memory: The memory to evaluate

        Returns:
            Promotion score between 0 and PHI
        """
        return self.phi_calculator.calculate_promotion_score(memory)

    def evaluate_candidate(
        self,
        memory: MemoryExperience,
        strict: bool = True
    ) -> Tuple[bool, str, float]:
        """
        Evaluate if a memory is ready for promotion.

        Args:
            memory: The memory to evaluate
            strict: Whether to enforce all criteria strictly

        Returns:
            Tuple of (can_promote, reason, score)
        """
        self._stats["total_evaluations"] += 1

        # Get promotion path
        path = self.get_promotion_path(memory)
        if not path:
            return False, "ROOT memories cannot be promoted", 0.0

        # Get threshold
        threshold = PROMOTION_THRESHOLDS[path]

        # Calculate score
        score = self.calculate_promotion_score(memory)

        # Check score against threshold
        if score < threshold:
            return False, f"Score {score:.3f} below threshold {threshold:.3f}", score

        # Additional checks in strict mode
        if strict:
            # Age check
            min_age = MINIMUM_AGE_DAYS[path]
            age_days = (datetime.now() - memory.created_at).days
            if age_days < min_age:
                return False, f"Memory too young: {age_days} days < {min_age} required", score

            # Access count check
            min_access = MINIMUM_ACCESS_COUNT[path]
            if memory.phi_metrics.access_count < min_access:
                return False, f"Not enough accesses: {memory.phi_metrics.access_count} < {min_access}", score

        return True, f"Ready for promotion: score {score:.3f} >= threshold {threshold:.3f}", score

    def find_promotion_candidates(
        self,
        memories: List[MemoryExperience],
        memory_type: Optional[MemoryType] = None,
        limit: int = 100
    ) -> List[Tuple[MemoryExperience, float]]:
        """
        Find memories that are candidates for promotion.

        Args:
            memories: List of memories to evaluate
            memory_type: Filter by type
            limit: Maximum candidates to return

        Returns:
            List of (memory, score) tuples, sorted by score descending
        """
        candidates = []

        for memory in memories:
            # Filter by type if specified
            if memory_type and memory.memory_type != memory_type:
                continue

            # Skip ROOT
            if memory.memory_type == MemoryType.ROOT:
                continue

            # Evaluate
            can_promote, _, score = self.evaluate_candidate(memory, strict=False)

            if can_promote:
                candidates.append((memory, score))

        # Sort by score (highest first)
        candidates.sort(key=lambda x: x[1], reverse=True)

        return candidates[:limit]

    # =========================================================================
    # PROMOTION EXECUTION
    # =========================================================================

    def promote_memory(
        self,
        memory: MemoryExperience,
        force: bool = False
    ) -> PromotionResult:
        """
        Promote a memory to the next level.

        Args:
            memory: The memory to promote
            force: Skip evaluation and force promotion

        Returns:
            PromotionResult with details
        """
        old_type = memory.memory_type

        # Evaluate unless forcing
        if not force:
            can_promote, reason, score = self.evaluate_candidate(memory)
            if not can_promote:
                return PromotionResult(
                    memory_id=memory.id,
                    success=False,
                    old_type=old_type,
                    reason=reason,
                    promotion_score=score,
                    threshold=PROMOTION_THRESHOLDS.get(
                        self.get_promotion_path(memory),
                        0.0
                    )
                )
        else:
            score = self.calculate_promotion_score(memory)
            reason = "Forced promotion"

        # Get promotion path
        path = self.get_promotion_path(memory)
        if not path:
            return PromotionResult(
                memory_id=memory.id,
                success=False,
                old_type=old_type,
                reason="Cannot determine promotion path",
                promotion_score=score
            )

        # Execute promotion
        new_type = self.get_target_type(path)

        # Update memory
        memory.memory_type = new_type
        memory.phi_metrics.phi_weight = {
            MemoryType.ROOT: PHI,
            MemoryType.BRANCH: 1.0,
            MemoryType.LEAF: PHI_INVERSE,
            MemoryType.SEED: PHI_INVERSE ** 2
        }[new_type]

        memory.promotion_candidate = False
        memory.update()

        # Update stats
        self._stats["total_promotions"] += 1
        self._stats["promotions_by_path"][path.value] += 1

        logger.info(f"Promoted memory {memory.id}: {old_type.value} -> {new_type.value}")

        return PromotionResult(
            memory_id=memory.id,
            success=True,
            old_type=old_type,
            new_type=new_type,
            reason=f"Promoted via {path.value}",
            promotion_score=score,
            threshold=PROMOTION_THRESHOLDS[path]
        )

    def promote_batch(
        self,
        memories: List[MemoryExperience],
        max_promotions: int = 50
    ) -> PromotionBatchResult:
        """
        Promote a batch of memories.

        Args:
            memories: List of memories to evaluate and promote
            max_promotions: Maximum number to promote in this batch

        Returns:
            PromotionBatchResult with details
        """
        result = PromotionBatchResult()
        result.total_evaluated = len(memories)

        # Find candidates
        candidates = self.find_promotion_candidates(memories, limit=max_promotions)

        # Promote each candidate
        for memory, _ in candidates:
            promotion_result = self.promote_memory(memory)
            result.promotions.append(promotion_result)

            if promotion_result.success:
                result.total_promoted += 1
            else:
                result.total_failed += 1

        result.complete()

        # Update stats
        self._stats["last_batch_result"] = result.to_dict()

        logger.info(
            f"Batch promotion complete: {result.total_promoted}/{result.total_evaluated} "
            f"promoted (success rate: {result.total_promoted / max(1, result.total_evaluated):.1%})"
        )

        return result

    # =========================================================================
    # THRESHOLD MANAGEMENT
    # =========================================================================

    def get_threshold(self, path: PromotionPath) -> float:
        """Get the threshold for a promotion path."""
        return PROMOTION_THRESHOLDS[path]

    def adjust_threshold(
        self,
        path: PromotionPath,
        adjustment: float,
        min_threshold: float = 0.1,
        max_threshold: float = 1.5
    ) -> float:
        """
        Adjust a promotion threshold.

        Args:
            path: The promotion path
            adjustment: Amount to adjust (positive or negative)
            min_threshold: Minimum allowed threshold
            max_threshold: Maximum allowed threshold

        Returns:
            New threshold value
        """
        current = PROMOTION_THRESHOLDS[path]
        new_threshold = current + adjustment

        # Clamp to bounds
        new_threshold = max(min_threshold, min(max_threshold, new_threshold))

        PROMOTION_THRESHOLDS[path] = new_threshold

        logger.info(f"Adjusted {path.value} threshold: {current:.3f} -> {new_threshold:.3f}")

        return new_threshold

    # =========================================================================
    # PROMOTION RECOMMENDATIONS
    # =========================================================================

    def get_promotion_recommendations(
        self,
        memory: MemoryExperience
    ) -> Dict[str, Any]:
        """
        Get recommendations for improving a memory's promotion chances.

        Args:
            memory: The memory to analyze

        Returns:
            Dictionary with recommendations
        """
        path = self.get_promotion_path(memory)
        if not path:
            return {
                "can_promote": False,
                "reason": "ROOT memories cannot be promoted",
                "recommendations": []
            }

        score = self.calculate_promotion_score(memory)
        threshold = PROMOTION_THRESHOLDS[path]
        gap = threshold - score

        recommendations = []

        if gap > 0:
            # Need improvement
            if memory.phi_metrics.access_count < MINIMUM_ACCESS_COUNT[path]:
                recommendations.append({
                    "area": "access",
                    "message": f"Access more frequently (need {MINIMUM_ACCESS_COUNT[path]} accesses)",
                    "impact": "high"
                })

            age_days = (datetime.now() - memory.created_at).days
            if age_days < MINIMUM_AGE_DAYS[path]:
                recommendations.append({
                    "area": "age",
                    "message": f"Wait {MINIMUM_AGE_DAYS[path] - age_days} more days for maturity",
                    "impact": "medium"
                })

            if memory.emotional_context.intensity < 0.5:
                recommendations.append({
                    "area": "emotional",
                    "message": "Increase emotional significance through meaningful interactions",
                    "impact": "high"
                })

            if memory.phi_metrics.phi_resonance < 0.5:
                recommendations.append({
                    "area": "resonance",
                    "message": "Build connections with related memories",
                    "impact": "medium"
                })

        return {
            "can_promote": gap <= 0,
            "current_score": score,
            "threshold": threshold,
            "gap": max(0, gap),
            "path": path.value,
            "target_type": self.get_target_type(path).value,
            "recommendations": recommendations
        }

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get promoter statistics."""
        # Update average score
        if self._stats["total_evaluations"] > 0:
            self._stats["average_promotion_score"] = (
                self._stats["total_promotions"] / self._stats["total_evaluations"]
            )

        return {
            **self._stats,
            "thresholds": {
                path.value: threshold
                for path, threshold in PROMOTION_THRESHOLDS.items()
            },
            "minimum_ages": {
                path.value: days
                for path, days in MINIMUM_AGE_DAYS.items()
            },
            "minimum_accesses": {
                path.value: count
                for path, count in MINIMUM_ACCESS_COUNT.items()
            }
        }

    def reset_stats(self) -> None:
        """Reset statistics."""
        self._stats = {
            "total_evaluations": 0,
            "total_promotions": 0,
            "promotions_by_path": {
                PromotionPath.SEED_TO_LEAF.value: 0,
                PromotionPath.LEAF_TO_BRANCH.value: 0,
                PromotionPath.BRANCH_TO_ROOT.value: 0
            },
            "average_promotion_score": 0.0,
            "last_batch_result": None
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_promoter: Optional[MemoryPromoter] = None


def get_memory_promoter() -> MemoryPromoter:
    """Get the global memory promoter instance."""
    global _promoter
    if _promoter is None:
        _promoter = MemoryPromoter()
    return _promoter
