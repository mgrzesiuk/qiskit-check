from typing import Dict

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertTeleported(AbstractAssertion):
    """
    assert if a qubit has been teleported (equality checked by equal probabilities)
    """
    def __init__(self, qubit_to_teleport: Qubit, target_qubit: Qubit) -> None:
        """
        initialize
        Args:
            qubit_to_teleport: qubit template of the qubit to be teleported
            target_qubit: qubit template of where qubit should be teleported
        """
        self.qubit_to_teleport = qubit_to_teleport
        self.target_qubit = target_qubit

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p_value of statistical test if the qubit has been teleported
        Args:
            result: result of the batch of tests executed
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """

        if self.qubit_to_teleport not in resource_matcher or self.target_qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)
        expected_ground_state_probability = resource_matcher[self.qubit_to_teleport].value.probabilities()[0]
        assert_probability = AssertProbability(self.target_qubit, "0", expected_ground_state_probability)
        return assert_probability.get_p_value(result, resource_matcher)
