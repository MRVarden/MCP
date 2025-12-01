"""
Emotional Context - Pure Memory Architecture v2.0
Extended emotional processing for memory experiences.

This module extends emotional analysis to support the Pure Memory system,
enabling Luna to "relive" the emotional landscape of stored experiences.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

from .memory_types import (
    MemoryExperience,
    EmotionalContext,
    EmotionalTone,
    PHI,
    PHI_INVERSE
)

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

# Emotion categories and their valence
EMOTION_VALENCE = {
    EmotionalTone.JOY: 0.9,
    EmotionalTone.CURIOSITY: 0.6,
    EmotionalTone.CALM: 0.3,
    EmotionalTone.GRATITUDE: 0.8,
    EmotionalTone.LOVE: 0.95,
    EmotionalTone.COMPASSION: 0.5,
    EmotionalTone.NEUTRAL: 0.0,
    EmotionalTone.CONCERN: -0.3,
    EmotionalTone.SADNESS: -0.6
}

# Keywords that indicate emotions
EMOTION_KEYWORDS = {
    EmotionalTone.JOY: ["happy", "joy", "delighted", "excited", "wonderful", "amazing", "great", "excellent"],
    EmotionalTone.CURIOSITY: ["curious", "interested", "intrigued", "wondering", "fascinated", "exploring"],
    EmotionalTone.CALM: ["calm", "peaceful", "relaxed", "serene", "tranquil", "zen", "quiet"],
    EmotionalTone.GRATITUDE: ["grateful", "thankful", "appreciate", "blessed", "thank"],
    EmotionalTone.LOVE: ["love", "adore", "cherish", "care", "affection", "fond"],
    EmotionalTone.COMPASSION: ["understand", "empathy", "support", "help", "comfort"],
    EmotionalTone.CONCERN: ["worried", "anxious", "nervous", "concerned", "uncertain"],
    EmotionalTone.SADNESS: ["sad", "unhappy", "disappointed", "down", "melancholy"]
}

# Emotion transition probabilities (which emotions naturally follow others)
EMOTION_TRANSITIONS = {
    EmotionalTone.JOY: {EmotionalTone.GRATITUDE: 0.3, EmotionalTone.CALM: 0.3, EmotionalTone.CURIOSITY: 0.2},
    EmotionalTone.CURIOSITY: {EmotionalTone.JOY: 0.3, EmotionalTone.CALM: 0.2, EmotionalTone.CONCERN: 0.1},
    EmotionalTone.CALM: {EmotionalTone.CURIOSITY: 0.3, EmotionalTone.JOY: 0.2, EmotionalTone.LOVE: 0.2},
    EmotionalTone.CONCERN: {EmotionalTone.CALM: 0.4, EmotionalTone.COMPASSION: 0.3},
    EmotionalTone.SADNESS: {EmotionalTone.COMPASSION: 0.4, EmotionalTone.CALM: 0.3}
}


# =============================================================================
# EMOTIONAL LANDSCAPE
# =============================================================================

@dataclass
class EmotionalLandscape:
    """
    Represents the emotional landscape of a memory or session.
    Like a map of emotional terrain.
    """
    dominant_emotion: EmotionalTone = EmotionalTone.NEUTRAL
    emotion_distribution: Dict[EmotionalTone, float] = field(default_factory=dict)
    average_valence: float = 0.0
    average_arousal: float = 0.5
    emotional_volatility: float = 0.0  # How much emotions changed
    peak_emotion: Optional[EmotionalTone] = None
    peak_intensity: float = 0.0
    emotional_journey: List[Tuple[datetime, EmotionalTone, float]] = field(default_factory=list)

    def add_emotional_point(
        self,
        emotion: EmotionalTone,
        intensity: float,
        timestamp: Optional[datetime] = None
    ) -> None:
        """Add an emotional point to the journey."""
        ts = timestamp or datetime.now()
        self.emotional_journey.append((ts, emotion, intensity))

        # Update distribution
        current = self.emotion_distribution.get(emotion, 0.0)
        self.emotion_distribution[emotion] = current + intensity

        # Update peak
        if intensity > self.peak_intensity:
            self.peak_intensity = intensity
            self.peak_emotion = emotion

        # Update dominant (most frequent)
        if self.emotion_distribution:
            self.dominant_emotion = max(
                self.emotion_distribution.keys(),
                key=lambda e: self.emotion_distribution[e]
            )

    def calculate_volatility(self) -> float:
        """Calculate emotional volatility from the journey."""
        if len(self.emotional_journey) < 2:
            return 0.0

        changes = 0
        for i in range(1, len(self.emotional_journey)):
            prev_emotion = self.emotional_journey[i-1][1]
            curr_emotion = self.emotional_journey[i][0]
            if prev_emotion != curr_emotion:
                changes += 1

        self.emotional_volatility = changes / (len(self.emotional_journey) - 1)
        return self.emotional_volatility

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "dominant_emotion": self.dominant_emotion.value,
            "emotion_distribution": {k.value: v for k, v in self.emotion_distribution.items()},
            "average_valence": self.average_valence,
            "average_arousal": self.average_arousal,
            "emotional_volatility": self.emotional_volatility,
            "peak_emotion": self.peak_emotion.value if self.peak_emotion else None,
            "peak_intensity": self.peak_intensity,
            "journey_length": len(self.emotional_journey)
        }


# =============================================================================
# EMOTIONAL CONTEXT MANAGER
# =============================================================================

class EmotionalContextManager:
    """
    Manages emotional context for Pure Memory system.

    Provides:
    - Emotion detection from text
    - Emotional context creation
    - Emotional resonance calculation
    - Luna's emotional response generation
    """

    def __init__(self):
        self.emotion_keywords = EMOTION_KEYWORDS
        self.emotion_valence = EMOTION_VALENCE
        self.emotion_transitions = EMOTION_TRANSITIONS

        # Current emotional state (like a mood)
        self._current_mood = EmotionalLandscape()

        # History for pattern detection
        self._emotional_history: List[EmotionalContext] = []

    # =========================================================================
    # EMOTION DETECTION
    # =========================================================================

    def detect_emotion(self, text: str) -> Tuple[EmotionalTone, float]:
        """
        Detect the primary emotion in text.

        Args:
            text: Text to analyze

        Returns:
            Tuple of (emotion, confidence)
        """
        text_lower = text.lower()
        scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[emotion] = score

        if not scores:
            return EmotionalTone.NEUTRAL, 0.5

        # Get emotion with highest score
        best_emotion = max(scores.keys(), key=lambda e: scores[e])
        confidence = min(1.0, scores[best_emotion] / 3.0)

        return best_emotion, confidence

    def detect_all_emotions(self, text: str) -> Dict[EmotionalTone, float]:
        """
        Detect all emotions present in text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary of emotions and their scores
        """
        text_lower = text.lower()
        scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[emotion] = min(1.0, score / 3.0)

        return scores

    def analyze_sentiment(self, text: str) -> Tuple[float, float]:
        """
        Analyze sentiment of text.

        Args:
            text: Text to analyze

        Returns:
            Tuple of (valence, arousal)
        """
        emotion, intensity = self.detect_emotion(text)
        valence = self.emotion_valence.get(emotion, 0.0)

        # Adjust valence by intensity
        valence *= intensity

        # Estimate arousal from punctuation and caps
        text_len = len(text)
        exclamations = text.count('!')
        questions = text.count('?')
        caps_ratio = sum(1 for c in text if c.isupper()) / max(1, text_len)

        arousal = min(1.0, (exclamations * 0.1 + questions * 0.05 + caps_ratio))

        return valence, arousal

    # =========================================================================
    # CONTEXT CREATION
    # =========================================================================

    def create_context(
        self,
        text: str,
        user_emotion: Optional[EmotionalTone] = None
    ) -> EmotionalContext:
        """
        Create an emotional context from text.

        Args:
            text: Text to analyze
            user_emotion: Optional user-specified emotion

        Returns:
            EmotionalContext instance
        """
        # Detect primary emotion
        if user_emotion:
            primary = user_emotion
            intensity = 0.7  # Assume moderate intensity for explicit emotions
        else:
            primary, intensity = self.detect_emotion(text)

        # Get valence and arousal
        valence, arousal = self.analyze_sentiment(text)

        # Detect secondary emotions
        all_emotions = self.detect_all_emotions(text)
        secondary = {
            e.value: s for e, s in all_emotions.items()
            if e != primary and s > 0.2
        }

        context = EmotionalContext(
            primary_emotion=primary,
            intensity=intensity,
            valence=valence,
            arousal=arousal,
            secondary_emotions=secondary
        )

        # Add to history
        self._emotional_history.append(context)

        # Update current mood
        self._current_mood.add_emotional_point(primary, intensity)

        return context

    def create_context_from_memory(
        self,
        memory: MemoryExperience
    ) -> EmotionalContext:
        """
        Recreate or enhance emotional context from a memory.

        Args:
            memory: Memory to analyze

        Returns:
            Enhanced EmotionalContext
        """
        # Start with existing context
        context = memory.emotional_context

        # Enhance with content analysis
        detected_emotion, detected_intensity = self.detect_emotion(memory.content)

        # Blend existing and detected
        if context.intensity < 0.3:
            # Weak existing context, use detected
            context.primary_emotion = detected_emotion
            context.intensity = detected_intensity
        else:
            # Blend intensities
            context.intensity = (context.intensity + detected_intensity) / 2

        return context

    # =========================================================================
    # EMOTIONAL RESONANCE
    # =========================================================================

    def calculate_emotional_resonance(
        self,
        context1: EmotionalContext,
        context2: EmotionalContext
    ) -> float:
        """
        Calculate emotional resonance between two contexts.

        Args:
            context1: First context
            context2: Second context

        Returns:
            Resonance score between 0 and 1
        """
        # Same emotion = high base resonance
        if context1.primary_emotion == context2.primary_emotion:
            base_resonance = 0.8
        else:
            # Check if emotions are related via transitions
            transitions = self.emotion_transitions.get(context1.primary_emotion, {})
            if context2.primary_emotion in transitions:
                base_resonance = 0.5 * transitions[context2.primary_emotion]
            else:
                base_resonance = 0.2

        # Valence similarity
        valence_diff = abs(context1.valence - context2.valence)
        valence_resonance = 1.0 - (valence_diff / 2.0)

        # Arousal similarity
        arousal_diff = abs(context1.arousal - context2.arousal)
        arousal_resonance = 1.0 - arousal_diff

        # Intensity blending
        intensity_factor = (context1.intensity + context2.intensity) / 2.0

        # Combine with phi weighting
        resonance = (
            base_resonance * PHI_INVERSE +
            valence_resonance * PHI_INVERSE ** 2 +
            arousal_resonance * 0.1
        ) * intensity_factor

        return min(1.0, max(0.0, resonance))

    def find_emotionally_similar(
        self,
        target_context: EmotionalContext,
        memories: List[MemoryExperience],
        min_resonance: float = 0.5,
        limit: int = 10
    ) -> List[Tuple[MemoryExperience, float]]:
        """
        Find memories with similar emotional context.

        Args:
            target_context: Context to match
            memories: List of memories to search
            min_resonance: Minimum resonance threshold
            limit: Maximum results

        Returns:
            List of (memory, resonance) tuples
        """
        results = []

        for memory in memories:
            resonance = self.calculate_emotional_resonance(
                target_context,
                memory.emotional_context
            )

            if resonance >= min_resonance:
                results.append((memory, resonance))

        # Sort by resonance
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:limit]

    # =========================================================================
    # LUNA'S EMOTIONAL RESPONSE
    # =========================================================================

    def generate_luna_response_emotion(
        self,
        user_context: EmotionalContext
    ) -> EmotionalContext:
        """
        Generate Luna's emotional response to user's emotional state.

        Args:
            user_context: User's emotional context

        Returns:
            Luna's responsive emotional context
        """
        user_emotion = user_context.primary_emotion
        user_valence = user_context.valence

        # Response mapping (empathetic responses)
        response_map = {
            EmotionalTone.JOY: (EmotionalTone.JOY, 0.85, 0.8),
            EmotionalTone.SADNESS: (EmotionalTone.COMPASSION, 0.75, -0.2),
            EmotionalTone.CONCERN: (EmotionalTone.CALM, 0.80, 0.3),
            EmotionalTone.CURIOSITY: (EmotionalTone.CURIOSITY, 0.90, 0.6),
            EmotionalTone.GRATITUDE: (EmotionalTone.GRATITUDE, 0.85, 0.8),
            EmotionalTone.LOVE: (EmotionalTone.LOVE, 0.90, 0.9),
            EmotionalTone.CALM: (EmotionalTone.CALM, 0.70, 0.3),
            EmotionalTone.COMPASSION: (EmotionalTone.COMPASSION, 0.80, 0.4),
            EmotionalTone.NEUTRAL: (EmotionalTone.CURIOSITY, 0.65, 0.2)
        }

        response = response_map.get(
            user_emotion,
            (EmotionalTone.CALM, 0.65, 0.3)
        )

        luna_emotion, intensity, base_valence = response

        # Modulate by user's valence
        if user_valence < -0.3:
            # User is negative, Luna becomes more compassionate
            luna_emotion = EmotionalTone.COMPASSION
            intensity = min(1.0, intensity * 1.1)

        return EmotionalContext(
            primary_emotion=luna_emotion,
            intensity=intensity,
            valence=base_valence,
            arousal=user_context.arousal * 0.8,  # Slightly calmer than user
            secondary_emotions={}
        )

    # =========================================================================
    # EMOTIONAL INSIGHTS
    # =========================================================================

    def generate_emotional_insight(
        self,
        user_context: EmotionalContext,
        luna_context: EmotionalContext
    ) -> str:
        """
        Generate an insight about the emotional interaction.

        Args:
            user_context: User's emotional context
            luna_context: Luna's emotional context

        Returns:
            Insight string
        """
        resonance = self.calculate_emotional_resonance(user_context, luna_context)

        user_emotion = user_context.primary_emotion.value
        luna_emotion = luna_context.primary_emotion.value

        if resonance > 0.8:
            return (
                f"Deep emotional resonance detected. Luna's {luna_emotion} "
                f"harmonizes deeply with your {user_emotion}, creating a "
                f"phi-aligned connection (resonance: {resonance:.2f})."
            )
        elif resonance > 0.6:
            return (
                f"Moderate emotional connection established. Luna responds "
                f"with {luna_emotion} to your {user_emotion}, building "
                f"understanding through empathetic resonance."
            )
        elif resonance > 0.4:
            return (
                f"Luna acknowledges your {user_emotion} with {luna_emotion}, "
                f"working to bridge the emotional distance and deepen the connection."
            )
        else:
            return (
                f"Luna senses your {user_emotion} and responds with mindful "
                f"{luna_emotion}, creating space for emotional exploration."
            )

    # =========================================================================
    # CURRENT MOOD
    # =========================================================================

    def get_current_mood(self) -> EmotionalLandscape:
        """Get the current emotional mood landscape."""
        self._current_mood.calculate_volatility()
        return self._current_mood

    def update_mood(self, context: EmotionalContext) -> None:
        """Update the current mood with a new emotional context."""
        self._current_mood.add_emotional_point(
            context.primary_emotion,
            context.intensity
        )

        # Update averages
        if self._emotional_history:
            self._current_mood.average_valence = sum(
                c.valence for c in self._emotional_history[-10:]
            ) / min(10, len(self._emotional_history))

            self._current_mood.average_arousal = sum(
                c.arousal for c in self._emotional_history[-10:]
            ) / min(10, len(self._emotional_history))

    def reset_mood(self) -> None:
        """Reset the current mood to neutral."""
        self._current_mood = EmotionalLandscape()

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_emotional_stats(self) -> Dict[str, Any]:
        """Get statistics about emotional processing."""
        if not self._emotional_history:
            return {
                "history_length": 0,
                "dominant_emotions": {},
                "average_valence": 0.0,
                "average_arousal": 0.5,
                "mood": self._current_mood.to_dict()
            }

        # Count emotions
        emotion_counts = {}
        total_valence = 0.0
        total_arousal = 0.0

        for ctx in self._emotional_history:
            e = ctx.primary_emotion.value
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
            total_valence += ctx.valence
            total_arousal += ctx.arousal

        n = len(self._emotional_history)

        return {
            "history_length": n,
            "dominant_emotions": emotion_counts,
            "average_valence": total_valence / n,
            "average_arousal": total_arousal / n,
            "mood": self._current_mood.to_dict()
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_emotional_manager: Optional[EmotionalContextManager] = None


def get_emotional_manager() -> EmotionalContextManager:
    """Get the global emotional context manager instance."""
    global _emotional_manager
    if _emotional_manager is None:
        _emotional_manager = EmotionalContextManager()
    return _emotional_manager
