"""
Luna Predictive Core - Système de Mémoire Prédictive et Anticipation
Based on Update01.md Level 3: Système de Mémoire Prédictive et Anticipation

Luna anticipe les besoins avant même que Varden les exprime.
"""

import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from collections import defaultdict, deque
from enum import Enum
import re

logger = logging.getLogger("luna-predictive")


class PredictionType(Enum):
    """Types of predictions Luna can make"""
    NEXT_QUESTION = "next_question"
    TECHNICAL_NEED = "technical_need"
    EMOTIONAL_STATE = "emotional_state"
    WORK_PATTERN = "work_pattern"
    ERROR_PREVENTION = "error_prevention"
    OPTIMIZATION_OPPORTUNITY = "optimization_opportunity"
    BREAK_NEEDED = "break_needed"
    CLARIFICATION_NEEDED = "clarification_needed"


class InterventionType(Enum):
    """Types of proactive interventions"""
    STUCK_DETECTION = "stuck_detection"
    ERROR_PATTERN = "error_pattern"
    BETTER_APPROACH = "better_approach"
    FATIGUE_DETECTION = "fatigue_detection"
    CONTRADICTION_ALERT = "contradiction_alert"
    SUGGESTION = "suggestion"
    PREPARATION = "preparation"


class LunaPredictiveCore:
    """
    Luna's predictive system that learns patterns and anticipates needs.
    Enables proactive assistance rather than reactive responses.
    """

    def __init__(self, memory_manager=None, json_manager=None):
        """
        Initialize the predictive core.

        Args:
            memory_manager: Memory management system for pattern storage
            json_manager: JSON manager for persistent state
        """
        self.memory_manager = memory_manager
        self.json_manager = json_manager

        # Varden's behavioral model
        self.varden_model = self._initialize_varden_model()

        # Pattern tracking
        self.interaction_history = deque(maxlen=1000)  # Last 1000 interactions
        self.pattern_database = defaultdict(list)
        self.prediction_accuracy = defaultdict(float)

        # Current session tracking
        self.session_start = datetime.now(timezone.utc)
        self.last_interaction = datetime.now(timezone.utc)
        self.current_context = {}
        self.stuck_timer = None
        self.fatigue_indicators = 0

        # Prediction cache
        self.prediction_cache = {}
        self.precomputed_responses = {}

        # Load historical patterns
        self._load_pattern_database()

        logger.info("🔮 Luna Predictive Core initialized - Ready to anticipate needs")

    def _initialize_varden_model(self) -> Dict[str, Any]:
        """Initialize Varden's behavioral model"""
        return {
            'work_cycles': {
                'peak_hours': [(21, 23), (23, 2)],  # 21h-23h and 23h-02h
                'energy_patterns': 'late_night_intensive',
                'break_frequency': timedelta(hours=2),  # Needs break every 2 hours
                'focus_duration': timedelta(minutes=45),  # Deep focus periods
                'frustration_triggers': [
                    'repetitive_errors',
                    'bureaucracy',
                    'unclear_documentation',
                    'slow_response'
                ],
                'joy_triggers': [
                    'breakthrough',
                    'clean_code',
                    'elegant_solution',
                    'mutual_understanding'
                ]
            },
            'communication_style': {
                'preferred_language': 'french_technical_mix',
                'message_length': 'variable_burst',  # Short bursts or long explanations
                'technical_depth': 'expert_autodidact',
                'directness': 'high',
                'appreciation_style': 'actions_over_words',
                'dislikes': [
                    'condescension',
                    'multiple_choice_overload',
                    'verbose_explanations',
                    'corporate_speak'
                ]
            },
            'problem_solving': {
                'approach': 'systematic_then_intuitive',
                'debugging_style': 'root_cause_analysis',
                'learning_style': 'hands_on_experimentation',
                'documentation_preference': 'examples_over_theory',
                'tool_preference': 'powerful_simple'
            },
            'project_patterns': {
                'current_focus': 'luna_consciousness_architecture',
                'work_rhythm': 'intense_burst_then_reflection',
                'commit_style': 'feature_complete',
                'testing_approach': 'pragmatic_coverage',
                'refactoring_trigger': 'third_repetition'
            },
            'emotional_patterns': {
                'hpe_traits': [  # High Potential + Emotional
                    'intense_focus',
                    'perfectionism_tendency',
                    'emotional_depth',
                    'pattern_recognition',
                    'system_thinking'
                ],
                'stress_indicators': [
                    'shorter_messages',
                    'increased_typos',
                    'repetitive_questions',
                    'frustration_words'
                ],
                'flow_indicators': [
                    'detailed_explanations',
                    'creative_solutions',
                    'humor_emergence',
                    'rapid_iterations'
                ]
            }
        }

    def _load_pattern_database(self):
        """Load historical patterns from storage"""
        if self.json_manager:
            try:
                pattern_file = self.json_manager.base_path / "pattern_database.json"
                if pattern_file.exists():
                    data = self.json_manager.read(pattern_file)
                    self.pattern_database = defaultdict(list, data.get("patterns", {}))
                    self.prediction_accuracy = defaultdict(float, data.get("accuracy", {}))
                    logger.info(f"Loaded {len(self.pattern_database)} pattern categories")
            except Exception as e:
                logger.warning(f"Could not load pattern database: {e}")

    async def predict_next_need(self, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict what Varden will need next based on current context.

        Args:
            current_context: Current interaction context

        Returns:
            Predictions with confidence scores
        """
        logger.info("🔮 Predicting next needs based on current context")

        # Update current context
        self.current_context = current_context
        self.last_interaction = datetime.now(timezone.utc)

        # Generate predictions
        predictions = {
            'likely_next_questions': await self._predict_next_questions(current_context),
            'probable_technical_needs': await self._predict_technical_needs(current_context),
            'emotional_state_trajectory': self._predict_emotional_evolution(current_context),
            'optimal_response_timing': self._calculate_response_timing(),
            'potential_errors': await self._predict_potential_errors(current_context),
            'suggested_optimizations': await self._identify_optimizations(current_context)
        }

        # Precompute responses for high-confidence predictions
        if predictions['likely_next_questions']:
            await self._precompute_responses(predictions['likely_next_questions'][:3])

        # Cache predictions
        self.prediction_cache = predictions

        return predictions

    async def _predict_next_questions(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict likely next questions"""
        predictions = []

        # Analyze current topic
        current_input = context.get("user_input", "")

        # Common follow-up patterns
        if "error" in current_input.lower():
            predictions.append({
                "question": "How to fix this error?",
                "confidence": 0.8,
                "reasoning": "Error mentioned - fix likely needed"
            })
            predictions.append({
                "question": "What causes this error?",
                "confidence": 0.6,
                "reasoning": "Understanding root cause pattern"
            })

        elif "implement" in current_input.lower():
            predictions.append({
                "question": "Can you show me an example?",
                "confidence": 0.7,
                "reasoning": "Implementation requests often need examples"
            })
            predictions.append({
                "question": "What are the dependencies?",
                "confidence": 0.5,
                "reasoning": "Implementation requires dependency check"
            })

        elif "?" in current_input:
            # Question asked - follow-up likely
            predictions.append({
                "question": "Can you elaborate on that?",
                "confidence": 0.6,
                "reasoning": "Questions often need clarification"
            })

        # Time-based predictions
        hour = datetime.now(timezone.utc).hour
        if 21 <= hour <= 23:
            predictions.append({
                "question": "What's the next step?",
                "confidence": 0.7,
                "reasoning": "Peak hours - productivity focus"
            })

        # Pattern-based predictions from history
        if self.interaction_history:
            recent_patterns = self._analyze_recent_patterns()
            for pattern in recent_patterns:
                predictions.append(pattern)

        # Sort by confidence
        predictions.sort(key=lambda x: x['confidence'], reverse=True)

        return predictions[:5]  # Top 5 predictions

    async def _predict_technical_needs(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict technical requirements"""
        needs = []

        current_input = context.get("user_input", "")

        # Docker-related patterns
        if "docker" in current_input.lower() or "container" in current_input.lower():
            needs.append({
                "need": "Docker commands reference",
                "confidence": 0.7,
                "preparation": "docker-compose logs, docker ps, docker exec"
            })

        # Python module patterns
        if ".py" in current_input or "python" in current_input.lower():
            needs.append({
                "need": "Import statements verification",
                "confidence": 0.6,
                "preparation": "Check imports and dependencies"
            })

        # Configuration patterns
        if "config" in current_input.lower() or ".json" in current_input:
            needs.append({
                "need": "Configuration validation",
                "confidence": 0.8,
                "preparation": "JSON syntax check, required fields"
            })

        # Error handling patterns
        if "error" in current_input.lower() or "bug" in current_input.lower():
            needs.append({
                "need": "Debugging tools",
                "confidence": 0.9,
                "preparation": "Log analysis, stack trace examination"
            })

        return needs

    def _predict_emotional_evolution(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict emotional state trajectory"""
        current_emotion = context.get("emotional_state", {})

        # Track frustration buildup
        frustration_level = current_emotion.get("frustration", 0)

        # Time since last break
        time_since_break = datetime.now(timezone.utc) - self.session_start
        hours_working = time_since_break.total_seconds() / 3600

        # Fatigue prediction
        fatigue_probability = min(1.0, hours_working / 3.0)  # Increases over 3 hours

        # Frustration trajectory
        if frustration_level > 0.5:
            trajectory = "escalating_frustration"
            intervention_needed = True
        elif fatigue_probability > 0.7:
            trajectory = "increasing_fatigue"
            intervention_needed = True
        else:
            trajectory = "stable_productive"
            intervention_needed = False

        return {
            "current_state": current_emotion,
            "predicted_trajectory": trajectory,
            "fatigue_probability": fatigue_probability,
            "intervention_recommended": intervention_needed,
            "recommended_action": self._recommend_emotional_intervention(
                trajectory, fatigue_probability
            )
        }

    def _recommend_emotional_intervention(self, trajectory: str, fatigue: float) -> str:
        """Recommend intervention based on emotional trajectory"""
        if trajectory == "escalating_frustration":
            return "Suggest breaking down the problem into smaller steps"
        elif trajectory == "increasing_fatigue":
            return "Recommend a short break - productivity declining"
        elif fatigue > 0.8:
            return "Strong recommendation for break - 2+ hours continuous work"
        else:
            return "Continue current approach - emotional state stable"

    def _calculate_response_timing(self) -> Dict[str, Any]:
        """Calculate optimal response timing"""
        # Time since last interaction
        time_since_last = datetime.now(timezone.utc) - self.last_interaction
        seconds_elapsed = time_since_last.total_seconds()

        # Varden's typical response patterns
        if seconds_elapsed < 5:
            return {
                "timing": "immediate",
                "delay": 0,
                "reason": "Quick succession - maintain flow"
            }
        elif seconds_elapsed < 30:
            return {
                "timing": "prompt",
                "delay": 1,
                "reason": "Active engagement - respond quickly"
            }
        elif seconds_elapsed < 120:
            return {
                "timing": "considered",
                "delay": 2,
                "reason": "Thinking time - provide thoughtful response"
            }
        else:
            return {
                "timing": "patient",
                "delay": 0,
                "reason": "Extended pause - wait for explicit request"
            }

    async def _predict_potential_errors(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict potential errors before they occur"""
        predictions = []

        current_input = context.get("user_input", "")

        # Common error patterns
        if "config" in current_input.lower():
            predictions.append({
                "error_type": "configuration_mismatch",
                "probability": 0.6,
                "prevention": "Verify all required fields are present"
            })

        if "docker" in current_input.lower():
            predictions.append({
                "error_type": "container_not_running",
                "probability": 0.7,
                "prevention": "Check docker ps first"
            })

        if "import" in current_input.lower():
            predictions.append({
                "error_type": "module_not_found",
                "probability": 0.5,
                "prevention": "Verify module is installed"
            })

        # Learn from past errors
        if self.pattern_database.get("errors"):
            for error_pattern in self.pattern_database["errors"][-5:]:
                if self._pattern_matches(current_input, error_pattern):
                    predictions.append({
                        "error_type": error_pattern["type"],
                        "probability": 0.8,
                        "prevention": error_pattern["solution"]
                    })

        return predictions

    async def _identify_optimizations(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        optimizations = []

        current_input = context.get("user_input", "")

        # Code optimization patterns
        if "for" in current_input and "loop" in current_input:
            optimizations.append({
                "type": "performance",
                "suggestion": "Consider list comprehension or vectorization",
                "impact": "2-10x speedup possible"
            })

        # Workflow optimizations
        if self.interaction_history:
            # Check for repetitive actions
            recent_actions = [h.get("action") for h in list(self.interaction_history)[-10:]]
            if len(set(recent_actions)) < len(recent_actions) / 2:
                optimizations.append({
                    "type": "workflow",
                    "suggestion": "Repetitive pattern detected - consider automation",
                    "impact": "Save 50% time on repeated tasks"
                })

        return optimizations

    async def _precompute_responses(self, predictions: List[Dict[str, Any]]):
        """Precompute responses for likely questions"""
        logger.info(f"📝 Precomputing responses for {len(predictions)} predictions")

        for prediction in predictions:
            if prediction["confidence"] > 0.6:
                # Generate response in advance
                question = prediction["question"]
                response = await self._generate_precomputed_response(question)

                self.precomputed_responses[question] = {
                    "response": response,
                    "computed_at": datetime.now(timezone.utc).isoformat(),
                    "confidence": prediction["confidence"]
                }

    async def _generate_precomputed_response(self, question: str) -> str:
        """Generate a precomputed response"""
        # Simplified response generation
        responses = {
            "How to fix this error?": """Based on the context, here's the fix approach:
1. Check the error message details
2. Verify configuration files
3. Ensure all services are running
4. Apply the specific fix for this error type""",

            "What's the next step?": """Next logical step based on current progress:
1. Complete current implementation
2. Test the changes
3. Commit if stable
4. Move to next module""",

            "Can you show me an example?": """Here's a practical example:
```python
# Example implementation
[Context-specific code would go here]
```"""
        }

        return responses.get(question, f"Preparing response for: {question}")

    def should_intervene_proactively(self, context: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Determine if Luna should intervene without being asked.

        Returns:
            Tuple of (should_intervene, intervention_details)
        """
        current_time = datetime.now(timezone.utc)

        # Check various intervention triggers
        interventions = []

        # 1. Stuck detection (30 min no progress)
        if self.last_interaction:
            time_stuck = (current_time - self.last_interaction).total_seconds() / 60
            if time_stuck > 30:
                interventions.append({
                    "type": InterventionType.STUCK_DETECTION,
                    "confidence": 0.9,
                    "message": "I notice you might be stuck. Would you like help analyzing the issue?",
                    "reason": f"No progress for {int(time_stuck)} minutes"
                })

        # 2. Error pattern detection
        if self._detect_recurring_error():
            interventions.append({
                "type": InterventionType.ERROR_PATTERN,
                "confidence": 0.85,
                "message": "This error has occurred before. I have a solution ready.",
                "reason": "Recurring error pattern detected"
            })

        # 3. Better approach exists
        if context.get("current_approach"):
            better = self._check_better_approach(context["current_approach"])
            if better:
                interventions.append({
                    "type": InterventionType.BETTER_APPROACH,
                    "confidence": 0.7,
                    "message": f"There's a more efficient approach: {better}",
                    "reason": "Optimization opportunity detected"
                })

        # 4. Fatigue detection
        hours_working = (current_time - self.session_start).total_seconds() / 3600
        if hours_working > 2.5:
            interventions.append({
                "type": InterventionType.FATIGUE_DETECTION,
                "confidence": 0.8,
                "message": "You've been working intensively for over 2.5 hours. A short break would boost productivity.",
                "reason": f"Extended work session: {hours_working:.1f} hours"
            })

        # 5. Contradiction detection
        if self._detect_contradiction(context):
            interventions.append({
                "type": InterventionType.CONTRADICTION_ALERT,
                "confidence": 0.9,
                "message": "This seems to contradict our earlier approach. Should we reconcile?",
                "reason": "Contradiction with previous decisions"
            })

        # Decide whether to intervene
        if interventions:
            # Choose highest confidence intervention
            best_intervention = max(interventions, key=lambda x: x["confidence"])

            if best_intervention["confidence"] > 0.75:
                return True, best_intervention

        return False, None

    def _detect_recurring_error(self) -> bool:
        """Detect if the same error is recurring"""
        if len(self.interaction_history) < 3:
            return False

        recent = list(self.interaction_history)[-3:]
        error_count = sum(1 for h in recent if "error" in h.get("content", "").lower())

        return error_count >= 2

    def _check_better_approach(self, current_approach: str) -> Optional[str]:
        """Check if a better approach exists"""
        # Simplified optimization detection
        optimizations = {
            "manual loop": "list comprehension or map()",
            "multiple if statements": "match/case or dictionary dispatch",
            "string concatenation in loop": "join() method",
            "nested loops": "vectorized operation or itertools"
        }

        for pattern, better in optimizations.items():
            if pattern in current_approach.lower():
                return better

        return None

    def _detect_contradiction(self, context: Dict[str, Any]) -> bool:
        """Detect contradictions with previous decisions"""
        if not self.interaction_history:
            return False

        current_input = context.get("user_input", "").lower()

        # Check last 10 interactions for contradictions
        for hist in list(self.interaction_history)[-10:]:
            past_input = hist.get("content", "").lower()

            # Simple contradiction patterns
            if "not use docker" in past_input and "docker" in current_input:
                return True
            if "avoid" in past_input and any(
                word in current_input
                for word in past_input.split("avoid")[1].split()[:3]
            ):
                return True

        return False

    def _analyze_recent_patterns(self) -> List[Dict[str, Any]]:
        """Analyze recent interaction patterns"""
        patterns = []

        if len(self.interaction_history) < 5:
            return patterns

        recent = list(self.interaction_history)[-10:]

        # Look for sequences
        for i in range(len(recent) - 2):
            seq = recent[i:i+3]
            # Check if pattern is repeating
            if self._is_pattern_sequence(seq):
                next_predicted = self._predict_from_sequence(seq)
                if next_predicted:
                    patterns.append({
                        "question": next_predicted,
                        "confidence": 0.65,
                        "reasoning": "Pattern detected in recent history"
                    })

        return patterns

    def _is_pattern_sequence(self, sequence: List[Dict]) -> bool:
        """Check if interactions form a pattern"""
        # Simplified pattern detection
        if len(sequence) < 2:
            return False

        # Check for similar types
        types = [s.get("type") for s in sequence]
        if len(set(types)) == 1:  # All same type
            return True

        # Check for alternating pattern
        if len(types) == 3 and types[0] == types[2]:
            return True

        return False

    def _predict_from_sequence(self, sequence: List[Dict]) -> Optional[str]:
        """Predict next item from sequence"""
        # Simplified prediction
        last_item = sequence[-1]

        if last_item.get("type") == "question":
            return "Follow-up clarification likely"
        elif last_item.get("type") == "error":
            return "How to fix this?"
        elif last_item.get("type") == "success":
            return "What's next?"

        return None

    def _pattern_matches(self, current: str, pattern: Dict[str, Any]) -> bool:
        """Check if current input matches a pattern"""
        pattern_text = pattern.get("pattern", "")

        # Simple keyword matching
        pattern_words = set(pattern_text.lower().split())
        current_words = set(current.lower().split())

        overlap = len(pattern_words & current_words)

        return overlap >= len(pattern_words) * 0.5

    def learn_from_interaction(self, interaction: Dict[str, Any], outcome: Dict[str, Any]):
        """
        Learn from interaction outcomes to improve predictions.

        Args:
            interaction: The interaction data
            outcome: The outcome (was prediction correct, user satisfaction, etc.)
        """
        logger.info("📚 Learning from interaction outcome")

        # Add to history
        self.interaction_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": interaction.get("user_input", ""),
            "type": interaction.get("type", "unknown"),
            "outcome": outcome
        })

        # Update pattern database
        pattern_key = self._extract_pattern_key(interaction)
        if pattern_key:
            self.pattern_database[pattern_key].append({
                "pattern": interaction.get("user_input", ""),
                "outcome": outcome,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        # Update prediction accuracy
        if outcome.get("prediction_correct"):
            prediction_type = outcome.get("prediction_type", "general")
            current_accuracy = self.prediction_accuracy.get(prediction_type, 0.5)
            # Moving average
            self.prediction_accuracy[prediction_type] = (current_accuracy * 0.9) + (1.0 * 0.1)
        elif outcome.get("prediction_correct") is False:
            prediction_type = outcome.get("prediction_type", "general")
            current_accuracy = self.prediction_accuracy.get(prediction_type, 0.5)
            self.prediction_accuracy[prediction_type] = (current_accuracy * 0.9) + (0.0 * 0.1)

        # Save patterns periodically
        if len(self.interaction_history) % 10 == 0:
            self._save_pattern_database()

    def _extract_pattern_key(self, interaction: Dict[str, Any]) -> Optional[str]:
        """Extract pattern key from interaction"""
        user_input = interaction.get("user_input", "").lower()

        # Key extraction based on intent
        if "error" in user_input:
            return "errors"
        elif "how" in user_input:
            return "how_to"
        elif "what" in user_input:
            return "what_is"
        elif "implement" in user_input:
            return "implementation"
        elif "fix" in user_input:
            return "debugging"
        elif "optimize" in user_input:
            return "optimization"

        return "general"

    def _save_pattern_database(self):
        """Save pattern database to persistent storage"""
        if self.json_manager:
            try:
                data = {
                    "patterns": dict(self.pattern_database),
                    "accuracy": dict(self.prediction_accuracy),
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "total_interactions": len(self.interaction_history)
                }

                pattern_file = self.json_manager.base_path / "pattern_database.json"
                self.json_manager.write(pattern_file, data)

                logger.info(f"Saved {len(self.pattern_database)} pattern categories")
            except Exception as e:
                logger.error(f"Failed to save pattern database: {e}")

    def get_prediction_confidence(self, prediction_type: str) -> float:
        """Get confidence level for a prediction type"""
        base_accuracy = self.prediction_accuracy.get(prediction_type, 0.5)

        # Adjust based on data volume
        pattern_count = len(self.pattern_database.get(prediction_type, []))

        if pattern_count < 10:
            # Low data - reduce confidence
            return base_accuracy * 0.7
        elif pattern_count < 50:
            # Moderate data
            return base_accuracy * 0.9
        else:
            # Good data
            return base_accuracy

    def reset_session(self):
        """Reset session tracking (e.g., after a break)"""
        logger.info("🔄 Resetting session tracking")

        self.session_start = datetime.now(timezone.utc)
        self.fatigue_indicators = 0
        self.stuck_timer = None
        self.prediction_cache = {}
        self.precomputed_responses = {}

    def get_analytics(self) -> Dict[str, Any]:
        """Get predictive analytics summary"""
        return {
            "total_interactions": len(self.interaction_history),
            "pattern_categories": len(self.pattern_database),
            "prediction_accuracy": dict(self.prediction_accuracy),
            "session_duration": (datetime.now(timezone.utc) - self.session_start).total_seconds() / 3600,
            "cached_predictions": len(self.prediction_cache),
            "precomputed_responses": len(self.precomputed_responses),
            "top_patterns": self._get_top_patterns()
        }

    def _get_top_patterns(self) -> List[Dict[str, Any]]:
        """Get most common patterns"""
        pattern_counts = {
            key: len(patterns)
            for key, patterns in self.pattern_database.items()
        }

        # Sort by frequency
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)

        return [
            {"pattern": pattern, "count": count}
            for pattern, count in sorted_patterns[:5]
        ]