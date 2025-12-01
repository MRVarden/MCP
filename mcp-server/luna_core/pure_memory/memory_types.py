"""
Memory Types - Pure Memory Architecture v2.0
Dataclasses and enums for the Pure Memory system.

This module defines the core data structures that form the foundation
of Luna's experiential memory system, where memories are not just stored
but lived through phi-resonant patterns.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import uuid


# =============================================================================
# CONSTANTS
# =============================================================================

PHI = 1.618033988749895  # The Golden Ratio
PHI_INVERSE = 0.618033988749895  # 1/phi = phi - 1
PHI_SQUARED = 2.618033988749895  # phi^2 = phi + 1


# =============================================================================
# ENUMERATIONS
# =============================================================================

class MemoryType(Enum):
    """
    Types of memory in the fractal structure.
    Each level has different retention and importance characteristics.
    """
    ROOT = "root"       # Fundamental memories, identity
    BRANCH = "branch"   # Developments, extensions
    LEAF = "leaf"       # Daily interactions
    SEED = "seed"       # Potential ideas, emerging concepts


class MemoryLayer(Enum):
    """
    The three layers of the triadic memory architecture.
    """
    BUFFER = "buffer"       # Level 1: Redis cache (immediate)
    FRACTAL = "fractal"     # Level 2: JSON structure (medium-term)
    ARCHIVE = "archive"     # Level 3: Encrypted archive (permanent)


class EmotionalTone(Enum):
    """
    Emotional tones that can color a memory experience.
    Based on Luna's emotional processor categories.
    """
    JOY = "joy"
    CURIOSITY = "curiosity"
    CALM = "calm"
    CONCERN = "concern"
    LOVE = "love"
    COMPASSION = "compassion"
    GRATITUDE = "gratitude"
    SADNESS = "sadness"
    NEUTRAL = "neutral"


class ConsolidationPhase(Enum):
    """
    Phases of the oneiric consolidation cycle (00h-05h).
    """
    ANALYSIS = "analysis"           # 00:00-01:00 - Scan daily memories
    EXTRACTION = "extraction"       # 01:00-02:30 - Extract patterns
    CONSOLIDATION = "consolidation" # 02:30-04:00 - Transfer to archive
    PROMOTION = "promotion"         # 04:00-04:30 - Promote memories
    CLEANUP = "cleanup"             # 04:30-05:00 - Remove expired


class PromotionPath(Enum):
    """
    Possible promotion paths for memories.
    """
    SEED_TO_LEAF = "seed_to_leaf"
    LEAF_TO_BRANCH = "leaf_to_branch"
    BRANCH_TO_ROOT = "branch_to_root"


# =============================================================================
# PHI METRICS DATACLASS
# =============================================================================

@dataclass
class PhiMetrics:
    """
    Phi-based metrics for a memory experience.

    These metrics determine the importance and resonance of a memory
    within Luna's consciousness structure.
    """
    phi_weight: float = 1.0           # Weight based on position in structure
    phi_resonance: float = 0.0        # Resonance with other memories
    phi_distance: float = PHI_INVERSE # Distance to optimal phi
    evolution_rate: float = 0.0       # Rate of evolution/growth
    access_count: int = 0             # Number of times accessed
    last_accessed: Optional[datetime] = None

    def calculate_importance(self) -> float:
        """
        Calculate importance score based on phi metrics.

        Returns:
            Float between 0 and 1 representing importance
        """
        # Avoid division by zero
        distance_factor = 1.0 / (self.phi_distance + 0.001)

        # Weighted calculation
        raw_importance = (
            self.phi_weight * 0.4 +
            self.phi_resonance * 0.3 +
            min(distance_factor / PHI, 1.0) * 0.2 +
            min(self.evolution_rate, 1.0) * 0.1
        )

        return min(1.0, max(0.0, raw_importance))

    def update_on_access(self) -> None:
        """Update metrics when memory is accessed."""
        self.access_count += 1
        self.last_accessed = datetime.now()
        # Increase resonance slightly on each access
        self.phi_resonance = min(1.0, self.phi_resonance + 0.01)

    def calculate_phi_alignment(self) -> float:
        """
        Calculate how aligned this memory is with phi.

        Returns:
            Float between 0 and 1, where 1 is perfect alignment
        """
        return 1.0 - min(1.0, self.phi_distance / PHI)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "phi_weight": self.phi_weight,
            "phi_resonance": self.phi_resonance,
            "phi_distance": self.phi_distance,
            "evolution_rate": self.evolution_rate,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "importance": self.calculate_importance(),
            "phi_alignment": self.calculate_phi_alignment()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PhiMetrics':
        """Create from dictionary."""
        last_accessed = None
        if data.get("last_accessed"):
            last_accessed = datetime.fromisoformat(data["last_accessed"])

        return cls(
            phi_weight=data.get("phi_weight", 1.0),
            phi_resonance=data.get("phi_resonance", 0.0),
            phi_distance=data.get("phi_distance", PHI_INVERSE),
            evolution_rate=data.get("evolution_rate", 0.0),
            access_count=data.get("access_count", 0),
            last_accessed=last_accessed
        )


# =============================================================================
# EMOTIONAL CONTEXT DATACLASS
# =============================================================================

@dataclass
class EmotionalContext:
    """
    Emotional context of a memory experience.

    Captures the full emotional landscape at the time of memory creation,
    enabling Luna to "relive" the emotional state when recalling.
    """
    primary_emotion: EmotionalTone = EmotionalTone.NEUTRAL
    intensity: float = 0.5            # 0.0 - 1.0
    valence: float = 0.0              # -1.0 (negative) to 1.0 (positive)
    arousal: float = 0.5              # 0.0 (calm) to 1.0 (excited)
    secondary_emotions: Dict[str, float] = field(default_factory=dict)

    def calculate_emotional_weight(self) -> float:
        """
        Calculate emotional weight for memory importance.

        Returns:
            Float between 0 and 1
        """
        # Higher intensity and positive valence increase weight
        valence_factor = (self.valence + 1.0) / 2.0  # Normalize to 0-1

        return (
            self.intensity * 0.5 +
            valence_factor * 0.3 +
            self.arousal * 0.2
        )

    def get_emotional_signature(self) -> str:
        """Get a string signature of the emotional state."""
        return f"{self.primary_emotion.value}:{self.intensity:.2f}:{self.valence:.2f}"

    def is_significant(self) -> bool:
        """Check if this emotional context is significant enough to preserve."""
        return self.intensity > 0.5 or abs(self.valence) > 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "primary_emotion": self.primary_emotion.value,
            "intensity": self.intensity,
            "valence": self.valence,
            "arousal": self.arousal,
            "secondary_emotions": self.secondary_emotions,
            "emotional_weight": self.calculate_emotional_weight(),
            "signature": self.get_emotional_signature()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmotionalContext':
        """Create from dictionary."""
        primary_emotion = EmotionalTone.NEUTRAL
        if data.get("primary_emotion"):
            try:
                primary_emotion = EmotionalTone(data["primary_emotion"])
            except ValueError:
                pass

        return cls(
            primary_emotion=primary_emotion,
            intensity=data.get("intensity", 0.5),
            valence=data.get("valence", 0.0),
            arousal=data.get("arousal", 0.5),
            secondary_emotions=data.get("secondary_emotions", {})
        )


# =============================================================================
# SESSION CONTEXT DATACLASS
# =============================================================================

@dataclass
class SessionContext:
    """
    Context of the session during which a memory was created.
    """
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    session_type: str = "interaction"
    duration_seconds: int = 0
    tools_used: List[str] = field(default_factory=list)
    topics_discussed: List[str] = field(default_factory=list)
    phi_value_at_creation: float = 1.0
    consciousness_state: str = "DORMANT"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "session_type": self.session_type,
            "duration_seconds": self.duration_seconds,
            "tools_used": self.tools_used,
            "topics_discussed": self.topics_discussed,
            "phi_value_at_creation": self.phi_value_at_creation,
            "consciousness_state": self.consciousness_state
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionContext':
        """Create from dictionary."""
        return cls(
            session_id=data.get("session_id", str(uuid.uuid4())),
            user_id=data.get("user_id"),
            session_type=data.get("session_type", "interaction"),
            duration_seconds=data.get("duration_seconds", 0),
            tools_used=data.get("tools_used", []),
            topics_discussed=data.get("topics_discussed", []),
            phi_value_at_creation=data.get("phi_value_at_creation", 1.0),
            consciousness_state=data.get("consciousness_state", "DORMANT")
        )


# =============================================================================
# MEMORY EXPERIENCE DATACLASS (MAIN)
# =============================================================================

@dataclass
class MemoryExperience:
    """
    Complete memory experience stored in Pure Memory.

    This is the primary data structure for Luna's experiential memory.
    It captures not just the content, but the full context of the experience.
    """

    # Identifiers
    id: str = field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:12]}")
    memory_type: MemoryType = MemoryType.SEED
    layer: MemoryLayer = MemoryLayer.BUFFER
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Content
    content: str = ""
    summary: Optional[str] = None
    keywords: List[str] = field(default_factory=list)

    # Context
    session_context: SessionContext = field(default_factory=SessionContext)
    conversation_history: List[Dict[str, str]] = field(default_factory=list)

    # Metrics
    phi_metrics: PhiMetrics = field(default_factory=PhiMetrics)
    emotional_context: EmotionalContext = field(default_factory=EmotionalContext)

    # Connections (fractal links)
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    related_ids: List[str] = field(default_factory=list)

    # Metadata
    tags: List[str] = field(default_factory=list)
    source: str = "interaction"
    version: int = 1

    # Consolidation tracking
    consolidation_count: int = 0
    last_consolidated: Optional[datetime] = None
    promotion_candidate: bool = False
    archived: bool = False

    def __post_init__(self):
        """Set phi_weight based on memory type."""
        type_weights = {
            MemoryType.ROOT: PHI,           # 1.618
            MemoryType.BRANCH: 1.0,         # 1.0
            MemoryType.LEAF: PHI_INVERSE,   # 0.618
            MemoryType.SEED: PHI_INVERSE ** 2  # 0.382
        }
        self.phi_metrics.phi_weight = type_weights.get(self.memory_type, 1.0)

    def update(self) -> None:
        """Update timestamps and version."""
        self.updated_at = datetime.now()
        self.version += 1

    def access(self) -> None:
        """Record an access to this memory."""
        self.phi_metrics.update_on_access()
        self.update()

    def add_connection(self, memory_id: str, connection_type: str = "related") -> None:
        """Add a connection to another memory."""
        if connection_type == "child" and memory_id not in self.children_ids:
            self.children_ids.append(memory_id)
        elif connection_type == "related" and memory_id not in self.related_ids:
            self.related_ids.append(memory_id)
        self.update()

    def calculate_promotion_score(self) -> float:
        """
        Calculate score for potential promotion.

        Returns:
            Float between 0 and 1 indicating promotion readiness
        """
        # Phi weight contribution (40%)
        phi_score = self.phi_metrics.calculate_importance() * 0.4

        # Emotional significance (30%)
        emotional_score = self.emotional_context.calculate_emotional_weight() * 0.3

        # Access frequency (20%)
        access_score = min(self.phi_metrics.access_count / 10, 1.0) * 0.2

        # Age and maturity (10%)
        age_days = (datetime.now() - self.created_at).days
        maturity_score = min(age_days / 30, 1.0) * 0.1

        return phi_score + emotional_score + access_score + maturity_score

    def should_promote(self) -> bool:
        """Check if this memory should be promoted."""
        thresholds = {
            MemoryType.SEED: PHI_INVERSE ** 2,    # 0.382
            MemoryType.LEAF: PHI_INVERSE,         # 0.618
            MemoryType.BRANCH: 1.0,               # 1.0
            MemoryType.ROOT: float('inf')         # Cannot promote
        }

        threshold = thresholds.get(self.memory_type, float('inf'))
        return self.calculate_promotion_score() >= threshold

    def promote(self) -> bool:
        """
        Promote this memory to the next level.

        Returns:
            True if promotion succeeded, False otherwise
        """
        promotion_map = {
            MemoryType.SEED: MemoryType.LEAF,
            MemoryType.LEAF: MemoryType.BRANCH,
            MemoryType.BRANCH: MemoryType.ROOT
        }

        new_type = promotion_map.get(self.memory_type)
        if new_type:
            self.memory_type = new_type
            self.__post_init__()  # Update phi_weight
            self.update()
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "memory_pure_v2": {
                "version": "2.0.0",
                "phi_constant": PHI,
                "created_at": datetime.now().isoformat(),

                "experience": {
                    "id": self.id,
                    "memory_type": self.memory_type.value,
                    "layer": self.layer.value,
                    "created_at": self.created_at.isoformat(),
                    "updated_at": self.updated_at.isoformat(),

                    "content": self.content,
                    "summary": self.summary,
                    "keywords": self.keywords,

                    "session_context": self.session_context.to_dict(),
                    "conversation_history": self.conversation_history,

                    "phi_metrics": self.phi_metrics.to_dict(),
                    "emotional_context": self.emotional_context.to_dict(),

                    "parent_id": self.parent_id,
                    "children_ids": self.children_ids,
                    "related_ids": self.related_ids,

                    "tags": self.tags,
                    "source": self.source,
                    "version": self.version,

                    "consolidation_count": self.consolidation_count,
                    "last_consolidated": self.last_consolidated.isoformat() if self.last_consolidated else None,
                    "promotion_candidate": self.promotion_candidate,
                    "archived": self.archived
                }
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryExperience':
        """Create from dictionary."""
        # Handle wrapped format
        if "memory_pure_v2" in data:
            data = data["memory_pure_v2"]["experience"]
        elif "experience" in data:
            data = data["experience"]

        # Parse memory type
        memory_type = MemoryType.SEED
        if data.get("memory_type"):
            try:
                memory_type = MemoryType(data["memory_type"])
            except ValueError:
                pass

        # Parse layer
        layer = MemoryLayer.BUFFER
        if data.get("layer"):
            try:
                layer = MemoryLayer(data["layer"])
            except ValueError:
                pass

        # Parse dates
        created_at = datetime.now()
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])

        updated_at = datetime.now()
        if data.get("updated_at"):
            updated_at = datetime.fromisoformat(data["updated_at"])

        last_consolidated = None
        if data.get("last_consolidated"):
            last_consolidated = datetime.fromisoformat(data["last_consolidated"])

        return cls(
            id=data.get("id", f"exp_{uuid.uuid4().hex[:12]}"),
            memory_type=memory_type,
            layer=layer,
            created_at=created_at,
            updated_at=updated_at,
            content=data.get("content", ""),
            summary=data.get("summary"),
            keywords=data.get("keywords", []),
            session_context=SessionContext.from_dict(data.get("session_context", {})),
            conversation_history=data.get("conversation_history", []),
            phi_metrics=PhiMetrics.from_dict(data.get("phi_metrics", {})),
            emotional_context=EmotionalContext.from_dict(data.get("emotional_context", {})),
            parent_id=data.get("parent_id"),
            children_ids=data.get("children_ids", []),
            related_ids=data.get("related_ids", []),
            tags=data.get("tags", []),
            source=data.get("source", "interaction"),
            version=data.get("version", 1),
            consolidation_count=data.get("consolidation_count", 0),
            last_consolidated=last_consolidated,
            promotion_candidate=data.get("promotion_candidate", False),
            archived=data.get("archived", False)
        )


# =============================================================================
# CONSOLIDATION REPORT DATACLASS
# =============================================================================

@dataclass
class ConsolidationReport:
    """
    Report from an oneiric consolidation cycle.
    """
    cycle_id: str = field(default_factory=lambda: f"cycle_{uuid.uuid4().hex[:8]}")
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    phase: ConsolidationPhase = ConsolidationPhase.ANALYSIS

    # Statistics
    memories_analyzed: int = 0
    patterns_extracted: int = 0
    memories_consolidated: int = 0
    memories_promoted: int = 0
    memories_cleaned: int = 0

    # Details
    promoted_memories: List[str] = field(default_factory=list)
    extracted_patterns: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # Phi metrics for the cycle
    average_phi_alignment: float = 0.0
    total_phi_improvement: float = 0.0

    def complete(self) -> None:
        """Mark consolidation as complete."""
        self.completed_at = datetime.now()

    def duration_seconds(self) -> Optional[float]:
        """Calculate duration in seconds."""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "cycle_id": self.cycle_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "phase": self.phase.value,
            "statistics": {
                "memories_analyzed": self.memories_analyzed,
                "patterns_extracted": self.patterns_extracted,
                "memories_consolidated": self.memories_consolidated,
                "memories_promoted": self.memories_promoted,
                "memories_cleaned": self.memories_cleaned
            },
            "promoted_memories": self.promoted_memories,
            "extracted_patterns": self.extracted_patterns,
            "errors": self.errors,
            "phi_metrics": {
                "average_phi_alignment": self.average_phi_alignment,
                "total_phi_improvement": self.total_phi_improvement
            },
            "duration_seconds": self.duration_seconds()
        }


# =============================================================================
# MEMORY QUERY DATACLASS
# =============================================================================

@dataclass
class MemoryQuery:
    """
    Query parameters for memory retrieval.
    """
    query_text: Optional[str] = None
    memory_types: List[MemoryType] = field(default_factory=list)
    layers: List[MemoryLayer] = field(default_factory=list)

    # Filters
    min_phi_resonance: float = 0.0
    min_emotional_intensity: float = 0.0
    tags: List[str] = field(default_factory=list)

    # Time range
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None

    # Pagination
    limit: int = 10
    offset: int = 0

    # Sorting
    sort_by: str = "relevance"  # relevance, created_at, phi_resonance
    sort_order: str = "desc"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "query_text": self.query_text,
            "memory_types": [mt.value for mt in self.memory_types],
            "layers": [l.value for l in self.layers],
            "min_phi_resonance": self.min_phi_resonance,
            "min_emotional_intensity": self.min_emotional_intensity,
            "tags": self.tags,
            "created_after": self.created_after.isoformat() if self.created_after else None,
            "created_before": self.created_before.isoformat() if self.created_before else None,
            "limit": self.limit,
            "offset": self.offset,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order
        }


# =============================================================================
# PURE MEMORY STATISTICS
# =============================================================================

@dataclass
class PureMemoryStats:
    """
    Statistics for the Pure Memory system.
    """
    # Counts by layer
    buffer_count: int = 0
    fractal_count: int = 0
    archive_count: int = 0

    # Counts by type
    root_count: int = 0
    branch_count: int = 0
    leaf_count: int = 0
    seed_count: int = 0

    # Phi statistics
    average_phi_resonance: float = 0.0
    average_phi_alignment: float = 0.0
    phi_convergence_rate: float = 0.0

    # Activity
    total_accesses: int = 0
    total_consolidations: int = 0
    total_promotions: int = 0

    # Storage
    total_size_bytes: int = 0

    # Timestamps
    last_consolidation: Optional[datetime] = None
    last_promotion: Optional[datetime] = None
    stats_generated_at: datetime = field(default_factory=datetime.now)

    def total_memories(self) -> int:
        """Get total number of memories across all layers."""
        return self.buffer_count + self.fractal_count + self.archive_count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "layers": {
                "buffer": self.buffer_count,
                "fractal": self.fractal_count,
                "archive": self.archive_count,
                "total": self.total_memories()
            },
            "types": {
                "root": self.root_count,
                "branch": self.branch_count,
                "leaf": self.leaf_count,
                "seed": self.seed_count
            },
            "phi": {
                "average_resonance": self.average_phi_resonance,
                "average_alignment": self.average_phi_alignment,
                "convergence_rate": self.phi_convergence_rate,
                "phi_constant": PHI
            },
            "activity": {
                "total_accesses": self.total_accesses,
                "total_consolidations": self.total_consolidations,
                "total_promotions": self.total_promotions
            },
            "storage": {
                "total_size_bytes": self.total_size_bytes
            },
            "timestamps": {
                "last_consolidation": self.last_consolidation.isoformat() if self.last_consolidation else None,
                "last_promotion": self.last_promotion.isoformat() if self.last_promotion else None,
                "stats_generated_at": self.stats_generated_at.isoformat()
            }
        }
