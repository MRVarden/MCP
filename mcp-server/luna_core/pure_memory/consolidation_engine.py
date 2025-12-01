"""
Consolidation Engine - Pure Memory Architecture v2.0
Manages the Oneiric Consolidation cycle.

This module implements the "sleep-like" consolidation process that:
1. Transfers memories between layers
2. Extracts patterns
3. Promotes memories
4. Cleans up expired memories
"""

import asyncio
import logging
from datetime import datetime, time, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field

from .memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    ConsolidationPhase,
    ConsolidationReport,
    PHI,
    PHI_INVERSE
)
from .memory_buffer import MemoryBuffer
from .fractal_memory import FractalMemory
from .archive_manager import ArchiveManager
from .memory_promoter import MemoryPromoter, get_memory_promoter
from .phi_metrics import PhiMetricsCalculator, get_phi_calculator

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Consolidation schedule (military time)
CONSOLIDATION_SCHEDULE = {
    ConsolidationPhase.ANALYSIS: (0, 0),       # 00:00
    ConsolidationPhase.EXTRACTION: (1, 0),     # 01:00
    ConsolidationPhase.CONSOLIDATION: (2, 30), # 02:30
    ConsolidationPhase.PROMOTION: (4, 0),      # 04:00
    ConsolidationPhase.CLEANUP: (4, 30),       # 04:30
}

# Phase durations (minutes)
PHASE_DURATIONS = {
    ConsolidationPhase.ANALYSIS: 60,
    ConsolidationPhase.EXTRACTION: 90,
    ConsolidationPhase.CONSOLIDATION: 90,
    ConsolidationPhase.PROMOTION: 30,
    ConsolidationPhase.CLEANUP: 30,
}

# Thresholds
MIN_IMPORTANCE_FOR_FRACTAL = 0.3   # Minimum importance to move buffer -> fractal
MIN_IMPORTANCE_FOR_ARCHIVE = 0.6  # Minimum importance to move fractal -> archive
MAX_MEMORIES_PER_PHASE = 500      # Maximum memories to process per phase


# =============================================================================
# PATTERN EXTRACTION
# =============================================================================

@dataclass
class ExtractedPattern:
    """A pattern extracted during consolidation."""
    pattern_id: str
    pattern_type: str  # semantic, emotional, temporal
    description: str
    memory_ids: List[str]
    phi_resonance: float
    confidence: float
    extracted_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "description": self.description,
            "memory_ids": self.memory_ids,
            "phi_resonance": self.phi_resonance,
            "confidence": self.confidence,
            "extracted_at": self.extracted_at.isoformat()
        }


# =============================================================================
# CONSOLIDATION ENGINE
# =============================================================================

class ConsolidationEngine:
    """
    Manages the Oneiric Consolidation process.

    Implements a "sleep-like" cycle that:
    - Analyzes daily memories
    - Extracts patterns
    - Consolidates to archive
    - Promotes memories
    - Cleans up expired data
    """

    def __init__(
        self,
        buffer: MemoryBuffer,
        fractal: FractalMemory,
        archive: ArchiveManager,
        promoter: Optional[MemoryPromoter] = None,
        phi_calculator: Optional[PhiMetricsCalculator] = None
    ):
        """
        Initialize the consolidation engine.

        Args:
            buffer: Memory buffer layer
            fractal: Fractal memory layer
            archive: Archive layer
            promoter: Memory promoter
            phi_calculator: Phi metrics calculator
        """
        self.buffer = buffer
        self.fractal = fractal
        self.archive = archive
        self.promoter = promoter or get_memory_promoter()
        self.phi_calculator = phi_calculator or get_phi_calculator()

        # State
        self._current_phase = ConsolidationPhase.ANALYSIS
        self._is_running = False
        self._current_report: Optional[ConsolidationReport] = None

        # History
        self._consolidation_history: List[ConsolidationReport] = []

        # Callbacks
        self._phase_callbacks: Dict[ConsolidationPhase, List[Callable]] = {
            phase: [] for phase in ConsolidationPhase
        }

        logger.info("ConsolidationEngine initialized")

    # =========================================================================
    # MAIN CONSOLIDATION CYCLE
    # =========================================================================

    async def run_consolidation_cycle(
        self,
        force: bool = False
    ) -> ConsolidationReport:
        """
        Run a complete consolidation cycle.

        Args:
            force: Force run even outside scheduled time

        Returns:
            ConsolidationReport with results
        """
        if self._is_running and not force:
            logger.warning("Consolidation already running")
            return self._current_report

        self._is_running = True
        self._current_report = ConsolidationReport()

        try:
            logger.info("Starting consolidation cycle...")

            # Phase 1: Analysis
            await self._run_phase(ConsolidationPhase.ANALYSIS)

            # Phase 2: Extraction
            await self._run_phase(ConsolidationPhase.EXTRACTION)

            # Phase 3: Consolidation
            await self._run_phase(ConsolidationPhase.CONSOLIDATION)

            # Phase 4: Promotion
            await self._run_phase(ConsolidationPhase.PROMOTION)

            # Phase 5: Cleanup
            await self._run_phase(ConsolidationPhase.CLEANUP)

            # Complete
            self._current_report.complete()
            self._consolidation_history.append(self._current_report)

            logger.info(
                f"Consolidation cycle complete: "
                f"analyzed={self._current_report.memories_analyzed}, "
                f"consolidated={self._current_report.memories_consolidated}, "
                f"promoted={self._current_report.memories_promoted}, "
                f"cleaned={self._current_report.memories_cleaned}"
            )

        except Exception as e:
            logger.error(f"Consolidation cycle failed: {e}")
            self._current_report.errors.append(str(e))

        finally:
            self._is_running = False

        return self._current_report

    async def _run_phase(self, phase: ConsolidationPhase) -> None:
        """Run a single consolidation phase."""
        self._current_phase = phase
        self._current_report.phase = phase

        logger.info(f"Starting phase: {phase.value}")

        # Run phase-specific logic
        if phase == ConsolidationPhase.ANALYSIS:
            await self._phase_analysis()
        elif phase == ConsolidationPhase.EXTRACTION:
            await self._phase_extraction()
        elif phase == ConsolidationPhase.CONSOLIDATION:
            await self._phase_consolidation()
        elif phase == ConsolidationPhase.PROMOTION:
            await self._phase_promotion()
        elif phase == ConsolidationPhase.CLEANUP:
            await self._phase_cleanup()

        # Run callbacks
        for callback in self._phase_callbacks[phase]:
            try:
                await callback(self._current_report)
            except Exception as e:
                logger.warning(f"Phase callback failed: {e}")

    # =========================================================================
    # PHASE IMPLEMENTATIONS
    # =========================================================================

    async def _phase_analysis(self) -> None:
        """
        Phase 1: Analysis (00:00-01:00)
        - Scan all memories from the day
        - Calculate phi weights
        - Identify promotion candidates
        """
        # Get memories from buffer
        buffer_memories = await self.buffer.get_recent_memories(
            limit=MAX_MEMORIES_PER_PHASE
        )

        # Analyze each memory
        total_importance = 0.0
        promotion_candidates = []

        for memory in buffer_memories:
            self._current_report.memories_analyzed += 1

            # Calculate importance
            importance = self.phi_calculator.calculate_importance(memory)
            total_importance += importance

            # Check promotion candidacy
            should_promote, reason = self.phi_calculator.should_promote(memory)
            if should_promote:
                memory.promotion_candidate = True
                promotion_candidates.append(memory.id)

        # Update report
        if buffer_memories:
            self._current_report.average_phi_alignment = total_importance / len(buffer_memories)

        logger.info(
            f"Analysis complete: {len(buffer_memories)} memories, "
            f"{len(promotion_candidates)} promotion candidates"
        )

    async def _phase_extraction(self) -> None:
        """
        Phase 2: Extraction (01:00-02:30)
        - Extract recurring patterns
        - Semantic clustering
        - Generate summaries
        """
        # Get memories from buffer and fractal
        buffer_memories = await self.buffer.get_recent_memories(limit=200)

        # Simple pattern extraction (keyword-based)
        keyword_patterns = self._extract_keyword_patterns(buffer_memories)
        emotional_patterns = self._extract_emotional_patterns(buffer_memories)

        # Store patterns
        for pattern in keyword_patterns + emotional_patterns:
            self._current_report.patterns_extracted += 1
            self._current_report.extracted_patterns.append(pattern.to_dict())

        logger.info(f"Extraction complete: {self._current_report.patterns_extracted} patterns")

    async def _phase_consolidation(self) -> None:
        """
        Phase 3: Consolidation (02:30-04:00)
        - Transfer to Pure Memory archive
        - Encrypt experiences
        - Update phi indices
        """
        # Get candidates from buffer for fractal
        buffer_candidates = await self.buffer.get_candidates_for_fractal(
            min_importance=MIN_IMPORTANCE_FOR_FRACTAL
        )

        # Transfer buffer -> fractal
        transferred_to_fractal = []
        for memory in buffer_candidates[:MAX_MEMORIES_PER_PHASE]:
            try:
                await self.fractal.store(memory)
                transferred_to_fractal.append(memory.id)
                self._current_report.memories_consolidated += 1
            except Exception as e:
                self._current_report.errors.append(f"Fractal transfer failed: {e}")

        # Mark as transferred in buffer
        await self.buffer.mark_as_flushed(transferred_to_fractal)

        # Get high-importance memories from fractal for archive
        from .memory_types import MemoryQuery
        high_importance_query = MemoryQuery(
            min_phi_resonance=MIN_IMPORTANCE_FOR_ARCHIVE,
            limit=100
        )

        fractal_candidates = await self.fractal.search(high_importance_query)

        # Transfer fractal -> archive (only roots and high-value branches)
        for memory in fractal_candidates:
            if memory.memory_type in [MemoryType.ROOT, MemoryType.BRANCH]:
                if memory.phi_metrics.calculate_importance() >= MIN_IMPORTANCE_FOR_ARCHIVE:
                    try:
                        await self.archive.archive(memory)
                        self._current_report.memories_consolidated += 1
                    except Exception as e:
                        self._current_report.errors.append(f"Archive failed: {e}")

        logger.info(f"Consolidation complete: {self._current_report.memories_consolidated} memories")

    async def _phase_promotion(self) -> None:
        """
        Phase 4: Promotion (04:00-04:30)
        - Promote deserving memories
        - seed -> leaf -> branch -> root
        - Update connections
        """
        # Get promotion candidates from fractal
        from .memory_types import MemoryQuery

        # Check seeds first
        for memory_type in [MemoryType.SEED, MemoryType.LEAF, MemoryType.BRANCH]:
            query = MemoryQuery(
                memory_types=[memory_type],
                limit=50
            )

            candidates = await self.fractal.search(query)

            for memory in candidates:
                if memory.promotion_candidate or memory.should_promote():
                    promoted = await self.fractal.promote(memory.id)

                    if promoted:
                        self._current_report.memories_promoted += 1
                        self._current_report.promoted_memories.append(memory.id)

        logger.info(f"Promotion complete: {self._current_report.memories_promoted} memories promoted")

    async def _phase_cleanup(self) -> None:
        """
        Phase 5: Cleanup (04:30-05:00)
        - Remove expired memories
        - Compress archives
        - Verify integrity
        """
        # Cleanup fractal expired memories
        cleaned = await self.fractal.cleanup_expired()
        self._current_report.memories_cleaned += cleaned

        # Calculate phi improvement
        buffer_stats = self.buffer.get_stats()
        fractal_stats = self.fractal.get_stats()

        current_phi = (
            buffer_stats["phi_metrics"]["average_importance"] +
            fractal_stats.get("phi_alignment", 0)
        ) / 2

        if self._consolidation_history:
            last_phi = self._consolidation_history[-1].average_phi_alignment
            self._current_report.total_phi_improvement = current_phi - last_phi

        logger.info(f"Cleanup complete: {self._current_report.memories_cleaned} memories removed")

    # =========================================================================
    # PATTERN EXTRACTION HELPERS
    # =========================================================================

    def _extract_keyword_patterns(
        self,
        memories: List[MemoryExperience]
    ) -> List[ExtractedPattern]:
        """Extract keyword-based patterns."""
        import uuid

        # Collect all keywords
        keyword_memories: Dict[str, List[str]] = {}

        for memory in memories:
            for keyword in memory.keywords:
                if keyword not in keyword_memories:
                    keyword_memories[keyword] = []
                keyword_memories[keyword].append(memory.id)

        # Find patterns (keywords appearing in multiple memories)
        patterns = []
        for keyword, memory_ids in keyword_memories.items():
            if len(memory_ids) >= 3:  # At least 3 memories
                patterns.append(ExtractedPattern(
                    pattern_id=f"kw_{uuid.uuid4().hex[:8]}",
                    pattern_type="semantic",
                    description=f"Recurring topic: {keyword}",
                    memory_ids=memory_ids,
                    phi_resonance=len(memory_ids) / len(memories),
                    confidence=min(1.0, len(memory_ids) / 10)
                ))

        return patterns[:20]  # Limit patterns

    def _extract_emotional_patterns(
        self,
        memories: List[MemoryExperience]
    ) -> List[ExtractedPattern]:
        """Extract emotional patterns."""
        import uuid

        # Group by primary emotion
        emotion_memories: Dict[str, List[str]] = {}

        for memory in memories:
            emotion = memory.emotional_context.primary_emotion.value
            if emotion not in emotion_memories:
                emotion_memories[emotion] = []
            emotion_memories[emotion].append(memory.id)

        patterns = []
        for emotion, memory_ids in emotion_memories.items():
            if len(memory_ids) >= 3:
                patterns.append(ExtractedPattern(
                    pattern_id=f"em_{uuid.uuid4().hex[:8]}",
                    pattern_type="emotional",
                    description=f"Emotional thread: {emotion}",
                    memory_ids=memory_ids,
                    phi_resonance=len(memory_ids) / len(memories),
                    confidence=min(1.0, len(memory_ids) / 10)
                ))

        return patterns[:10]

    # =========================================================================
    # SCHEDULING
    # =========================================================================

    def is_consolidation_time(self) -> bool:
        """Check if current time is within consolidation window."""
        now = datetime.now().time()
        start = time(0, 0)  # 00:00
        end = time(5, 0)    # 05:00

        return start <= now <= end

    def get_current_phase_by_time(self) -> ConsolidationPhase:
        """Get the phase that should be running based on current time."""
        now = datetime.now().time()

        for phase, (hour, minute) in reversed(list(CONSOLIDATION_SCHEDULE.items())):
            phase_time = time(hour, minute)
            if now >= phase_time:
                return phase

        return ConsolidationPhase.ANALYSIS

    async def schedule_next_consolidation(self) -> Optional[datetime]:
        """Calculate when the next consolidation should run."""
        now = datetime.now()
        today_start = datetime.combine(now.date(), time(0, 0))

        if now.time() < time(5, 0):
            # Before 5 AM - run tonight
            return today_start
        else:
            # After 5 AM - run tomorrow
            return today_start + timedelta(days=1)

    # =========================================================================
    # MANUAL TRIGGERS
    # =========================================================================

    async def trigger_manual_consolidation(
        self,
        phase: Optional[ConsolidationPhase] = None
    ) -> ConsolidationReport:
        """
        Trigger a manual consolidation.

        Args:
            phase: Specific phase to run (or all if None)

        Returns:
            ConsolidationReport
        """
        if phase:
            # Run single phase
            self._current_report = ConsolidationReport()
            await self._run_phase(phase)
            self._current_report.complete()
            return self._current_report
        else:
            # Run full cycle
            return await self.run_consolidation_cycle(force=True)

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def register_phase_callback(
        self,
        phase: ConsolidationPhase,
        callback: Callable
    ) -> None:
        """Register a callback for a specific phase."""
        self._phase_callbacks[phase].append(callback)

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get consolidation statistics."""
        return {
            "is_running": self._is_running,
            "current_phase": self._current_phase.value,
            "total_cycles": len(self._consolidation_history),
            "last_report": self._current_report.to_dict() if self._current_report else None,
            "history_summary": [
                {
                    "cycle_id": r.cycle_id,
                    "memories_consolidated": r.memories_consolidated,
                    "memories_promoted": r.memories_promoted,
                    "duration_seconds": r.duration_seconds()
                }
                for r in self._consolidation_history[-10:]
            ],
            "schedule": {
                phase.value: f"{h:02d}:{m:02d}"
                for phase, (h, m) in CONSOLIDATION_SCHEDULE.items()
            },
            "is_consolidation_time": self.is_consolidation_time()
        }

    def get_last_report(self) -> Optional[ConsolidationReport]:
        """Get the most recent consolidation report."""
        if self._consolidation_history:
            return self._consolidation_history[-1]
        return None


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_consolidation_engine(
    buffer: MemoryBuffer,
    fractal: FractalMemory,
    archive: ArchiveManager
) -> ConsolidationEngine:
    """
    Factory function to create a ConsolidationEngine.

    Args:
        buffer: Memory buffer layer
        fractal: Fractal memory layer
        archive: Archive layer

    Returns:
        Configured ConsolidationEngine instance
    """
    return ConsolidationEngine(
        buffer=buffer,
        fractal=fractal,
        archive=archive
    )
