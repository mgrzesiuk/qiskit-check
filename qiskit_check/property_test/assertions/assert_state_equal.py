from typing import Tuple, Dict

from numpy import asarray
from scipy.stats import ttest_1samp, combine_pvalues

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import hopf_coordinates_to_bloch_vector


class AssertStateEqual(AbstractAssertion):
    def __init__(
            self, qubit: Qubit, location: int, expected_state: Tuple[float, float]) -> None:
        self.qubit = qubit
        self.location = location
        self.expected_state = hopf_coordinates_to_bloch_vector(*expected_state)
        self.test = ttest_1samp

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        samples = asarray(experiments.tomography_result.get_estimates(self.qubit, self.location))
        x_p_value = self.test(samples[:, 0], self.expected_state[0], alternative="two-sided").pvalue
        y_p_value = self.test(samples[:, 1], self.expected_state[1], alternative="two-sided").pvalue
        z_p_value = self.test(samples[:, 2], self.expected_state[2], alternative="two-sided").pvalue

        _, p_value = combine_pvalues([x_p_value, y_p_value, z_p_value])
        return p_value

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {self.qubit: self.location}
