from math import isnan
from typing import Dict, List

from numpy import asarray
from scipy.spatial.transform import Rotation
from scipy.stats import ttest_1samp, combine_pvalues
from qiskit_check.property_test.test_results.test_result import TestResult

from qiskit_check.property_test.assertions.abstract_state_assertions import AbstractDirectInversionStateAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_bloch_vector
from qiskit_check.property_test.utils import round_floats


class AssertTransformedByState(AbstractDirectInversionStateAssertion):
    """
    assert if qubit has been rotated by given rotation at a given location in circuit (via quantum tomography)
    """
    def __init__(self, qubit: Qubit, rotation: Rotation, location: int = None) -> None:
        """
        initialize
        Args:
            qubit: qubit which state to measure
            location: where in the circuit measure the qubits state (index in QuantumCircuit.data)
            rotation: scipy rotation object that specifies the expected rotation in 3d
        """
        super().__init__(self.get_xyz_measurements(), location, self.combiner)
        self.qubit = qubit
        self.rotation = rotation
        self.test = ttest_1samp

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        """
        get p_value of statistical test if the qubit has been transformed by given rotation
        Args:
            result: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion

        """
        qubit_initial_value = resource_matcher[self.qubit].value.data
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value[0], qubit_initial_value[1])
        initial_bloch_vector = hopf_coordinates_to_bloch_vector(theta, phi)
        expected_bloch_vector = self.rotation.apply(initial_bloch_vector).flatten()
        expected_bloch_vector = (
            round_floats(expected_bloch_vector[0]),
            round_floats(expected_bloch_vector[1]),
            round_floats(expected_bloch_vector[2])
        )

        x_p_value = self.test(experiments.individual_measurements[self.qubit][0], expected_bloch_vector[0], alternative="two-sided").pvalue
        if isnan(x_p_value):
            x_p_value = 1

        y_p_value = self.test(experiments.individual_measurements[self.qubit][1], expected_bloch_vector[1], alternative="two-sided").pvalue
        if isnan(y_p_value):
            y_p_value = 1

        z_p_value = self.test(experiments.individual_measurements[self.qubit][2], expected_bloch_vector[2], alternative="two-sided").pvalue
        if isnan(z_p_value):
            z_p_value = 1

        _, p_value = combine_pvalues([x_p_value, y_p_value, z_p_value])
        return p_value

