from abc import ABC, abstractmethod

from qiskit_check._test_engine.concerete_property_test import ConcretePropertyTest
from qiskit_check._test_engine.test_case import TestCase


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


class TerminalPrinter(AbstractPrinter):
    # TODO: make those proper messages with colors
    def print_property_test_header(self, property_test: ConcretePropertyTest) -> None:
        print("starting test: ", property_test.property_test_class.__name__)

    def print_test_case_header(self, test_case: TestCase) -> None:
        print("starting test with circuit:")
        test_case.circuit.draw()

    def print_test_case_success(self, test_case: TestCase) -> None:
        print("test case passed")

    def print_test_case_failure(self, test_case: TestCase, error: Exception) -> None:
        print("test case FAILED with error:", error)

    def print_property_test_success(self, property_test: ConcretePropertyTest) -> None:
        print("entire property test PASSED")

    def print_property_test_failure(self, property_test: ConcretePropertyTest, error: Exception) -> None:
        print("entire property test FAILED", error)

    def print_summary(self, num_tests_failed: int, num_tests_succeeded: int) -> None:
        print("all tests finished")
        print("number of tests failed", num_tests_failed)
        print("number of successes", num_tests_succeeded)
