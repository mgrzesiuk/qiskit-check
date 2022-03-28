from math import pi
from typing import Sequence

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.assertions import AssertStateEqual
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class XStateEqualPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (pi, 0))


class H0StateEqualPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (pi/2, 0))


class H1StateEqualPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(pi, 0, pi, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (pi/2, pi))


class S0StateEqualPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (0, pi/2))


class S1StateEqualPropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.s(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(pi, 0, pi, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertStateEqual(qubits[0], 1, (pi, pi/2))
