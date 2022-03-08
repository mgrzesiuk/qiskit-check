from abc import ABC, abstractmethod
from typing import Dict

from qiskit_check.property_test.property_test_errors import NoExperimentsError

from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AbstractAssertion(ABC):
    @abstractmethod
    def verify(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        verify if the assertion holds
        Args:
            experiments: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """
        pass

    @staticmethod
    def check_if_experiments_empty(experiments: TestResult) -> None:
        if experiments.measurement_results == 0:
            raise NoExperimentsError("no experiments have been provided")
