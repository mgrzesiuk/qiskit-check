from abc import abstractmethod
from typing import Sequence, List

from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator import QubitInputGenerator
from qiskit_check.property_test.resources import Qubit


class IndependentInputGenerator(QubitInputGenerator):
    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        return [self._generate_single_value(qubit) for qubit in qubits]

    @staticmethod
    @abstractmethod
    def _generate_single_value(qubit: Qubit) -> Statevector:
        pass
