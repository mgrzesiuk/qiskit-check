from typing import Collection, Sequence

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.phase_estimation.src import phase_estimation
from qiskit_check.property_test.assertions.assertion import AbstractAssertion, AssertMeasurementEqual
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class PhaseEstimationPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        return phase_estimation(QuantumCircuit(len(self.qubits), len(self.bits)))

    def get_qubits(self) -> Collection[Qubit]:
        return [
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0))
        ]

    def get_bits(self) -> Collection[Bit]:
        return [Bit() for _ in range(len(self.qubits) - 1)]

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> AbstractAssertion:
        return AssertMeasurementEqual("001")
