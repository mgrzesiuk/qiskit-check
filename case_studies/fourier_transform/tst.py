from typing import Sequence, List

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.fourier_transform.src import qft, inverse_qft
from qiskit_check.property_test.assertions.assertion import AbstractAssertion, AssertTransformed
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import AnyRange


class FourierInverseAndFourierGiveIdentityProperty(ExampleTestBase):
    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange()), Qubit(AnyRange()), Qubit(AnyRange())]

    def get_bits(self) -> Sequence[Bit]:
        return []

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> List[AbstractAssertion]:
        assertions = []
        for qubit in self.qubits:
            assertions.append(AssertTransformed(qubit, 0, 0))
        return assertions

    @property
    def circuit(self) -> QuantumCircuit:
        number_qubits = len(self.qubits)
        test_circuit = qft(number_qubits)
        test_circuit = test_circuit.compose(inverse_qft(number_qubits))
        return test_circuit
