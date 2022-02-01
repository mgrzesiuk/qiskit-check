from typing import Collection

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.fourier_transform.src import qft, inverse_qft
from qiskit_property_testing.property_test.assertions.assertion import AbstractAssertion, AssertTransformed
from qiskit_property_testing.property_test.resources.test_resource import Qubit, Bit
from qiskit_property_testing.property_test.resources.qubit_range import AnyRange


class FourierInverseAndFourierGiveIdentityProperty(ExampleTestBase):
    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(AnyRange()), Qubit(AnyRange()), Qubit(AnyRange())]

    @property
    def bits(self) -> Collection[Bit]:
        return []

    @property
    def assertions(self) -> Collection[AbstractAssertion]:
        assertions = []
        for qubit in self.qubits:
            assertions.append(AssertTransformed(qubit, 0, 0))
        return assertions

    @property
    def circuit(self) -> QuantumCircuit:
        number_qubits = len(self.qubits)
        test_circuit = qft(number_qubits)
        test_circuit += inverse_qft(number_qubits)
        return test_circuit
