from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def qft(num_qubits: int) -> QuantumCircuit:
    return QFT(num_qubits)


def inverse_qft(num_qubits: int) -> QuantumCircuit:
    return QFT(num_qubits, inverse=True)


def add_measurement(circuit: QuantumCircuit) -> QuantumCircuit:
    circuit.measure_all()
    return circuit
