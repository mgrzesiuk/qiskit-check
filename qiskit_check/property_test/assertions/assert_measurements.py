from typing import List, Dict

from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import ConcreteQubit, Qubit
from qiskit_check.property_test.test_results import TestResult


class AssertMostProbable(AbstractAssertion):
    def __init__(self, expected_state: str) -> None:
        self.expected_state = expected_state
        self.assert_true = AssertTrue(self._verify_function, 1)

    def _verify_function(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.expected_state not in experiment:
            return 0
        state_likelihood = experiment[self.expected_state]
        if state_likelihood >= max(experiment.values()):
            return 1
        else:
            return 0

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        return self.assert_true.verify(experiments, resource_matcher)


class AssertMeasurementEqual(AbstractAssertion):
    def __init__(self, expected_state) -> None:
        self.expected_state = expected_state

    def verify(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        self.check_if_experiments_empty(experiments)

        minimal_probability = 1

        num_shots = sum(experiments[0].values())

        for experiment in experiments:
            if self.expected_state not in experiment:
                return 0
            else:
                current_probability = experiment[self.expected_state]/float(num_shots)
                if current_probability < minimal_probability:
                    minimal_probability = current_probability

        return minimal_probability
