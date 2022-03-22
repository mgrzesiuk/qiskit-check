from typing import Dict, Sequence

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertStateEqual(AbstractAssertion):
    def __init__(self, qubit: Qubit) -> None:
        self.qubit = qubit

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        pass

    def verify(self, confidence_level: float, p_value: float) -> None:
        pass

    def get_qubits_requiring_tomography(self) -> Sequence[Qubit]:
        return self.qubit,


class AssertStateTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit) -> None:
        self.qubit = qubit

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        pass

    def verify(self, confidence_level: float, p_value: float) -> None:
        pass

    def get_qubits_requiring_tomography(self) -> Sequence[Qubit]:
        return self.qubit,
