from abc import ABC, abstractmethod
from typing import Dict, Tuple

from qiskit import Aer, transpile, IBMQ, QuantumCircuit
from qiskit.result import Result
from qiskit.tools.monitor import job_monitor

from qiskit_check.test_engine.concrete_property_test.concrete_property_test import ConcretePropertyTest, TestCase
from qiskit_check.test_engine.p_value_correction import NoCorrectionFactory, AbstractCorrectionFactory
from qiskit_check.test_engine.printers import AbstractPrinter
from qiskit_check.test_engine.test_runner.abstract_test_runner import AbstractTestRunner


class TestRunner(AbstractTestRunner, ABC):
    """
    class responsible for running tests
    """
    def _run_test(self, property_test: ConcretePropertyTest) -> None:
        """
        run singular test
        Args:
            property_test: test to run

        Returns: none

        """
        for test_case in property_test:
            self.printer.print_test_case_header(test_case)
            
            test_results = []
            for _ in range(test_case.num_experiments):
                test_results.append(self.get_test_results(test_case))
            num_assertions = len(test_case.assessor.assertions)
            corrector = self.corrector_factory.build(test_case.assessor.confidence_level, num_assertions)
            try:
                test_case.assessor.assess(test_results, corrector, test_case.num_measurements, test_case.num_experiments)
                self.printer.print_test_case_success(test_case)
            except Exception as error:
                self.printer.print_test_case_failure(test_case, error)
                raise error
    
    def get_test_results(self, test_case: TestCase) -> Dict[str, Tuple[Result, QuantumCircuit]]:
        measurement_circuits, circuit_names = self.circuit_creator.get_circuits(test_case)
        results = {}
        for circuit_name, encodings in measurement_circuits.items():
            circuit = circuit_names[circuit_name]
            result = self._run_circuit(circuit, test_case.num_measurements)
            for encoding in encodings:
                results[encoding] = (result, circuit)
        return results
    
    @abstractmethod
    def _run_circuit(self, circuit: QuantumCircuit, num_shots: int) -> Result:
        """
        execute a given circuit
        Args:
            circuit: QuantumCircuit to execute
            num_shots: number of shots to run the circuit with

        Returns: qiskit result

        """
        pass


class SimulatorTestRunner(TestRunner):
    """
    class responsible for running tests on aer simulators
    """
    def __init__(self, simulator_name: str, printer: AbstractPrinter, corrector_factory: AbstractCorrectionFactory = NoCorrectionFactory()) -> None:
        """
        initialize
        Args:
            simulator_name: name of the aer simulator to be used
            printer: object of subtype AbstractPrinter to print test information
            tomography: object of subtype AbstractPrinter to be used for state tomography, default none
            corrector_factory: factory to build corrector objects to correct confidence level to maintain specified
            family wise confidence level
        """
        super().__init__(printer, corrector_factory)
        self.backend = Aer.get_backend(simulator_name)

    def _run_circuit(self, circuit: QuantumCircuit, num_shots: int) -> Result:
        """
        execute a given  on a Aer simulator backend (which is exactly specified in simulator_name)
        Args:
            circuit: QuantumCircuit to execute
            num_shots: number of shots to run the circuit with

        Returns: qiskit result

        """
        transpiled_circuit = transpile(circuit, self.backend)
        return self.backend.run(transpiled_circuit, shots=num_shots).result()


class IBMQDeviceRunner(TestRunner):
    """
    class responsible for running tests on ibmq devices
    """
    def __init__(
            self, backend_name: str, provider_hub: str, provider_group: str, provider_project: str,
            printer: AbstractPrinter, corrector_factory: AbstractCorrectionFactory = NoCorrectionFactory()) -> None:
        """
        initialize
        Args:
            backend_name: IBMQ device name
            provider_hub: IBMQ provider hub name
            provider_group: IBMQ provider group name
            provider_project: IBMQ provider project name
            printer: object of subtype AbstractPrinter to print test information
            tomography: object of subtype AbstractPrinter to be used for state tomography, default none
            corrector_factory: factory to build corrector objects to correct confidence level to maintain specified
            family wise confidence level
        """
        super().__init__(printer, corrector_factory)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub=provider_hub, group=provider_group, project=provider_project)
        self.backend = provider.get_backend(backend_name)

    def _run_circuit(self, circuit: QuantumCircuit, num_shots: int) -> Result:
        """
        execute a given on a IBMQ device (which one is specified in constructor)
        Args:
            circuit: QuantumCircuit to execute
            num_shots: number of shots to run the circuit with

        Returns: qiskit result

        """
        transpiled_circuit = transpile(circuit, self.backend)
        job = self.backend.run(transpiled_circuit, shots=num_shots)
        job_monitor(job, interval=2)
        return job.result()
