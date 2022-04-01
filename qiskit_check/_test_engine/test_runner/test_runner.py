from abc import ABC, abstractmethod

from qiskit import Aer, transpile, IBMQ, QuantumCircuit
from qiskit.result import Result
from qiskit.tools.monitor import job_monitor

from qiskit_check._test_engine.concrete_property_test.concerete_property_test import ConcretePropertyTest, TestCase
from qiskit_check._test_engine.p_value_correction import NoCorrectionFactory, AbstractCorrectionFactory
from qiskit_check._test_engine.printers import AbstractPrinter
from qiskit_check._test_engine.state_estimation.tomography import AbstractTomography
from qiskit_check._test_engine.test_runner.abstract_test_runner import AbstractTestRunner
from qiskit_check.property_test.test_results import TestResult


class TestRunner(AbstractTestRunner, ABC):
    def _run_test(self, property_test: ConcretePropertyTest) -> None:
        for test_case in property_test:
            self.printer.print_test_case_header(test_case)

            experiment_results = []
            for _ in range(test_case.num_experiments):
                experiment_results.append(self._run_circuit(test_case.circuit, test_case.num_measurements))
            tomography_result = self.state_estimator.run(test_case, self._run_circuit)
            test_results = TestResult.from_qiskit_result(experiment_results, tomography_result, test_case.circuit)
            num_assertions = len(test_case.assessor.assertions)
            corrector = self.corrector_factory.build(test_case.assessor.confidence_level, num_assertions)
            try:
                test_case.assessor.assess(test_results, corrector)
                self.printer.print_test_case_success(test_case)
            except Exception as error:
                self.printer.print_test_case_failure(test_case, error)
                raise error

    @abstractmethod
    def _run_circuit(self, circuit: QuantumCircuit, num_shots: int) -> Result:
        pass


class SimulatorTestRunner(TestRunner):
    def __init__(
            self, simulator_name: str, printer: AbstractPrinter, tomography: AbstractTomography = None,
            corrector_factory: AbstractCorrectionFactory = NoCorrectionFactory()) -> None:
        super().__init__(printer, tomography, corrector_factory)
        self.backend = Aer.get_backend(simulator_name)

    def _run_circuit(self, circuit: QuantumCircuit, num_shots: int) -> Result:
        transpiled_circuit = transpile(circuit, self.backend)
        return self.backend.run(transpiled_circuit, shots=num_shots).result()


class IBMQDeviceRunner(TestRunner):
    def __init__(
            self, backend_name: str, provider_hub: str, provider_group: str, provider_project: str,
            printer: AbstractPrinter, tomography: AbstractTomography = None,
            corrector_factory: AbstractCorrectionFactory = NoCorrectionFactory()) -> None:
        super().__init__(printer, tomography, corrector_factory)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub=provider_hub, group=provider_group, project=provider_project)
        self.backend = provider.get_backend(backend_name)

    def _run_circuit(self, circuit: QuantumCircuit, num_shots: int) -> Result:
        transpiled_circuit = transpile(circuit, self.backend)
        job = self.backend.run(transpiled_circuit, shots=num_shots)
        job_monitor(job, interval=2)
        return job.result()
