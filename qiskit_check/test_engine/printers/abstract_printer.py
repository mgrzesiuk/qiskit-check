from abc import ABC, abstractmethod
from typing import Type, Set, List

from qiskit_check.test_engine.concrete_property_test.concrete_property_test import ConcretePropertyTest
from qiskit_check.test_engine.concrete_property_test.test_case import TestCase
from qiskit_check.property_test import PropertyTest


class AbstractPrinter(ABC):
    """
    abstract class for printing test results
    """
    @abstractmethod
    def print_introduction(self, collected_tests: Set[Type[PropertyTest]]) -> None:
        """
        print introduction (number of tests collected etc), this is called before tests are run
        Args:
            collected_tests: set of collected property test classes

        Returns: None

        """
        pass

    @abstractmethod
    def print_property_test_header(self, property_test: ConcretePropertyTest) -> None:
        """
        print info about property test, this is called before each property test is run
        Args:
            property_test: property test for which this is being called

        Returns: None

        """
        pass

    @abstractmethod
    def print_test_case_header(self, test_case: TestCase) -> None:
        """
        print information about test case (qubits for which the circuit has been initialized etc), this is called
        before each of the test cases in property test
        Args:
            test_case: test case for which this method is called

        Returns: None

        """
        pass

    @abstractmethod
    def print_test_case_success(self, test_case: TestCase) -> None:
        """
        print message on test case successfully passing
        Args:
            test_case: test case that passed

        Returns: None

        """
        pass

    @abstractmethod
    def print_test_case_failure(self, test_case: TestCase, error: Exception) -> None:
        """
        print information on test case that failed
        Args:
            test_case: test case that failed
            error: error that was thrown (AssertionError, or any that was thrown during test execution)

        Returns: None

        """
        pass

    @abstractmethod
    def print_property_test_success(self, property_test: ConcretePropertyTest) -> None:
        """
        print message on entire property test successfully passing
        Args:
            property_test: property test that passed

        Returns: None

        """
        pass

    @abstractmethod
    def print_property_test_failure(self, property_test: ConcretePropertyTest, error: Exception) -> None:
        """
        print message for when property test fails
        Args:
            property_test: property test that failed
            error: error that was thrown (AssertionError, or any that was thrown during test execution)

        Returns: None

        """
        pass

    @abstractmethod
    def print_summary(self, tests_failed: List[str], tests_succeeded: List[str]) -> None:
        """
        print summary, method called after all tests have been finished
        Args:
            tests_failed: list of names of the property tests that failed
            tests_succeeded: list of names of the property tests that passed

        Returns: None

        """
        pass
