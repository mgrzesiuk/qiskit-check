from typing import Sequence

from qiskit import QuantumCircuit

from e2e_test.base_property_test import BasePropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion, AssertEqualByProbability
from qiskit_check.property_test.resources import Qubit, QubitRange
from qiskit_check.test_engine.config import DefaultConfig
from qiskit_check.test_engine.main import get_processor

def get_circuit():
    return QuantumCircuit(2)

def get_faulty_circuit():
    qc = QuantumCircuit(2)
    qc.x(0)
    return qc

class SimplePropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return get_circuit()

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertEqualByProbability(qubits[0], qubits[1])

class SimpleFailingPropertyTest(BasePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return get_faulty_circuit()

    def get_qubits(self) -> Sequence[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)), Qubit(QubitRange(0, 0, 0, 0))]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertEqualByProbability(qubits[0], qubits[1])


if __name__ == "__main__":
    processor = get_processor(DefaultConfig())
    passing, failing = processor.process({SimpleFailingPropertyTest, SimplePropertyTest})
    print(f"passing test {passing}")
    print(f"failing test {failing}")

