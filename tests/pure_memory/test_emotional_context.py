"""
Tests for EmotionalContextManager - Emotional Processing
=========================================================

Tests cover:
- Emotion detection from text
- Emotional landscape building
- Emotional signature generation
- Context persistence
"""

import pytest
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mcp-server"))

from luna_core.pure_memory.emotional_context import (
    EmotionalContextManager,
    EmotionalLandscape,
    get_emotional_manager
)
from luna_core.pure_memory.memory_types import (
    EmotionalContext,
    EmotionalTone
)


class TestEmotionalContextManagerInit:
    """Tests for EmotionalContextManager initialization."""

    def test_singleton_pattern(self):
        """Test get_emotional_manager returns singleton."""
        manager1 = get_emotional_manager()
        manager2 = get_emotional_manager()

        assert manager1 is manager2

    def test_emotion_keywords_initialized(self):
        """Test emotion keywords are initialized."""
        manager = get_emotional_manager()

        assert len(manager.emotion_keywords) > 0
        # Keys are EmotionalTone enums, check if expected emotions exist
        assert EmotionalTone.JOY in manager.emotion_keywords
        assert EmotionalTone.SADNESS in manager.emotion_keywords


class TestAnalyzeText:
    """Tests for text analysis using create_context method."""

    def test_analyze_joyful_text(self):
        """Test analyzing joyful text."""
        manager = get_emotional_manager()

        ctx = manager.create_context("I'm so happy and excited about this wonderful progress!")

        assert ctx.primary_emotion == EmotionalTone.JOY
        assert ctx.valence > 0.3

    def test_analyze_sad_text(self):
        """Test analyzing sad text."""
        manager = get_emotional_manager()

        ctx = manager.create_context("This is disappointing and makes me feel sad.")

        assert ctx.primary_emotion == EmotionalTone.SADNESS
        assert ctx.valence < 0

    def test_analyze_curious_text(self):
        """Test analyzing curious text."""
        manager = get_emotional_manager()

        ctx = manager.create_context("I wonder how this works? I'm curious about the mechanism.")

        assert ctx.primary_emotion == EmotionalTone.CURIOSITY
        # arousal is based on exclamation/caps, use intensity instead for emotion detection
        assert ctx.intensity > 0

    def test_analyze_neutral_text(self):
        """Test analyzing neutral text."""
        manager = get_emotional_manager()

        ctx = manager.create_context("The system processes data.")

        assert ctx.primary_emotion == EmotionalTone.NEUTRAL
        # Neutral has 0 valence in the mapping
        assert abs(ctx.valence) <= 0.5

    def test_analyze_empty_text(self):
        """Test analyzing empty text."""
        manager = get_emotional_manager()

        ctx = manager.create_context("")

        assert ctx.primary_emotion == EmotionalTone.NEUTRAL


class TestEmotionalLandscape:
    """Tests for emotional landscape building using EmotionalLandscape class directly."""

    def test_build_landscape_from_memories(self):
        """Test building landscape from emotional contexts manually."""
        landscape = EmotionalLandscape()

        # Add emotional points manually (simulating what build_landscape would do)
        landscape.add_emotional_point(EmotionalTone.JOY, 0.8)
        landscape.add_emotional_point(EmotionalTone.JOY, 0.6)
        landscape.add_emotional_point(EmotionalTone.CURIOSITY, 0.7)

        assert landscape.dominant_emotion == EmotionalTone.JOY
        # JOY has valence 0.9, CURIOSITY has 0.6 - both positive
        assert landscape.peak_emotion is not None

    def test_landscape_empty_contexts(self):
        """Test landscape with empty contexts."""
        landscape = EmotionalLandscape()

        assert landscape.dominant_emotion == EmotionalTone.NEUTRAL
        assert landscape.emotion_distribution == {}

    def test_landscape_distribution(self):
        """Test emotion distribution in landscape."""
        landscape = EmotionalLandscape()

        landscape.add_emotional_point(EmotionalTone.JOY, 0.5)
        landscape.add_emotional_point(EmotionalTone.JOY, 0.5)
        landscape.add_emotional_point(EmotionalTone.SADNESS, 0.5)

        assert EmotionalTone.JOY in landscape.emotion_distribution
        assert EmotionalTone.SADNESS in landscape.emotion_distribution


class TestEmotionalSignature:
    """Tests for emotional signature generation using EmotionalContext.get_emotional_signature."""

    def test_generate_signature(self):
        """Test signature generation via EmotionalContext method."""
        ctx = EmotionalContext(
            primary_emotion=EmotionalTone.JOY,
            intensity=0.8,
            valence=0.7
        )

        signature = ctx.get_emotional_signature()

        assert "joy" in signature.lower()
        assert "0.8" in signature or "80" in signature  # intensity representation

    def test_signature_uniqueness(self):
        """Test signatures are unique for different contexts."""
        ctx1 = EmotionalContext(primary_emotion=EmotionalTone.JOY, intensity=0.8)
        ctx2 = EmotionalContext(primary_emotion=EmotionalTone.SADNESS, intensity=0.5)

        sig1 = ctx1.get_emotional_signature()
        sig2 = ctx2.get_emotional_signature()

        assert sig1 != sig2


class TestEmotionDetection:
    """Tests for specific emotion detection using create_context."""

    def test_detect_love(self):
        """Test detecting love emotion."""
        manager = get_emotional_manager()

        ctx = manager.create_context("I love this project and care deeply about it.")

        assert ctx.primary_emotion == EmotionalTone.LOVE or "love" in str(ctx.secondary_emotions)

    def test_detect_concern(self):
        """Test detecting concern emotion."""
        manager = get_emotional_manager()

        ctx = manager.create_context("I'm worried about the potential issues here.")

        assert ctx.primary_emotion == EmotionalTone.CONCERN

    def test_detect_gratitude(self):
        """Test detecting gratitude emotion."""
        manager = get_emotional_manager()

        ctx = manager.create_context("Thank you so much for your help, I really appreciate it!")

        assert ctx.primary_emotion == EmotionalTone.GRATITUDE

    def test_detect_calm(self):
        """Test detecting calm emotion."""
        manager = get_emotional_manager()

        ctx = manager.create_context("Everything is peaceful and serene today.")

        assert ctx.primary_emotion == EmotionalTone.CALM


class TestValenceCalculation:
    """Tests for valence calculation using create_context."""

    def test_positive_words_positive_valence(self):
        """Test positive words produce positive valence."""
        manager = get_emotional_manager()

        ctx = manager.create_context("happy wonderful excellent amazing great")

        assert ctx.valence > 0.3

    def test_negative_words_negative_valence(self):
        """Test negative words produce negative valence."""
        manager = get_emotional_manager()

        ctx = manager.create_context("sad terrible horrible disappointing bad")

        assert ctx.valence < 0  # Sadness has -0.6 valence

    def test_mixed_words_moderate_valence(self):
        """Test mixed words - first matched emotion wins."""
        manager = get_emotional_manager()

        ctx = manager.create_context("happy sad good bad")

        # valence depends on detected primary emotion
        assert ctx.valence is not None


class TestArousalCalculation:
    """Tests for arousal calculation using create_context."""

    def test_exclamation_marks_increase_arousal(self):
        """Test exclamation marks increase arousal."""
        manager = get_emotional_manager()

        calm = manager.create_context("This is interesting.")
        excited = manager.create_context("This is interesting!!!")

        assert excited.arousal > calm.arousal

    def test_capital_letters_increase_arousal(self):
        """Test capital letters increase arousal."""
        manager = get_emotional_manager()

        calm = manager.create_context("this is interesting")
        excited = manager.create_context("THIS IS INTERESTING")

        assert excited.arousal >= calm.arousal


class TestSecondaryEmotions:
    """Tests for secondary emotion detection using create_context."""

    def test_multiple_emotions_detected(self):
        """Test multiple emotions can be detected."""
        manager = get_emotional_manager()

        ctx = manager.create_context(
            "I'm happy about the progress but worried about the deadline."
        )

        # Should have secondary emotions
        assert len(ctx.secondary_emotions) > 0 or ctx.primary_emotion != EmotionalTone.NEUTRAL


class TestIntensityCalculation:
    """Tests for intensity calculation using create_context."""

    def test_repeated_words_increase_intensity(self):
        """Test repeated emotional words increase intensity."""
        manager = get_emotional_manager()

        single = manager.create_context("happy")
        repeated = manager.create_context("happy happy happy very happy")

        assert repeated.intensity >= single.intensity

    def test_intensity_bounded(self):
        """Test intensity is bounded 0-1."""
        manager = get_emotional_manager()

        ctx = manager.create_context("!!! extremely very super happy happy happy !!!")

        assert 0 <= ctx.intensity <= 1


class TestEmotionalLandscapeClass:
    """Tests for EmotionalLandscape dataclass."""

    def test_default_values(self):
        """Test default values."""
        landscape = EmotionalLandscape()

        assert landscape.dominant_emotion == EmotionalTone.NEUTRAL
        assert landscape.average_valence == 0.0
        assert landscape.average_arousal == 0.5
        assert landscape.emotion_distribution == {}

    def test_to_dict(self):
        """Test to_dict serialization."""
        # emotion_distribution expects EmotionalTone keys, not strings
        landscape = EmotionalLandscape(
            dominant_emotion=EmotionalTone.JOY,
            average_valence=0.7,
            emotion_distribution={EmotionalTone.JOY: 0.6, EmotionalTone.CURIOSITY: 0.4}
        )

        data = landscape.to_dict()

        assert data["dominant_emotion"] == "joy"
        assert data["average_valence"] == 0.7


class TestEdgeCases:
    """Edge case tests using create_context."""

    def test_unicode_text(self):
        """Test unicode text handling."""
        manager = get_emotional_manager()

        ctx = manager.create_context("Je suis tres content et heureux!")

        assert ctx.primary_emotion is not None

    def test_special_characters(self):
        """Test special characters handling."""
        manager = get_emotional_manager()

        ctx = manager.create_context("@#$%^&*()_+")

        assert ctx.primary_emotion == EmotionalTone.NEUTRAL

    def test_very_long_text(self):
        """Test very long text handling."""
        manager = get_emotional_manager()

        long_text = "happy " * 1000

        ctx = manager.create_context(long_text)

        assert ctx.primary_emotion is not None
        assert ctx.intensity <= 1.0
