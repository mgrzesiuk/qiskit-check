from math import pi
from typing import List, Sequence, Dict

from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class XEqualTruePropertyPropertyTest(BasePropertyTest):
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
        return AssertTrue(qubits, self.verify, 0)

    def verify(self, measurement: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_0_index = resource_matcher[self.qubits[0]].qubit_index
        qubit_1_index = resource_matcher[self.qubits[1]].qubit_index
        difference = 0
        for state, value in measurement[0].items():
            if state[qubit_0_index] != state[qubit_1_index]:
                difference += value

        return difference


class HEqualTruePropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(1)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertTrue(qubits, self.verify, 0)

    def verify(self, measurement: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_0_index = resource_matcher[self.qubits[0]].qubit_index
        qubit_1_index = resource_matcher[self.qubits[1]].qubit_index
        qubit_0_0_state_count = 0
        qubit_1_0_state_count = 0
    
        for state, value in measurement[0].items():
            if state[qubit_0_index] == "0":
                qubit_0_0_state_count += value
            if state[qubit_1_index] == "0":
                qubit_1_0_state_count += value

        return qubit_0_0_state_count - qubit_1_0_state_count


class QPETruePropertyPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        circuit = QuantumCircuit(4, 3)
        for qubit in circuit.qubits[:-1]:
            circuit.h(qubit)
        circuit.x(circuit.qubits[-1])
        repetitions = 1
        for counting_qubit in range(len(circuit.qubits) - 1):
            for _ in range(repetitions):
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
        return AssertTrue(qubits[:-1], self.verify, 1/8)

    @staticmethod
    def verify(measurement: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        max_state = ""
        max_count = 0
        for state, count in measurement[0].items():
            if count > max_count:
                max_count = count
                max_state = state
        nominator = int(max_state[:-1][::-1], 2)  # measured output
        denominator = 2**3  # num of estimation qubits

        return nominator/denominator
