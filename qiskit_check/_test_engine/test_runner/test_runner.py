from abc import ABC, abstractmethod

from qiskit import Aer, transpile

from qiskit_check._test_engine.concrete_property_test.concerete_property_test import ConcretePropertyTest, TestCase
from qiskit_check._test_engine.printers import AbstractPrinter
from qiskit_check._test_engine.test_runner.abstract_test_runner import AbstractTestRunner
from qiskit_check.property_test.test_results import TestResult


class TestRunner(AbstractTestRunner, ABC):
    def _run_test(self, property_test: ConcretePropertyTest, printer: AbstractPrinter) -> None:
        for test_case in property_test:
            printer.print_test_case_header(test_case)
            experiment_results = []
            for _ in range(test_case.num_experiments):
                experiment_results.append(self._run_test_case(test_case))
            try:
                test_case.assessor.assess(experiment_results)
                printer.print_test_case_success(test_case)
            except Exception as error:
                printer.print_test_case_failure(test_case, error)
                raise Exception(error)
            # TODO: rerunning tests that failed? save failed test cases to file and rerun them with new batch

    @abstractmethod
    def _run_test_case(self, test_case: TestCase) -> TestResult:
        pass


class SimulatorTestRunner(TestRunner):
    def __init__(self, simulator_name: str) -> None:
        self.backend = Aer.get_backend(simulator_name)

    def _run_test_case(self, test_case: TestCase) -> TestResult:
        transpiled_circuit = transpile(test_case.circuit, self.backend)
        return self.backend.run(transpiled_circuit, shots=test_case.num_measurements).result()


class IBMQDeviceRunner(TestRunner):  # TODO: implement this
    def __init__(self) -> None:
        pass

    def _run_test_case(self, test_case: TestCase) -> TestResult:
        pass
