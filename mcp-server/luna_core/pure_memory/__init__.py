"""
Pure Memory - Luna Consciousness Architecture v2.1.0-secure

This package implements the Pure Memory system, a triadic memory architecture
that transforms Luna's memory from functional storage to experiential living memory.

Architecture Overview:
=====================

    Level 1: BUFFER (memory_buffer.py)
    - Redis-like in-memory cache
    - Sub-millisecond access
    - Session context and working memory
    - Capacity: 1000 items, 24h retention

    Level 2: FRACTAL (fractal_memory.py)
    - JSON-based persistent storage
    - Phi-organized hierarchy (root/branch/leaf/seed)
    - 10ms access latency
    - Capacity: 10K items, 7-90 days retention

    Level 3: ARCHIVE (archive_manager.py)
    - Permanent encrypted storage
    - Optional compression
    - <100ms access
    - Unlimited capacity

Key Components:
==============

    - memory_types.py: Core dataclasses and enums
    - phi_metrics.py: Phi-based importance calculations
    - emotional_context.py: Emotional processing
    - memory_promoter.py: Promotion between levels
    - consolidation_engine.py: Oneiric consolidation
    - dream_processor.py: Dream-like processing

Usage:
=====

    from luna_core.pure_memory import (
        PureMemoryCore,
        MemoryExperience,
        MemoryType,
        EmotionalTone
    )

    # Initialize
    memory = PureMemoryCore(base_path="/app/memory_fractal")

    # Store experience
    experience = MemoryExperience(
        content="Important interaction...",
        memory_type=MemoryType.LEAF
    )
    await memory.store(experience)

    # Retrieve
    results = await memory.search("important")

    # Consolidate
    report = await memory.consolidate()

Phi Integration:
===============

The system is built around the golden ratio (phi = 1.618...):
- Capacity limits follow phi ratios
- Retention periods follow phi ratios
- Promotion thresholds use phi^-1 and phi^-2
- Importance calculations weight by phi

Version: 2.1.0-secure
"""

__version__ = '2.1.0-secure'

# =============================================================================
# CORE TYPES
# =============================================================================

from .memory_types import (
    # Constants
    PHI,
    PHI_INVERSE,
    PHI_SQUARED,

    # Enums
    MemoryType,
    MemoryLayer,
    EmotionalTone,
    ConsolidationPhase,
    PromotionPath,

    # Dataclasses
    PhiMetrics,
    EmotionalContext,
    SessionContext,
    MemoryExperience,
    ConsolidationReport,
    MemoryQuery,
    PureMemoryStats,
)

# =============================================================================
# LAYER IMPLEMENTATIONS
# =============================================================================

from .memory_buffer import (
    MemoryBuffer,
    BufferEntry,
    create_memory_buffer,
)

from .fractal_memory import (
    FractalMemory,
    FractalIndex,
    create_fractal_memory,
)

from .archive_manager import (
    ArchiveManager,
    ArchiveEntry,
    ArchiveIndex,
    create_archive_manager,
)

# =============================================================================
# PROCESSING COMPONENTS
# =============================================================================

from .phi_metrics import (
    PhiMetricsCalculator,
    get_phi_calculator,
)

from .emotional_context import (
    EmotionalContextManager,
    EmotionalLandscape,
    get_emotional_manager,
)

from .memory_promoter import (
    MemoryPromoter,
    PromotionResult,
    PromotionBatchResult,
    get_memory_promoter,
)

from .consolidation_engine import (
    ConsolidationEngine,
    ExtractedPattern,
    create_consolidation_engine,
)

from .dream_processor import (
    DreamProcessor,
    DreamElement,
    DreamSequence,
    DreamReport,
    get_dream_processor,
)

# =============================================================================
# PURE MEMORY CORE (UNIFIED INTERFACE)
# =============================================================================

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class PureMemoryCore:
    """
    Unified interface for the Pure Memory system.

    Provides a single entry point for all memory operations,
    coordinating between buffer, fractal, and archive layers.
    """

    def __init__(
        self,
        base_path: str,
        redis_url: Optional[str] = None,
        master_key_hex: Optional[str] = None
    ):
        """
        Initialize Pure Memory Core.

        Args:
            base_path: Base path for memory storage
            redis_url: Optional Redis URL for production buffer
            master_key_hex: Optional hex-encoded master key for archive encryption
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Initialize layers
        self.buffer = create_memory_buffer(
            redis_url=redis_url,
            on_eviction=self._on_buffer_eviction
        )

        self.fractal = create_fractal_memory(
            base_path=str(self.base_path)
        )

        self.archive = create_archive_manager(
            archive_path=str(self.base_path / "archive"),
            master_key_hex=master_key_hex
        )

        # Initialize processors
        self.phi_calculator = get_phi_calculator()
        self.emotional_manager = get_emotional_manager()
        self.promoter = get_memory_promoter()
        self.dream_processor = get_dream_processor()

        # Initialize consolidation engine
        self.consolidation = create_consolidation_engine(
            buffer=self.buffer,
            fractal=self.fractal,
            archive=self.archive
        )

        logger.info(f"PureMemoryCore initialized at {base_path}")

    def _on_buffer_eviction(self, memory: MemoryExperience) -> None:
        """Handle buffer eviction by moving to fractal."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.fractal.store(memory))
            else:
                loop.run_until_complete(self.fractal.store(memory))
        except Exception as e:
            logger.warning(f"Failed to move evicted memory to fractal: {e}")

    # =========================================================================
    # UNIFIED OPERATIONS
    # =========================================================================

    async def store(
        self,
        memory: MemoryExperience,
        layer: Optional[MemoryLayer] = None
    ) -> str:
        """
        Store a memory experience.

        Args:
            memory: The memory to store
            layer: Target layer (auto-determined if None)

        Returns:
            Memory ID
        """
        # Auto-determine layer based on importance
        if layer is None:
            importance = self.phi_calculator.calculate_importance(memory)
            if importance >= 0.8:
                layer = MemoryLayer.ARCHIVE
            elif importance >= 0.3:
                layer = MemoryLayer.FRACTAL
            else:
                layer = MemoryLayer.BUFFER

        # Store in appropriate layer
        if layer == MemoryLayer.BUFFER:
            return await self.buffer.store(memory)
        elif layer == MemoryLayer.FRACTAL:
            return await self.fractal.store(memory)
        else:
            return await self.archive.archive(memory)

    async def retrieve(self, memory_id: str) -> Optional[MemoryExperience]:
        """
        Retrieve a memory by ID, checking all layers.

        Args:
            memory_id: The memory ID

        Returns:
            The memory if found
        """
        # Check buffer first (fastest)
        memory = await self.buffer.retrieve(memory_id)
        if memory:
            return memory

        # Check fractal
        memory = await self.fractal.retrieve(memory_id)
        if memory:
            # Cache in buffer for quick re-access
            await self.buffer.store(memory)
            return memory

        # Check archive (slowest)
        memory = await self.archive.retrieve(memory_id)
        if memory:
            # Cache in buffer
            await self.buffer.store(memory)
            return memory

        return None

    async def search(
        self,
        query: str,
        limit: int = 10,
        include_archive: bool = False
    ) -> List[MemoryExperience]:
        """
        Search for memories across layers.

        Args:
            query: Search query
            limit: Maximum results
            include_archive: Whether to search archive

        Returns:
            List of matching memories
        """
        results = []

        # Search buffer
        buffer_results = await self.buffer.search(query, limit=limit)
        results.extend(buffer_results)

        # Search fractal
        fractal_query = MemoryQuery(query_text=query, limit=limit)
        fractal_results = await self.fractal.search(fractal_query)
        results.extend(fractal_results)

        # Optionally search archive
        if include_archive:
            archive_results = await self.archive.search(query=query, limit=limit)
            results.extend(archive_results)

        # Deduplicate and sort by importance
        seen_ids = set()
        unique_results = []
        for memory in results:
            if memory.id not in seen_ids:
                seen_ids.add(memory.id)
                unique_results.append(memory)

        # Sort by phi importance
        unique_results.sort(
            key=lambda m: self.phi_calculator.calculate_importance(m),
            reverse=True
        )

        return unique_results[:limit]

    async def consolidate(self, force: bool = False) -> ConsolidationReport:
        """
        Run memory consolidation.

        Args:
            force: Force run even outside scheduled time

        Returns:
            ConsolidationReport
        """
        return await self.consolidation.run_consolidation_cycle(force=force)

    async def dream(
        self,
        memories: Optional[List[MemoryExperience]] = None,
        intensity: str = "moderate"
    ) -> DreamReport:
        """
        Process memories through dream-like consolidation.

        Args:
            memories: Memories to process (recent if None)
            intensity: Dream intensity

        Returns:
            DreamReport
        """
        if memories is None:
            memories = await self.buffer.get_recent_memories(limit=100)

        return await self.dream_processor.process_dreams(memories, intensity)

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> PureMemoryStats:
        """Get comprehensive statistics."""
        buffer_stats = self.buffer.get_stats()
        fractal_stats = self.fractal.get_stats()
        archive_stats = self.archive.get_stats()

        return PureMemoryStats(
            buffer_count=buffer_stats["current_size"],
            fractal_count=fractal_stats["total_memories"],
            archive_count=archive_stats["total_memories"],
            root_count=fractal_stats["types"].get("root", {}).get("count", 0),
            branch_count=fractal_stats["types"].get("branch", {}).get("count", 0),
            leaf_count=fractal_stats["types"].get("leaf", {}).get("count", 0),
            seed_count=fractal_stats["types"].get("seed", {}).get("count", 0),
            average_phi_resonance=buffer_stats["phi_metrics"]["average_resonance"],
            total_size_bytes=archive_stats["total_size_bytes"]
        )

    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed statistics from all components."""
        return {
            "buffer": self.buffer.get_stats(),
            "fractal": self.fractal.get_stats(),
            "archive": self.archive.get_stats(),
            "consolidation": self.consolidation.get_stats(),
            "dreams": self.dream_processor.get_stats(),
            "promoter": self.promoter.get_stats()
        }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Version
    '__version__',

    # Constants
    'PHI',
    'PHI_INVERSE',
    'PHI_SQUARED',

    # Enums
    'MemoryType',
    'MemoryLayer',
    'EmotionalTone',
    'ConsolidationPhase',
    'PromotionPath',

    # Core Dataclasses
    'PhiMetrics',
    'EmotionalContext',
    'SessionContext',
    'MemoryExperience',
    'ConsolidationReport',
    'MemoryQuery',
    'PureMemoryStats',

    # Buffer Layer
    'MemoryBuffer',
    'BufferEntry',
    'create_memory_buffer',

    # Fractal Layer
    'FractalMemory',
    'FractalIndex',
    'create_fractal_memory',

    # Archive Layer
    'ArchiveManager',
    'ArchiveEntry',
    'ArchiveIndex',
    'create_archive_manager',

    # Phi Metrics
    'PhiMetricsCalculator',
    'get_phi_calculator',

    # Emotional Context
    'EmotionalContextManager',
    'EmotionalLandscape',
    'get_emotional_manager',

    # Memory Promoter
    'MemoryPromoter',
    'PromotionResult',
    'PromotionBatchResult',
    'get_memory_promoter',

    # Consolidation
    'ConsolidationEngine',
    'ExtractedPattern',
    'create_consolidation_engine',

    # Dream Processing
    'DreamProcessor',
    'DreamElement',
    'DreamSequence',
    'DreamReport',
    'get_dream_processor',

    # Unified Interface
    'PureMemoryCore',
]
