from math import pi
from typing import Sequence

from qiskit import QuantumCircuit

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.assertions.assert_phase import AssertPhase
from qiskit_check.property_test.resources import Qubit, AnyRange, QubitRange


class MutationAssertPhasePropertyTest(BasePropertyTest):
    phase = pi/4
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.p(self.phase, 0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertPhase(qubits[0], self.phase*3/4)

class MutationAssertPhaseMidCircuitPropertyTest(BasePropertyTest):
    phase = pi/4
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.p(self.phase, 0)
        qc.p(self.phase, 0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertPhase(qubits[0], self.phase*2/3, 2)
