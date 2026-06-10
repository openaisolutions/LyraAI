"""
Quantum circuit simulations using PennyLane.
"""

import pennylane as qml


def quantum_simulation(theta: float) -> float:
    """
    Simulate a quantum circuit with a single qubit and RX rotation.

    Args:
        theta: Rotation angle in radians for the RX gate.

    Returns:
        Expectation value of the PauliZ operator (float between -1 and 1).
    """
    dev = qml.device("default.qubit", wires=1)

    @qml.qnode(dev)
    def circuit():
        qml.RX(theta, wires=0)
        return qml.expval(qml.PauliZ(0))

    return circuit()
