from math import pi
from typing import Sequence

from qiskit import QuantumCircuit
from scipy.spatial.transform import Rotation

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AssertTransformedByProbability, AbstractAssertion
from qiskit_check.property_test.resources import Qubit, AnyRange


class MutationSSingleGateTransformedPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.x(0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTransformedByProbability(qubits[0], Rotation.from_euler("Z", [pi/2]))


class MutationXSingleGateTransformedPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTransformedByProbability(qubits[0], Rotation.from_euler("X", [pi]))


class MutationHSingleGateTransformedPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.h(0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTransformedByProbability(qubits[0], Rotation.from_euler("XY", [pi/2, pi]))

