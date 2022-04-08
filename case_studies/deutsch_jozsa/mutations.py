from qiskit import QuantumCircuit

from case_studies.deutsch_jozsa.src import mutation_no_oracle_deutsch_jozsa, mutation_no_final_h_deutsch_jozsa
from case_studies.deutsch_jozsa.src import mutation_no_starting_h_deutsch_jozsa
from case_studies.deutsch_jozsa.tst import AbstractDeutschJozsaPropertyTest


class MutationNoOracleDeutschJozsaPropertyTest(AbstractDeutschJozsaPropertyTest):
    def __init__(self):
        super().__init__()
        self.balanced_or_constant = 1

    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_oracle_deutsch_jozsa(QuantumCircuit(4, 3), self.balanced_or_constant)


class MutationNoFinalHDeutschJozsaPropertyTest(AbstractDeutschJozsaPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_final_h_deutsch_jozsa(QuantumCircuit(4, 3), self.balanced_or_constant)


class MutationNoStartingHDeutschJozsaPropertyTest(AbstractDeutschJozsaPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_starting_h_deutsch_jozsa(QuantumCircuit(4, 3), self.balanced_or_constant)
