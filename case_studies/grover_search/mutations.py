from qiskit import QuantumCircuit

from case_studies.grover_search.src import grover_search, oracle, mutation_add_h_grover_search, mutation_oracle
from case_studies.grover_search.src import mutation_wrong_gate_oracle
from case_studies.grover_search.tst import AbstractGroverSearchPropertyTest


class MutationOracleWrongGateGroverSearchPropertyTest(AbstractGroverSearchPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return grover_search(1, mutation_wrong_gate_oracle(QuantumCircuit(qubit_number)))


class MutationOracleGroverSearchPropertyTest(AbstractGroverSearchPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return grover_search(1, mutation_oracle(QuantumCircuit(qubit_number)))


class MutationAddHGateGroverSearchPropertyTest(AbstractGroverSearchPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return mutation_add_h_grover_search(1, oracle(QuantumCircuit(qubit_number)))


class MutationAddHWrongGateOracleGroverSearchPropertyTest(AbstractGroverSearchPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return mutation_add_h_grover_search(1, mutation_wrong_gate_oracle(QuantumCircuit(qubit_number)))


class MutationAddHWrongOracleGroverSearchPropertyTest(AbstractGroverSearchPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return mutation_add_h_grover_search(1, mutation_oracle(QuantumCircuit(qubit_number)))
