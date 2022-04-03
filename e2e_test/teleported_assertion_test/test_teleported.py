from abc import ABC
from typing import Sequence

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from e2e_test.test_base import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTeleported
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange, AnyRange


class AbstractTeleportationProperty(BasePropertyTest, ABC):
    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange()), Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTeleported(qubits[0], qubits[2])


class TeleportationProperty(AbstractTeleportationProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        qr = QuantumRegister(3, name="q")
        crz, crx = ClassicalRegister(1, name="crz"), ClassicalRegister(1, name="crx")
        teleportation_result = ClassicalRegister(1, name="teleportation_result")
        circuit = QuantumCircuit(qr, crz, crx, teleportation_result)

        # entangle
        circuit.h(1)
        circuit.cx(1, 2)

        circuit.cx(0, 1)
        circuit.h(0)

        circuit.measure(0, 0)
        circuit.measure(1, 1)

        circuit.x(2).c_if(crx, 1)  # Apply gates if the registers are in the state '1'
        circuit.z(2).c_if(crz, 1)

        circuit.measure(2, 2)
        return circuit

