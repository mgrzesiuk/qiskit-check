from typing import Sequence

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.teleportation.src import quantum_teleportation
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTeleported
from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.resources.qubit_range import QubitRange, AnyRange


class TeleportationProperty(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        return quantum_teleportation()

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange()), Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def get_bits(self) -> Sequence[Bit]:
        return [Bit(), Bit()]

    def assertions(self, qubits: Sequence[Qubit], bits: Sequence[Bit]) -> AbstractAssertion:
        return AssertTeleported(qubits[0], qubits[2])
