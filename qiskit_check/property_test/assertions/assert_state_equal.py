from math import isnan
from sys import maxsize
from typing import Callable, Sequence, Tuple, Dict, List

from numpy import asarray
from scipy.stats import ttest_1samp, combine_pvalues
from qiskit_check.property_test.test_results.test_result import TestResult

from qiskit_check.property_test.assertions.abstract_state_assertions import AbstractDirectInversionStateAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.utils import hopf_coordinates_to_bloch_vector


class AssertStateEqualConcreteValue(AbstractDirectInversionStateAssertion):
    """
    assert if qubit is in given state at given time of circuit execution via quantum tomography
    """
    def __init__(
            self, qubit: Qubit, expected_state: Tuple[float, float], location: int = None) -> None:
        super().__init__(self.get_xyz_measurements(), location, self.combiner)
        self.qubit = qubit
        self.expected_state = hopf_coordinates_to_bloch_vector(*expected_state)
        self.test = ttest_1samp

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        x_p_value = self.test(experiments.individual_measurements[self.qubit][0], self.expected_state[0], alternative="two-sided").pvalue
        if isnan(x_p_value):
            x_p_value = 1

        y_p_value = self.test(experiments.individual_measurements[self.qubit][1], self.expected_state[1], alternative="two-sided").pvalue
        if isnan(y_p_value):
            y_p_value = 1

        z_p_value = self.test(experiments.individual_measurements[self.qubit][2], self.expected_state[2], alternative="two-sided").pvalue
        if isnan(z_p_value):
            z_p_value = 1

        _, p_value = combine_pvalues([x_p_value, y_p_value, z_p_value])
        return p_value
