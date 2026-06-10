"""Tests for scientific models (informational collapse)."""

import numpy as np
from lyra.models import informational_collapse, simulate_collapse
from lyra.constants import ALPHA


class TestInformationalCollapse:
    """Test cases for informational_collapse function."""

    def test_informational_collapse_basic(self):
        """Test basic informational collapse calculation."""
        informational = 1.0
        t = 0.0
        alpha_G = 1.0
        result = informational_collapse(informational, t, alpha_G)
        expected = -alpha_G * (1 + ALPHA) * informational
        assert np.isclose(result, expected)

    def test_informational_collapse_zero_I(self):
        """Test collapse with zero informational gradient."""
        result = informational_collapse(0.0, 0.0, 1.0)
        assert result == 0.0

    def test_informational_collapse_zero_alpha_G(self):
        """Test collapse with zero coupling constant."""
        result = informational_collapse(1.0, 0.0, 0.0)
        assert result == 0.0

    def test_informational_collapse_negative_I(self):
        """Test collapse with negative informational gradient."""
        result = informational_collapse(-1.0, 0.0, 1.0)
        expected = -1.0 * (1 + ALPHA) * (-1.0)  # NOQA: W503
        assert np.isclose(result, expected)


class TestSimulateCollapse:
    """Test cases for simulate_collapse function."""

    def test_simulate_collapse_output_length(self):
        """Test that simulate_collapse returns 100 points."""
        results = simulate_collapse()
        assert len(results) == 100

    def test_simulate_collapse_initial_condition(self):
        """Test that the first value is the initial condition (1.0)."""
        results = simulate_collapse()
        assert np.isclose(results[0], 1.0)

    def test_simulate_collapse_decay(self):
        """Test that the informational gradient decays over time."""
        results = simulate_collapse(alpha_G=1.0)
        # All values should be positive and decreasing
        for i in range(len(results) - 1):
            assert results[i] > 0
            assert results[i] >= results[i + 1]

    def test_simulate_collapse_custom_alpha_G(self):
        """Test simulate_collapse with custom alpha_G."""
        results_low = simulate_collapse(alpha_G=0.1)
        results_high = simulate_collapse(alpha_G=10.0)

        # With higher alpha_G, decay should be faster
        # Compare values at t=5 (roughly middle of the simulation)
        assert results_low[50] > results_high[50]

    def test_simulate_collapse_final_value(self):
        """Test that the final value is close to zero for large alpha_G."""
        results = simulate_collapse(alpha_G=100.0)
        assert results[-1] < 0.01
