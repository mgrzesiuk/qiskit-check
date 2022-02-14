from typing import List, Dict, Callable

from scipy.stats import ttest_1samp

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertTrue(AbstractAssertion):
    def __init__(
            self, verify_function: Callable[[Dict[str, int], Dict[Qubit, ConcreteQubit]], float],
            target_value: float) -> None:
        self.verify_function = verify_function
        self.target_value = target_value

    def verify(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        self.check_if_experiments_empty(experiments)
        experiment_values = [self.verify_function(experiment, resource_matcher) for experiment in experiments]
        return ttest_1samp(experiment_values, self.target_value).pvalue
