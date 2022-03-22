from abc import ABC, abstractmethod

from qiskit_check._test_engine.generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.test_runner import AbstractTestRunner


class AbstractConfig(ABC):
    @abstractmethod
    def get_test_runner(self) -> AbstractTestRunner:
        pass

    @abstractmethod
    def get_input_generator_factory(self) -> QubitInputGeneratorFactory:
        pass
