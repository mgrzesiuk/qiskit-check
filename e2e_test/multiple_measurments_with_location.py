from math import pi
from typing import List, Sequence

from qiskit import QuantumCircuit
from qiskit.circuit import Measure

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.assertions import AssertEntangled, AssertEqualByProbability
from qiskit_check.property_test.assertions import AssertProbability
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange
from qiskit_check.property_test.utils import get_global_instruction_location

def get_x_measurement():
    measure_name = "measure_x"
    qc = QuantumCircuit(1, 1,  name=measure_name)
    qc.h(0)
    qc.measure(0, 0)
    return qc.to_instruction(label=measure_name)
    
def get_y_measurement():
    measure_name = "measure_y"
    qc = QuantumCircuit(1, 1, name=measure_name)
    qc.rx(-pi/2, 0)
    qc.measure(0, 0)
    return qc.to_instruction(label=measure_name)


class EntangledMidCircuitWithXMeasureAndZMeasurePropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.x(1)
        qc.h(0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertEntangled(qubits[0], qubits[1], measurements=(get_x_measurement(), Measure()), location=get_global_instruction_location(self.circuit, 1, 2))


class AssertEqualYBasisMidCircuitPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(1)
        qc.x(0)
        qc.x(1)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertEqualByProbability(qubits[0], qubits[1], measurements=(get_y_measurement(),), location=2)

class AssertProbabilityXBasisMidCircuitPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(1)
        qc.h(0)
        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertProbability(qubits[0], "0", 1, measurements=(get_x_measurement(),), location=1)


class MultipleAssertionsPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(0, 1) 
        qc.h(1)

        return qc

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> List[AbstractAssertion]:
        return [
            AssertProbability(qubits[0], "0", 0.5, location=1),
            AssertProbability(qubits[0], "0", 1, measurements=(get_x_measurement(), ), location=1),
            AssertEntangled(qubits[0], qubits[1], location=2),
            AssertEqualByProbability(qubits[0], qubits[1], measurements=(get_x_measurement(), get_y_measurement()))
        ]
