from abc import ABC, abstractmethod
from typing import List, Sequence

from qiskit.quantum_info import Statevector

from qiskit_check.property_test.resources.test_resource import Qubit


class QubitInputGenerator(ABC):
    @abstractmethod
    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        pass


class QubitInputGeneratorFactory:
    @abstractmethod
    def build(self) -> QubitInputGenerator:
        pass
