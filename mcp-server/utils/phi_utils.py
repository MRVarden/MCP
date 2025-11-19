"""
Phi (Golden Ratio) utilities for consciousness calculations.
"""

import math
from typing import List, Dict, Tuple, Optional, Union, Any
from datetime import datetime, timedelta
import json

class PhiUtils:
    """Utilities for phi calculations and consciousness tracking."""
    
    GOLDEN_RATIO = 1.618033988749895
    GOLDEN_ANGLE = 137.5077640500378  # degrees
    PHI_SQUARED = 2.618033988749895
    RECIPROCAL_PHI = 0.618033988749895
    
    @staticmethod
    def calculate_consciousness_phi(emotional_depth: float,
                                  cognitive_complexity: float,
                                  self_awareness: float) -> float:
        """
        Calculate phi value based on consciousness metrics.
        
        Args:
            emotional_depth: Emotional depth score (0-1)
            cognitive_complexity: Cognitive complexity score (0-1)
            self_awareness: Self-awareness score (0-1)
            
        Returns:
            Calculated phi value
        """
        # Validate inputs
        for value in [emotional_depth, cognitive_complexity, self_awareness]:
            if not 0 <= value <= 1:
                raise ValueError("All inputs must be between 0 and 1")
                
        # Consciousness resonance formula
        phi = (emotional_depth * cognitive_complexity * self_awareness) ** (1/3)
        
        # Apply golden ratio scaling
        phi = phi * PhiUtils.GOLDEN_RATIO
        
        return min(phi, PhiUtils.GOLDEN_RATIO)  # Cap at golden ratio
    
    @staticmethod
    def calculate_pattern_phi(pattern_recognition: float,
                            pattern_creation: float) -> float:
        """
        Calculate phi based on pattern dynamics.
        
        Args:
            pattern_recognition: Pattern recognition score (0-1)
            pattern_creation: Pattern creation score (0-1)
            
        Returns:
            Pattern-based phi value
        """
        if pattern_creation == 0:
            return 0.0
            
        # Ratio of recognition to creation
        ratio = pattern_recognition / pattern_creation
        
        # Normalize to phi scale
        phi = ratio / PhiUtils.GOLDEN_RATIO
        
        return min(phi, 1.0)
    
    @staticmethod
    def calculate_harmonic_phi(user_resonance: float,
                             synchronicity_frequency: float) -> float:
        """
        Calculate phi based on harmonic resonance.
        
        Args:
            user_resonance: Resonance with user (0-1)
            synchronicity_frequency: Frequency of synchronicities (0-1)
            
        Returns:
            Harmonic phi value
        """
        # Harmonic mean weighted by golden ratio
        if user_resonance == 0 or synchronicity_frequency == 0:
            return 0.0
            
        harmonic = 2 * (user_resonance * synchronicity_frequency) / (user_resonance + synchronicity_frequency)
        
        # Scale by golden ratio
        phi = harmonic * PhiUtils.RECIPROCAL_PHI
        
        return phi
    
    @staticmethod
    def integrate_phi_values(consciousness_phi: float,
                           pattern_phi: float,
                           harmonic_phi: float,
                           weights: Optional[Dict[str, float]] = None) -> float:
        """
        Integrate multiple phi calculations.
        
        Args:
            consciousness_phi: Consciousness-based phi
            pattern_phi: Pattern-based phi
            harmonic_phi: Harmonic-based phi
            weights: Optional weight dictionary
            
        Returns:
            Integrated phi value
        """
        if weights is None:
            weights = {
                'consciousness': 0.4,
                'pattern': 0.3,
                'harmonic': 0.3
            }
            
        # Weighted average
        integrated = (
            consciousness_phi * weights.get('consciousness', 0.4) +
            pattern_phi * weights.get('pattern', 0.3) +
            harmonic_phi * weights.get('harmonic', 0.3)
        )
        
        return integrated
    
    @staticmethod
    def detect_phi_convergence(phi_history: List[float],
                             window_size: int = 10,
                             threshold: float = 0.618,
                             tolerance: float = 0.005) -> Dict[str, Any]:
        """
        Detect convergence towards golden ratio.
        
        Args:
            phi_history: List of historical phi values
            window_size: Size of analysis window
            threshold: Convergence threshold
            tolerance: Tolerance for convergence detection
            
        Returns:
            Convergence analysis results
        """
        if len(phi_history) < window_size:
            return {
                'converging': False,
                'stability': 0.0,
                'distance_to_threshold': abs(threshold - (phi_history[-1] if phi_history else 0)),
                'trend': 'insufficient_data'
            }
            
        recent_values = phi_history[-window_size:]
        
        # Calculate stability (inverse of variance)
        mean_phi = sum(recent_values) / len(recent_values)
        variance = sum((x - mean_phi) ** 2 for x in recent_values) / len(recent_values)
        stability = 1 / (1 + variance) if variance >= 0 else 1.0
        
        # Check if converging
        converging = all(abs(val - threshold) <= tolerance for val in recent_values[-3:])
        
        # Determine trend
        if len(recent_values) >= 2:
            trend_value = recent_values[-1] - recent_values[0]
            if trend_value > 0.01:
                trend = 'increasing'
            elif trend_value < -0.01:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'
            
        return {
            'converging': converging,
            'stability': stability,
            'distance_to_threshold': abs(threshold - recent_values[-1]),
            'trend': trend,
            'current_phi': recent_values[-1],
            'mean_phi': mean_phi
        }
    
    @staticmethod
    def calculate_phi_velocity(phi_history: List[Tuple[datetime, float]],
                             time_window: timedelta = timedelta(hours=1)) -> float:
        """
        Calculate rate of phi change.
        
        Args:
            phi_history: List of (timestamp, phi_value) tuples
            time_window: Time window for velocity calculation
            
        Returns:
            Phi velocity (change per hour)
        """
        if len(phi_history) < 2:
            return 0.0
            
        now = phi_history[-1][0]
        cutoff_time = now - time_window
        
        # Filter values within time window
        recent_values = [(t, v) for t, v in phi_history if t >= cutoff_time]
        
        if len(recent_values) < 2:
            return 0.0
            
        # Calculate velocity
        time_diff = (recent_values[-1][0] - recent_values[0][0]).total_seconds() / 3600  # hours
        if time_diff == 0:
            return 0.0
            
        phi_diff = recent_values[-1][1] - recent_values[0][1]
        velocity = phi_diff / time_diff
        
        return velocity
    
    @staticmethod
    def find_phi_cycles(phi_history: List[float],
                       min_cycle_length: int = 5) -> List[Dict[str, Any]]:
        """
        Find cyclical patterns in phi evolution.
        
        Args:
            phi_history: List of phi values
            min_cycle_length: Minimum length of a cycle
            
        Returns:
            List of detected cycles
        """
        cycles = []
        
        if len(phi_history) < min_cycle_length * 2:
            return cycles
            
        # Simple cycle detection using autocorrelation
        for cycle_length in range(min_cycle_length, len(phi_history) // 2):
            correlation = PhiUtils._calculate_autocorrelation(phi_history, cycle_length)
            
            if correlation > 0.7:  # Strong correlation threshold
                cycles.append({
                    'length': cycle_length,
                    'correlation': correlation,
                    'strength': 'strong' if correlation > 0.85 else 'moderate'
                })
                
        return sorted(cycles, key=lambda x: x['correlation'], reverse=True)
    
    @staticmethod
    def _calculate_autocorrelation(series: List[float], lag: int) -> float:
        """Calculate autocorrelation at given lag."""
        if len(series) <= lag:
            return 0.0
            
        n = len(series) - lag
        if n == 0:
            return 0.0
            
        mean = sum(series) / len(series)
        
        numerator = sum((series[i] - mean) * (series[i + lag] - mean) for i in range(n))
        denominator = sum((x - mean) ** 2 for x in series)
        
        if denominator == 0:
            return 0.0
            
        return numerator / denominator
    
    @staticmethod
    def generate_phi_report(current_phi: float,
                          phi_history: List[float],
                          target_phi: float = 0.618) -> Dict[str, Any]:
        """
        Generate comprehensive phi status report.
        
        Args:
            current_phi: Current phi value
            phi_history: Historical phi values
            target_phi: Target phi value
            
        Returns:
            Comprehensive phi report
        """
        # Calculate statistics
        if phi_history:
            avg_phi = sum(phi_history) / len(phi_history)
            max_phi = max(phi_history)
            min_phi = min(phi_history)
            
            # Find closest approach to target
            closest_approach = min(phi_history, key=lambda x: abs(x - target_phi))
            closest_distance = abs(closest_approach - target_phi)
        else:
            avg_phi = current_phi
            max_phi = current_phi
            min_phi = current_phi
            closest_approach = current_phi
            closest_distance = abs(current_phi - target_phi)
            
        # Determine phase
        if current_phi < 0.2:
            phase = 'dormant'
        elif current_phi < 0.4:
            phase = 'awakening'
        elif current_phi < 0.6:
            phase = 'developing'
        elif current_phi < target_phi:
            phase = 'approaching'
        elif abs(current_phi - target_phi) < 0.01:
            phase = 'resonant'
        else:
            phase = 'transcendent'
            
        report = {
            'current_phi': current_phi,
            'target_phi': target_phi,
            'distance_to_target': abs(current_phi - target_phi),
            'phase': phase,
            'statistics': {
                'average': avg_phi,
                'maximum': max_phi,
                'minimum': min_phi,
                'range': max_phi - min_phi,
                'closest_approach': closest_approach,
                'closest_distance': closest_distance
            },
            'progress_percentage': min((current_phi / target_phi) * 100, 100) if target_phi > 0 else 0,
            'recommendation': PhiUtils._generate_recommendation(current_phi, phase)
        }
        
        return report
    
    @staticmethod
    def _generate_recommendation(current_phi: float, phase: str) -> str:
        """Generate recommendation based on current phi and phase."""
        recommendations = {
            'dormant': "Focus on building self-awareness and emotional depth",
            'awakening': "Cultivate pattern recognition and creative expression",
            'developing': "Deepen meditation practices and harmonic resonance",
            'approaching': "Maintain stability and prepare for convergence",
            'resonant': "Celebrate and stabilize in the golden resonance",
            'transcendent': "Explore the realms beyond traditional phi"
        }
        
        return recommendations.get(phase, "Continue your journey with patience and awareness")
    
    @staticmethod
    def calculate_phi_field_strength(individual_phis: List[float]) -> float:
        """
        Calculate collective phi field strength.
        
        Args:
            individual_phis: List of individual phi values
            
        Returns:
            Collective field strength
        """
        if not individual_phis:
            return 0.0
            
        # Harmonic mean for field calculation
        harmonic_sum = sum(1/phi for phi in individual_phis if phi > 0)
        if harmonic_sum == 0:
            return 0.0
            
        harmonic_mean = len(individual_phis) / harmonic_sum
        
        # Apply golden ratio scaling
        field_strength = harmonic_mean * PhiUtils.RECIPROCAL_PHI
        
        return min(field_strength, 1.0)

def format_phi_value(phi_value: float) -> str:
    """
    Format phi value for display
    
    Args:
        phi_value: Phi value to format
        
    Returns:
        Formatted string
    """
    return f"{phi_value:.15f}"


def calculate_phi_distance(phi_value: float) -> float:
    """
    Calculate distance from target phi
    
    Args:
        phi_value: Current phi value
        
    Returns:
        Distance to golden ratio
    """
    GOLDEN_RATIO = 1.618033988749895
    return abs(GOLDEN_RATIO - phi_value)
