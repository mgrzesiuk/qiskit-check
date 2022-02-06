from abc import ABC, abstractmethod
from typing import Sequence

from qiskit_check._test_engine.concerete_property_test import ConcretePropertyTest


class AbstractTestRunner(ABC):
    def run_tests(self, property_tests: Sequence[ConcretePropertyTest], force_run: bool = False) -> None:
        if force_run:
            self._force_run_tests(property_tests)
        else:
            self._run_test(property_tests)

    @abstractmethod
    def _force_run_tests(self, property_tests: Sequence[ConcretePropertyTest]) -> None:
        pass

    @abstractmethod
    def _run_tests(self, property_tests: Sequence[ConcretePropertyTest]) -> None:
        pass

    @abstractmethod
    def _run_test(self, property_test: ConcretePropertyTest) -> None:
        pass
