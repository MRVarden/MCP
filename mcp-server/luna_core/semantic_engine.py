"""
Semantic Validation Engine for Luna
Validates semantic coherence and detects potential hallucinations
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


class SemanticValidator:
    """
    Validates semantic coherence of statements and detects potential hallucinations
    """

    def __init__(self):
        self.coherence_threshold = 0.7
        self.hallucination_keywords = [
            'definitely', 'certainly', 'always', 'never', 'impossible',
            'absolutely', 'guaranteed', 'proven fact', 'undeniable'
        ]

    async def validate_coherence(self, statement: str, context: str = "") -> Dict[str, Any]:
        """
        Validate semantic coherence of a statement

        Args:
            statement: The statement to validate
            context: Optional context for validation

        Returns:
            Dictionary with validation results
        """
        if not statement or not statement.strip():
            return {
                'is_coherent': False,
                'coherence_score': 0.0,
                'hallucination_risk': 'high',
                'semantic_consistency': 0.0,
                'context_alignment': 0.0,
                'logical_flow': 0.0,
                'warning_message': 'Empty statement',
                'recommendation': 'Provide a valid statement'
            }

        # Calculate various coherence metrics
        semantic_consistency = self._check_semantic_consistency(statement)
        context_alignment = self._check_context_alignment(statement, context)
        logical_flow = self._check_logical_flow(statement)
        hallucination_risk = self._assess_hallucination_risk(statement)

        # Overall coherence score
        coherence_score = (semantic_consistency + context_alignment + logical_flow) / 3.0
        is_coherent = coherence_score >= self.coherence_threshold

        result = {
            'is_coherent': is_coherent,
            'coherence_score': coherence_score,
            'hallucination_risk': hallucination_risk,
            'semantic_consistency': semantic_consistency,
            'context_alignment': context_alignment,
            'logical_flow': logical_flow,
            'timestamp': datetime.now().isoformat()
        }

        # Add warnings and recommendations
        if not is_coherent:
            result['warning_message'] = self._generate_warning(coherence_score, hallucination_risk)
            result['recommendation'] = self._generate_recommendation(
                semantic_consistency, context_alignment, logical_flow
            )

        return result

    def _check_semantic_consistency(self, statement: str) -> float:
        """Check internal semantic consistency"""
        # Simple heuristic: longer, well-structured statements tend to be more coherent
        words = statement.split()
        word_count = len(words)

        # Check for contradictions
        contradiction_patterns = [
            (r'\bbut\b.*\bbut\b', -0.2),
            (r'\bhowever\b.*\bhowever\b', -0.15),
            (r'\bnot\b.*\bis\b.*\bis\b', -0.1),
        ]

        score = 0.8  # Base score

        for pattern, penalty in contradiction_patterns:
            if re.search(pattern, statement.lower()):
                score += penalty

        # Bonus for reasonable length
        if 10 <= word_count <= 100:
            score += 0.1
        elif word_count > 200:
            score -= 0.1

        return max(0.0, min(1.0, score))

    def _check_context_alignment(self, statement: str, context: str) -> float:
        """Check alignment with provided context"""
        if not context or not context.strip():
            return 0.75  # Neutral score when no context provided

        # Simple keyword overlap
        statement_words = set(statement.lower().split())
        context_words = set(context.lower().split())

        if len(context_words) == 0:
            return 0.75

        overlap = len(statement_words & context_words)
        alignment_score = min(1.0, overlap / (len(context_words) * 0.3))

        return alignment_score

    def _check_logical_flow(self, statement: str) -> float:
        """Check logical flow and structure"""
        # Check for logical connectors
        logical_connectors = [
            'therefore', 'because', 'thus', 'hence', 'consequently',
            'as a result', 'due to', 'since', 'so', 'accordingly'
        ]

        score = 0.7  # Base score

        statement_lower = statement.lower()
        connector_count = sum(1 for conn in logical_connectors if conn in statement_lower)

        # Bonus for logical connectors (but not too many)
        if 1 <= connector_count <= 3:
            score += 0.2
        elif connector_count > 5:
            score -= 0.1  # Too many connectors might indicate rambling

        # Check sentence structure
        sentences = statement.split('.')
        if len(sentences) > 1 and all(len(s.strip()) > 5 for s in sentences if s.strip()):
            score += 0.1

        return max(0.0, min(1.0, score))

    def _assess_hallucination_risk(self, statement: str) -> str:
        """Assess risk of hallucination"""
        statement_lower = statement.lower()

        # Count absolute/definitive keywords
        keyword_count = sum(1 for keyword in self.hallucination_keywords
                          if keyword in statement_lower)

        # Check for lack of qualifiers
        qualifiers = ['might', 'could', 'possibly', 'perhaps', 'likely', 'may', 'seems']
        has_qualifiers = any(qual in statement_lower for qual in qualifiers)

        # Assess risk
        if keyword_count >= 3:
            return 'high'
        elif keyword_count >= 1 and not has_qualifiers:
            return 'medium'
        else:
            return 'low'

    def _generate_warning(self, coherence_score: float, hallucination_risk: str) -> str:
        """Generate warning message"""
        if coherence_score < 0.3:
            return "Statement has very low semantic coherence"
        elif coherence_score < 0.5:
            return "Statement shows weak semantic coherence"
        elif hallucination_risk == 'high':
            return "High risk of hallucination detected (excessive certainty)"
        else:
            return "Statement coherence is below threshold"

    def _generate_recommendation(self, semantic: float, context: float, logical: float) -> str:
        """Generate recommendation based on scores"""
        issues = []

        if semantic < 0.6:
            issues.append("improve internal consistency")
        if context < 0.6:
            issues.append("better align with context")
        if logical < 0.6:
            issues.append("strengthen logical flow")

        if issues:
            return f"Consider: {', '.join(issues)}"
        else:
            return "Review statement structure and reduce absolute claims"
