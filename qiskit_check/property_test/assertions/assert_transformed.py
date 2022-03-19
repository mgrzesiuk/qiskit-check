from typing import Dict

from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_vector_state


class AssertTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, theta_shift: float, phi_shift: float) -> None:
        self.qubit = qubit
        self.theta_shift = theta_shift
        self.phi_shift = phi_shift

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)
        # TODO: this checks if prob check out but not if the qubit got transformed (maybe since -|0> != |0> but here they are)

        qubit_initial_value = resource_matcher[self.qubit].value.to_dict()
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value["0"], qubit_initial_value["1"])
        new_theta = theta + self.theta_shift
        new_phase = phi + self.phi_shift

        new_expected_state = Statevector([*hopf_coordinates_to_vector_state(new_theta, new_phase)])

        expected_ground_state_probability = new_expected_state.probabilities()[0]
        assert_probability = AssertProbability(self.qubit, "0", expected_ground_state_probability)
        return assert_probability.get_p_value(result, resource_matcher)

    def verify(self, confidence_level: float, p_value: float) -> None:
        if 1 - confidence_level > p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"AssertTransformed failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold} to fail to reject equality hypothesis")
