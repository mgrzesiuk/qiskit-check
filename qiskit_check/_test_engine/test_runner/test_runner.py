from typing import Sequence
from abc import ABC, abstractmethod

from qiskit import Aer, transpile
from qiskit.result import Result

from qiskit_check._test_engine.concerete_property_test import ConcretePropertyTest, TestCase
from qiskit_check._test_engine.test_runner.abstract_test_runner import AbstractTestRunner


# TODO: add result printing


class TestRunner(AbstractTestRunner, ABC):
    def _force_run_tests(self, property_tests: Sequence[ConcretePropertyTest]) -> None:
        for property_test in property_tests:
            try:
                self._run_test(property_test)
            except AssertionError as assertion_error:
                pass  # TODO: add printing results - maybe we can just give message that tests proceede since force flag is set

    def _run_tests(self, property_tests: Sequence[ConcretePropertyTest]) -> None:
        for property_test in property_tests:
            self._run_test(property_test)

    def _run_test(self, property_test: ConcretePropertyTest) -> None:
        for test_case in property_test:
            experiment_results = []
            for _ in range(test_case.num_experiments):
                results = self._run_test_case(test_case)
                experiment_results.append(results.get_counts())
            test_case.assessor.assess(experiment_results)
            # TODO: rerunning tests that failed? save failed test cases to file and rerun them with new batch

    @abstractmethod
    def _run_test_case(self, test_case: TestCase) -> Result:
        pass


class SimulatorTestRunner(TestRunner):
    def __init__(self, simulator_name: str) -> None:
        self.backend = Aer.get_backend(simulator_name)

    def _run_test_case(self, test_case: TestCase) -> Result:
        transpiled_circuit = transpile(test_case.circuit, self.backend)
        return self.backend.run(transpiled_circuit, shots=test_case.num_measurements).result()


class IBMQDeviceRunner(TestRunner):  # TODO: implement this
    def __init__(self) -> None:
        pass

    def _run_test_case(self, test_case: TestCase) -> Result:
        pass
