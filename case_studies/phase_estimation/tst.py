from typing import Collection

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.phase_estimation.src import phase_estimation
from qiskit_property_testing.property_test.assertions.assertion import AbstractAssertion, AssertMeasurement
from qiskit_property_testing.property_test.resources.test_resource import Qubit, Bit
from qiskit_property_testing.property_test.resources.qubit_range import AngleRange


class PhaseEstimationPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        return phase_estimation(QuantumCircuit(len(self.qubits), len(self.bits)))

    @property
    def qubits(self) -> Collection[Qubit]:
        return [
            Qubit(AngleRange(0, 0, 0, 0)),
            Qubit(AngleRange(0, 0, 0, 0)),
            Qubit(AngleRange(0, 0, 0, 0)),
            Qubit(AngleRange(0, 0, 0, 0))
        ]

    @property
    def bits(self) -> Collection[Bit]:
        return [Bit() for _ in range(len(self.qubits) - 1)]

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertMeasurement("001")
