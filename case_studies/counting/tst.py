from math import sin, pi
from typing import Dict, Sequence

from qiskit import QuantumCircuit

from case_studies.counting.src import counting
from case_studies.example_test_base import ExampleTestBase
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import Qubit, Bit, ConcreteQubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class CountingPropertyTest(ExampleTestBase):
    def __init__(self):
        self.num_counting_qubits = 4
        self.num_searching_qubits = 4
        self.num_qubits = self.num_counting_qubits + self.num_searching_qubits
        super().__init__()

    @property
    def circuit(self) -> QuantumCircuit:
        return counting(self.num_counting_qubits, self.num_searching_qubits)

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(self.num_qubits)]

    def get_bits(self) -> Sequence[Bit]:
        return [Bit() for _ in range(self.num_searching_qubits)]

    def check_number_of_solutions(
            self, measurement: dict[str, int], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        max_value = -1
        max_measurement = ""
        for key, value in measurement.items():
            if value > max_value:
                max_value = value
                max_measurement = key

        measured_int = int(max_measurement, 2)
        theta = (measured_int / (2 ** 4)) * pi * 2
        N = 2 ** self.num_searching_qubits
        M = N * (sin(theta / 2) ** 2)
        return N-M

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> AbstractAssertion:
        return AssertTrue(self.check_number_of_solutions, 16)
