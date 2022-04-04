from math import isnan
from typing import Tuple, Dict

from numpy import asarray
from scipy.stats import ttest_1samp, combine_pvalues

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoTomographyError
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import hopf_coordinates_to_bloch_vector


class AssertStateEqual(AbstractAssertion):
    """
    assert if qubit is in given state at given time of circuit execution via quantum tomography
    """
    def __init__(
            self, qubit: Qubit, location: int, expected_state: Tuple[float, float]) -> None:
        """
        initialize
        Args:
            qubit: qubit which state to measure
            location: where in the circuit measure the qubits state (index in QuantumCircuit.data)
            expected_state: expected state (in hopf coordinates) of the qubit
        """
        self.qubit = qubit
        self.location = location
        self.expected_state = hopf_coordinates_to_bloch_vector(*expected_state)
        self.test = ttest_1samp

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p_value of statistical test if the qubit is in a given state
        Args:
            result: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """
        if result.tomography_result is None:
            raise NoTomographyError("tomography is required for AssertStateTransformed but no tomography result was provided")

        samples = asarray(result.tomography_result.get_estimates(self.qubit, self.location))
        x_p_value = self.test(samples[:, 0], self.expected_state[0], alternative="two-sided").pvalue
        if isnan(x_p_value):
            x_p_value = 1

        y_p_value = self.test(samples[:, 1], self.expected_state[1], alternative="two-sided").pvalue
        if isnan(y_p_value):
            y_p_value = 1

        z_p_value = self.test(samples[:, 2], self.expected_state[2], alternative="two-sided").pvalue
        if isnan(z_p_value):
            z_p_value = 1

        _, p_value = combine_pvalues([x_p_value, y_p_value, z_p_value])
        return p_value

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        """

        Returns: map between qubit and location where tomography is to be inserted

        """
        return {self.qubit: self.location}
