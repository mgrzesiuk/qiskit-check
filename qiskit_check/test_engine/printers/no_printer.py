from typing import List, Set, Type

from colorama import init

from qiskit_check.test_engine.concrete_property_test.concrete_property_test import ConcretePropertyTest
from qiskit_check.test_engine.concrete_property_test.test_case import TestCase
from qiskit_check.test_engine.printers.abstract_printer import AbstractPrinter
from qiskit_check.property_test import PropertyTest


class NoPrinter(AbstractPrinter):
    """
    class for stubbing printer object that does not print out results
    """
    def __init__(self) -> None:
        """
        initialize
        """
        super().__init__()
        init(autoreset=True)

    def print_introduction(self, collected_tests: Set[Type[PropertyTest]]) -> None:
        pass

    def print_property_test_header(self, property_test: ConcretePropertyTest) -> None:
        pass

    def print_test_case_header(self, test_case: TestCase) -> None:
        pass

    def print_test_case_success(self, test_case: TestCase) -> None:
        pass

    def print_test_case_failure(self, test_case: TestCase, error: Exception) -> None:
        pass

    def print_property_test_success(self, property_test: ConcretePropertyTest) -> None:
        pass

    def print_property_test_failure(self, property_test: ConcretePropertyTest, error: Exception) -> None:
        pass

    def print_summary(self, tests_failed: List[str], tests_succeeded: List[str]) -> None:
        pass
