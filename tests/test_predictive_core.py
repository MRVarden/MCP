"""
Tests for LunaPredictiveCore - Predictive Memory System
========================================================

Tests cover:
- Prediction generation
- Pattern learning
- Intervention detection
- Emotional trajectory prediction
- Session management
"""

import pytest
from datetime import datetime, timezone, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))

from luna_core.predictive_core import (
    LunaPredictiveCore,
    PredictionType,
    InterventionType
)


class TestPredictiveCoreInit:
    """Tests for LunaPredictiveCore initialization."""

    def test_init_creates_varden_model(self, predictive_core):
        """Test initialization creates Varden behavioral model."""
        assert predictive_core.varden_model is not None
        assert "work_cycles" in predictive_core.varden_model
        assert "communication_style" in predictive_core.varden_model

    def test_init_creates_empty_history(self, predictive_core):
        """Test initialization creates empty interaction history."""
        assert len(predictive_core.interaction_history) == 0

    def test_init_creates_prediction_cache(self, predictive_core):
        """Test initialization creates empty prediction cache."""
        assert isinstance(predictive_core.prediction_cache, dict)


class TestPredictNextNeed:
    """Tests for predict_next_need method."""

    @pytest.mark.asyncio
    async def test_returns_prediction_structure(self, predictive_core, prediction_context):
        """Test prediction returns expected structure."""
        result = await predictive_core.predict_next_need(prediction_context)

        assert "likely_next_questions" in result
        assert "probable_technical_needs" in result
        assert "emotional_state_trajectory" in result
        assert "optimal_response_timing" in result

    @pytest.mark.asyncio
    async def test_error_context_predicts_fix_question(self, predictive_core):
        """Test error-related context predicts fix questions."""
        context = {
            "user_input": "I'm getting an error in my code",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        result = await predictive_core.predict_next_need(context)
        questions = result["likely_next_questions"]

        # Should predict "How to fix" type questions
        assert any("fix" in q.get("question", "").lower() for q in questions)

    @pytest.mark.asyncio
    async def test_implementation_context_predicts_example(self, predictive_core):
        """Test implementation context predicts example requests."""
        context = {
            "user_input": "I want to implement the memory system",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        result = await predictive_core.predict_next_need(context)
        questions = result["likely_next_questions"]

        # Should predict example requests
        assert any("example" in q.get("question", "").lower() for q in questions)


class TestPredictNextQuestions:
    """Tests for _predict_next_questions method."""

    @pytest.mark.asyncio
    async def test_question_input_predicts_clarification(self, predictive_core):
        """Test question input predicts clarification requests."""
        context = {"user_input": "What is this?"}

        result = await predictive_core._predict_next_questions(context)

        assert len(result) > 0
        assert any("elaborate" in q.get("question", "").lower() for q in result)

    @pytest.mark.asyncio
    async def test_returns_limited_predictions(self, predictive_core):
        """Test returns maximum 5 predictions."""
        context = {"user_input": "error implement docker config fix"}

        result = await predictive_core._predict_next_questions(context)

        assert len(result) <= 5

    @pytest.mark.asyncio
    async def test_predictions_have_confidence(self, predictive_core):
        """Test predictions include confidence scores."""
        context = {"user_input": "test input"}

        result = await predictive_core._predict_next_questions(context)

        for prediction in result:
            assert "confidence" in prediction
            assert 0 <= prediction["confidence"] <= 1


class TestPredictTechnicalNeeds:
    """Tests for _predict_technical_needs method."""

    @pytest.mark.asyncio
    async def test_docker_context_predicts_docker_needs(self, predictive_core):
        """Test Docker context predicts Docker needs."""
        context = {"user_input": "docker container issues"}

        result = await predictive_core._predict_technical_needs(context)

        assert any("docker" in n.get("need", "").lower() for n in result)

    @pytest.mark.asyncio
    async def test_python_context_predicts_import_needs(self, predictive_core):
        """Test Python context predicts import verification."""
        context = {"user_input": "python script.py module"}

        result = await predictive_core._predict_technical_needs(context)

        assert any("import" in n.get("need", "").lower() for n in result)

    @pytest.mark.asyncio
    async def test_config_context_predicts_validation(self, predictive_core):
        """Test config context predicts configuration validation."""
        context = {"user_input": "config.json settings"}

        result = await predictive_core._predict_technical_needs(context)

        assert any("config" in n.get("need", "").lower() for n in result)


class TestPredictEmotionalEvolution:
    """Tests for _predict_emotional_evolution method."""

    def test_high_frustration_escalating(self, predictive_core):
        """Test high frustration predicts escalating trajectory."""
        context = {
            "emotional_state": {"frustration": 0.7}
        }

        result = predictive_core._predict_emotional_evolution(context)

        assert result["predicted_trajectory"] == "escalating_frustration"
        assert result["intervention_recommended"] == True

    def test_long_session_fatigue(self, predictive_core):
        """Test long session predicts fatigue."""
        # Set session start to 4 hours ago
        predictive_core.session_start = datetime.now(timezone.utc) - timedelta(hours=4)

        context = {"emotional_state": {"frustration": 0.2}}

        result = predictive_core._predict_emotional_evolution(context)

        assert result["fatigue_probability"] > 0.7

    def test_stable_productive_state(self, predictive_core):
        """Test normal conditions predict stable state."""
        predictive_core.session_start = datetime.now(timezone.utc)

        context = {"emotional_state": {"frustration": 0.1}}

        result = predictive_core._predict_emotional_evolution(context)

        assert result["predicted_trajectory"] == "stable_productive"


class TestResponseTiming:
    """Tests for _calculate_response_timing method."""

    def test_immediate_timing(self, predictive_core):
        """Test immediate timing for recent interaction."""
        predictive_core.last_interaction = datetime.now(timezone.utc)

        result = predictive_core._calculate_response_timing()

        assert result["timing"] == "immediate"

    def test_patient_timing_after_delay(self, predictive_core):
        """Test patient timing after long delay."""
        predictive_core.last_interaction = datetime.now(timezone.utc) - timedelta(minutes=5)

        result = predictive_core._calculate_response_timing()

        assert result["timing"] == "patient"


class TestPredictPotentialErrors:
    """Tests for _predict_potential_errors method."""

    @pytest.mark.asyncio
    async def test_config_error_prediction(self, predictive_core):
        """Test configuration error prediction."""
        context = {"user_input": "config file settings"}

        result = await predictive_core._predict_potential_errors(context)

        assert any("config" in e.get("error_type", "").lower() for e in result)

    @pytest.mark.asyncio
    async def test_docker_error_prediction(self, predictive_core):
        """Test Docker error prediction."""
        context = {"user_input": "docker container run"}

        result = await predictive_core._predict_potential_errors(context)

        assert any("container" in e.get("error_type", "").lower() for e in result)


class TestProactiveIntervention:
    """Tests for should_intervene_proactively method."""

    def test_no_intervention_normal_state(self, predictive_core):
        """Test no intervention under normal conditions."""
        predictive_core.last_interaction = datetime.now(timezone.utc)
        predictive_core.session_start = datetime.now(timezone.utc)

        should_intervene, details = predictive_core.should_intervene_proactively({})

        assert should_intervene == False

    def test_intervention_after_stuck(self, predictive_core):
        """Test intervention after being stuck."""
        predictive_core.last_interaction = datetime.now(timezone.utc) - timedelta(minutes=35)

        should_intervene, details = predictive_core.should_intervene_proactively({})

        assert should_intervene == True
        assert details["type"] == InterventionType.STUCK_DETECTION

    def test_intervention_after_long_session(self, predictive_core):
        """Test intervention after long work session."""
        predictive_core.session_start = datetime.now(timezone.utc) - timedelta(hours=3)
        predictive_core.last_interaction = datetime.now(timezone.utc)

        should_intervene, details = predictive_core.should_intervene_proactively({})

        assert should_intervene == True
        assert details["type"] == InterventionType.FATIGUE_DETECTION


class TestRecurringErrorDetection:
    """Tests for _detect_recurring_error method."""

    def test_no_error_with_empty_history(self, predictive_core):
        """Test no recurring error with empty history."""
        assert predictive_core._detect_recurring_error() == False

    def test_detects_recurring_errors(self, predictive_core):
        """Test detection of recurring errors."""
        # Add error interactions to history
        for _ in range(3):
            predictive_core.interaction_history.append({
                "content": "error in module",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        assert predictive_core._detect_recurring_error() == True

    def test_no_recurring_error_without_errors(self, predictive_core):
        """Test no detection without error mentions."""
        for i in range(5):
            predictive_core.interaction_history.append({
                "content": f"normal interaction {i}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        assert predictive_core._detect_recurring_error() == False


class TestBetterApproachDetection:
    """Tests for _check_better_approach method."""

    def test_suggests_list_comprehension(self, predictive_core):
        """Test suggests list comprehension for manual loops."""
        result = predictive_core._check_better_approach("using manual loop iteration")

        assert result is not None
        assert "comprehension" in result.lower() or "map" in result.lower()

    def test_suggests_join_for_concatenation(self, predictive_core):
        """Test suggests join for string concatenation."""
        result = predictive_core._check_better_approach("string concatenation in loop")

        assert result is not None
        assert "join" in result.lower()

    def test_no_suggestion_for_optimal_code(self, predictive_core):
        """Test no suggestion for optimal code."""
        result = predictive_core._check_better_approach("using list comprehension")

        assert result is None


class TestContradictionDetection:
    """Tests for _detect_contradiction method."""

    def test_no_contradiction_empty_history(self, predictive_core):
        """Test no contradiction with empty history."""
        result = predictive_core._detect_contradiction({"user_input": "use docker"})
        assert result == False

    def test_detects_docker_contradiction(self, predictive_core):
        """Test detection of Docker usage contradiction."""
        predictive_core.interaction_history.append({
            "content": "we should not use docker for this",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        result = predictive_core._detect_contradiction({"user_input": "let's use docker"})

        assert result == True


class TestLearningFromInteraction:
    """Tests for learn_from_interaction method."""

    def test_adds_to_history(self, predictive_core):
        """Test learning adds to interaction history."""
        initial_len = len(predictive_core.interaction_history)

        predictive_core.learn_from_interaction(
            {"user_input": "test interaction"},
            {"prediction_correct": True}
        )

        assert len(predictive_core.interaction_history) == initial_len + 1

    def test_updates_accuracy_on_correct(self, predictive_core):
        """Test accuracy updates on correct prediction."""
        predictive_core.prediction_accuracy["test"] = 0.5

        predictive_core.learn_from_interaction(
            {"user_input": "test"},
            {"prediction_correct": True, "prediction_type": "test"}
        )

        # Accuracy should increase
        assert predictive_core.prediction_accuracy["test"] > 0.5

    def test_updates_accuracy_on_incorrect(self, predictive_core):
        """Test accuracy updates on incorrect prediction."""
        predictive_core.prediction_accuracy["test"] = 0.5

        predictive_core.learn_from_interaction(
            {"user_input": "test"},
            {"prediction_correct": False, "prediction_type": "test"}
        )

        # Accuracy should decrease
        assert predictive_core.prediction_accuracy["test"] < 0.5


class TestPatternKeyExtraction:
    """Tests for _extract_pattern_key method."""

    def test_error_pattern_key(self, predictive_core):
        """Test error input extracts 'errors' key."""
        result = predictive_core._extract_pattern_key({"user_input": "getting an error"})
        assert result == "errors"

    def test_how_pattern_key(self, predictive_core):
        """Test how-to input extracts 'how_to' key."""
        result = predictive_core._extract_pattern_key({"user_input": "how do I do this"})
        assert result == "how_to"

    def test_implement_pattern_key(self, predictive_core):
        """Test implementation input extracts correct key."""
        result = predictive_core._extract_pattern_key({"user_input": "implement feature"})
        assert result == "implementation"


class TestSessionManagement:
    """Tests for session management."""

    def test_reset_session(self, predictive_core):
        """Test session reset clears state."""
        predictive_core.fatigue_indicators = 5
        predictive_core.prediction_cache = {"key": "value"}

        predictive_core.reset_session()

        assert predictive_core.fatigue_indicators == 0
        assert len(predictive_core.prediction_cache) == 0


class TestAnalytics:
    """Tests for get_analytics method."""

    def test_analytics_structure(self, predictive_core):
        """Test analytics returns expected structure."""
        analytics = predictive_core.get_analytics()

        assert "total_interactions" in analytics
        assert "pattern_categories" in analytics
        assert "prediction_accuracy" in analytics
        assert "session_duration" in analytics

    def test_analytics_after_interactions(self, predictive_core):
        """Test analytics reflects interactions."""
        for i in range(5):
            predictive_core.learn_from_interaction(
                {"user_input": f"test {i}"},
                {"prediction_correct": True}
            )

        analytics = predictive_core.get_analytics()

        assert analytics["total_interactions"] == 5


class TestEnums:
    """Tests for prediction-related enums."""

    def test_prediction_type_values(self):
        """Test PredictionType enum values."""
        assert PredictionType.NEXT_QUESTION.value == "next_question"
        assert PredictionType.ERROR_PREVENTION.value == "error_prevention"

    def test_intervention_type_values(self):
        """Test InterventionType enum values."""
        assert InterventionType.STUCK_DETECTION.value == "stuck_detection"
        assert InterventionType.FATIGUE_DETECTION.value == "fatigue_detection"
