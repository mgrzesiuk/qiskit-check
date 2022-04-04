from math import isnan
from typing import Dict, Callable

from scipy.stats import ttest_1samp

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class AssertTrue(AbstractAssertion):
    """
    assert that a given condition is true, allows used to specify function that takes measurement result and
    resource matcher and outputs a float, than that float is tested against specified expected value
    """
    def __init__(
            self, verify_function: Callable[[MeasurementResult, Dict[Qubit, ConcreteQubit]], float],
            target_value: float) -> None:
        """
        initialize
        Args:
            verify_function: user specified function, takes measurement result and resource matcher and outputs
            float that measures goodness of the result
            target_value: expected output of the verify_function
        """
        self.verify_function = verify_function
        self.target_value = target_value

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get_p_value if the condition specified holds
        Args:
            result: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """
        self.check_if_experiments_empty(result)

        experiment_values = []
        for measurement in result.measurement_results:
            experiment_values.append(self.verify_function(measurement, resource_matcher))
        p_value = ttest_1samp(experiment_values, self.target_value).pvalue
        if isnan(p_value):
            p_value = 1
        return p_value
