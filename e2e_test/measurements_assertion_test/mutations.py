from typing import Sequence

from qiskit import QuantumCircuit, ClassicalRegister

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion, AssertMeasurementEqual, AssertMostProbable
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class MutationXMeasurementPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> Sequence[AbstractAssertion]:
        return [AssertMeasurementEqual("1"), AssertMostProbable("1")]


class MutationSMeasurementPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> Sequence[AbstractAssertion]:
        return [AssertMeasurementEqual("0"), AssertMostProbable("0")]


class MutationXTMeasurementPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.t(0)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> Sequence[AbstractAssertion]:
        return [AssertMeasurementEqual("1"), AssertMostProbable("1")]


class MutationMultipleRegistersMeasurementPropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        creg1 = ClassicalRegister(1)
        creg2 = ClassicalRegister(1)

        qc = QuantumCircuit(2)
        qc.add_register(creg2)
        qc.add_register(creg1)

        qc.x(0)
        qc.t(0)
        qc.measure(0, creg1[0])
        qc.measure(1, creg2[0])

        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> Sequence[AbstractAssertion]:
        return [AssertMeasurementEqual("01"), AssertMostProbable("01")]
