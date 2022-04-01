from math import pi
from typing import Sequence

from qiskit import QuantumCircuit
from scipy.spatial.transform import Rotation

from e2e_test.test_base import TestBase
from qiskit_check.property_test.assertions import AssertTransformed, AbstractAssertion
from qiskit_check.property_test.resources import Qubit, AnyRange


class MutationSSingleGateTransformedPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTransformed(qubits[0], Rotation.from_euler("Z", [pi/2]))


class MutationXSingleGateTransformedPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTransformed(qubits[0], Rotation.from_euler("X", [pi]))


class MutationHSingleGateTransformedPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTransformed(qubits[0], Rotation.from_euler("XY", [pi/2, pi]))

