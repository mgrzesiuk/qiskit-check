from typing import Dict

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertTeleported(AbstractAssertion):
    def __init__(self, qubit_to_teleport: Qubit, target_qubit: Qubit) -> None:
        self.qubit_to_teleport = qubit_to_teleport
        self.target_qubit = target_qubit

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_to_teleport not in resource_matcher or self.target_qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)
        # TODO: this checks if prob check out but not if the qubit got teleported (maybe since -|0> != |0> but here they are)
        expected_ground_state_probability = resource_matcher[self.qubit_to_teleport].value.probabilities()[0]
        assert_probability = AssertProbability(self.target_qubit, "0", expected_ground_state_probability)
        return assert_probability.get_p_value(result, resource_matcher)
