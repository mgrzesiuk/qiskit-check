from math import pi

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

"""
code from https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html
"""


def add_controlled_unitaries(circuit: QuantumCircuit, phase: float) -> QuantumCircuit:
    repetitions = 1
    for counting_qubit in range(len(circuit.qubits) - 1):
        for i in range(repetitions):
            circuit.cp(phase, counting_qubit, circuit.qubits[-1])
        repetitions *= 2
    return circuit


def phase_estimation(circuit: QuantumCircuit, phase: float) -> QuantumCircuit:
    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)
    circuit.x(circuit.qubits[-1])
    circuit = add_controlled_unitaries(circuit, phase)
    qft_inverse = QFT(len(circuit.qubits) - 1, inverse=True).to_instruction()
    circuit.append(qft_inverse, circuit.qubits[:-1])
    for qubit_index in range(len(circuit.qubits) - 1):
        circuit.measure(qubit_index, qubit_index)

    return circuit


def mutation_no_x_gate_phase_estimation(circuit: QuantumCircuit, phase: float) -> QuantumCircuit:
    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)
    circuit = add_controlled_unitaries(circuit, phase)
    qft_inverse = QFT(len(circuit.qubits) - 1, inverse=True).to_instruction()
    circuit.append(qft_inverse, circuit.qubits[:-1])
    for qubit_index in range(len(circuit.qubits) - 1):
        circuit.measure(qubit_index, qubit_index)

    return circuit


def mutation_no_h_gate_phase_estimation(circuit: QuantumCircuit, phase: float) -> QuantumCircuit:
    circuit.x(circuit.qubits[-1])
    circuit = add_controlled_unitaries(circuit, phase)
    qft_inverse = QFT(len(circuit.qubits) - 1, inverse=True).to_instruction()
    circuit.append(qft_inverse, circuit.qubits[:-1])
    for qubit_index in range(len(circuit.qubits) - 1):
        circuit.measure(qubit_index, qubit_index)

    return circuit


def mutation_no_iqft_phase_estimation(circuit: QuantumCircuit, phase: float) -> QuantumCircuit:
    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)
    circuit.x(circuit.qubits[-1])
    circuit = add_controlled_unitaries(circuit, phase)
    for qubit_index in range(len(circuit.qubits) - 1):
        circuit.measure(qubit_index, qubit_index)

    return circuit


def mutation_additional_h_gate_phase_estimation(circuit: QuantumCircuit, phase: float) -> QuantumCircuit:
    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)
    circuit.x(circuit.qubits[-1])
    circuit = add_controlled_unitaries(circuit, phase)
    qft_inverse = QFT(len(circuit.qubits) - 1, inverse=True).to_instruction()
    circuit.append(qft_inverse, circuit.qubits[:-1])
    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)
    for qubit_index in range(len(circuit.qubits) - 1):
        circuit.measure(qubit_index, qubit_index)

    return circuit
