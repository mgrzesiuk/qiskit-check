from math import pi
from typing import Sequence, List

from qiskit import QuantumCircuit
from scipy.spatial.transform import Rotation

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.assertions import AssertStateTransformed
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import AnyRange


class SingleGateStateTransformedPropertyPropertyTest(BasePropertyTest):
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
        return AssertStateTransformed(qubits[0], 1, Rotation.from_euler("X", [pi]))


class SSingleGateStateTransformedPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateTransformed(qubits[0], 1, Rotation.from_euler("Z", [pi/2]))


class HSingleGateStateTransformedPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateTransformed(qubits[0], 1, Rotation.from_euler("XY", [pi, pi/2]))


class MultipleGateStateTransformedPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.h(0)
        qc.x(0)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(AnyRange())]

    def assertions(self, qubits: Sequence[Qubit]) -> List[AbstractAssertion]:
        return [
            AssertStateTransformed(qubits[0], 1, Rotation.from_euler("XY", [pi, pi/2])),
            AssertStateTransformed(qubits[0], 2, Rotation.identity()),
            AssertStateTransformed(qubits[0], 3, Rotation.from_euler("X", [pi])),
            AssertStateTransformed(qubits[0], 4, Rotation.from_euler("XYX", [pi, pi/2, pi]))
        ]
