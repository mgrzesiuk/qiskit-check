import math

import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile, Aer
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram

"""
code from https://qiskit.org/textbook/ch-algorithms/quantum-phase-estimation.html
"""


def add_controlled_unitaries(circuit: QuantumCircuit) -> QuantumCircuit:
    repetitions = 1
    for counting_qubit in range(len(circuit.qubits) - 1):
        for i in range(repetitions):
            circuit.cp(math.pi / 4, counting_qubit, circuit.qubits[-1])  # This is CU
        repetitions *= 2
    return circuit


def phase_estimation(circuit: QuantumCircuit) -> QuantumCircuit:
    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)
    circuit.x(circuit.qubits[-1])
    circuit = add_controlled_unitaries(circuit)
    qft_inverse = QFT(len(circuit.qubits) - 1, inverse=True).to_instruction()
    circuit.append(qft_inverse, circuit.qubits[:-1])
    for qubit_index in range(len(circuit.qubits) - 1):
        circuit.measure(qubit_index, qubit_index)

    return circuit


if __name__ == "__main__":
    qubit_number = 4
    qpe = phase_estimation(QuantumCircuit(qubit_number, qubit_number-1))
    qpe.draw(output='mpl')
    backend = Aer.get_backend('aer_simulator')
    qpe = transpile(qpe, backend)

    result = backend.run(qpe).result()

    plot_histogram(result.get_counts(), title='Bell-State counts')
    plt.show()

