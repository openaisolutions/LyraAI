"""
LYRA AI: A quantum-inspired AI framework for empathy, wisdom, and distributed computing.
"""

from .constants import ALPHA, G, C, H_BAR
from .quantum import quantum_simulation
from .models import informational_collapse, simulate_collapse
from .wisdom import WisdomDatabase
from .network import AINodeServer, ai_node_server
from .api import create_app, app as flask_app

__version__ = "0.1.0"
__all__ = [
    "ALPHA",
    "G",
    "C",
    "H_BAR",
    "quantum_simulation",
    "informational_collapse",
    "simulate_collapse",
    "WisdomDatabase",
    "AINodeServer",
    "ai_node_server",
    "create_app",
    "flask_app",
]
