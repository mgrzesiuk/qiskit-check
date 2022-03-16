from abc import ABC, abstractmethod
from typing import Union, Sequence

from qiskit import QuantumCircuit

from qiskit_check.property_test.resources.test_resource import Qubit, Bit
from qiskit_check.property_test.assertions import AbstractAssertion


class PropertyTest(ABC):
    def __init__(self) -> None:
        self.qubits = self.get_qubits()
        self.bits = self.get_bits()

    @property
    @abstractmethod
    def circuit(self) -> QuantumCircuit:
        pass

    @abstractmethod
    def get_qubits(self) -> Sequence[Qubit]:
        pass

    @abstractmethod
    def get_bits(self) -> Sequence[Bit]:
        pass  # TODO: remove this?

    @abstractmethod
    def assertions(
            self, qubits: Sequence[Qubit],
            bits: Sequence[Bit]) -> Union[AbstractAssertion, Sequence[AbstractAssertion]]:
        pass

    @staticmethod
    @abstractmethod
    def confidence_level() -> float:
        pass

    @staticmethod
    @abstractmethod
    def num_test_cases() -> int:
        pass

    @staticmethod
    @abstractmethod
    def num_measurements() -> int:
        pass

    @staticmethod
    @abstractmethod
    def num_experiments() -> int:
        pass
