from abc import ABC, abstractmethod

from qiskit_check._test_engine.generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.test_runner import AbstractTestRunner


class AbstractConfig(ABC):
    """
    base class for getting configuration for the test engine
    """
    @abstractmethod
    def get_test_runner(self) -> AbstractTestRunner:
        """
        get test runner
        Returns: instance of subclass of AbstractTestRunner

        """
        pass

    @abstractmethod
    def get_input_generator_factory(self) -> QubitInputGeneratorFactory:
        """
        get qubit input generator factory
        Returns: instance of subclass QubitInputGeneratorFactory

        """
        pass
