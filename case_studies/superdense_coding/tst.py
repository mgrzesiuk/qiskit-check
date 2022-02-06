from typing import Collection

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.superdense_coding.src import superdense_coding
from qiskit_check.property_test.assertion import AbstractAssertion, AssertMeasurementEqual
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import AnyRange


class SuperdenseCodingPropertyTest(ExampleTestBase):
    @property
    def bitstring(self) -> str:
        bits = self.bits
        return str(bits[0].value()) + str(bits[1].value())

    @property
    def circuit(self) -> QuantumCircuit:
        return superdense_coding(self.bitstring)

    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(AnyRange()), Qubit(AnyRange())]

    @property
    def bits(self) -> Collection[Bit]:
        return [Bit(), Bit()]

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertMeasurementEqual(self.bitstring)
