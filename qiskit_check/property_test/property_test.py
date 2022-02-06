from abc import ABC, abstractmethod
from typing import Union, Sequence

from qiskit import QuantumCircuit

from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.assertion import AbstractAssertion


class PropertyTest(ABC):
    @property
    @abstractmethod
    def circuit(self) -> QuantumCircuit:
        pass

    @property
    @abstractmethod
    def qubits(self) -> Sequence[Qubit]:
        pass

    @property
    @abstractmethod
    def bits(self) -> Sequence[Bit]:
        pass

    @property
    @abstractmethod
    def assertions(self) -> Union[AbstractAssertion, Sequence[AbstractAssertion]]:
        pass

    @property
    @abstractmethod
    def confidence_level(self) -> float:
        pass

    @staticmethod
    @abstractmethod
    def num_test_cases() -> int:
        pass

    @property
    @abstractmethod
    def num_measurements(self) -> int:
        pass

    @property
    @abstractmethod
    def num_experiments(self) -> int:
        pass
