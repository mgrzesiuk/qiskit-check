from abc import ABC, abstractmethod

from qiskit import Aer, transpile, IBMQ
from qiskit.result import Result
from qiskit.tools.monitor import job_monitor

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
            test_results = TestResult.from_qiskit_result(experiment_results, test_case.circuit)
            try:
                test_case.assessor.assess(test_results)
                printer.print_test_case_success(test_case)
            except Exception as error:
                printer.print_test_case_failure(test_case, error)
                raise error

    @abstractmethod
    def _run_test_case(self, test_case: TestCase) -> Result:
        pass


class SimulatorTestRunner(TestRunner):
    def __init__(self, simulator_name: str) -> None:
        self.backend = Aer.get_backend(simulator_name)

    def _run_test_case(self, test_case: TestCase) -> Result:
        transpiled_circuit = transpile(test_case.circuit, self.backend)
        return self.backend.run(transpiled_circuit, shots=test_case.num_measurements).result()


class IBMQDeviceRunner(TestRunner):
    def __init__(self, backend_name: str, provider_hub: str, provider_group: str, provider_project: str) -> None:
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub=provider_hub, group=provider_group, project=provider_project)
        self.backend = provider.get_backend(backend_name)

    def _run_test_case(self, test_case: TestCase) -> Result:
        transpiled_circuit = transpile(test_case.circuit, self.backend)
        job = self.backend.run(transpiled_circuit, shots=test_case.num_measurements)
        job_monitor(job, interval=2)
        return job.result()
