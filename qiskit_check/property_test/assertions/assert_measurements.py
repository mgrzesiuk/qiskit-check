from typing import Dict

from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import ConcreteQubit, Qubit
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class AssertMostProbable(AbstractAssertion):
    def __init__(self, expected_state: str) -> None:
        self.expected_state = expected_state
        self.assert_true = AssertTrue(self._verify_function, 1)

    def _verify_function(self, result: MeasurementResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        counts = result.get_counts()
        if self.expected_state not in counts:
            return 0
        state_likelihood = counts[self.expected_state]
        if state_likelihood >= max(counts.values()):
            return 1
        else:
            return 0

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        return self.assert_true.get_p_value(result, resource_matcher)

    def verify(self, confidence_level: float, p_value: float) -> None:
        if 1 - confidence_level > p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"AssertMostProbable failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold}")


class AssertMeasurementEqual(AbstractAssertion):
    def __init__(self, expected_state) -> None:
        self.expected_state = expected_state

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        self.check_if_experiments_empty(result)

        minimal_probability = 1

        num_shots = result.num_shots

        for measurement_result in result.measurement_results:
            counts = measurement_result.get_counts()
            if self.expected_state not in counts:
                return 0
            else:
                current_probability = counts[self.expected_state]/float(num_shots)
                if current_probability < minimal_probability:
                    minimal_probability = current_probability

        return minimal_probability

    def verify(self, confidence_level: float, p_value: float) -> None:
        if 1 - confidence_level > p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"AssertMeasurementEqual failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold}")
