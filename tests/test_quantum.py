"""Tests for quantum circuit simulations."""

import numpy as np
from lyra.quantum import quantum_simulation


class TestQuantumSimulation:
    """Test cases for quantum_simulation function."""

    def test_quantum_simulation_zero_theta(self):
        """Test quantum simulation with theta=0 (no rotation)."""
        result = quantum_simulation(0.0)
        # With theta=0, RX(0) is identity, so |0> state -> <Z> = 1
        assert np.isclose(result, 1.0, atol=1e-5)

    def test_quantum_simulation_pi_theta(self):
        """Test quantum simulation with theta=pi (full rotation)."""
        result = quantum_simulation(np.pi)
        # RX(pi) flips |0> to |1>, so <Z> = -1
        assert np.isclose(result, -1.0, atol=1e-5)

    def test_quantum_simulation_pi_half_theta(self):
        """Test quantum simulation with theta=pi/2."""
        result = quantum_simulation(np.pi / 2)
        # RX(pi/2) creates superposition: (|0> + i|1>)/sqrt(2)
        # <Z> = 0 for this state
        assert np.isclose(result, 0.0, atol=1e-5)

    def test_quantum_simulation_negative_theta(self):
        """Test quantum simulation with negative theta."""
        result = quantum_simulation(-np.pi / 2)
        # RX(-pi/2) creates superposition: (|0> - i|1>)/sqrt(2)
        # <Z> = 0 for this state
        assert np.isclose(result, 0.0, atol=1e-5)

    def test_quantum_simulation_result_range(self):
        """Test that quantum simulation results are in [-1, 1]."""
        for theta in np.linspace(-2 * np.pi, 2 * np.pi, 20):
            result = quantum_simulation(theta)
            msg = f"Result {result} out of range for theta={theta}"
            assert -1.0 <= result <= 1.0, msg
