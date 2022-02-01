import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.circuit import Gate
from qiskit.visualization import plot_histogram

"""
algorithm from https://qiskit.org/textbook/ch-algorithms/deutsch-jozsa.html
"""


def constant_oracle(circuit: QuantumCircuit) -> Gate:
    return circuit.to_gate()


def balanced_oracle(circuit: QuantumCircuit) -> Gate:
    i = 0
    for qubit in circuit.qubits[:-1]:
        if i % 2 == 0:
            circuit.x(qubit)
        i += 1
        circuit.cnot(qubit, circuit.qubits[-1])

    return circuit.to_gate()


def deutsch_jozsa(circuit: QuantumCircuit, oracle: int) -> QuantumCircuit:
    circuit.x(circuit.qubits[-1])

    for qubit in circuit.qubits:
        circuit.h(qubit)
    if oracle == 1:
        oracle_gate = balanced_oracle(QuantumCircuit(len(circuit.qubits)))
    else:
        oracle_gate = constant_oracle(QuantumCircuit(len(circuit.qubits)))

    circuit.append(oracle_gate, circuit.qubits)

    for qubit in circuit.qubits[:-1]:
        circuit.h(qubit)

    for qubit_index in range(len(circuit.qubits[:-1])):
        circuit.measure(qubit_index, qubit_index)

    return circuit


if __name__ == "__main__":
    test_circuit = deutsch_jozsa(QuantumCircuit(4, 3), 1)
    backend = Aer.get_backend('aer_simulator')
    grover_circuit = transpile(test_circuit, backend)

    result = backend.run(grover_circuit).result()

    plot_histogram(result.get_counts(), title='Bell-State counts')
    plt.show()
