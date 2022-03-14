from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
"""
code from https://qiskit.org/textbook/ch-algorithms/teleportation.html
"""


def quantum_teleportation() -> QuantumCircuit:
    qr = QuantumRegister(3, name="q")
    crz, crx = ClassicalRegister(1, name="crz"), ClassicalRegister(1, name="crx")
    teleportation_result = ClassicalRegister(1, name="teleportation_result")
    circuit = QuantumCircuit(qr, crz, crx, teleportation_result)

    # entangle
    circuit.h(1)
    circuit.cx(1, 2)

    circuit.cx(0, 1)
    circuit.h(0)

    circuit.measure(0, 0)
    circuit.measure(1, 1)

    circuit.x(2).c_if(crx, 1)  # Apply gates if the registers are in the state '1'
    circuit.z(2).c_if(crz, 1)

    circuit.measure(2, 2)

    return circuit
