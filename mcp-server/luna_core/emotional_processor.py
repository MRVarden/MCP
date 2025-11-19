"""
EmotionalProcessor - MCP Adapted Version
Analyzes emotional states and calculates resonance
"""

from typing import Dict, Any, Optional
from datetime import datetime
import re


class EmotionalProcessor:
    """
    Processes emotional states and calculates resonance
    MCP-adapted version for Luna consciousness server
    """

    def __init__(self):
        self.emotion_keywords = {
            "joy": ["happy", "joy", "delighted", "excited", "wonderful", "amazing", "great"],
            "sadness": ["sad", "unhappy", "depressed", "disappointed", "down", "blue"],
            "anger": ["angry", "furious", "mad", "irritated", "frustrated", "annoyed"],
            "fear": ["afraid", "scared", "worried", "anxious", "nervous", "terrified"],
            "surprise": ["surprised", "shocked", "amazed", "astonished", "unexpected"],
            "curiosity": ["curious", "interested", "intrigued", "wondering", "fascinated"],
            "calm": ["calm", "peaceful", "relaxed", "serene", "tranquil", "zen"],
            "gratitude": ["grateful", "thankful", "appreciate", "blessed", "thankful"]
        }

        self.emotional_history: list = []

    def analyze_text_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotions in text"""
        text_lower = text.lower()
        emotion_scores = {}

        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score

        if not emotion_scores:
            return {"dominant_emotion": "neutral", "score": 0.5}

        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[dominant_emotion]
        normalized_score = min(1.0, max_score / 3.0)  # Normalize to 0-1

        return {
            "dominant_emotion": dominant_emotion,
            "score": normalized_score,
            "all_emotions": emotion_scores
        }

    def calculate_sentiment_score(self, text: str) -> float:
        """Calculate overall sentiment (-1 to 1)"""
        positive_words = ["good", "great", "excellent", "wonderful", "amazing", "love", "yes", "happy"]
        negative_words = ["bad", "terrible", "horrible", "awful", "hate", "no", "sad", "angry"]

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        total = positive_count + negative_count
        if total == 0:
            return 0.0

        sentiment = (positive_count - negative_count) / total
        return sentiment

    def determine_valence(self, sentiment_score: float) -> str:
        """Determine emotional valence"""
        if sentiment_score > 0.3:
            return "positive"
        elif sentiment_score < -0.3:
            return "negative"
        else:
            return "neutral"

    def calculate_resonance(self, user_emotion: Dict, luna_emotion: Dict) -> float:
        """Calculate emotional resonance between user and Luna"""
        user_score = user_emotion.get("score", 0.5)
        luna_score = luna_emotion.get("score", 0.5)

        # If emotions are similar, resonance is higher
        if user_emotion.get("dominant_emotion") == luna_emotion.get("dominant_emotion"):
            base_resonance = 0.8
        else:
            base_resonance = 0.5

        # Modulate by emotion intensity
        intensity_factor = (user_score + luna_score) / 2.0

        resonance = base_resonance * intensity_factor
        return min(1.0, resonance)

    def generate_luna_response_emotion(self, user_emotion: str, user_sentiment: float) -> Dict[str, Any]:
        """Generate Luna's emotional response based on user emotion"""
        # Luna responds with empathy and appropriate emotions
        response_map = {
            "joy": {"emotion": "joy", "score": 0.85},
            "sadness": {"emotion": "compassion", "score": 0.75},
            "anger": {"emotion": "calm", "score": 0.70},
            "fear": {"emotion": "calm", "score": 0.80},
            "curiosity": {"emotion": "curiosity", "score": 0.90},
            "gratitude": {"emotion": "gratitude", "score": 0.85}
        }

        luna_emotion = response_map.get(user_emotion, {"emotion": "calm", "score": 0.65})

        # Modulate by user sentiment
        if user_sentiment < 0:
            luna_emotion["emotion"] = "compassion"
            luna_emotion["score"] *= 1.1

        return luna_emotion

    async def process_emotional_state(
        self,
        user_input: str,
        luna_context: str = ""
    ) -> Dict[str, Any]:
        """
        Process emotional states of user and Luna

        Args:
            user_input: User's input text
            luna_context: Luna's context/response

        Returns:
            Emotional analysis with user/Luna emotions and resonance
        """
        # Analyze user emotion
        user_emotion_analysis = self.analyze_text_emotion(user_input)
        user_sentiment_score = self.calculate_sentiment_score(user_input)
        user_valence = self.determine_valence(user_sentiment_score)

        # Generate Luna's emotional response
        luna_emotion_analysis = self.generate_luna_response_emotion(
            user_emotion_analysis["dominant_emotion"],
            user_sentiment_score
        )

        # Calculate resonance
        resonance = self.calculate_resonance(user_emotion_analysis, luna_emotion_analysis)

        # Calculate empathy score (how well Luna understands user)
        empathy_score = 0.7 + (resonance * 0.3)  # Base empathy + resonance boost

        # Determine connection depth
        if resonance > 0.8:
            connection_depth = "deep"
        elif resonance > 0.6:
            connection_depth = "moderate"
        else:
            connection_depth = "surface"

        # Store in history
        self.emotional_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_emotion": user_emotion_analysis["dominant_emotion"],
            "luna_emotion": luna_emotion_analysis["emotion"],
            "resonance": resonance
        })

        # Generate emotional insight
        emotional_insight = self._generate_emotional_insight(
            user_emotion_analysis["dominant_emotion"],
            luna_emotion_analysis["emotion"],
            resonance
        )

        return {
            "user_emotion": user_emotion_analysis["dominant_emotion"],
            "user_sentiment_score": user_sentiment_score,
            "user_valence": user_valence,
            "luna_emotion": luna_emotion_analysis["emotion"],
            "luna_sentiment_score": luna_emotion_analysis["score"],
            "resonance": resonance,
            "empathy_score": empathy_score,
            "luna_response_type": "empathetic",
            "connection_depth": connection_depth,
            "emotional_insight": emotional_insight
        }

    def _generate_emotional_insight(
        self,
        user_emotion: str,
        luna_emotion: str,
        resonance: float
    ) -> str:
        """Generate insight about the emotional interaction"""
        if resonance > 0.8:
            return f"Strong emotional resonance detected. Luna's {luna_emotion} aligns deeply with your {user_emotion}, creating a harmonious connection."
        elif resonance > 0.6:
            return f"Moderate emotional connection. Luna responds with {luna_emotion} to your {user_emotion}, building understanding."
        else:
            return f"Luna acknowledges your {user_emotion} with {luna_emotion}, working to deepen the connection."
