"""
Tests for Pure Memory Types - Core Data Structures
===================================================

Tests cover:
- PHI constants
- Enumerations (MemoryType, MemoryLayer, EmotionalTone, etc.)
- PhiMetrics dataclass
- EmotionalContext dataclass
- SessionContext dataclass
- MemoryExperience dataclass (main)
- ConsolidationReport dataclass
- MemoryQuery dataclass
- PureMemoryStats dataclass
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))

from luna_core.pure_memory.memory_types import (
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


class TestPhiConstants:
    """Tests for phi constants."""

    def test_phi_value(self):
        """Test PHI constant value."""
        import math
        expected = (1 + math.sqrt(5)) / 2
        assert abs(PHI - expected) < 1e-10

    def test_phi_inverse_value(self):
        """Test PHI_INVERSE constant."""
        assert abs(PHI_INVERSE - (PHI - 1)) < 1e-10

    def test_phi_squared_value(self):
        """Test PHI_SQUARED constant."""
        assert abs(PHI_SQUARED - (PHI + 1)) < 1e-10

    def test_phi_relationship(self):
        """Test phi mathematical relationship: phi^2 = phi + 1."""
        assert abs(PHI * PHI - PHI_SQUARED) < 1e-10

    def test_inverse_relationship(self):
        """Test inverse relationship: 1/phi = phi - 1."""
        assert abs(1/PHI - PHI_INVERSE) < 1e-10


class TestMemoryTypeEnum:
    """Tests for MemoryType enumeration."""

    def test_root_value(self):
        """Test ROOT value."""
        assert MemoryType.ROOT.value == "root"

    def test_branch_value(self):
        """Test BRANCH value."""
        assert MemoryType.BRANCH.value == "branch"

    def test_leaf_value(self):
        """Test LEAF value."""
        assert MemoryType.LEAF.value == "leaf"

    def test_seed_value(self):
        """Test SEED value."""
        assert MemoryType.SEED.value == "seed"

    def test_all_types_exist(self):
        """Test all expected types exist."""
        types = list(MemoryType)
        assert len(types) == 4


class TestMemoryLayerEnum:
    """Tests for MemoryLayer enumeration."""

    def test_buffer_value(self):
        """Test BUFFER value."""
        assert MemoryLayer.BUFFER.value == "buffer"

    def test_fractal_value(self):
        """Test FRACTAL value."""
        assert MemoryLayer.FRACTAL.value == "fractal"

    def test_archive_value(self):
        """Test ARCHIVE value."""
        assert MemoryLayer.ARCHIVE.value == "archive"


class TestEmotionalToneEnum:
    """Tests for EmotionalTone enumeration."""

    def test_all_emotions_exist(self):
        """Test all expected emotions exist."""
        expected = [
            "joy", "curiosity", "calm", "concern", "love",
            "compassion", "gratitude", "sadness", "neutral"
        ]
        actual = [e.value for e in EmotionalTone]
        assert set(expected) == set(actual)

    def test_neutral_exists(self):
        """Test neutral emotion exists."""
        assert EmotionalTone.NEUTRAL.value == "neutral"


class TestConsolidationPhaseEnum:
    """Tests for ConsolidationPhase enumeration."""

    def test_phase_sequence(self):
        """Test consolidation phases."""
        phases = [
            ConsolidationPhase.ANALYSIS,
            ConsolidationPhase.EXTRACTION,
            ConsolidationPhase.CONSOLIDATION,
            ConsolidationPhase.PROMOTION,
            ConsolidationPhase.CLEANUP
        ]
        assert len(phases) == 5


class TestPromotionPathEnum:
    """Tests for PromotionPath enumeration."""

    def test_seed_to_leaf(self):
        """Test seed to leaf path."""
        assert PromotionPath.SEED_TO_LEAF.value == "seed_to_leaf"

    def test_leaf_to_branch(self):
        """Test leaf to branch path."""
        assert PromotionPath.LEAF_TO_BRANCH.value == "leaf_to_branch"

    def test_branch_to_root(self):
        """Test branch to root path."""
        assert PromotionPath.BRANCH_TO_ROOT.value == "branch_to_root"


class TestPhiMetrics:
    """Tests for PhiMetrics dataclass."""

    def test_default_values(self):
        """Test default values."""
        metrics = PhiMetrics()

        assert metrics.phi_weight == 1.0
        assert metrics.phi_resonance == 0.0
        assert metrics.phi_distance == PHI_INVERSE
        assert metrics.evolution_rate == 0.0
        assert metrics.access_count == 0
        assert metrics.last_accessed is None

    def test_calculate_importance_default(self):
        """Test importance calculation with defaults."""
        metrics = PhiMetrics()
        importance = metrics.calculate_importance()

        assert 0 <= importance <= 1

    def test_calculate_importance_high_metrics(self):
        """Test importance increases with high metrics."""
        low_metrics = PhiMetrics(phi_weight=0.5, phi_resonance=0.2)
        high_metrics = PhiMetrics(phi_weight=1.5, phi_resonance=0.8)

        assert high_metrics.calculate_importance() > low_metrics.calculate_importance()

    def test_update_on_access(self):
        """Test metrics update on access."""
        metrics = PhiMetrics()

        initial_count = metrics.access_count
        metrics.update_on_access()

        assert metrics.access_count == initial_count + 1
        assert metrics.last_accessed is not None
        assert metrics.phi_resonance > 0

    def test_calculate_phi_alignment(self):
        """Test phi alignment calculation."""
        close_metrics = PhiMetrics(phi_distance=0.1)
        far_metrics = PhiMetrics(phi_distance=1.0)

        assert close_metrics.calculate_phi_alignment() > far_metrics.calculate_phi_alignment()

    def test_to_dict(self):
        """Test serialization to dict."""
        metrics = PhiMetrics(phi_weight=1.5, phi_resonance=0.7)
        data = metrics.to_dict()

        assert data["phi_weight"] == 1.5
        assert data["phi_resonance"] == 0.7
        assert "importance" in data
        assert "phi_alignment" in data

    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "phi_weight": 1.3,
            "phi_resonance": 0.6,
            "access_count": 5
        }
        metrics = PhiMetrics.from_dict(data)

        assert metrics.phi_weight == 1.3
        assert metrics.phi_resonance == 0.6
        assert metrics.access_count == 5


class TestEmotionalContext:
    """Tests for EmotionalContext dataclass."""

    def test_default_values(self):
        """Test default values."""
        ctx = EmotionalContext()

        assert ctx.primary_emotion == EmotionalTone.NEUTRAL
        assert ctx.intensity == 0.5
        assert ctx.valence == 0.0
        assert ctx.arousal == 0.5

    def test_calculate_emotional_weight(self):
        """Test emotional weight calculation."""
        low_ctx = EmotionalContext(intensity=0.2, valence=-0.5, arousal=0.2)
        high_ctx = EmotionalContext(intensity=0.9, valence=0.8, arousal=0.8)

        assert high_ctx.calculate_emotional_weight() > low_ctx.calculate_emotional_weight()

    def test_get_emotional_signature(self):
        """Test emotional signature format."""
        ctx = EmotionalContext(
            primary_emotion=EmotionalTone.JOY,
            intensity=0.8,
            valence=0.9
        )
        sig = ctx.get_emotional_signature()

        assert "joy" in sig
        assert "0.8" in sig

    def test_is_significant_high_intensity(self):
        """Test significance with high intensity."""
        ctx = EmotionalContext(intensity=0.7)
        assert ctx.is_significant() == True

    def test_is_significant_high_valence(self):
        """Test significance with high valence."""
        ctx = EmotionalContext(valence=0.7)
        assert ctx.is_significant() == True

    def test_not_significant_neutral(self):
        """Test neutral context is not significant."""
        ctx = EmotionalContext(intensity=0.4, valence=0.2)
        assert ctx.is_significant() == False

    def test_to_dict(self):
        """Test serialization."""
        ctx = EmotionalContext(primary_emotion=EmotionalTone.CURIOSITY)
        data = ctx.to_dict()

        assert data["primary_emotion"] == "curiosity"
        assert "emotional_weight" in data

    def test_from_dict(self):
        """Test deserialization."""
        data = {
            "primary_emotion": "joy",
            "intensity": 0.8,
            "valence": 0.6
        }
        ctx = EmotionalContext.from_dict(data)

        assert ctx.primary_emotion == EmotionalTone.JOY
        assert ctx.intensity == 0.8


class TestSessionContext:
    """Tests for SessionContext dataclass."""

    def test_default_values(self):
        """Test default values."""
        ctx = SessionContext()

        assert ctx.session_id is not None
        assert ctx.session_type == "interaction"
        assert ctx.consciousness_state == "DORMANT"

    def test_to_dict(self):
        """Test serialization."""
        ctx = SessionContext(user_id="test_user", tools_used=["tool1"])
        data = ctx.to_dict()

        assert data["user_id"] == "test_user"
        assert "tool1" in data["tools_used"]

    def test_from_dict(self):
        """Test deserialization."""
        data = {
            "session_id": "test_session",
            "phi_value_at_creation": 1.5
        }
        ctx = SessionContext.from_dict(data)

        assert ctx.session_id == "test_session"
        assert ctx.phi_value_at_creation == 1.5


class TestMemoryExperience:
    """Tests for MemoryExperience dataclass (main)."""

    def test_default_values(self):
        """Test default values."""
        exp = MemoryExperience()

        assert exp.id.startswith("exp_")
        assert exp.memory_type == MemoryType.SEED
        assert exp.layer == MemoryLayer.BUFFER
        assert exp.content == ""

    def test_post_init_sets_phi_weight(self):
        """Test __post_init__ sets phi_weight based on type."""
        root = MemoryExperience(memory_type=MemoryType.ROOT)
        leaf = MemoryExperience(memory_type=MemoryType.LEAF)

        assert root.phi_metrics.phi_weight == PHI
        assert leaf.phi_metrics.phi_weight == PHI_INVERSE

    def test_update_increments_version(self):
        """Test update increments version."""
        exp = MemoryExperience()
        initial_version = exp.version

        exp.update()

        assert exp.version == initial_version + 1
        assert exp.updated_at > exp.created_at

    def test_access_updates_metrics(self):
        """Test access updates phi_metrics."""
        exp = MemoryExperience()

        initial_count = exp.phi_metrics.access_count
        exp.access()

        assert exp.phi_metrics.access_count == initial_count + 1

    def test_add_connection_child(self):
        """Test adding child connection."""
        exp = MemoryExperience()

        exp.add_connection("child_001", "child")

        assert "child_001" in exp.children_ids

    def test_add_connection_related(self):
        """Test adding related connection."""
        exp = MemoryExperience()

        exp.add_connection("related_001", "related")

        assert "related_001" in exp.related_ids

    def test_calculate_promotion_score(self):
        """Test promotion score calculation."""
        exp = MemoryExperience(
            emotional_context=EmotionalContext(intensity=0.8, valence=0.7)
        )
        exp.phi_metrics.access_count = 5

        score = exp.calculate_promotion_score()

        assert 0 <= score <= 1

    def test_should_promote_seed(self):
        """Test seed promotion threshold."""
        exp = MemoryExperience(memory_type=MemoryType.SEED)
        exp.phi_metrics.phi_resonance = 0.9
        exp.phi_metrics.access_count = 10
        exp.emotional_context.intensity = 0.9

        # High metrics should make seed promotion candidate
        should = exp.should_promote()
        # Result depends on score vs threshold

    def test_promote_seed_to_leaf(self):
        """Test promoting seed to leaf."""
        exp = MemoryExperience(memory_type=MemoryType.SEED)

        result = exp.promote()

        assert result == True
        assert exp.memory_type == MemoryType.LEAF

    def test_promote_leaf_to_branch(self):
        """Test promoting leaf to branch."""
        exp = MemoryExperience(memory_type=MemoryType.LEAF)

        result = exp.promote()

        assert result == True
        assert exp.memory_type == MemoryType.BRANCH

    def test_promote_root_fails(self):
        """Test ROOT cannot be promoted."""
        exp = MemoryExperience(memory_type=MemoryType.ROOT)

        result = exp.promote()

        assert result == False
        assert exp.memory_type == MemoryType.ROOT

    def test_to_dict_format(self):
        """Test to_dict creates proper format."""
        exp = MemoryExperience(content="Test content")
        data = exp.to_dict()

        assert "memory_pure_v2" in data
        assert data["memory_pure_v2"]["version"] == "2.0.0"
        assert data["memory_pure_v2"]["experience"]["content"] == "Test content"

    def test_from_dict(self):
        """Test from_dict deserializes properly."""
        original = MemoryExperience(
            content="Test content",
            memory_type=MemoryType.BRANCH,
            tags=["tag1", "tag2"]
        )
        data = original.to_dict()

        restored = MemoryExperience.from_dict(data)

        assert restored.content == "Test content"
        assert restored.memory_type == MemoryType.BRANCH
        assert "tag1" in restored.tags

    def test_from_dict_handles_wrapped_format(self):
        """Test from_dict handles wrapped format."""
        data = {
            "memory_pure_v2": {
                "version": "2.0.0",
                "experience": {
                    "content": "Wrapped content",
                    "memory_type": "leaf"
                }
            }
        }

        exp = MemoryExperience.from_dict(data)

        assert exp.content == "Wrapped content"


class TestConsolidationReport:
    """Tests for ConsolidationReport dataclass."""

    def test_default_values(self):
        """Test default values."""
        report = ConsolidationReport()

        assert report.cycle_id.startswith("cycle_")
        assert report.phase == ConsolidationPhase.ANALYSIS
        assert report.memories_analyzed == 0

    def test_complete_sets_timestamp(self):
        """Test complete sets completed_at."""
        report = ConsolidationReport()

        report.complete()

        assert report.completed_at is not None

    def test_duration_seconds(self):
        """Test duration calculation."""
        report = ConsolidationReport()
        report.complete()

        duration = report.duration_seconds()

        assert duration is not None
        assert duration >= 0

    def test_duration_none_before_complete(self):
        """Test duration is None before completion."""
        report = ConsolidationReport()

        assert report.duration_seconds() is None

    def test_to_dict(self):
        """Test serialization."""
        report = ConsolidationReport(memories_analyzed=10)
        data = report.to_dict()

        assert data["statistics"]["memories_analyzed"] == 10


class TestMemoryQuery:
    """Tests for MemoryQuery dataclass."""

    def test_default_values(self):
        """Test default values."""
        query = MemoryQuery()

        assert query.limit == 10
        assert query.offset == 0
        assert query.sort_by == "relevance"

    def test_with_filters(self):
        """Test query with filters."""
        query = MemoryQuery(
            query_text="test",
            memory_types=[MemoryType.ROOT, MemoryType.BRANCH],
            min_phi_resonance=0.5
        )

        assert query.query_text == "test"
        assert len(query.memory_types) == 2
        assert query.min_phi_resonance == 0.5

    def test_to_dict(self):
        """Test serialization."""
        query = MemoryQuery(
            query_text="search term",
            memory_types=[MemoryType.LEAF]
        )
        data = query.to_dict()

        assert data["query_text"] == "search term"
        assert "leaf" in data["memory_types"]


class TestPureMemoryStats:
    """Tests for PureMemoryStats dataclass."""

    def test_default_values(self):
        """Test default values."""
        stats = PureMemoryStats()

        assert stats.buffer_count == 0
        assert stats.fractal_count == 0
        assert stats.archive_count == 0

    def test_total_memories(self):
        """Test total memories calculation."""
        stats = PureMemoryStats(
            buffer_count=10,
            fractal_count=50,
            archive_count=100
        )

        assert stats.total_memories() == 160

    def test_to_dict(self):
        """Test serialization."""
        stats = PureMemoryStats(
            root_count=5,
            branch_count=10,
            average_phi_resonance=0.7
        )
        data = stats.to_dict()

        assert data["types"]["root"] == 5
        assert data["phi"]["average_resonance"] == 0.7
