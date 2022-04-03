from qiskit_check._test_engine.printers import TerminalPrinter
from qiskit_check._test_engine.config.abstract_config import AbstractConfig
from qiskit_check._test_engine.generator import QubitInputGeneratorFactory, NaiveInputGeneratorFactory
from qiskit_check._test_engine.test_runner import AbstractTestRunner, SimulatorTestRunner


class DefaultConfig(AbstractConfig):
    """
    default configuration of test engine to be used in absence of specified coniguration
    """
    def get_test_runner(self) -> AbstractTestRunner:
        """
        get default test runner
        Returns: instance of subclass of AbstractTestRunner

        """
        return SimulatorTestRunner('aer_simulator', TerminalPrinter())

    def get_input_generator_factory(self) -> QubitInputGeneratorFactory:
        """
        get default qubit input generator factory
        Returns: instance of subclass QubitInputGeneratorFactory

        """
        return NaiveInputGeneratorFactory()
