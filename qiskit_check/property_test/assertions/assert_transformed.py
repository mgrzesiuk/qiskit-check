from typing import List, Dict

from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_vector_state


class AssertTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, phase_shift: float, angle_shift: float) -> None:  # TODO: is this naming even worth keeping, maybe just theta and phi will be more intuitive
        self.qubit = qubit
        self.phase_shift = phase_shift
        self.angle_shift = angle_shift

    def verify(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        # TODO: this checks if prob check out but not if the qubit got transformed (maybe since -|0> != |0> but here they are)

        qubit_initial_value = resource_matcher[self.qubit].value.to_dict()
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value["0"], qubit_initial_value["1"])
        new_theta = theta + self.angle_shift
        new_phase = phi + self.phase_shift

        new_expected_state = Statevector([*hopf_coordinates_to_vector_state(new_theta, new_phase)])

        expected_ground_state_probability = new_expected_state.probabilities()[0]
        assert_probability = AssertProbability(self.qubit, "0", expected_ground_state_probability)
        return assert_probability.verify(experiments, resource_matcher)
