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

    @abstractmethod
    def verify(self, confidence_level: float, p_value: float) -> None:
        """
        verify if assertion passed (do nothing then) or raise an error if it failed
        Args:
            confidence_level: expected confidence level of the test
            p_value: p value obtained from get_p_value()

        Returns: None
        """
        pass

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
