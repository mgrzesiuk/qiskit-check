from typing import Dict, List

from scipy.stats import chi2_contingency
from numpy import asarray, argwhere, all, delete

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertEntangled(AbstractAssertion):
    """
    assert that 2 qubits are entangled
    """
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit) -> None:
        """
        initialize
        Args:
            qubit_0: qubit 0 template
            qubit_1: qubit 1 template
        """
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p value of the test that 2 qubits are entangled given the results
        Args:
            result: test results obtained from running property test
            resource_matcher: mapping between qubit templates and ConcreteQubit holding information about
            initial state and index in the circuit of the real qubit

        Returns: p-value, float between 0 and 1

        """
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)

        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        contingency_table = self._get_contingency_table(result, qubit_0_index, qubit_1_index)

        _, p_value, _, _ = chi2_contingency(contingency_table)
        return p_value

    def verify(self, confidence_level: float, p_value: float) -> None:
        """
        verify if given confidence level and p value obtained form get_p_value the test passes, if not throw assertion
        error. if test passes do nothing
        Args:
            confidence_level: statistical tests confidence level
            p_value: obtained p value

        Returns: none

        """
        if p_value >= 1 - confidence_level:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"AssertEntangled failed, p value of the test was {p_value} which "
                                 f"was higher then required {threshold} to reject independence hypothesis")

    @staticmethod
    def _get_contingency_table(result: TestResult, qubit_0_index: int, qubit_1_index: int) -> List[List[int]]:
        """
        computes contingency table
        """
        contingency_table = asarray([
            [0, 0],
            [0, 0]
        ])

        for measurement_result in result.measurement_results:
            for states, value in measurement_result.get_counts().items():
                qubit_0_state = int(states[qubit_0_index])
                qubit_1_state = int(states[qubit_1_index])
                contingency_table[qubit_0_state][qubit_1_state] += value

        contingency_table = delete(contingency_table, argwhere(all(contingency_table[..., :] == 0, axis=0)), axis=1)
        contingency_table = delete(contingency_table, argwhere(all(contingency_table[..., :] == 0, axis=1)), axis=0)

        return contingency_table
