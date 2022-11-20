from abc import ABC, abstractmethod
from typing import Sequence, List, Tuple
from qiskit_check.test_engine.circuit_creator import CircuitCreator

from qiskit_check.test_engine.concrete_property_test.concrete_property_test import ConcretePropertyTest
from qiskit_check.test_engine.p_value_correction import NoCorrectionFactory
from qiskit_check.test_engine.p_value_correction.abstract_correction import AbstractCorrectionFactory

from qiskit_check.test_engine.printers import AbstractPrinter


class AbstractTestRunner(ABC):
    """
    class responsible for running tests
    """
    def __init__(self, printer: AbstractPrinter, corrector_factory: AbstractCorrectionFactory = NoCorrectionFactory(), circuit_creator: CircuitCreator = CircuitCreator()) -> None:
        """
        initialize
        Args:
            printer: object of subtype AbstractPrinter to print test information
            corrector_factory: factory to build corrector objects to correct confidence level to maintain specified
            family wise confidence level
        """
        self.printer = printer
        self.corrector_factory = corrector_factory
        self.circuit_creator= circuit_creator

    def run_tests(self, property_tests: Sequence[ConcretePropertyTest]) -> Tuple[List[str], List[str]]:
        """
        run collected tests
        Args:
            property_tests: sequence of property tests to be run

        Returns: 2 values: list of the names that failed, list of the names that passed

        """
        failed_tests = []
        succeeded_tests = []
        for property_test in property_tests:
            self.printer.print_property_test_header(property_test)
            try:
                self._run_test(property_test)
                self.printer.print_property_test_success(property_test)
                succeeded_tests.append(property_test.property_test_class.__name__)
            except Exception as error:
                self.printer.print_property_test_failure(property_test, error)
                failed_tests.append(property_test.property_test_class.__name__)
        return failed_tests, succeeded_tests

    @abstractmethod
    def _run_test(self, property_test: ConcretePropertyTest) -> None:
        """
        run singular test
        Args:
            property_test: test to run

        Returns: none

        """
        pass
