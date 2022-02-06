from abc import ABC, abstractmethod
from typing import Tuple, Sequence

from qiskit.quantum_info import Statevector

from qiskit_check.property_test.resources.test_resource import Qubit


class QubitInputGenerator(ABC):
    @abstractmethod
    def generate(self, qubits: Sequence[Qubit]) -> Tuple[Statevector]:
        pass


class QubitInputGeneratorFactory:
    @abstractmethod
    def build(self) -> QubitInputGenerator:
        pass
