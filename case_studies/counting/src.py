from math import pi, sin

import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.algorithms import AmplificationProblem, Grover
from qiskit.circuit import Gate
from qiskit.visualization import plot_histogram

from case_studies.fourier_transform.src import inverse_qft

"""
code from https://qiskit.org/textbook/ch-algorithms/quantum-counting.html
"""


def oracle(circuit: QuantumCircuit) -> QuantumCircuit:
    circuit.z(circuit.qubits[-1])
    return circuit


def controlled_grover(oracle_circuit: QuantumCircuit) -> Gate:
    problem = AmplificationProblem(oracle_circuit, is_good_state=[])
    grover_gate = Grover(iterations=1).construct_circuit(problem).to_gate()
    grover_gate = grover_gate.control()
    return grover_gate


def counting(num_counting_qubits: int, num_searching_qubits: int) -> QuantumCircuit:
    num_qubits = num_counting_qubits + num_searching_qubits
    circuit = QuantumCircuit(num_qubits, num_counting_qubits)

    for qubit in circuit.qubits:
        circuit.h(qubit)

    oracle_circuit = oracle(QuantumCircuit(num_searching_qubits))

    controlled_grover_gate = controlled_grover(oracle_circuit)

    iterations = 1
    for qubit in range(num_counting_qubits):
        for i in range(iterations):
            circuit.append(controlled_grover_gate, [qubit] + [*range(num_counting_qubits, num_qubits)])
        iterations *= 2

    inverse_qft_gate = inverse_qft(num_counting_qubits).to_gate()
    circuit.append(inverse_qft_gate, range(num_counting_qubits))

    circuit.measure(range(num_counting_qubits), range(num_counting_qubits))

    return circuit


if __name__ == "__main__":
    counting_circuit = counting(4, 4)
    counting_circuit.draw(output='mpl')
    backend = Aer.get_backend('aer_simulator')
    counting_circuit = transpile(counting_circuit, backend)

    result = backend.run(counting_circuit).result()
    hist = result.get_counts()
    plot_histogram(hist, title='Bell-State counts', figsize=(8, 7))
    plt.show()

    measured_str = max(hist, key=hist.get)
    measured_int = int(measured_str, 2)
    print("Register Output = %i" % measured_int)

    theta = (measured_int/(2**4))*pi*2
    print("Theta = %.5f" % theta)


    N = 2**4
    M = N * (sin(theta/2)**2)
    print("No. of Solutions = %.1f" % (N-M))
