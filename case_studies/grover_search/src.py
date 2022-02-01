from math import ceil, pi, sqrt

import matplotlib.pyplot as plt

from qiskit import Aer, transpile
from qiskit import QuantumCircuit
from qiskit.algorithms import AmplificationProblem, Grover
from qiskit.visualization import plot_histogram


def oracle(circuit: QuantumCircuit) -> QuantumCircuit:
    circuit.mcrz(pi, circuit.qubits[:-1], circuit.qubits[-1])
    return circuit


def grover_search(number_of_solutions: int, oracle_circuit: QuantumCircuit) -> QuantumCircuit:
    search_space_size = 2**len(oracle_circuit.qubits)

    number_of_rotations = ceil(pi*sqrt(number_of_solutions/search_space_size)/4)

    problem = AmplificationProblem(oracle_circuit, is_good_state=[])
    grover = Grover(iterations=number_of_rotations)
    return grover.construct_circuit(problem)


if __name__ == "__main__":
    qubit_number = 3
    grover_circuit = grover_search(1, oracle(QuantumCircuit(qubit_number)))
    grover_circuit.measure_all()
    grover_circuit.draw(output='mpl')
    backend = Aer.get_backend('aer_simulator')
    grover_circuit = transpile(grover_circuit, backend)

    result = backend.run(grover_circuit).result()

    plot_histogram(result.get_counts(), title='Bell-State counts')
    plt.show()
