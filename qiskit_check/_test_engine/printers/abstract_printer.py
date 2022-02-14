from abc import ABC, abstractmethod

from qiskit_check._test_engine.concrete_property_test.concerete_property_test import ConcretePropertyTest
from qiskit_check._test_engine.concrete_property_test.test_case import TestCase


class AbstractPrinter(ABC):
    @abstractmethod
    def print_property_test_header(self, property_test: ConcretePropertyTest) -> None:
        pass

    @abstractmethod
    def print_test_case_header(self, test_case: TestCase) -> None:
        pass

    @abstractmethod
    def print_test_case_success(self, test_case: TestCase) -> None:
        pass

    @abstractmethod
    def print_test_case_failure(self, test_case: TestCase, error: Exception) -> None:
        pass

    @abstractmethod
    def print_property_test_success(self, property_test: ConcretePropertyTest) -> None:
        pass

    @abstractmethod
    def print_property_test_failure(self, property_test: ConcretePropertyTest, error: Exception) -> None:
        pass

    @abstractmethod
    def print_summary(self, num_tests_failed: int, num_tests_succeeded: int) -> None:
        pass