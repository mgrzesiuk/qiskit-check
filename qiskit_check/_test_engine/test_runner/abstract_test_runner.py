from abc import ABC, abstractmethod
from typing import Sequence

from qiskit_check._test_engine.concerete_property_test import ConcretePropertyTest
from qiskit_check._test_engine.printer import AbstractPrinter


class AbstractTestRunner(ABC):
    def run_tests(self, property_tests: Sequence[ConcretePropertyTest], printer: AbstractPrinter) -> int:
        num_test_failed = 0
        for property_test in property_tests:
            printer.print_property_test_header(property_test)
            try:
                self._run_test(property_test, printer)
                printer.print_property_test_success(property_test)
            except Exception as error:
                printer.print_property_test_failure(property_test, error)
                num_test_failed += 1
        return num_test_failed

    @abstractmethod
    def _run_test(self, property_test: ConcretePropertyTest, printer: AbstractPrinter) -> None:
        pass
