from typing import Dict, Tuple

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates


class AssertStateEqual(AbstractAssertion):
    def __init__(self, qubit: Qubit, location: int, expected_state: Tuple[float, float]) -> None:
        self.qubit = qubit
        self.location = location
        self.expected_state = expected_state

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        return experiments.tomography_result.get_p_value(self.qubit, self.location, self.expected_state)

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {self.qubit: self.location}


class AssertStateTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, location: int, theta_shift: float, phi_shift: float) -> None:
        self.qubit = qubit
        self.location = location
        self.theta_shift = theta_shift
        self.phi_shift = phi_shift

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        qubit_initial_value = resource_matcher[self.qubit].value.to_dict()
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value["0"], qubit_initial_value["1"])
        new_theta = theta + self.theta_shift
        new_phi = phi + self.phi_shift
        assert_state_equal = AssertStateEqual(self.qubit, self.location, (new_theta, new_phi))
        return assert_state_equal.get_p_value(experiments, resource_matcher)

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {self.qubit: self.location}
