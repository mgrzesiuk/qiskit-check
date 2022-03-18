from typing import Collection, Sequence

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from qiskit_check.property_test.assertions import AbstractAssertion, AssertEntangled
from qiskit_check.property_test.resources import Qubit, QubitRange


class EntanglePropertyTest(ExampleTestBase):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(1)
        qc.measure_all()
        return qc

    def get_qubits(self) -> Collection[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(2)]

    def assertions(self, qubits: Sequence[Qubit]) -> AbstractAssertion:
        return AssertEntangled(qubits[0], qubits[1])
