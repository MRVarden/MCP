"""
Memory Buffer - Pure Memory Architecture v2.0
Level 1: Experiential Buffer (Redis-like in-memory cache)

This module provides the immediate memory layer with sub-millisecond access.
Acts as a Redis-compatible buffer for session context and working memory.
"""

import asyncio
import logging
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, field
import json
import hashlib
import threading

from .memory_types import (
    MemoryExperience,
    MemoryType,
    MemoryLayer,
    PhiMetrics,
    EmotionalContext,
    PHI,
    PHI_INVERSE
)

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

DEFAULT_BUFFER_CAPACITY = 1000  # Maximum items
DEFAULT_TTL_HOURS = 24          # Default time-to-live
FLUSH_THRESHOLD = 0.8           # Flush when 80% full
PHI_EVICTION_WEIGHT = PHI_INVERSE  # Use phi for LRU weighting


# =============================================================================
# BUFFER ENTRY DATACLASS
# =============================================================================

@dataclass
class BufferEntry:
    """
    An entry in the memory buffer with TTL and access tracking.
    """
    key: str
    value: MemoryExperience
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    ttl_seconds: Optional[int] = None

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.ttl_seconds is None:
            return False
        expiry = self.created_at + timedelta(seconds=self.ttl_seconds)
        return datetime.now() > expiry

    def access(self) -> None:
        """Record an access."""
        self.last_accessed = datetime.now()
        self.access_count += 1

    def priority_score(self) -> float:
        """
        Calculate priority for eviction (lower = more likely to evict).
        Uses phi-weighted LRU algorithm.
        """
        # Time since last access (in hours)
        hours_since_access = (datetime.now() - self.last_accessed).total_seconds() / 3600

        # Phi-weighted score: more accesses = higher priority
        # Older last access = lower priority
        access_weight = min(self.access_count / 10, 1.0) * PHI
        recency_weight = max(0, 1.0 - (hours_since_access / 24)) * PHI_INVERSE

        # Emotional importance
        emotional_weight = self.value.emotional_context.calculate_emotional_weight()

        return (
            access_weight * 0.4 +
            recency_weight * 0.4 +
            emotional_weight * 0.2
        )


# =============================================================================
# MEMORY BUFFER CLASS
# =============================================================================

class MemoryBuffer:
    """
    Level 1 Memory Buffer - Fast in-memory cache.

    Provides:
    - Sub-millisecond access to recent memories
    - LRU eviction with phi-weighted priorities
    - Session context management
    - Working memory for active concepts

    Designed to work without Redis in development,
    with optional Redis backend in production.
    """

    def __init__(
        self,
        capacity: int = DEFAULT_BUFFER_CAPACITY,
        ttl_hours: int = DEFAULT_TTL_HOURS,
        redis_client: Optional[Any] = None,
        on_eviction: Optional[Callable[[MemoryExperience], None]] = None
    ):
        """
        Initialize the memory buffer.

        Args:
            capacity: Maximum number of entries
            ttl_hours: Default TTL for entries
            redis_client: Optional Redis client for production
            on_eviction: Callback when entry is evicted
        """
        self.capacity = capacity
        self.default_ttl = ttl_hours * 3600  # Convert to seconds
        self.redis_client = redis_client
        self.on_eviction = on_eviction

        # In-memory storage (used when Redis not available)
        self._buffer: OrderedDict[str, BufferEntry] = OrderedDict()
        self._lock = threading.RLock()

        # Session context storage
        self._session_context: Dict[str, Any] = {}

        # Working memory (active concepts)
        self._working_memory: Set[str] = set()

        # Emotional state cache
        self._emotional_state: Dict[str, float] = {
            "valence": 0.0,
            "arousal": 0.5,
            "dominant_emotion": "neutral"
        }

        # Statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "stores": 0
        }

        logger.info(f"MemoryBuffer initialized: capacity={capacity}, ttl={ttl_hours}h")

    # =========================================================================
    # CORE OPERATIONS
    # =========================================================================

    async def store(
        self,
        memory: MemoryExperience,
        ttl_seconds: Optional[int] = None
    ) -> str:
        """
        Store a memory experience in the buffer.

        Args:
            memory: The memory to store
            ttl_seconds: Optional TTL override

        Returns:
            The memory ID
        """
        # Ensure memory is marked as buffer layer
        memory.layer = MemoryLayer.BUFFER

        # Create entry
        entry = BufferEntry(
            key=memory.id,
            value=memory,
            ttl_seconds=ttl_seconds or self.default_ttl
        )

        with self._lock:
            # Check capacity and evict if needed
            await self._ensure_capacity()

            # Store in buffer
            self._buffer[memory.id] = entry
            self._buffer.move_to_end(memory.id)

            self._stats["stores"] += 1

        # If Redis is available, also store there
        if self.redis_client:
            await self._store_redis(memory, ttl_seconds)

        logger.debug(f"Stored memory in buffer: {memory.id}")
        return memory.id

    async def retrieve(self, memory_id: str) -> Optional[MemoryExperience]:
        """
        Retrieve a memory from the buffer.

        Args:
            memory_id: The memory ID to retrieve

        Returns:
            The memory if found, None otherwise
        """
        # Try in-memory first
        with self._lock:
            entry = self._buffer.get(memory_id)

            if entry:
                # Check expiration
                if entry.is_expired():
                    await self._evict(memory_id)
                    self._stats["misses"] += 1
                    return None

                # Update access
                entry.access()
                entry.value.access()
                self._buffer.move_to_end(memory_id)

                self._stats["hits"] += 1
                return entry.value

        # Try Redis if available
        if self.redis_client:
            memory = await self._retrieve_redis(memory_id)
            if memory:
                # Cache in local buffer
                await self.store(memory)
                self._stats["hits"] += 1
                return memory

        self._stats["misses"] += 1
        return None

    async def search(
        self,
        query: str,
        limit: int = 10,
        min_relevance: float = 0.3
    ) -> List[MemoryExperience]:
        """
        Search memories in the buffer.

        Args:
            query: Search query
            limit: Maximum results
            min_relevance: Minimum relevance score

        Returns:
            List of matching memories
        """
        results = []
        query_lower = query.lower()
        query_words = set(query_lower.split())

        with self._lock:
            for entry in self._buffer.values():
                if entry.is_expired():
                    continue

                memory = entry.value
                content_lower = memory.content.lower()

                # Calculate relevance
                relevance = self._calculate_relevance(
                    query_words,
                    content_lower,
                    memory
                )

                if relevance >= min_relevance:
                    results.append((relevance, memory))

        # Sort by relevance and return
        results.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in results[:limit]]

    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory from the buffer.

        Args:
            memory_id: The memory ID to delete

        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if memory_id in self._buffer:
                del self._buffer[memory_id]

                # Also delete from Redis if available
                if self.redis_client:
                    await self._delete_redis(memory_id)

                return True

        return False

    async def clear(self) -> int:
        """
        Clear all entries from the buffer.

        Returns:
            Number of entries cleared
        """
        with self._lock:
            count = len(self._buffer)
            self._buffer.clear()
            self._session_context.clear()
            self._working_memory.clear()

            if self.redis_client:
                await self._clear_redis()

            logger.info(f"Buffer cleared: {count} entries")
            return count

    # =========================================================================
    # SESSION CONTEXT
    # =========================================================================

    async def set_session_context(self, key: str, value: Any) -> None:
        """Set a session context variable."""
        self._session_context[key] = value

    async def get_session_context(self, key: str) -> Optional[Any]:
        """Get a session context variable."""
        return self._session_context.get(key)

    async def get_all_session_context(self) -> Dict[str, Any]:
        """Get all session context variables."""
        return self._session_context.copy()

    async def clear_session_context(self) -> None:
        """Clear all session context variables."""
        self._session_context.clear()

    # =========================================================================
    # WORKING MEMORY
    # =========================================================================

    async def add_to_working_memory(self, concept: str) -> None:
        """Add a concept to working memory."""
        self._working_memory.add(concept)
        # Limit working memory size based on phi
        max_concepts = int(self.capacity * PHI_INVERSE)
        if len(self._working_memory) > max_concepts:
            # Remove oldest (arbitrary since set)
            self._working_memory.pop()

    async def is_in_working_memory(self, concept: str) -> bool:
        """Check if concept is in working memory."""
        return concept in self._working_memory

    async def get_working_memory(self) -> Set[str]:
        """Get all concepts in working memory."""
        return self._working_memory.copy()

    async def clear_working_memory(self) -> None:
        """Clear working memory."""
        self._working_memory.clear()

    # =========================================================================
    # EMOTIONAL STATE
    # =========================================================================

    async def update_emotional_state(
        self,
        valence: Optional[float] = None,
        arousal: Optional[float] = None,
        dominant_emotion: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update the current emotional state."""
        if valence is not None:
            self._emotional_state["valence"] = max(-1.0, min(1.0, valence))
        if arousal is not None:
            self._emotional_state["arousal"] = max(0.0, min(1.0, arousal))
        if dominant_emotion is not None:
            self._emotional_state["dominant_emotion"] = dominant_emotion

        return self._emotional_state.copy()

    async def get_emotional_state(self) -> Dict[str, Any]:
        """Get the current emotional state."""
        return self._emotional_state.copy()

    # =========================================================================
    # RECENT INTERACTIONS
    # =========================================================================

    async def get_recent_memories(
        self,
        limit: int = 100,
        memory_type: Optional[MemoryType] = None
    ) -> List[MemoryExperience]:
        """
        Get most recent memories from the buffer.

        Args:
            limit: Maximum number to return
            memory_type: Filter by type

        Returns:
            List of recent memories
        """
        results = []

        with self._lock:
            # Iterate in reverse order (most recent first)
            for entry in reversed(list(self._buffer.values())):
                if entry.is_expired():
                    continue

                if memory_type and entry.value.memory_type != memory_type:
                    continue

                results.append(entry.value)

                if len(results) >= limit:
                    break

        return results

    # =========================================================================
    # FLUSH TO FRACTAL
    # =========================================================================

    async def get_candidates_for_fractal(
        self,
        min_importance: float = 0.3
    ) -> List[MemoryExperience]:
        """
        Get memories ready to be moved to fractal layer.

        Args:
            min_importance: Minimum importance score

        Returns:
            List of candidate memories
        """
        candidates = []

        with self._lock:
            for entry in self._buffer.values():
                if entry.is_expired():
                    continue

                memory = entry.value
                importance = memory.phi_metrics.calculate_importance()

                if importance >= min_importance:
                    candidates.append(memory)

        # Sort by importance (highest first)
        candidates.sort(
            key=lambda m: m.phi_metrics.calculate_importance(),
            reverse=True
        )

        return candidates

    async def mark_as_flushed(self, memory_ids: List[str]) -> int:
        """
        Mark memories as flushed to fractal layer.

        Args:
            memory_ids: List of memory IDs that were flushed

        Returns:
            Number of memories marked
        """
        count = 0
        with self._lock:
            for memory_id in memory_ids:
                if memory_id in self._buffer:
                    self._buffer[memory_id].value.layer = MemoryLayer.FRACTAL
                    count += 1

        return count

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get buffer statistics."""
        with self._lock:
            current_size = len(self._buffer)

            # Calculate average phi metrics
            total_resonance = 0.0
            total_importance = 0.0

            for entry in self._buffer.values():
                total_resonance += entry.value.phi_metrics.phi_resonance
                total_importance += entry.value.phi_metrics.calculate_importance()

            avg_resonance = total_resonance / max(1, current_size)
            avg_importance = total_importance / max(1, current_size)

            return {
                "current_size": current_size,
                "capacity": self.capacity,
                "utilization": current_size / self.capacity,
                "hits": self._stats["hits"],
                "misses": self._stats["misses"],
                "hit_rate": self._stats["hits"] / max(1, self._stats["hits"] + self._stats["misses"]),
                "evictions": self._stats["evictions"],
                "stores": self._stats["stores"],
                "phi_metrics": {
                    "average_resonance": avg_resonance,
                    "average_importance": avg_importance
                },
                "session_context_keys": len(self._session_context),
                "working_memory_size": len(self._working_memory),
                "redis_enabled": self.redis_client is not None
            }

    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================

    async def _ensure_capacity(self) -> None:
        """Ensure buffer has capacity, evicting if necessary."""
        while len(self._buffer) >= self.capacity:
            await self._evict_lowest_priority()

    async def _evict_lowest_priority(self) -> None:
        """Evict the entry with lowest priority."""
        if not self._buffer:
            return

        # Find entry with lowest priority
        min_priority = float('inf')
        evict_key = None

        for key, entry in self._buffer.items():
            # First evict expired entries
            if entry.is_expired():
                evict_key = key
                break

            priority = entry.priority_score()
            if priority < min_priority:
                min_priority = priority
                evict_key = key

        if evict_key:
            await self._evict(evict_key)

    async def _evict(self, key: str) -> None:
        """Evict an entry from the buffer."""
        if key in self._buffer:
            entry = self._buffer.pop(key)
            self._stats["evictions"] += 1

            # Call eviction callback
            if self.on_eviction:
                self.on_eviction(entry.value)

            logger.debug(f"Evicted memory from buffer: {key}")

    def _calculate_relevance(
        self,
        query_words: Set[str],
        content_lower: str,
        memory: MemoryExperience
    ) -> float:
        """Calculate relevance score for a memory."""
        content_words = set(content_lower.split())

        # Word overlap
        overlap = len(query_words & content_words)
        word_score = overlap / max(1, len(query_words))

        # Keyword match
        keyword_score = 0.0
        for keyword in memory.keywords:
            if keyword.lower() in content_lower:
                keyword_score += 0.2

        # Tag match
        tag_score = 0.0
        for tag in memory.tags:
            if any(qw in tag.lower() for qw in query_words):
                tag_score += 0.15

        # Phi resonance boost
        phi_boost = memory.phi_metrics.phi_resonance * 0.2

        return min(1.0, word_score * 0.5 + keyword_score + tag_score + phi_boost)

    # =========================================================================
    # REDIS METHODS (for production)
    # =========================================================================

    async def _store_redis(
        self,
        memory: MemoryExperience,
        ttl_seconds: Optional[int]
    ) -> None:
        """Store memory in Redis."""
        if not self.redis_client:
            return

        try:
            key = f"luna:buffer:{memory.id}"
            value = json.dumps(memory.to_dict())
            ttl = ttl_seconds or self.default_ttl

            # Use async Redis if available
            if hasattr(self.redis_client, 'setex'):
                await self.redis_client.setex(key, ttl, value)
            else:
                self.redis_client.setex(key, ttl, value)

        except Exception as e:
            logger.warning(f"Failed to store in Redis: {e}")

    async def _retrieve_redis(self, memory_id: str) -> Optional[MemoryExperience]:
        """Retrieve memory from Redis."""
        if not self.redis_client:
            return None

        try:
            key = f"luna:buffer:{memory_id}"

            if hasattr(self.redis_client, 'get'):
                value = await self.redis_client.get(key)
            else:
                value = self.redis_client.get(key)

            if value:
                data = json.loads(value)
                return MemoryExperience.from_dict(data)

        except Exception as e:
            logger.warning(f"Failed to retrieve from Redis: {e}")

        return None

    async def _delete_redis(self, memory_id: str) -> None:
        """Delete memory from Redis."""
        if not self.redis_client:
            return

        try:
            key = f"luna:buffer:{memory_id}"
            if hasattr(self.redis_client, 'delete'):
                await self.redis_client.delete(key)
            else:
                self.redis_client.delete(key)

        except Exception as e:
            logger.warning(f"Failed to delete from Redis: {e}")

    async def _clear_redis(self) -> None:
        """Clear Luna buffer keys from Redis."""
        if not self.redis_client:
            return

        try:
            pattern = "luna:buffer:*"
            if hasattr(self.redis_client, 'keys'):
                keys = await self.redis_client.keys(pattern)
                if keys:
                    await self.redis_client.delete(*keys)
            else:
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)

        except Exception as e:
            logger.warning(f"Failed to clear Redis: {e}")


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_memory_buffer(
    capacity: int = DEFAULT_BUFFER_CAPACITY,
    ttl_hours: int = DEFAULT_TTL_HOURS,
    redis_url: Optional[str] = None,
    on_eviction: Optional[Callable[[MemoryExperience], None]] = None
) -> MemoryBuffer:
    """
    Factory function to create a MemoryBuffer with optional Redis.

    Args:
        capacity: Buffer capacity
        ttl_hours: Default TTL
        redis_url: Optional Redis URL for production
        on_eviction: Callback for evictions

    Returns:
        Configured MemoryBuffer instance
    """
    redis_client = None

    if redis_url:
        try:
            import redis.asyncio as aioredis
            redis_client = aioredis.from_url(redis_url)
            logger.info(f"Connected to Redis: {redis_url}")
        except ImportError:
            logger.warning("redis package not installed, using in-memory buffer only")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}, using in-memory buffer only")

    return MemoryBuffer(
        capacity=capacity,
        ttl_hours=ttl_hours,
        redis_client=redis_client,
        on_eviction=on_eviction
    )
