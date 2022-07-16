from typing import Union, Dict, List, Sequence

from scipy.stats import chi2_contingency, combine_pvalues
from numpy import asarray, argwhere, all, delete
from qiskit.circuit import Instruction, Measure

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class AssertEntangled(AbstractAssertion):
    """
    assert that 2 qubits are entangled
    """
    def __init__(
            self, qubit_0: Qubit, qubit_1: Qubit, measurements: Sequence[Instruction] = (Measure(),), location: Union[int, None] = None) -> None:
        """
        initialize
        Args:
            qubit_0: qubit 0 template
            qubit_1: qubit 1 template
        """
        super().__init__(measurements, location, lambda _: [[]])
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
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

        contingency_tables = self._get_contingency_tables(experiments.counts, resource_matcher)

        p_values = []
        for contingency_table in contingency_tables:
            _, p_value, _, _ = chi2_contingency(contingency_table)
            p_values.append(p_value)
            
        _, final_p_value = combine_pvalues(p_values)

        return final_p_value

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

    def _get_contingency_tables(self, counts: List[List[Dict[str, int]]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> List[List[List[int]]]:
        """
        computes contingency table
        """
        contingency_tables = []
        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        for counts_per_instruction in counts:

            contingency_table = asarray([
                [0, 0],
                [0, 0]
            ])

            for measurement_result in counts_per_instruction:
                for states, value in measurement_result.items():
                    qubit_0_state = int(states[qubit_0_index])
                    qubit_1_state = int(states[qubit_1_index])
                    contingency_table[qubit_0_state][qubit_1_state] += value

            contingency_table = delete(contingency_table, argwhere(all(contingency_table[..., :] == 0, axis=0)), axis=1)
            contingency_table = delete(contingency_table, argwhere(all(contingency_table[..., :] == 0, axis=1)), axis=0)
        contingency_tables.append(contingency_table)

        return contingency_tables
