from abc import ABC, abstractmethod
from typing import Sequence, List, Tuple

from qiskit_check._test_engine.concrete_property_test.concerete_property_test import ConcretePropertyTest
from qiskit_check._test_engine.printers import AbstractPrinter


class AbstractTestRunner(ABC):
    def run_tests(
            self, property_tests: Sequence[ConcretePropertyTest],
            printer: AbstractPrinter) -> Tuple[List[str], List[str]]:
        failed_tests = []
        succeeded_tests = []
        for property_test in property_tests:
            printer.print_property_test_header(property_test)
            try:
                self._run_test(property_test, printer)
                printer.print_property_test_success(property_test)
                succeeded_tests.append(property_test.property_test_class.__name__)
            except Exception as error:
                printer.print_property_test_failure(property_test, error)
                failed_tests.append(property_test.property_test_class.__name__)
        return failed_tests, succeeded_tests

    @abstractmethod
    def _run_test(self, property_test: ConcretePropertyTest, printer: AbstractPrinter) -> None:
        pass
