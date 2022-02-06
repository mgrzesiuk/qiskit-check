from typing import Collection

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.teleportation.src import quantum_teleportation
from qiskit_check.property_test.assertion import AbstractAssertion, AssertTeleported
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import AngleRange, AnyRange


class TeleportationProperty(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        return quantum_teleportation()

    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(AnyRange()), Qubit(AngleRange(0, 0, 0, 0)), Qubit(AngleRange(0, 0, 0, 0))]

    @property
    def bits(self) -> Collection[Bit]:
        return [Bit(), Bit()]

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertTeleported(self.qubits[0])
