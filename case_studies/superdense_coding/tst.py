from typing import Collection, Sequence, List

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.superdense_coding.src import superdense_coding
from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class SuperdenseCodingPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        return superdense_coding('11')

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def get_bits(self) -> Collection[Bit]:
        return [Bit(), Bit()]

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> List[AbstractAssertion]:
        return [
            AssertProbability(self.qubits[0], "1", 1),
            AssertProbability(self.qubits[1], "1", 1)
        ]
