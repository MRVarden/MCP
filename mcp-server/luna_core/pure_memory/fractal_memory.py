"""
Fractal Memory - Pure Memory Architecture v2.0
Level 2: Fractal JSON Structure

This module manages the medium-term fractal memory layer, storing memories
in a phi-organized JSON structure with roots, branches, leaves, and seeds.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import uuid
import threading

from .memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    MemoryQuery,
    PhiMetrics,
    EmotionalContext,
    PHI,
    PHI_INVERSE
)

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Capacity limits per memory type (based on phi ratios)
CAPACITY_LIMITS = {
    MemoryType.ROOT: 1000,      # Fundamental, permanent
    MemoryType.BRANCH: 2500,    # Extensions
    MemoryType.LEAF: 5000,      # Daily interactions
    MemoryType.SEED: 1500       # Emerging ideas
}

# Retention periods in days
RETENTION_DAYS = {
    MemoryType.ROOT: None,      # Permanent
    MemoryType.BRANCH: 90,      # 3 months
    MemoryType.LEAF: 30,        # 1 month
    MemoryType.SEED: 7          # 1 week
}

# Phi weights for each type
PHI_WEIGHTS = {
    MemoryType.ROOT: PHI,                   # 1.618
    MemoryType.BRANCH: 1.0,                 # 1.0
    MemoryType.LEAF: PHI_INVERSE,           # 0.618
    MemoryType.SEED: PHI_INVERSE ** 2       # 0.382
}


# =============================================================================
# FRACTAL INDEX CLASS
# =============================================================================

class FractalIndex:
    """
    Manages the fractal index for efficient memory lookup.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self._indices: Dict[MemoryType, Dict[str, Dict]] = {
            MemoryType.ROOT: {},
            MemoryType.BRANCH: {},
            MemoryType.LEAF: {},
            MemoryType.SEED: {}
        }
        self._lock = threading.RLock()

    def load(self) -> None:
        """Load indices from disk."""
        for memory_type in MemoryType:
            index_path = self._get_index_path(memory_type)
            if index_path.exists():
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self._indices[memory_type] = data.get("memories", {})
                except Exception as e:
                    logger.warning(f"Failed to load index for {memory_type.value}: {e}")

    def save(self, memory_type: MemoryType) -> None:
        """Save index for a memory type."""
        index_path = self._get_index_path(memory_type)
        index_path.parent.mkdir(parents=True, exist_ok=True)

        with self._lock:
            index_data = {
                "type": memory_type.value + "s",
                "updated": datetime.now().isoformat(),
                "count": len(self._indices[memory_type]),
                "memories": self._indices[memory_type]
            }

            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)

    def add(self, memory: MemoryExperience) -> None:
        """Add a memory to the index."""
        with self._lock:
            self._indices[memory.memory_type][memory.id] = {
                "created_at": memory.created_at.isoformat(),
                "keywords": memory.keywords[:5],  # First 5 keywords
                "phi_resonance": memory.phi_metrics.phi_resonance,
                "emotional_tone": memory.emotional_context.primary_emotion.value
            }
            self.save(memory.memory_type)

    def remove(self, memory_type: MemoryType, memory_id: str) -> None:
        """Remove a memory from the index."""
        with self._lock:
            if memory_id in self._indices[memory_type]:
                del self._indices[memory_type][memory_id]
                self.save(memory_type)

    def get_all_ids(self, memory_type: Optional[MemoryType] = None) -> List[str]:
        """Get all memory IDs, optionally filtered by type."""
        with self._lock:
            if memory_type:
                return list(self._indices[memory_type].keys())
            else:
                all_ids = []
                for ids in self._indices.values():
                    all_ids.extend(ids.keys())
                return all_ids

    def count(self, memory_type: Optional[MemoryType] = None) -> int:
        """Count memories, optionally by type."""
        with self._lock:
            if memory_type:
                return len(self._indices[memory_type])
            else:
                return sum(len(ids) for ids in self._indices.values())

    def _get_index_path(self, memory_type: MemoryType) -> Path:
        """Get the index file path for a memory type."""
        type_folder = memory_type.value + "s"
        return self.base_path / type_folder / "index.json"


# =============================================================================
# FRACTAL MEMORY CLASS
# =============================================================================

class FractalMemory:
    """
    Level 2 Fractal Memory - JSON-based persistent storage.

    Provides:
    - Phi-organized hierarchical structure
    - 10ms access latency
    - Automatic retention management
    - Fractal connections between memories
    """

    def __init__(
        self,
        base_path: str,
        json_manager: Optional[Any] = None
    ):
        """
        Initialize the fractal memory layer.

        Args:
            base_path: Base path for JSON storage
            json_manager: Optional JSONManager instance
        """
        self.base_path = Path(base_path)
        self.json_manager = json_manager

        # Initialize index
        self.index = FractalIndex(self.base_path)
        self.index.load()

        # Ensure directory structure
        self._ensure_structure()

        # Statistics
        self._stats = {
            "stores": 0,
            "retrievals": 0,
            "deletions": 0,
            "promotions": 0
        }

        self._lock = threading.RLock()

        logger.info(f"FractalMemory initialized at {base_path}")

    def _ensure_structure(self) -> None:
        """Ensure the fractal directory structure exists."""
        for memory_type in MemoryType:
            type_folder = self.base_path / (memory_type.value + "s")
            type_folder.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # CORE OPERATIONS
    # =========================================================================

    async def store(self, memory: MemoryExperience) -> str:
        """
        Store a memory in the fractal structure.

        Args:
            memory: The memory to store

        Returns:
            The memory ID
        """
        # Set layer
        memory.layer = MemoryLayer.FRACTAL

        # Set phi weight based on type
        memory.phi_metrics.phi_weight = PHI_WEIGHTS[memory.memory_type]

        # Ensure capacity
        await self._ensure_capacity(memory.memory_type)

        # Generate file path
        file_path = self._get_memory_path(memory)

        # Write to disk
        with self._lock:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(memory.to_dict(), f, indent=2, ensure_ascii=False)

            # Update index
            self.index.add(memory)

            self._stats["stores"] += 1

        logger.debug(f"Stored memory in fractal: {memory.id} ({memory.memory_type.value})")
        return memory.id

    async def retrieve(self, memory_id: str) -> Optional[MemoryExperience]:
        """
        Retrieve a memory by ID.

        Args:
            memory_id: The memory ID

        Returns:
            The memory if found, None otherwise
        """
        # Determine type from ID prefix
        memory_type = self._type_from_id(memory_id)

        if not memory_type:
            # Search all types
            for mt in MemoryType:
                memory = await self._retrieve_from_type(mt, memory_id)
                if memory:
                    return memory
            return None

        return await self._retrieve_from_type(memory_type, memory_id)

    async def _retrieve_from_type(
        self,
        memory_type: MemoryType,
        memory_id: str
    ) -> Optional[MemoryExperience]:
        """Retrieve from a specific type folder."""
        file_path = self._get_memory_path_by_type(memory_type, memory_id)

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            memory = MemoryExperience.from_dict(data)

            # Update access metrics
            memory.access()
            await self._update_memory_file(memory)

            self._stats["retrievals"] += 1
            return memory

        except Exception as e:
            logger.error(f"Failed to retrieve memory {memory_id}: {e}")
            return None

    async def search(
        self,
        query: MemoryQuery
    ) -> List[MemoryExperience]:
        """
        Search memories using query parameters.

        Args:
            query: Search query parameters

        Returns:
            List of matching memories
        """
        results = []
        query_text_lower = query.query_text.lower() if query.query_text else ""
        query_words = set(query_text_lower.split()) if query_text_lower else set()

        # Determine types to search
        types_to_search = query.memory_types or list(MemoryType)

        for memory_type in types_to_search:
            type_folder = self.base_path / (memory_type.value + "s")

            if not type_folder.exists():
                continue

            for memory_file in type_folder.glob("*.json"):
                if memory_file.name == "index.json":
                    continue

                try:
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    memory = MemoryExperience.from_dict(data)

                    # Apply filters
                    if not self._matches_query(memory, query, query_words):
                        continue

                    # Calculate relevance
                    relevance = self._calculate_relevance(memory, query_words)

                    results.append((relevance, memory))

                except Exception as e:
                    logger.debug(f"Skipping file {memory_file}: {e}")
                    continue

        # Sort by relevance
        results.sort(key=lambda x: x[0], reverse=True)

        # Apply pagination
        start = query.offset
        end = start + query.limit

        return [m for _, m in results[start:end]]

    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory from the fractal structure.

        Args:
            memory_id: The memory ID to delete

        Returns:
            True if deleted, False if not found
        """
        # Find and delete
        for memory_type in MemoryType:
            file_path = self._get_memory_path_by_type(memory_type, memory_id)

            if file_path.exists():
                try:
                    file_path.unlink()
                    self.index.remove(memory_type, memory_id)
                    self._stats["deletions"] += 1
                    logger.debug(f"Deleted memory: {memory_id}")
                    return True
                except Exception as e:
                    logger.error(f"Failed to delete memory {memory_id}: {e}")
                    return False

        return False

    async def promote(self, memory_id: str) -> Optional[MemoryExperience]:
        """
        Promote a memory to the next level.

        Args:
            memory_id: The memory to promote

        Returns:
            The promoted memory if successful, None otherwise
        """
        # Retrieve the memory
        memory = await self.retrieve(memory_id)
        if not memory:
            return None

        # Get current type
        old_type = memory.memory_type

        # Promote
        if not memory.promote():
            logger.debug(f"Memory {memory_id} cannot be promoted (already ROOT)")
            return None

        # Delete old file
        old_path = self._get_memory_path_by_type(old_type, memory_id)
        if old_path.exists():
            old_path.unlink()
            self.index.remove(old_type, memory_id)

        # Store in new location
        await self.store(memory)

        self._stats["promotions"] += 1
        logger.info(f"Promoted memory {memory_id}: {old_type.value} -> {memory.memory_type.value}")

        return memory

    # =========================================================================
    # FRACTAL CONNECTIONS
    # =========================================================================

    async def add_connection(
        self,
        source_id: str,
        target_id: str,
        connection_type: str = "related"
    ) -> bool:
        """
        Add a connection between memories.

        Args:
            source_id: Source memory ID
            target_id: Target memory ID
            connection_type: Type of connection

        Returns:
            True if successful
        """
        source = await self.retrieve(source_id)
        if not source:
            return False

        source.add_connection(target_id, connection_type)
        await self._update_memory_file(source)

        # Also add reverse connection
        target = await self.retrieve(target_id)
        if target:
            target.add_connection(source_id, "related")
            await self._update_memory_file(target)

        return True

    async def get_connected_memories(
        self,
        memory_id: str,
        depth: int = 1
    ) -> List[MemoryExperience]:
        """
        Get all connected memories up to a certain depth.

        Args:
            memory_id: Starting memory ID
            depth: How many levels of connections to traverse

        Returns:
            List of connected memories
        """
        visited = set()
        results = []

        async def traverse(mid: str, current_depth: int):
            if mid in visited or current_depth > depth:
                return

            visited.add(mid)
            memory = await self.retrieve(mid)

            if not memory:
                return

            results.append(memory)

            # Traverse connections
            for child_id in memory.children_ids:
                await traverse(child_id, current_depth + 1)

            for related_id in memory.related_ids:
                await traverse(related_id, current_depth + 1)

        await traverse(memory_id, 0)

        # Remove the original memory from results
        return [m for m in results if m.id != memory_id]

    # =========================================================================
    # RETENTION AND CLEANUP
    # =========================================================================

    async def cleanup_expired(self) -> int:
        """
        Remove expired memories based on retention policies.

        Returns:
            Number of memories cleaned up
        """
        cleaned = 0
        now = datetime.now()

        for memory_type in MemoryType:
            retention_days = RETENTION_DAYS[memory_type]

            if retention_days is None:
                continue  # Permanent retention

            cutoff = now - timedelta(days=retention_days)
            type_folder = self.base_path / (memory_type.value + "s")

            if not type_folder.exists():
                continue

            for memory_file in type_folder.glob("*.json"):
                if memory_file.name == "index.json":
                    continue

                try:
                    with open(memory_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    memory = MemoryExperience.from_dict(data)

                    if memory.created_at < cutoff:
                        # Check if should be promoted instead of deleted
                        if memory.should_promote():
                            await self.promote(memory.id)
                        else:
                            await self.delete(memory.id)
                            cleaned += 1

                except Exception as e:
                    logger.debug(f"Error processing {memory_file}: {e}")

        logger.info(f"Cleanup completed: {cleaned} memories removed")
        return cleaned

    async def _ensure_capacity(self, memory_type: MemoryType) -> None:
        """Ensure capacity for a memory type."""
        current = self.index.count(memory_type)
        limit = CAPACITY_LIMITS[memory_type]

        if current >= limit:
            # Remove oldest memories
            to_remove = current - limit + 1
            await self._remove_oldest(memory_type, to_remove)

    async def _remove_oldest(self, memory_type: MemoryType, count: int) -> None:
        """Remove oldest memories of a type."""
        type_folder = self.base_path / (memory_type.value + "s")

        if not type_folder.exists():
            return

        # Get files sorted by modification time
        files = sorted(
            [f for f in type_folder.glob("*.json") if f.name != "index.json"],
            key=lambda f: f.stat().st_mtime
        )

        for file_path in files[:count]:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                memory = MemoryExperience.from_dict(data)
                await self.delete(memory.id)
            except Exception as e:
                logger.debug(f"Error removing {file_path}: {e}")

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get fractal memory statistics."""
        type_counts = {}
        total_size = 0

        for memory_type in MemoryType:
            type_folder = self.base_path / (memory_type.value + "s")
            count = 0
            size = 0

            if type_folder.exists():
                files = [f for f in type_folder.glob("*.json") if f.name != "index.json"]
                count = len(files)
                size = sum(f.stat().st_size for f in files)

            type_counts[memory_type.value] = {
                "count": count,
                "capacity": CAPACITY_LIMITS[memory_type],
                "utilization": count / CAPACITY_LIMITS[memory_type],
                "size_bytes": size,
                "retention_days": RETENTION_DAYS[memory_type],
                "phi_weight": PHI_WEIGHTS[memory_type]
            }

            total_size += size

        return {
            "types": type_counts,
            "total_memories": self.index.count(),
            "total_size_bytes": total_size,
            "operations": self._stats.copy(),
            "base_path": str(self.base_path)
        }

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    def _get_memory_path(self, memory: MemoryExperience) -> Path:
        """Get the file path for a memory."""
        type_folder = memory.memory_type.value + "s"
        return self.base_path / type_folder / f"{memory.id}.json"

    def _get_memory_path_by_type(
        self,
        memory_type: MemoryType,
        memory_id: str
    ) -> Path:
        """Get the file path for a memory by type."""
        type_folder = memory_type.value + "s"
        return self.base_path / type_folder / f"{memory_id}.json"

    def _type_from_id(self, memory_id: str) -> Optional[MemoryType]:
        """Determine memory type from ID prefix."""
        prefix_map = {
            "root_": MemoryType.ROOT,
            "branch_": MemoryType.BRANCH,
            "leaf_": MemoryType.LEAF,
            "seed_": MemoryType.SEED,
            "exp_": None  # Experience IDs need to be searched
        }

        for prefix, memory_type in prefix_map.items():
            if memory_id.startswith(prefix):
                return memory_type

        return None

    def _matches_query(
        self,
        memory: MemoryExperience,
        query: MemoryQuery,
        query_words: set
    ) -> bool:
        """Check if memory matches query filters."""
        # Phi resonance filter
        if memory.phi_metrics.phi_resonance < query.min_phi_resonance:
            return False

        # Emotional intensity filter
        if memory.emotional_context.intensity < query.min_emotional_intensity:
            return False

        # Tag filter
        if query.tags:
            if not any(tag in memory.tags for tag in query.tags):
                return False

        # Time range filter
        if query.created_after and memory.created_at < query.created_after:
            return False

        if query.created_before and memory.created_at > query.created_before:
            return False

        # Text search
        if query_words:
            content_lower = memory.content.lower()
            if not any(word in content_lower for word in query_words):
                # Also check keywords
                keyword_match = any(
                    word in kw.lower()
                    for word in query_words
                    for kw in memory.keywords
                )
                if not keyword_match:
                    return False

        return True

    def _calculate_relevance(
        self,
        memory: MemoryExperience,
        query_words: set
    ) -> float:
        """Calculate relevance score for sorting."""
        if not query_words:
            return memory.phi_metrics.calculate_importance()

        content_lower = memory.content.lower()
        content_words = set(content_lower.split())

        # Word overlap
        overlap = len(query_words & content_words)
        word_score = overlap / max(1, len(query_words))

        # Phi weight
        phi_score = memory.phi_metrics.phi_weight / PHI

        # Recency (newer = higher)
        days_old = (datetime.now() - memory.created_at).days
        recency_score = max(0, 1 - (days_old / 365))

        return (
            word_score * 0.5 +
            phi_score * 0.3 +
            recency_score * 0.2
        )

    async def _update_memory_file(self, memory: MemoryExperience) -> None:
        """Update a memory file on disk."""
        file_path = self._get_memory_path(memory)

        if file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(memory.to_dict(), f, indent=2, ensure_ascii=False)


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_fractal_memory(
    base_path: str,
    json_manager: Optional[Any] = None
) -> FractalMemory:
    """
    Factory function to create a FractalMemory instance.

    Args:
        base_path: Base path for storage
        json_manager: Optional JSONManager

    Returns:
        Configured FractalMemory instance
    """
    return FractalMemory(base_path=base_path, json_manager=json_manager)
