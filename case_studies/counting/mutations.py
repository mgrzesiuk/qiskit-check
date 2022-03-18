from qiskit import QuantumCircuit

from case_studies.counting.src import mutation_counting_additional_x_gates, mutation_counting_no_inverse
from case_studies.counting.src import mutation_counting_too_little_grover_gates

from case_studies.counting.tst import AbstractCountingPropertyTest


class MutationCountingNoInversePropertyTest(AbstractCountingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_counting_no_inverse(self.num_counting_qubits, self.num_searching_qubits)


class MutationCountingTooLittleGroverPropertyTest(AbstractCountingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_counting_too_little_grover_gates(self.num_counting_qubits, self.num_searching_qubits)


class MutationCountingXGatesPropertyTest(AbstractCountingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_counting_additional_x_gates(self.num_counting_qubits, self.num_searching_qubits)
