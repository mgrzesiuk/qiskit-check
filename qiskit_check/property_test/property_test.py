from abc import ABC, abstractmethod
from typing import Union, Sequence

from qiskit import QuantumCircuit

from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.assertions.abstract_assertion import AbstractAssertion


class PropertyTest(ABC):
    """
    superclass for all property tests, every property test defined needs to implement this class
    to be found and executed
    """
    def __init__(self) -> None:
        """
        initialize, set generated qubits and modify the get_qubits method to return already generated qubit templates
        """
        self.qubits = self.get_qubits()
        self.get_qubits = self._get_generated_qubits

    def _get_generated_qubits(self) -> Sequence[Qubit]:
        """

        Returns: return self.qubits (generated qubit templates)

        """
        return self.qubits

    @property
    @abstractmethod
    def circuit(self) -> QuantumCircuit:
        """
        get a circuit to be tested
        Returns: circuit to be tested

        """
        pass

    @abstractmethod
    def get_qubits(self) -> Sequence[Qubit]:
        """
        get qubit templates with the ranges specified, number of qubit templates must match number of qubits in
        the circuit
        Returns: sequence of qubit templates

        """
        pass

    @abstractmethod
    def assertions(self, qubits: Sequence[Qubit]) -> Union[AbstractAssertion, Sequence[AbstractAssertion]]:
        """
        specify assertions to be run for this test
        Args:
            qubits: qubit templates generated (can be also accessed via self.qubits)

        Returns: assertion or sequence of assertions

        """
        pass

    @staticmethod
    @abstractmethod
    def confidence_level() -> float:
        """

        Returns: desired confidence level of this test

        """
        pass

    @staticmethod
    @abstractmethod
    def num_test_cases() -> int:
        """

        Returns: desired number of test cases (number of times this test will be run with new inputs)

        """
        pass

    @staticmethod
    @abstractmethod
    def num_measurements() -> int:
        """

        Returns: number of shots that qiskit backend is going to make

        """
        pass

    @staticmethod
    @abstractmethod
    def num_experiments() -> int:
        """

        Returns: number of times a test is going to be rerun with the same parameters

        """
        pass
