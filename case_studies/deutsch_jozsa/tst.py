import random
from typing import Collection

from qiskit import QuantumCircuit

from case_studies.deutsch_jozsa.src import deutsch_jozsa
from case_studies.example_test_base import ExampleTestBase
from qiskit_property_testing.property_test.assertions.assertion import AbstractAssertion, AssertTrue
from qiskit_property_testing.property_test.resources.test_resource import Qubit, Bit
from qiskit_property_testing.property_test.resources.qubit_range import AngleRange, AnyRange


class DeutschJozsaPropertyTest(ExampleTestBase):
    def __init__(self):
        self.balanced_or_constant = random.randint(0, 1)

    @property
    def circuit(self) -> QuantumCircuit:
        return deutsch_jozsa(QuantumCircuit(4, 3), self.balanced_or_constant)

    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(AngleRange(0, 0, 0, 0)) for _ in range(4)]

    @property
    def bits(self) -> Collection[Bit]:

        return [Bit() for _ in range(3)]

    def evaluate_correctness(self, measurement):
        if self.balanced_or_constant == 1:
            return measurement == "1"*len(self.bits)
        else:
            return measurement == "0"*len(self.bits)

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertTrue(self.evaluate_correctness)
