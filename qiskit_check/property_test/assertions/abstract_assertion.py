from abc import ABC, abstractmethod
from typing import Dict

from qiskit_check.property_test.property_test_errors import NoExperimentsError

from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AbstractAssertion(ABC):
    @abstractmethod
    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get_p_value if the assertion holds
        Args:
            experiments: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """
        pass

    def verify(self, confidence_level: float, p_value: float) -> None:
        """
        verify if assertion passed (do nothing then) or raise an error if it failed
        Args:
            confidence_level: expected confidence level of the test
            p_value: p value obtained from get_p_value()

        Returns: None
        """

        if 1 - confidence_level >= p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"{self.__class__.__name__} failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold} to fail to reject equality hypothesis")

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {}

    @staticmethod
    def check_if_experiments_empty(result: TestResult) -> None:
        """
        check if number of experiments is 0 and if so raise an error
        Args:
            result: results obtained from test runner

        Returns: None
        """
        if result.num_experiments == 0:
            raise NoExperimentsError("no experiments have been provided")
