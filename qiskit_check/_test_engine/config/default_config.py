from qiskit_check._test_engine.printers import TerminalPrinter
from qiskit_check._test_engine.config.abstract_config import AbstractConfig
from qiskit_check._test_engine.generator import QubitInputGeneratorFactory, NaiveInputGeneratorFactory
from qiskit_check._test_engine.test_runner import AbstractTestRunner, SimulatorTestRunner


class DefaultConfig(AbstractConfig):
    def get_test_runner(self) -> AbstractTestRunner:
        return SimulatorTestRunner('aer_simulator', TerminalPrinter())

    def get_input_generator_factory(self) -> QubitInputGeneratorFactory:
        return NaiveInputGeneratorFactory()
