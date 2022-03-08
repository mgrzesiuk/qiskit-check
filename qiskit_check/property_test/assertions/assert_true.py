from typing import Dict, Callable

from scipy.stats import ttest_1samp

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class AssertTrue(AbstractAssertion):
    def __init__(
            self, verify_function: Callable[[MeasurementResult, Dict[Qubit, ConcreteQubit]], float],
            target_value: float) -> None:
        self.verify_function = verify_function
        self.target_value = target_value

    def verify(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        self.check_if_experiments_empty(result)

        experiment_values = []
        for measurement in result.measurement_results:
            experiment_values.append(self.verify_function(measurement, resource_matcher))
        return ttest_1samp(experiment_values, self.target_value).pvalue
