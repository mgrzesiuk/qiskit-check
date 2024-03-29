from abc import ABC, abstractmethod
from typing import List, Sequence, Callable

from qiskit.quantum_info import Statevector

from qiskit_check.property_test.resources.test_resource import Qubit


class QubitInputGenerator(ABC):
    """
    base class for qubit input generator which is responsible for generating initial states of qubits in circuit
    """
    def __init__(self, state_filter: Callable[[Statevector], bool] = lambda x: True, tolerance: int = 100):
        self.state_filter = state_filter
        self.tolerance = tolerance

    @abstractmethod
    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        """
        generate initial state for qubits
        Args:
            qubits: sequence of qubits for which to generate initial values

        Returns: sequence of qiskit Statevectors which are to be initial values for qubits (respectively to position
        of qubits in the input sequence)

        """
        pass


class QubitInputGeneratorFactory:
    """
    class for creating QubitInputGenerator objects
    """
    def __init__(self, state_filter: Callable[[Statevector], bool] = lambda x: True, tolerance: int = 100):
        self.state_filter = state_filter
        self.tolerance = tolerance

    @abstractmethod
    def build(self) -> QubitInputGenerator:
        """
        create QubitInputGenerator object
        Returns: QubitInputGenerator object

        """
        pass
