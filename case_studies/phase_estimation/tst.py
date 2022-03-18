from abc import ABC
from typing import Collection, Sequence, List

from qiskit import QuantumCircuit

from case_studies.example_test_base import ExampleTestBase
from case_studies.phase_estimation.src import phase_estimation
from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.resources.qubit_range import QubitRange


class AbstractPhaseEstimationPropertyTest(ExampleTestBase, ABC):
    def get_qubits(self) -> Collection[Qubit]:
        return [
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0)),
            Qubit(QubitRange(0, 0, 0, 0))
        ]

    def assertions(self, qubits: Sequence[Qubit]) -> List[AbstractAssertion]:
        return [  # check if this works well 001 should be output
            AssertProbability(self.qubits[0], "1", 1),
            AssertProbability(self.qubits[1], "0", 1),
            AssertProbability(self.qubits[2], "0", 1),
        ]


class PhaseEstimationPropertyTest(AbstractPhaseEstimationPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return phase_estimation(QuantumCircuit(len(self.qubits), 3))
