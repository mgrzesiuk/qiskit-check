from typing import Collection

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.grover_search.src import grover_search, oracle
from qiskit_check.property_test.assertion import AbstractAssertion, AssertMostProbable
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class GroverSearchPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return grover_search(1, oracle(QuantumCircuit(qubit_number)))

    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(5)]

    @property
    def bits(self) -> Collection[Bit]:
        return []

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertMostProbable("1"*len(self.qubits))
