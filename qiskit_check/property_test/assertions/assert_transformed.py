from typing import Dict
from math import acos, cos

from scipy.spatial.transform import Rotation

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_bloch_vector


class AssertTransformed(AbstractAssertion):
    """
    assert that given qubit has been rotated by specified rotation (equality checked by equal probabilities)
    """
    def __init__(self, qubit: Qubit, rotation: Rotation) -> None:
        """
        initialized
        Args:
            qubit: qubit template
            rotation: scipy object to specify rotation
        """
        self.qubit = qubit
        self.rotation = rotation

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p_value of statistical test if the qubit has been transformed
        Args:
            result: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)

        qubit_initial_value = resource_matcher[self.qubit].value.data
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value[0], qubit_initial_value[1])
        bloch_vector = hopf_coordinates_to_bloch_vector(theta, phi)
        expected_bloch_vector = self.rotation.apply(bloch_vector).flatten()
        theta = acos(expected_bloch_vector[2])
        expected_ground_state_probability = cos(theta/2)**2
        assert_probability = AssertProbability(self.qubit, "0", expected_ground_state_probability)
        return assert_probability.get_p_value(result, resource_matcher)
