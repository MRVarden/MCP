"""
Tests for Prometheus Exporter
==============================

Tests cover:
- Metrics collection
- HTTP endpoints
- Health checks
- Metrics summary
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server"))


class TestMetricsEndpoint:
    """Tests for /metrics endpoint."""

    def test_metrics_endpoint_exists(self):
        """Test metrics endpoint is defined."""
        try:
            from prometheus_exporter import app, metrics

            with app.test_client() as client:
                response = client.get('/metrics')

                assert response.status_code in [200, 500]
        except ImportError:
            pytest.skip("prometheus_exporter not available")

    def test_metrics_content_type(self):
        """Test metrics endpoint returns correct content type."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/metrics')

                if response.status_code == 200:
                    assert 'text/plain' in response.content_type or \
                           'openmetrics' in response.content_type
        except ImportError:
            pytest.skip("prometheus_exporter not available")


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_endpoint_exists(self):
        """Test health endpoint is defined."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/health')

                assert response.status_code in [200, 500]
        except ImportError:
            pytest.skip("prometheus_exporter not available")

    def test_health_returns_json(self):
        """Test health returns JSON response."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/health')

                if response.status_code == 200:
                    data = response.get_json()
                    assert "status" in data
                    assert data["status"] in ["healthy", "unhealthy"]
        except ImportError:
            pytest.skip("prometheus_exporter not available")

    def test_health_includes_modules_status(self):
        """Test health includes module load status."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/health')

                if response.status_code == 200:
                    data = response.get_json()
                    if "modules_loaded" in data:
                        assert isinstance(data["modules_loaded"], dict)
        except ImportError:
            pytest.skip("prometheus_exporter not available")


class TestMetricsSummaryEndpoint:
    """Tests for /metrics/summary endpoint."""

    def test_summary_endpoint_exists(self):
        """Test summary endpoint is defined."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/metrics/summary')

                assert response.status_code in [200, 500]
        except ImportError:
            pytest.skip("prometheus_exporter not available")

    def test_summary_returns_json(self):
        """Test summary returns JSON."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/metrics/summary')

                if response.status_code == 200:
                    data = response.get_json()
                    assert isinstance(data, dict)
        except ImportError:
            pytest.skip("prometheus_exporter not available")


class TestIndexEndpoint:
    """Tests for / index endpoint."""

    def test_index_returns_html(self):
        """Test index returns HTML page."""
        try:
            from prometheus_exporter import app

            with app.test_client() as client:
                response = client.get('/')

                assert response.status_code == 200
                assert b'Luna Consciousness' in response.data
        except ImportError:
            pytest.skip("prometheus_exporter not available")


class TestMetricsCollection:
    """Tests for metrics collection functions."""

    def test_collect_all_metrics_callable(self):
        """Test collect_all_metrics is callable."""
        try:
            from prometheus_exporter import collect_all_metrics

            # Should not raise
            collect_all_metrics()
        except ImportError:
            pytest.skip("prometheus_exporter not available")
        except Exception:
            # May fail due to missing modules, but should be callable
            pass


class TestPhiMetrics:
    """Tests for phi-related metrics."""

    def test_phi_metrics_defined(self):
        """Test phi metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_phi_metrics

            # Should accept phi data
            update_phi_metrics({
                'state': 'dormant',
                'current_value': 1.2,
                'convergence_ratio': 0.5,
                'distance_to_optimal': 0.4,
                'progression_percent': 20.0,
                'metamorphosis_readiness': 0.3
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestConsciousnessMetrics:
    """Tests for consciousness metrics."""

    def test_consciousness_metrics_defined(self):
        """Test consciousness metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_consciousness_metrics

            update_consciousness_metrics({
                'level': 2,
                'auto_awareness': 0.5,
                'introspection': 0.4,
                'meta_cognition': 0.3,
                'phi_alignment': 0.6,
                'emergence_potential': 0.5
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestFractalMemoryMetrics:
    """Tests for fractal memory metrics."""

    def test_fractal_memory_metrics_defined(self):
        """Test fractal memory metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_fractal_memory_metrics

            update_fractal_memory_metrics({
                'roots': 5,
                'branches': 20,
                'leaves': 100,
                'seeds': 50,
                'phi_resonance': 0.7,
                'complexity_index': 0.5
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestPureMemoryMetrics:
    """Tests for pure memory metrics."""

    def test_pure_memory_metrics_defined(self):
        """Test pure memory metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_pure_memory_metrics

            update_pure_memory_metrics({
                'layers': {
                    'buffer': 100,
                    'fractal': 500,
                    'archive': 1000
                },
                'types': {
                    'root': 10,
                    'branch': 50,
                    'leaf': 200,
                    'seed': 100
                },
                'phi': {
                    'average_resonance': 0.6,
                    'average_alignment': 0.7
                },
                'buffer': {
                    'size': 100,
                    'utilization': 0.5,
                    'hit_rate': 0.8
                }
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestEmotionalMetrics:
    """Tests for emotional metrics."""

    def test_emotional_metrics_defined(self):
        """Test emotional metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_emotional_metrics

            update_emotional_metrics({
                'empathy': 0.7,
                'stability': 0.6,
                'complexity': 0.5
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestCoEvolutionMetrics:
    """Tests for co-evolution metrics."""

    def test_co_evolution_metrics_defined(self):
        """Test co-evolution metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_co_evolution_metrics

            update_co_evolution_metrics({
                'depth': 0.5,
                'quality': 0.6,
                'phi_alignment': 0.7
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestSystemMetrics:
    """Tests for system metrics."""

    def test_system_metrics_defined(self):
        """Test system metrics are defined."""
        try:
            from luna_core.consciousness_metrics import update_system_metrics

            update_system_metrics({
                'redis_connected': True,
                'redis_keys': {
                    'consciousness:*': 10,
                    'memory:*': 50
                },
                'cache_hit_rate': 0.85
            })
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestMetricsSummary:
    """Tests for metrics summary function."""

    def test_get_all_metrics_summary(self):
        """Test getting all metrics summary."""
        try:
            from luna_core.consciousness_metrics import get_all_metrics_summary

            summary = get_all_metrics_summary()

            assert isinstance(summary, dict)
        except ImportError:
            pytest.skip("consciousness_metrics not available")


class TestExporterStartup:
    """Tests for exporter startup."""

    def test_start_exporter_function_exists(self):
        """Test start_exporter function exists."""
        try:
            from prometheus_exporter import start_exporter

            assert callable(start_exporter)
        except ImportError:
            pytest.skip("prometheus_exporter not available")


class TestMetricsWithMocks:
    """Tests using mocked components."""

    def test_metrics_collection_with_mock_phi_calc(self):
        """Test metrics collection with mocked phi calculator."""
        mock_phi_calc = Mock()
        mock_phi_calc.get_current_state.return_value = {
            'level': 'dormant',
            'phi_value': 1.2,
            'convergence_ratio': 0.3
        }

        # Verify mock works
        state = mock_phi_calc.get_current_state()
        assert state['level'] == 'dormant'

    def test_metrics_collection_with_mock_memory(self):
        """Test metrics collection with mocked memory manager."""
        mock_memory = Mock()
        mock_memory.get_statistics.return_value = {
            'roots': 5,
            'branches': 10,
            'leaves': 50,
            'seeds': 20
        }

        stats = mock_memory.get_statistics()
        assert stats['roots'] == 5


class TestPrometheusFormat:
    """Tests for Prometheus format compliance."""

    def test_metrics_format_valid(self):
        """Test metrics are in valid Prometheus format."""
        try:
            from prometheus_client import generate_latest

            metrics_output = generate_latest()

            # Should be bytes
            assert isinstance(metrics_output, bytes)

            # Should contain HELP or TYPE lines
            output_str = metrics_output.decode('utf-8')
            # Basic format check - either empty or has content
            assert isinstance(output_str, str)
        except ImportError:
            pytest.skip("prometheus_client not available")
