from abc import ABC
from typing import Sequence

from qiskit import QuantumCircuit

from e2e_test.test_base import TestBase
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.assertions import AssertEqual
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class AbstractEqualPropertyTest(TestBase, ABC):
    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertEqual(qubits[0], qubits[1])


class XEqualPropertyTest(AbstractEqualPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.x(1)
        qc.measure_all()
        return qc


class HEqualPropertyTest(AbstractEqualPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(1)
        qc.measure_all()
        return qc


class SEqualPropertyTest(AbstractEqualPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.x(1)
        qc.s(0)
        qc.s(1)
        qc.measure_all()
        return qc


class DoubleHEqualPropertyTest(AbstractEqualPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(0)
        qc.x(1)
        qc.x(1)
        qc.measure_all()
        return qc
