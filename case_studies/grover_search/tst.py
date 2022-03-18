from abc import ABC
from typing import Collection, Sequence

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.grover_search.src import grover_search, oracle
from qiskit_check.property_test.assertions import AbstractAssertion, AssertMostProbable
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class AbstractGroverSearchPropertyTest(ExampleTestBase, ABC):
    def get_qubits(self) -> Collection[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(5)]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertMostProbable("1"*len(self.qubits))


class GroverSearchPropertyTest(AbstractGroverSearchPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qubit_number = len(self.qubits)
        return grover_search(1, oracle(QuantumCircuit(qubit_number)))
