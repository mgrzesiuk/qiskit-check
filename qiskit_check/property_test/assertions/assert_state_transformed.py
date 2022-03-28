from typing import Dict

from numpy import asarray
from scipy.spatial.transform import Rotation
from scipy.stats import ttest_1samp, combine_pvalues

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_bloch_vector


class AssertStateTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, location: int, rotation: Rotation, norm_threshold: float = 1) -> None:
        self.qubit = qubit
        self.location = location
        self.rotation = rotation
        self.test = ttest_1samp
        self.norm_threshold = norm_threshold

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_initial_value = resource_matcher[self.qubit].value.to_dict()
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value["0"], qubit_initial_value["1"])
        initial_bloch_vector = hopf_coordinates_to_bloch_vector(theta, phi)
        expected_bloch_vector = self.rotation.apply(initial_bloch_vector).flatten()
        samples = asarray(experiments.tomography_result.get_estimates(self.qubit, self.location))

        x_p_value = self.test(samples[:, 0], expected_bloch_vector[0], alternative="two-sided").pvalue
        y_p_value = self.test(samples[:, 1], expected_bloch_vector[1], alternative="two-sided").pvalue
        z_p_value = self.test(samples[:, 2], expected_bloch_vector[2], alternative="two-sided").pvalue

        _, p_value = combine_pvalues([x_p_value, y_p_value, z_p_value])
        return p_value

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {self.qubit: self.location}
