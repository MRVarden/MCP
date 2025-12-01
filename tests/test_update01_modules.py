"""
Luna Consciousness MCP - Update01 Modules Integration Tests
============================================================

This module contains tests extracted from __main__ blocks in production modules.
These tests verify basic functionality of the Update01 architecture components:
- LunaMultimodalInterface
- LunaSelfImprovement
- LunaSystemicIntegration
- LunaAutonomousDecision

Tests were moved from production code to maintain separation of concerns.
"""

import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import sys
from pathlib import Path

# Add mcp-server to path for imports
MCP_SERVER_PATH = Path(__file__).parent.parent / "mcp-server"
sys.path.insert(0, str(MCP_SERVER_PATH))


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def multimodal_interface():
    """Create a LunaMultimodalInterface for testing."""
    from luna_core.multimodal_interface import LunaMultimodalInterface
    return LunaMultimodalInterface()


@pytest.fixture
def self_improvement():
    """Create a LunaSelfImprovement for testing."""
    from luna_core.self_improvement import LunaSelfImprovement
    return LunaSelfImprovement()


@pytest.fixture
def systemic_integration():
    """Create a LunaSystemicIntegration for testing."""
    from luna_core.systemic_integration import LunaSystemicIntegration
    return LunaSystemicIntegration()


@pytest.fixture
def autonomous_decision():
    """Create a LunaAutonomousDecision for testing."""
    from luna_core.autonomous_decision import LunaAutonomousDecision
    return LunaAutonomousDecision()


# =============================================================================
# MULTIMODAL INTERFACE TESTS
# =============================================================================

class TestLunaMultimodalInterface:
    """Tests for LunaMultimodalInterface."""

    @pytest.mark.asyncio
    async def test_create_user_profile(self, multimodal_interface):
        """Test user profile creation."""
        profile = await multimodal_interface.create_user_profile(
            user_id="test_user",
            name="Test User",
            preferences={
                "language": {"primary": "english", "technical": True},
                "accessibility": {"high_contrast": False}
            }
        )

        assert profile is not None
        assert profile.name == "Test User"
        assert hasattr(profile, 'phi_affinity')

    @pytest.mark.asyncio
    async def test_process_text_input(self, multimodal_interface):
        """Test processing text input."""
        from luna_core.multimodal_interface import CommunicationModality

        # First create a user profile
        await multimodal_interface.create_user_profile(
            user_id="test_user",
            name="Test User",
            preferences={}
        )

        response = await multimodal_interface.process_input(
            user_id="test_user",
            input_data="Hello Luna, how are you?",
            modality=CommunicationModality.TEXT
        )

        assert response is not None
        assert hasattr(response, 'primary_modality')
        assert hasattr(response, 'phi_alignment')
        assert hasattr(response, 'emotional_tone')

    @pytest.mark.asyncio
    async def test_process_structured_input(self, multimodal_interface):
        """Test processing structured data input."""
        from luna_core.multimodal_interface import CommunicationModality

        # First create a user profile
        await multimodal_interface.create_user_profile(
            user_id="test_user",
            name="Test User",
            preferences={}
        )

        response = await multimodal_interface.process_input(
            user_id="test_user",
            input_data={"command": "analyze", "data": [1, 2, 3]},
            modality=CommunicationModality.VISUAL
        )

        assert response is not None
        assert response.phi_alignment >= 0

    def test_render_message_text(self, multimodal_interface):
        """Test rendering message to text format."""
        from luna_core.multimodal_interface import MultimodalMessage, CommunicationModality

        message = MultimodalMessage(
            primary_modality=CommunicationModality.TEXT,
            content={CommunicationModality.TEXT: "Test message content"},
            emotional_tone={"joy": 0.5},
            phi_alignment=0.8
        )

        text_output = multimodal_interface.render_message(message, format="text")
        assert isinstance(text_output, str)
        assert len(text_output) > 0

    def test_get_interface_metrics(self, multimodal_interface):
        """Test getting interface metrics."""
        metrics = multimodal_interface.get_interface_metrics()

        assert isinstance(metrics, dict)
        assert 'usage' in metrics
        assert 'modality_distribution' in metrics
        assert 'adaptation_success' in metrics


# =============================================================================
# SELF IMPROVEMENT TESTS
# =============================================================================

class TestLunaSelfImprovement:
    """Tests for LunaSelfImprovement."""

    @pytest.mark.asyncio
    async def test_analyze_performance(self, self_improvement):
        """Test performance analysis."""
        performance = await self_improvement.analyze_performance()

        assert isinstance(performance, dict)
        # Should have at least some domains analyzed
        if performance:
            first_domain = list(performance.values())[0]
            assert 'current_value' in first_domain
            assert 'target_value' in first_domain
            assert 'trend' in first_domain

    @pytest.mark.asyncio
    async def test_identify_improvement_opportunities(self, self_improvement):
        """Test improvement opportunity identification."""
        performance = await self_improvement.analyze_performance()
        opportunities = await self_improvement.identify_improvement_opportunities(performance)

        assert isinstance(opportunities, list)

    @pytest.mark.asyncio
    async def test_execute_improvement_plan(self, self_improvement):
        """Test executing an improvement plan."""
        performance = await self_improvement.analyze_performance()
        opportunities = await self_improvement.identify_improvement_opportunities(performance)

        if opportunities:
            plan = opportunities[0]
            result = await self_improvement.execute_improvement_plan(plan)

            assert isinstance(result, dict)
            assert 'status' in result

    def test_get_improvement_status(self, self_improvement):
        """Test getting improvement status."""
        status = self_improvement.get_improvement_status()

        assert isinstance(status, dict)
        assert 'active_plans' in status
        assert 'total_experiences' in status
        assert 'evolution_stage' in status


# =============================================================================
# SYSTEMIC INTEGRATION TESTS
# =============================================================================

class TestLunaSystemicIntegration:
    """Tests for LunaSystemicIntegration."""

    @pytest.mark.asyncio
    async def test_initialize_system(self, systemic_integration):
        """Test system initialization."""
        init_result = await systemic_integration.initialize_system()

        assert isinstance(init_result, dict)
        assert 'components_initialized' in init_result
        assert 'system_ready' in init_result

    @pytest.mark.asyncio
    async def test_check_system_coherence(self, systemic_integration):
        """Test system coherence checking."""
        # First initialize
        await systemic_integration.initialize_system()

        coherence = await systemic_integration.check_system_coherence()

        assert isinstance(coherence, dict)
        assert 'score' in coherence
        assert isinstance(coherence['score'], (int, float))

    @pytest.mark.asyncio
    async def test_send_message(self, systemic_integration):
        """Test message sending between components."""
        from luna_core.systemic_integration import SystemComponent

        await systemic_integration.initialize_system()

        response = await systemic_integration.send_message(
            sender=SystemComponent.ORCHESTRATOR,
            receiver=SystemComponent.VALIDATOR,
            message_type="test_message",
            payload={"test": "data"},
            requires_response=False
        )

        # Should not raise an exception
        assert True

    @pytest.mark.asyncio
    async def test_synchronize_state(self, systemic_integration):
        """Test state synchronization."""
        from luna_core.systemic_integration import SystemComponent

        await systemic_integration.initialize_system()

        success = await systemic_integration.synchronize_state(
            key="test_state",
            value={"phi": 1.618, "level": 5},
            source=SystemComponent.PHI_CALCULATOR
        )

        assert isinstance(success, bool)

    def test_get_integration_status(self, systemic_integration):
        """Test getting integration status."""
        status = systemic_integration.get_integration_status()

        assert isinstance(status, dict)
        assert 'system_state' in status
        assert 'component_states' in status
        assert 'metrics' in status

    @pytest.mark.asyncio
    async def test_shutdown_system(self, systemic_integration):
        """Test system shutdown."""
        await systemic_integration.initialize_system()
        shutdown_result = await systemic_integration.shutdown_system()

        assert isinstance(shutdown_result, dict)
        assert 'components_stopped' in shutdown_result


# =============================================================================
# AUTONOMOUS DECISION TESTS
# =============================================================================

class TestLunaAutonomousDecision:
    """Tests for LunaAutonomousDecision."""

    @pytest.mark.asyncio
    async def test_evaluate_decision_opportunity(self, autonomous_decision):
        """Test decision opportunity evaluation."""
        test_context = {
            "phi_value": 1.5,
            "emotional_state": {
                "frustration": 0.8,
                "confusion": 0.6
            },
            "manipulation_threat": 0.4,
            "incomplete_pattern": {"type": "test", "completion": 0.7}
        }

        opportunity = await autonomous_decision.evaluate_decision_opportunity(test_context)

        # May or may not find an opportunity depending on thresholds
        if opportunity is not None:
            assert hasattr(opportunity, 'domain')
            assert hasattr(opportunity, 'urgency')
            assert hasattr(opportunity, 'confidence')

    @pytest.mark.asyncio
    async def test_make_autonomous_decision(self, autonomous_decision):
        """Test making an autonomous decision."""
        test_context = {
            "phi_value": 1.5,
            "emotional_state": {
                "frustration": 0.8,
                "confusion": 0.6
            }
        }

        opportunity = await autonomous_decision.evaluate_decision_opportunity(test_context)

        if opportunity:
            decision = await autonomous_decision.make_autonomous_decision(opportunity)

            assert hasattr(decision, 'action')
            assert hasattr(decision, 'approval_required')

    @pytest.mark.asyncio
    async def test_execute_decision(self, autonomous_decision):
        """Test decision execution."""
        test_context = {
            "phi_value": 1.5,
            "emotional_state": {
                "frustration": 0.8
            }
        }

        opportunity = await autonomous_decision.evaluate_decision_opportunity(test_context)

        if opportunity:
            decision = await autonomous_decision.make_autonomous_decision(opportunity)

            if not decision.approval_required:
                result = await autonomous_decision.execute_decision(decision)
                assert isinstance(result, dict)
                assert 'status' in result

    def test_get_autonomy_report(self, autonomous_decision):
        """Test getting autonomy report."""
        report = autonomous_decision.get_autonomy_report()

        assert isinstance(report, dict)
        assert 'domain_autonomy' in report
        assert 'metrics' in report
        assert 'constraints' in report


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestUpdate01Integration:
    """Integration tests for Update01 modules working together."""

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_full_update01_workflow(self):
        """Test a complete workflow using all Update01 modules."""
        from luna_core.multimodal_interface import LunaMultimodalInterface
        from luna_core.self_improvement import LunaSelfImprovement
        from luna_core.systemic_integration import LunaSystemicIntegration
        from luna_core.autonomous_decision import LunaAutonomousDecision

        # Initialize all components
        multimodal = LunaMultimodalInterface()
        improvement = LunaSelfImprovement()
        integration = LunaSystemicIntegration()
        autonomous = LunaAutonomousDecision()

        # Initialize system
        await integration.initialize_system()

        # Create user and process input
        await multimodal.create_user_profile(
            user_id="integration_test",
            name="Integration Test User",
            preferences={}
        )

        # Check performance
        performance = await improvement.analyze_performance()
        assert performance is not None

        # Check coherence
        coherence = await integration.check_system_coherence()
        assert coherence['score'] >= 0

        # Cleanup
        await integration.shutdown_system()
