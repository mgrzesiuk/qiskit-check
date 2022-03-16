from random import choices
from typing import Collection, Sequence, List

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.superdense_coding.src import superdense_coding
from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class SuperdenseCodingPropertyTest(ExampleTestBase):
    def __init__(self) -> None:
        super().__init__()
        self.bitstring = choices(['11', '10', '01', '00'])[0]

    @property
    def circuit(self) -> QuantumCircuit:
        return superdense_coding(self.bitstring)

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def get_bits(self) -> Collection[Bit]:
        return [Bit(), Bit()]

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> List[AbstractAssertion]:
        return [
            AssertProbability(self.qubits[0], self.bitstring[1], 1),
            AssertProbability(self.qubits[1], self.bitstring[0], 1)
        ]
