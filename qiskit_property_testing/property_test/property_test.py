from abc import ABC, abstractmethod
from typing import Collection, Union

from qiskit import QuantumCircuit

from qiskit_property_testing.property_test.resources.test_resource import Qubit, Bit
from qiskit_property_testing.property_test.assertions.assertion import AbstractAssertion


class PropertyTest(ABC):
    @property
    @abstractmethod
    def circuit(self) -> QuantumCircuit:
        pass

    @property
    @abstractmethod
    def qubits(self) -> Collection[Qubit]:
        pass

    @property
    @abstractmethod
    def bits(self) -> Collection[Bit]:
        pass

    @property
    @abstractmethod
    def assertions(self) -> Union[AbstractAssertion, Collection[AbstractAssertion]]:
        pass

    @property
    @abstractmethod
    def confidence_level(self) -> float:
        pass

    @property
    @abstractmethod
    def num_test_cases(self) -> int:
        pass

    @property
    @abstractmethod
    def num_measurements(self) -> int:
        pass

    @property
    @abstractmethod
    def num_experiments(self) -> int:
        pass
