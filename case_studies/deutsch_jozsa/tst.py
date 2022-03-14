from random import randint
from typing import Collection, Sequence, Dict

from qiskit import QuantumCircuit

from case_studies.deutsch_jozsa.src import deutsch_jozsa
from case_studies.example_test_base import ExampleTestBase
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources import Bit, Qubit, QubitRange, ConcreteQubit
from qiskit_check.property_test.test_results import MeasurementResult


class DeutschJozsaPropertyTest(ExampleTestBase):
    def __init__(self):
        self.balanced_or_constant = randint(0, 1)
        super().__init__()

    @property
    def circuit(self) -> QuantumCircuit:
        return deutsch_jozsa(QuantumCircuit(4, 3), self.balanced_or_constant)

    def get_qubits(self) -> Collection[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(4)]

    def get_bits(self) -> Collection[Bit]:

        return [Bit() for _ in range(3)]

    def evaluate_correctness(self, measurement: MeasurementResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> int:
        counts = measurement.get_counts()
        measurement = list(counts.keys())[0]
        if len(counts.keys()) > 1:
            return 0
        if self.balanced_or_constant == 1:
            return measurement == "1"*len(self.bits)
        else:
            return measurement == "0"*len(self.bits)

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> AbstractAssertion:
        return AssertTrue(self.evaluate_correctness, 1)
