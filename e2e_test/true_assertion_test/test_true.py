from math import pi
from typing import Sequence, Dict

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

from e2e_test.test_base import TestBase
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.resources.qubit_range import QubitRange
from qiskit_check.property_test.test_results import MeasurementResult


class XEqualTruePropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.x(1)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTrue(self.verify, 0)

    def verify(self, measurement: MeasurementResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_0_index = resource_matcher[self.qubits[0]].qubit_index
        qubit_1_index = resource_matcher[self.qubits[1]].qubit_index

        difference = measurement.get_qubit_result(qubit_0_index, "0") - measurement.get_qubit_result(qubit_1_index, "0")
        return difference


class HEqualTruePropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(1)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]  # TODO: possible direction - allow random but equal qubit generation

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTrue(self.verify, 0)

    def verify(self, measurement: MeasurementResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_0_index = resource_matcher[self.qubits[0]].qubit_index
        qubit_1_index = resource_matcher[self.qubits[1]].qubit_index

        difference = measurement.get_qubit_result(qubit_0_index, "0") - measurement.get_qubit_result(qubit_1_index, "0")
        return difference


class QPETruePropertyTest(TestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        circuit = QuantumCircuit(4, 3)
        for qubit in circuit.qubits[:-1]:
            circuit.h(qubit)
        circuit.x(circuit.qubits[-1])
        repetitions = 1
        for counting_qubit in range(len(circuit.qubits) - 1):
            for i in range(repetitions):
                circuit.cp(pi/4, counting_qubit, circuit.qubits[-1])
            repetitions *= 2
        qft_inverse = QFT(len(circuit.qubits) - 1, inverse=True).to_instruction()
        circuit.append(qft_inverse, circuit.qubits[:-1])
        for qubit_index in range(len(circuit.qubits) - 1):
            circuit.measure(qubit_index, qubit_index)
        return circuit

    def get_qubits(self) -> Sequence[Qubit]:
        return [
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0))
        ]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTrue(self.verify, 1/8)

    @staticmethod
    def verify(measurement: MeasurementResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        counts = measurement.get_counts()
        max_state = ""
        max_count = 0
        for state, count in counts.items():
            if count > max_count:
                max_count = count
                max_state = state
        nominator = int(max_state, 2)  # measured output
        denominator = 2**3  # num of estimation qubits

        return nominator/denominator
