from math import sin, pi
from typing import Collection

from qiskit import QuantumCircuit

from case_studies.counting.src import counting
from case_studies.example_test_base import ExampleTestBase
from qiskit_check.property_test.assertion import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import AngleRange


class CountingPropertyTest(ExampleTestBase):
    def __init__(self):
        self.num_counting_qubits = 4
        self.num_searching_qubits = 4
        self.num_qubits = self.num_counting_qubits + self.num_searching_qubits

    @property
    def circuit(self) -> QuantumCircuit:
        return counting(self.num_counting_qubits, self.num_searching_qubits)

    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(AngleRange(0, 0, 0, 0)) for _ in range(self.num_qubits)]

    @property
    def bits(self) -> Collection[Bit]:
        return [Bit() for _ in range(self.num_searching_qubits)]

    def check_number_of_solutions(self, measurement: str):
        measured_int = int(measurement, 2)
        theta = (measured_int / (2 ** 4)) * pi * 2
        N = 2 ** self.num_searching_qubits
        M = N * (sin(theta / 2) ** 2)
        return (N-M) == N

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertTrue(self.check_number_of_solutions)
