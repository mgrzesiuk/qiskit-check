from typing import Collection, Sequence

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.superdense_coding.src import superdense_coding
from qiskit_check.property_test.assertions.assertion import AbstractAssertion, AssertMeasurementEqual
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import AnyRange


class SuperdenseCodingPropertyTest(ExampleTestBase):
    @property
    def bitstring(self) -> str:
        bits = self.bits
        #return str(bits[0].value()) + str(bits[1].value())
        return '11'

    @property
    def circuit(self) -> QuantumCircuit:
        return superdense_coding(self.bitstring)

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange()), Qubit(AnyRange())]

    def get_bits(self) -> Collection[Bit]:
        return [Bit(), Bit()]

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> AbstractAssertion:
        return AssertMeasurementEqual(self.bitstring)
