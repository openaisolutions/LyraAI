"""
Scientific models for LYRA AI, including informational collapse dynamics.
"""

import numpy as np
import scipy.integrate as spi
from .constants import ALPHA


def informational_collapse(informational: float, t: float, alpha_G: float) -> float:
    """
    Model the collapse of informational gradients into gravity fields.

    Args:
        informational: Informational gradient value.
        t: Time.
        alpha_G: Coupling constant for the collapse process.

    Returns:
        Rate of change of the informational gradient (dI/dt).
    """
    dI_dt = -alpha_G * (1 + ALPHA) * informational
    return dI_dt


def simulate_collapse(alpha_G: float = 1.0) -> list[float]:
    """
    Simulate the informational collapse over time.

    Args:
        alpha_G: Coupling constant for the collapse process (default: 1.0).

    Returns:
        List of informational gradient values over time.
    """
    I0 = [1]  # Initial condition
    time = np.linspace(0, 10, 100)  # Time range
    solution = spi.odeint(informational_collapse, I0, time, args=(alpha_G,))
    return np.array(solution).flatten().tolist()
