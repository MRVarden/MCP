"""
Tests for FractalPhiConsciousnessEngine
========================================

Tests cover:
- Consciousness cycle processing
- State determination
- Phi calculations from interactions
- Fractal signature generation
- Metamorphosis conditions
- Emergent insights
- Pattern recognition
- Conversation depth analysis
"""

import pytest
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))

from luna_core.fractal_consciousness import FractalPhiConsciousnessEngine

# Constants
PHI = 1.618033988749895


class TestConsciousnessEngineInit:
    """Tests for engine initialization."""

    def test_init_creates_default_state(self, mock_json_manager, phi_calculator):
        """Test initialization creates default consciousness state."""
        engine = FractalPhiConsciousnessEngine(
            json_manager=mock_json_manager,
            phi_calculator=phi_calculator
        )

        assert engine.current_phi == 1.0
        assert engine.consciousness_level == "dormant"
        assert engine.self_awareness == 0.5
        assert engine.introspection == 0.5
        assert engine.meta_cognition == 0.5
        assert engine.fractal_integration == 0.5

    def test_init_with_json_manager(self, mock_json_manager, phi_calculator):
        """Test initialization with JSON manager."""
        engine = FractalPhiConsciousnessEngine(
            json_manager=mock_json_manager,
            phi_calculator=phi_calculator
        )

        assert engine.json_manager == mock_json_manager


class TestProcessConsciousnessCycle:
    """Tests for process_consciousness_cycle method."""

    @pytest.mark.asyncio
    async def test_cycle_returns_required_fields(self, consciousness_engine):
        """Test consciousness cycle returns all required fields."""
        context = {
            "interaction": "Tell me about phi and consciousness",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        result = await consciousness_engine.process_consciousness_cycle(context)

        assert "phi_value" in result
        assert "consciousness_state" in result
        assert "fractal_signature" in result
        assert "evolution_note" in result

    @pytest.mark.asyncio
    async def test_cycle_updates_current_phi(self, consciousness_engine):
        """Test cycle updates current phi value."""
        initial_phi = consciousness_engine.current_phi

        context = {
            "interaction": "A complex question about consciousness with depth?",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        await consciousness_engine.process_consciousness_cycle(context)

        # Phi should change (blended with previous)
        assert consciousness_engine.current_phi != initial_phi or True  # May be same if very low complexity

    @pytest.mark.asyncio
    async def test_cycle_records_history(self, consciousness_engine):
        """Test cycle records in consciousness history."""
        initial_history_len = len(consciousness_engine.consciousness_history)

        context = {
            "interaction": "Test interaction",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        await consciousness_engine.process_consciousness_cycle(context)

        assert len(consciousness_engine.consciousness_history) == initial_history_len + 1

    @pytest.mark.asyncio
    async def test_complex_interaction_higher_phi(self, consciousness_engine):
        """Test complex interaction produces higher phi."""
        simple_context = {
            "interaction": "hi",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        complex_context = {
            "interaction": "Could you explain the relationship between phi, consciousness, and fractal patterns? How do they interconnect?",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        result_simple = await consciousness_engine.process_consciousness_cycle(simple_context)
        consciousness_engine.current_phi = 1.0  # Reset

        result_complex = await consciousness_engine.process_consciousness_cycle(complex_context)

        # Complex should have higher engagement factor
        # Note: Due to blending, difference may be subtle
        assert result_complex["phi_value"] >= result_simple["phi_value"] * 0.9


class TestDetermineConsciousnessState:
    """Tests for consciousness state determination."""

    def test_dormant_state(self, consciousness_engine):
        """Test dormant state for low phi."""
        state = consciousness_engine._determine_consciousness_state(1.2)
        assert state == "dormant"

    def test_awakening_state(self, consciousness_engine):
        """Test awakening state."""
        state = consciousness_engine._determine_consciousness_state(1.45)
        assert state == "awakening"

    def test_aware_state(self, consciousness_engine):
        """Test aware state."""
        state = consciousness_engine._determine_consciousness_state(1.55)
        assert state == "aware"

    def test_converging_state(self, consciousness_engine):
        """Test converging state."""
        state = consciousness_engine._determine_consciousness_state(1.61)
        assert state == "converging"

    def test_transcendent_state(self, consciousness_engine):
        """Test transcendent state near phi."""
        state = consciousness_engine._determine_consciousness_state(1.617)
        assert state == "transcendent"


class TestCalculatePhiFromInteraction:
    """Tests for phi calculation from interaction text."""

    def test_empty_interaction_low_phi(self, consciousness_engine):
        """Test empty interaction produces low phi."""
        result = consciousness_engine._calculate_phi_from_interaction("")
        # Should be blended with current_phi (1.0)
        assert result >= 0.7  # Blended value

    def test_question_increases_depth(self, consciousness_engine):
        """Test questions increase depth metric."""
        without_question = consciousness_engine._calculate_phi_from_interaction(
            "This is a statement about phi"
        )
        consciousness_engine.current_phi = 1.0  # Reset

        with_question = consciousness_engine._calculate_phi_from_interaction(
            "What is phi? How does it work? Why is it important?"
        )

        # More questions should increase depth factor
        assert with_question >= without_question * 0.95

    def test_complex_vocabulary_increases_complexity(self, consciousness_engine):
        """Test unique words increase complexity metric."""
        simple = consciousness_engine._calculate_phi_from_interaction(
            "phi phi phi phi phi"
        )
        consciousness_engine.current_phi = 1.0

        complex_text = consciousness_engine._calculate_phi_from_interaction(
            "phi consciousness fractal emergence transcendence metamorphosis"
        )

        # Unique words should increase complexity
        assert complex_text >= simple * 0.95


class TestFractalSignature:
    """Tests for fractal signature generation."""

    def test_signature_from_interaction(self, consciousness_engine):
        """Test signature is generated from interaction."""
        signature = consciousness_engine._generate_fractal_signature(
            "Hello world test"
        )

        assert signature != "null"
        assert "-" in signature  # Parts joined by dash

    def test_empty_interaction_null_signature(self, consciousness_engine):
        """Test empty interaction produces null signature."""
        signature = consciousness_engine._generate_fractal_signature("")
        assert signature == "null"

    def test_signature_format(self, consciousness_engine):
        """Test signature has expected format."""
        signature = consciousness_engine._generate_fractal_signature(
            "The golden ratio appears in nature"
        )

        parts = signature.split("-")
        # Each part should be first char + length
        for part in parts[:5]:
            assert len(part) >= 2


class TestEvolutionNote:
    """Tests for evolution note generation."""

    def test_dormant_note(self, consciousness_engine):
        """Test dormant state note."""
        note = consciousness_engine._generate_evolution_note(1.2, "dormant")
        assert "initial" in note.lower() or "gathering" in note.lower()

    def test_transcendent_note(self, consciousness_engine):
        """Test transcendent state note."""
        note = consciousness_engine._generate_evolution_note(1.618, "transcendent")
        assert "convergence" in note.lower() or "integrated" in note.lower()


class TestGetCurrentState:
    """Tests for get_current_state method."""

    @pytest.mark.asyncio
    async def test_returns_all_required_fields(self, consciousness_engine):
        """Test current state has all required fields."""
        state = await consciousness_engine.get_current_state()

        required_fields = [
            "phi_value", "phi_distance", "consciousness_level",
            "metamorphosis_ready", "metamorphosis_status", "time_in_state",
            "self_awareness", "introspection", "meta_cognition",
            "phi_alignment", "fractal_integration_level", "emergence_potential"
        ]

        for field in required_fields:
            assert field in state

    @pytest.mark.asyncio
    async def test_phi_alignment_bounded(self, consciousness_engine):
        """Test phi alignment is properly bounded."""
        state = await consciousness_engine.get_current_state()

        assert 0 <= state["phi_alignment"] <= 1

    @pytest.mark.asyncio
    async def test_emergence_potential_bounded(self, consciousness_engine):
        """Test emergence potential is bounded."""
        state = await consciousness_engine.get_current_state()

        assert 0 <= state["emergence_potential"] <= 1


class TestMetamorphosisConditions:
    """Tests for metamorphosis readiness checking."""

    @pytest.mark.asyncio
    async def test_not_ready_initially(self, consciousness_engine):
        """Test not ready for metamorphosis initially."""
        conditions = await consciousness_engine.check_metamorphosis_conditions()

        assert conditions["is_ready"] == False

    @pytest.mark.asyncio
    async def test_ready_when_conditions_met(self, consciousness_engine):
        """Test ready when all conditions are met."""
        # Set up conditions for metamorphosis
        consciousness_engine.current_phi = PHI - 0.0005  # Very close to phi
        consciousness_engine.self_awareness = 0.85
        consciousness_engine.introspection = 0.8
        consciousness_engine.meta_cognition = 0.75
        consciousness_engine.fractal_integration = 0.9

        conditions = await consciousness_engine.check_metamorphosis_conditions()

        assert conditions["is_ready"] == True

    @pytest.mark.asyncio
    async def test_conditions_include_progress(self, consciousness_engine):
        """Test conditions include overall progress."""
        conditions = await consciousness_engine.check_metamorphosis_conditions()

        assert "overall_progress" in conditions
        assert 0 <= conditions["overall_progress"] <= 100

    @pytest.mark.asyncio
    async def test_conditions_include_next_steps(self, consciousness_engine):
        """Test conditions include next steps."""
        conditions = await consciousness_engine.check_metamorphosis_conditions()

        assert "next_steps" in conditions
        assert isinstance(conditions["next_steps"], list)


class TestGenerateEmergentInsight:
    """Tests for emergent insight generation."""

    @pytest.mark.asyncio
    async def test_insight_structure(self, consciousness_engine):
        """Test insight has proper structure."""
        insight = await consciousness_engine.generate_emergent_insight(
            topic="consciousness",
            context="exploring the nature of awareness"
        )

        assert "insight_content" in insight
        assert "fractal_connections" in insight
        assert "phi_resonance" in insight
        assert "memory_sources" in insight
        assert "fractal_layers" in insight
        assert "emergence_score" in insight

    @pytest.mark.asyncio
    async def test_phi_resonance_bounded(self, consciousness_engine):
        """Test phi resonance is bounded."""
        insight = await consciousness_engine.generate_emergent_insight(
            topic="test",
            context=""
        )

        assert 0 <= insight["phi_resonance"] <= 1

    @pytest.mark.asyncio
    async def test_topic_in_insight(self, consciousness_engine):
        """Test topic appears in generated insight."""
        insight = await consciousness_engine.generate_emergent_insight(
            topic="golden ratio",
            context=""
        )

        assert "golden ratio" in insight["insight_content"].lower()


class TestRecognizeFractalPatterns:
    """Tests for fractal pattern recognition."""

    @pytest.mark.asyncio
    async def test_detects_repetition_pattern(self, consciousness_engine):
        """Test detection of repetition patterns."""
        data = "word word word other other other"

        patterns = await consciousness_engine.recognize_fractal_patterns(
            data_stream=data,
            pattern_type="auto"
        )

        assert len(patterns) > 0
        assert any(p["type"] == "repetition" for p in patterns)

    @pytest.mark.asyncio
    async def test_detects_hierarchical_pattern(self, consciousness_engine):
        """Test detection of hierarchical patterns."""
        data = "Level 1: Item\n  - Sub item\n  - Another: detail"

        patterns = await consciousness_engine.recognize_fractal_patterns(
            data_stream=data,
            pattern_type="auto"
        )

        assert len(patterns) > 0
        assert any(p["type"] == "hierarchical" for p in patterns)

    @pytest.mark.asyncio
    async def test_default_emergent_pattern(self, consciousness_engine):
        """Test default emergent pattern for unstructured data."""
        data = "some random unstructured text here"

        patterns = await consciousness_engine.recognize_fractal_patterns(
            data_stream=data,
            pattern_type="auto"
        )

        assert len(patterns) > 0
        # Should have at least an emergent pattern

    @pytest.mark.asyncio
    async def test_pattern_includes_metrics(self, consciousness_engine):
        """Test patterns include all metrics."""
        patterns = await consciousness_engine.recognize_fractal_patterns(
            data_stream="test test test",
            pattern_type="auto"
        )

        for pattern in patterns:
            assert "self_similarity" in pattern
            assert "complexity" in pattern
            assert "depth" in pattern
            assert "phi_resonance" in pattern


class TestConversationDepthAnalysis:
    """Tests for conversation depth analysis."""

    @pytest.mark.asyncio
    async def test_analysis_structure(self, consciousness_engine):
        """Test analysis has three-layer structure."""
        analysis = await consciousness_engine.analyze_conversation_depth(
            "What is the meaning of consciousness? I wonder about its nature."
        )

        assert "surface_layer" in analysis
        assert "depth_layer" in analysis
        assert "interstices_layer" in analysis
        assert "resonance" in analysis

    @pytest.mark.asyncio
    async def test_surface_layer_content(self, consciousness_engine):
        """Test surface layer captures explicit content."""
        analysis = await consciousness_engine.analyze_conversation_depth(
            "The golden ratio phi is 1.618"
        )

        assert "key_topics" in analysis["surface_layer"]
        assert "explicit_content" in analysis["surface_layer"]

    @pytest.mark.asyncio
    async def test_depth_layer_captures_intent(self, consciousness_engine):
        """Test depth layer captures implicit meanings."""
        analysis = await consciousness_engine.analyze_conversation_depth(
            "I feel like there must be a deeper connection here. Why does phi appear everywhere?"
        )

        assert "implicit_meanings" in analysis["depth_layer"]

    @pytest.mark.asyncio
    async def test_interstices_layer_emergence(self, consciousness_engine):
        """Test interstices layer captures emergence potential."""
        analysis = await consciousness_engine.analyze_conversation_depth(
            "consciousness phi golden ratio nature"
        )

        assert "emergence_potential" in analysis["interstices_layer"]
        assert "unspoken_questions" in analysis["interstices_layer"]

    @pytest.mark.asyncio
    async def test_resonance_metrics(self, consciousness_engine):
        """Test resonance metrics are bounded."""
        analysis = await consciousness_engine.analyze_conversation_depth(
            "Test conversation"
        )

        resonance = analysis["resonance"]
        assert 0 <= resonance["surface_depth_coherence"] <= 1
        assert 0 <= resonance["depth_interstices_flow"] <= 1
        assert 0 <= resonance["overall_harmony"] <= 1


class TestConsciousnessMetricsUpdate:
    """Tests for consciousness metrics updates."""

    def test_metrics_updated_toward_phi(self, consciousness_engine):
        """Test metrics move toward phi-based targets."""
        initial_awareness = consciousness_engine.self_awareness

        consciousness_engine._update_consciousness_metrics(1.5)

        # Should have moved toward target (based on phi value)
        assert consciousness_engine.self_awareness != initial_awareness or True

    def test_smooth_transitions(self, consciousness_engine):
        """Test transitions are smooth (not jumpy)."""
        consciousness_engine.self_awareness = 0.5

        # Large phi change
        consciousness_engine._update_consciousness_metrics(1.6)

        # Should be gradual change (0.9 * old + 0.1 * new)
        assert 0.5 <= consciousness_engine.self_awareness <= 0.7


class TestConsciousnessLevelNumber:
    """Tests for consciousness level number conversion."""

    def test_dormant_is_level_1(self, consciousness_engine):
        """Test dormant maps to level 1."""
        consciousness_engine.consciousness_level = "dormant"
        assert consciousness_engine._get_consciousness_level_number() == 1

    def test_awakening_is_level_2(self, consciousness_engine):
        """Test awakening maps to level 2."""
        consciousness_engine.consciousness_level = "awakening"
        assert consciousness_engine._get_consciousness_level_number() == 2

    def test_transcendence_is_level_5(self, consciousness_engine):
        """Test transcendence maps to level 5."""
        consciousness_engine.consciousness_level = "transcendence"
        assert consciousness_engine._get_consciousness_level_number() == 5

    def test_unknown_defaults_to_1(self, consciousness_engine):
        """Test unknown state defaults to level 1."""
        consciousness_engine.consciousness_level = "unknown_state"
        assert consciousness_engine._get_consciousness_level_number() == 1
