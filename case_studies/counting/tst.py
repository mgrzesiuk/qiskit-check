from abc import ABC
from math import sin, pi
from typing import Dict, List, Sequence

from qiskit import QuantumCircuit

from case_studies.counting.src import counting
from case_studies.example_test_base import ExampleTestBase
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class AbstractCountingPropertyTest(ExampleTestBase, ABC):
    def __init__(self):
        self.num_counting_qubits = 4
        self.num_searching_qubits = 4
        self.num_qubits = self.num_counting_qubits + self.num_searching_qubits
        super().__init__()

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(self.num_qubits)]

    def check_number_of_solutions(self, measurement: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        max_state = ""
        max_count = -1
        for state, count in measurement[0].items():
            if count > max_count:
                max_count = count
                max_state = state

        measured_int = int(max_state[:self.num_counting_qubits][::-1], 2)
        theta = (measured_int / (2 ** 4)) * pi * 2
        N = 2 ** self.num_searching_qubits
        M = N * (sin(theta / 2) ** 2)
        return N-M

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTrue(qubits[:self.num_counting_qubits], self.check_number_of_solutions, 16)


class CountingPropertyTest(AbstractCountingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return counting(self.num_counting_qubits, self.num_searching_qubits)
