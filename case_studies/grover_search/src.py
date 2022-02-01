from math import ceil, pi, sqrt

from qiskit import QuantumCircuit
from qiskit.algorithms import AmplificationProblem, Grover


def oracle(circuit: QuantumCircuit) -> QuantumCircuit:
    circuit.mcrz(pi, circuit.qubits[:-1], circuit.qubits[-1])
    return circuit


def grover_search(number_of_solutions: int, oracle_circuit: QuantumCircuit) -> QuantumCircuit:
    search_space_size = 2**len(oracle_circuit.qubits)

    number_of_rotations = ceil(pi*sqrt(number_of_solutions/search_space_size)/4)

    problem = AmplificationProblem(oracle_circuit, is_good_state=[])
    grover = Grover(iterations=number_of_rotations)
    return grover.construct_circuit(problem)