from math import pi
from typing import Sequence

from qiskit import QuantumCircuit

from e2e_test.test_base import TestBase
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.assertions import AssertStateEqual
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class MutationXStateEqualPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 0, (pi, 0))


class MutationH0StateEqualPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (pi/2, pi))


class MutationH1StateEqualPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(pi, 0, pi, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (pi/2, pi))


class MutationS0StateEqualPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 2, (0, pi/2))


class MutationS1StateEqualPropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(pi, 0, pi, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 2, (pi, pi/2))
