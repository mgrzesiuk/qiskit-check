from abc import ABC
from typing import Sequence, List

from qiskit import QuantumCircuit
from scipy.spatial.transform import Rotation

from case_studies.example_test_base import ExampleTestBase
from case_studies.fourier_transform.src import qft
from qiskit_check.property_test.assertions import AssertTransformedByProbability, AbstractAssertion
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import AnyRange


class AbstractFourierInverseAndFourierGiveIdentityProperty(ExampleTestBase, ABC):
    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange()), Qubit(AnyRange()), Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> List[AbstractAssertion]:
        assertions = []
        for qubit in self.qubits:
            assertions.append(AssertTransformedByProbability(qubit, Rotation.identity()))
        return assertions


class FourierInverseAndFourierGiveIdentityProperty(AbstractFourierInverseAndFourierGiveIdentityProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        number_qubits = len(self.qubits)
        test_circuit = qft(number_qubits)
        test_circuit = test_circuit.compose(qft(number_qubits).inverse())
        test_circuit.measure_all()
        return test_circuit
