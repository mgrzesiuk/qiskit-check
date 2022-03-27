from typing import Dict, Tuple

from hyppo.ksample import Hotelling
from numpy import asarray
from scipy.spatial.transform import Rotation

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_bloch_vector


class AssertStateTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, location: int, rotation: Rotation) -> None:
        self.qubit = qubit
        self.location = location
        self.rotation = rotation
        self.test = Hotelling().test

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_initial_value = resource_matcher[self.qubit].value.to_dict()
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value["0"], qubit_initial_value["1"])
        initial_bloch_vector = hopf_coordinates_to_bloch_vector(theta, phi)
        expected_bloch_vector = self.rotation.apply(initial_bloch_vector).flatten()
        samples = asarray(experiments.tomography_result.get_estimates(self.qubit, self.location))
        _, p_value = self.test(samples, asarray([expected_bloch_vector]*len(samples)))

        return p_value

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {self.qubit: self.location}
