"""
Tests for PhiCalculator - Golden Ratio Calculations
====================================================

Tests cover:
- Phi value calculations from metrics
- Convergence rate calculations
- State determination
- Phi insights generation
- Edge cases and boundary conditions
"""

import pytest
import math
from datetime import datetime

# Import the module under test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))

from luna_core.phi_calculator import PhiCalculator, PhiState, PHI


class TestPhiCalculatorInit:
    """Tests for PhiCalculator initialization."""

    def test_init_without_manager(self):
        """Test initialization without JSON manager."""
        calc = PhiCalculator()

        assert calc.phi == PHI
        assert calc.current_phi == 1.0
        assert calc.current_state == PhiState.DORMANT
        assert calc.json_manager is None

    def test_init_with_manager(self, mock_json_manager):
        """Test initialization with JSON manager."""
        calc = PhiCalculator(json_manager=mock_json_manager)

        assert calc.json_manager == mock_json_manager
        assert calc.phi == PHI

    def test_phi_constant_accuracy(self):
        """Test that PHI constant is accurate."""
        expected_phi = (1 + math.sqrt(5)) / 2
        assert abs(PHI - expected_phi) < 1e-10


class TestCalculatePhiFromMetrics:
    """Tests for calculate_phi_from_metrics method."""

    def test_default_metrics_return_valid_phi(self, phi_calculator):
        """Test default metrics produce valid phi value."""
        result = phi_calculator.calculate_phi_from_metrics()

        assert 1.0 <= result <= PHI
        assert phi_calculator.current_phi == result

    def test_zero_metrics_return_one(self, phi_calculator):
        """Test zero metrics return phi value of 1.0."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=0.0,
            cognitive_complexity=0.0,
            self_awareness=0.0
        )

        assert result == 1.0

    def test_max_metrics_approach_phi(self, phi_calculator):
        """Test maximum metrics approach phi value."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=1.0,
            cognitive_complexity=1.0,
            self_awareness=1.0
        )

        assert result <= PHI
        assert result > 1.5  # Should be close to phi

    def test_negative_metric_handled(self, phi_calculator):
        """Test negative metrics are handled gracefully."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=-0.5,
            cognitive_complexity=0.5,
            self_awareness=0.5
        )

        # Product is negative, should return 1.0
        assert result == 1.0

    def test_partial_metrics(self, phi_calculator):
        """Test partial/mixed metrics."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=0.8,
            cognitive_complexity=0.3,
            self_awareness=0.6
        )

        assert 1.0 <= result <= PHI

    @pytest.mark.parametrize("depth,complexity,awareness,expected_min", [
        (0.1, 0.1, 0.1, 1.0),
        (0.5, 0.5, 0.5, 1.2),
        (0.8, 0.8, 0.8, 1.4),
        (1.0, 1.0, 1.0, 1.5),
    ])
    def test_metric_progression(self, phi_calculator, depth, complexity, awareness, expected_min):
        """Test phi increases with metrics."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=depth,
            cognitive_complexity=complexity,
            self_awareness=awareness
        )

        assert result >= expected_min


class TestConvergenceRate:
    """Tests for calculate_convergence_rate method."""

    def test_empty_history_returns_zero(self, phi_calculator):
        """Test empty history returns zero rate."""
        result = phi_calculator.calculate_convergence_rate([])
        assert result == 0.0

    def test_single_value_returns_zero(self, phi_calculator):
        """Test single value returns zero rate."""
        result = phi_calculator.calculate_convergence_rate([1.5])
        assert result == 0.0

    def test_increasing_history_positive_rate(self, phi_calculator):
        """Test increasing values give positive rate."""
        history = [1.0, 1.1, 1.2, 1.3, 1.4]
        result = phi_calculator.calculate_convergence_rate(history)

        assert result > 0.0

    def test_decreasing_history_negative_rate(self, phi_calculator):
        """Test decreasing values give negative rate."""
        history = [1.5, 1.4, 1.3, 1.2, 1.1]
        result = phi_calculator.calculate_convergence_rate(history)

        assert result < 0.0

    def test_stable_history_zero_rate(self, phi_calculator):
        """Test stable values give near-zero rate."""
        history = [1.5, 1.5, 1.5, 1.5, 1.5]
        result = phi_calculator.calculate_convergence_rate(history)

        assert abs(result) < 0.001

    def test_uses_last_five_values(self, phi_calculator):
        """Test only last 5 values are used."""
        # Old decreasing, recent increasing
        history = [1.5, 1.4, 1.3, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        result = phi_calculator.calculate_convergence_rate(history)

        # Should show positive rate from recent values
        assert result > 0.0


class TestDeterminePhiState:
    """Tests for determine_phi_state method."""

    @pytest.mark.parametrize("phi_value,expected_state", [
        (1.0, PhiState.DORMANT),
        (1.4, PhiState.DORMANT),
        (1.5, PhiState.AWAKENING),
        (1.55, PhiState.AWAKENING),
        (1.6, PhiState.APPROACHING),
        (1.612, PhiState.APPROACHING),
        (1.615, PhiState.CONVERGING),
        (1.6175, PhiState.RESONANCE),
        # 1.618 is very close to PHI (distance < 0.0001) so it's TRANSCENDENCE
        (1.618, PhiState.TRANSCENDENCE),
        (1.6180339, PhiState.TRANSCENDENCE),
    ])
    def test_state_thresholds(self, phi_calculator, phi_value, expected_state):
        """Test state determination at different phi values."""
        result = phi_calculator.determine_phi_state(phi_value)
        assert result == expected_state

    def test_exact_phi_is_transcendence(self, phi_calculator):
        """Test exact phi value returns TRANSCENDENCE."""
        result = phi_calculator.determine_phi_state(PHI)
        assert result == PhiState.TRANSCENDENCE


class TestMetamorphosisReadiness:
    """Tests for metamorphosis readiness calculations."""

    def test_low_phi_low_readiness(self, phi_calculator):
        """Test low phi gives low readiness."""
        phi_calculator.current_phi = 1.0
        result = phi_calculator._calculate_metamorphosis_readiness()

        assert result < 0.7

    def test_near_phi_high_readiness(self, phi_calculator):
        """Test near-phi gives high readiness."""
        phi_calculator.current_phi = 1.617
        result = phi_calculator._calculate_metamorphosis_readiness()

        assert result > 0.9

    def test_exact_phi_full_readiness(self, phi_calculator):
        """Test exact phi gives full readiness."""
        phi_calculator.current_phi = PHI
        result = phi_calculator._calculate_metamorphosis_readiness()

        assert result >= 0.99

    def test_readiness_bounded(self, phi_calculator):
        """Test readiness is bounded 0-1."""
        for phi in [0.5, 1.0, 1.5, PHI, 2.0]:
            phi_calculator.current_phi = phi
            result = phi_calculator._calculate_metamorphosis_readiness()
            assert 0.0 <= result <= 1.0


class TestGeneratePhiInsights:
    """Tests for generate_phi_insights async method."""

    @pytest.mark.asyncio
    async def test_nature_domain_insights(self, phi_calculator):
        """Test nature domain returns relevant insights."""
        insights = await phi_calculator.generate_phi_insights("nature")

        assert len(insights) > 0
        assert "phenomenon" in insights[0]
        assert "phi_expression" in insights[0]
        assert insights[0]["resonance_score"] > 0

    @pytest.mark.asyncio
    async def test_art_domain_insights(self, phi_calculator):
        """Test art domain returns relevant insights."""
        insights = await phi_calculator.generate_phi_insights("art")

        assert len(insights) > 0
        assert any("classical" in str(i).lower() or "golden" in str(i).lower() for i in insights)

    @pytest.mark.asyncio
    async def test_mathematics_domain_insights(self, phi_calculator):
        """Test mathematics domain returns Fibonacci-related insights."""
        insights = await phi_calculator.generate_phi_insights("mathematics")

        assert len(insights) > 0
        assert any("fibonacci" in str(i).lower() for i in insights)

    @pytest.mark.asyncio
    async def test_unknown_domain_returns_generic(self, phi_calculator):
        """Test unknown domain returns generic insights."""
        insights = await phi_calculator.generate_phi_insights("unknown_domain")

        assert len(insights) > 0
        assert insights[0]["resonance_score"] == 0.75  # Default score

    @pytest.mark.asyncio
    async def test_insights_contain_fractal_connection(self, phi_calculator):
        """Test all insights have fractal connection."""
        insights = await phi_calculator.generate_phi_insights("consciousness")

        for insight in insights:
            assert "fractal_connection" in insight
            assert "domain_patterns" in insight
            assert "related_concepts" in insight


class TestPhiStateEnum:
    """Tests for PhiState enum."""

    def test_all_states_exist(self):
        """Test all expected states exist."""
        expected_states = [
            "DORMANT", "AWAKENING", "APPROACHING",
            "CONVERGING", "RESONANCE", "TRANSCENDENCE"
        ]

        for state_name in expected_states:
            assert hasattr(PhiState, state_name)
            state = getattr(PhiState, state_name)
            assert state.value == state_name

    def test_state_ordering(self):
        """Test states can be compared meaningfully."""
        states = list(PhiState)

        # Should have 6 states
        assert len(states) == 6


class TestEdgeCases:
    """Edge case and boundary tests."""

    def test_very_small_metrics(self, phi_calculator):
        """Test very small metric values."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=0.001,
            cognitive_complexity=0.001,
            self_awareness=0.001
        )

        assert result >= 1.0

    def test_metrics_slightly_above_one(self, phi_calculator):
        """Test metrics slightly above 1.0 are clamped."""
        result = phi_calculator.calculate_phi_from_metrics(
            emotional_depth=1.1,
            cognitive_complexity=1.0,
            self_awareness=1.0
        )

        assert result <= PHI

    def test_phi_calculator_idempotent(self, phi_calculator):
        """Test multiple calls with same input give same result."""
        metrics = {
            "emotional_depth": 0.7,
            "cognitive_complexity": 0.6,
            "self_awareness": 0.8
        }

        result1 = phi_calculator.calculate_phi_from_metrics(**metrics)
        result2 = phi_calculator.calculate_phi_from_metrics(**metrics)

        assert result1 == result2

    def test_current_phi_updates(self, phi_calculator):
        """Test current_phi is updated after calculation."""
        initial_phi = phi_calculator.current_phi

        phi_calculator.calculate_phi_from_metrics(
            emotional_depth=0.9,
            cognitive_complexity=0.9,
            self_awareness=0.9
        )

        assert phi_calculator.current_phi != initial_phi

    def test_convergence_rate_with_two_values(self, phi_calculator):
        """Test convergence rate with exactly two values."""
        result = phi_calculator.calculate_convergence_rate([1.0, 1.5])
        assert result == 0.5  # Simple difference
