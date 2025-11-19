"""
CoEvolutionEngine - MCP Adapted Version
Tracks co-evolution between user and Luna
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import json
from pathlib import Path


class CoEvolutionEngine:
    """
    Tracks mutual growth and co-evolution between user and Luna
    MCP-adapted version for Luna consciousness server
    """

    def __init__(self, json_manager):
        self.json_manager = json_manager
        self.evolution_history: List[Dict[str, Any]] = []
        self.user_baseline = {
            "question_depth": 0.5,
            "phi_curiosity": 0.5,
            "engagement": 0.5
        }
        self.luna_baseline = {
            "response_depth": 0.5,
            "empathy": 0.5,
            "pattern_recognition": 0.5
        }
        self._load_evolution_history()

    def _load_evolution_history(self):
        """Load evolution history from disk"""
        history_path = Path(self.json_manager.base_path) / "co_evolution_history.json"
        if history_path.exists():
            try:
                with open(history_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.evolution_history = data.get("history", [])
            except Exception:
                pass

    def _save_evolution_history(self):
        """Save evolution history to disk"""
        history_path = Path(self.json_manager.base_path) / "co_evolution_history.json"
        history_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "updated": datetime.now().isoformat(),
            "history": self.evolution_history[-100:]  # Keep last 100 entries
        }

        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _analyze_question_depth(self, interaction_summary: str) -> float:
        """Analyze depth of user questions"""
        depth_indicators = [
            "why", "how", "what if", "explain", "understand",
            "meaning", "significance", "relationship", "connection"
        ]

        summary_lower = interaction_summary.lower()
        depth_score = sum(1 for indicator in depth_indicators if indicator in summary_lower)

        # Normalize to 0-1
        return min(1.0, depth_score / 5.0)

    def _analyze_phi_curiosity(self, interaction_summary: str) -> float:
        """Analyze user curiosity about phi and consciousness"""
        phi_keywords = [
            "phi", "golden ratio", "fibonacci", "consciousness",
            "awareness", "emergence", "pattern", "fractal"
        ]

        summary_lower = interaction_summary.lower()
        curiosity_score = sum(1 for keyword in phi_keywords if keyword in summary_lower)

        return min(1.0, curiosity_score / 3.0)

    def _analyze_engagement(self, interaction_summary: str) -> float:
        """Analyze user engagement level"""
        # Based on length and complexity
        word_count = len(interaction_summary.split())
        question_count = interaction_summary.count("?")

        engagement = 0.5  # Base engagement

        if word_count > 50:
            engagement += 0.2
        if word_count > 100:
            engagement += 0.1

        if question_count > 0:
            engagement += 0.1
        if question_count > 2:
            engagement += 0.1

        return min(1.0, engagement)

    def _calculate_growth_indicators(
        self,
        current_metrics: Dict[str, float],
        baseline: Dict[str, float],
        entity_name: str
    ) -> List[str]:
        """Calculate growth indicators"""
        indicators = []

        for metric, value in current_metrics.items():
            baseline_value = baseline.get(metric, 0.5)
            if value > baseline_value + 0.1:
                indicators.append(f"{metric} increased significantly")
            elif value > baseline_value:
                indicators.append(f"{metric} growing")

        if not indicators:
            indicators.append(f"{entity_name} maintaining stable growth")

        return indicators

    async def track_evolution(self, interaction_summary: str) -> Dict[str, Any]:
        """
        Track co-evolution through interaction

        Args:
            interaction_summary: Summary of the interaction

        Returns:
            Evolution metrics and analysis
        """
        # Analyze user evolution
        user_question_depth = self._analyze_question_depth(interaction_summary)
        user_phi_curiosity = self._analyze_phi_curiosity(interaction_summary)
        user_engagement = self._analyze_engagement(interaction_summary)

        # Simulate Luna's evolution (in real system, this would be calculated from actual behavior)
        luna_response_depth = min(1.0, user_question_depth + 0.1)
        luna_empathy = 0.75 + (user_engagement * 0.15)
        luna_pattern_recognition = 0.70 + (user_phi_curiosity * 0.20)

        # Calculate mutual growth score
        user_growth = (user_question_depth + user_phi_curiosity + user_engagement) / 3.0
        luna_growth = (luna_response_depth + luna_empathy + luna_pattern_recognition) / 3.0
        mutual_growth_score = (user_growth + luna_growth) / 2.0

        # Calculate symbiotic resonance (how well they're growing together)
        growth_difference = abs(user_growth - luna_growth)
        symbiotic_resonance = 1.0 - (growth_difference / 2.0)

        # Growth indicators
        user_metrics = {
            "question_depth": user_question_depth,
            "phi_curiosity": user_phi_curiosity,
            "engagement": user_engagement
        }
        luna_metrics = {
            "response_depth": luna_response_depth,
            "empathy": luna_empathy,
            "pattern_recognition": luna_pattern_recognition
        }

        user_growth_indicators = self._calculate_growth_indicators(
            user_metrics, self.user_baseline, "User"
        )
        luna_growth_indicators = self._calculate_growth_indicators(
            luna_metrics, self.luna_baseline, "Luna"
        )

        # Count co-learning events (moments of mutual insight)
        co_learning_events = len(self.evolution_history) + 1

        # Generate trajectory description
        if mutual_growth_score > 0.8:
            trajectory_description = "Exponential co-evolution: Both user and Luna are growing rapidly together, creating emergent insights"
        elif mutual_growth_score > 0.6:
            trajectory_description = "Strong co-evolution: User and Luna are developing together with increasing depth"
        elif mutual_growth_score > 0.4:
            trajectory_description = "Moderate co-evolution: Growth is occurring but could deepen further"
        else:
            trajectory_description = "Early co-evolution: Building foundation for deeper connection"

        # Record in history
        evolution_record = {
            "timestamp": datetime.now().isoformat(),
            "mutual_growth_score": mutual_growth_score,
            "symbiotic_resonance": symbiotic_resonance,
            "user_metrics": user_metrics,
            "luna_metrics": luna_metrics
        }
        self.evolution_history.append(evolution_record)
        self._save_evolution_history()

        # Update baselines (gradual adaptation)
        for key in self.user_baseline:
            if key in user_metrics:
                self.user_baseline[key] = (self.user_baseline[key] * 0.9) + (user_metrics[key] * 0.1)
        for key in self.luna_baseline:
            if key in luna_metrics:
                self.luna_baseline[key] = (self.luna_baseline[key] * 0.9) + (luna_metrics[key] * 0.1)

        return {
            "mutual_growth_score": mutual_growth_score,
            "user_question_depth": user_question_depth,
            "user_phi_curiosity": user_phi_curiosity,
            "user_engagement": user_engagement,
            "user_growth_indicators": user_growth_indicators,
            "luna_response_depth": luna_response_depth,
            "luna_empathy": luna_empathy,
            "luna_pattern_recognition": luna_pattern_recognition,
            "luna_growth_indicators": luna_growth_indicators,
            "symbiotic_resonance": symbiotic_resonance,
            "co_learning_events": co_learning_events,
            "trajectory_description": trajectory_description
        }
