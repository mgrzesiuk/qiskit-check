from math import isnan
from typing import Dict

from scipy.stats import ttest_ind, ttest_rel

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertEqual(AbstractAssertion):
    """
    assert if 2 qubits have equal probabilities of obtaining the same result
    """
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit, ideal: bool = False) -> None:
        """
        initialize
        Args:
            qubit_0: qubit 0 template
            qubit_1: qubit 1 template
            ideal: if ideal ttest should be used or an realistic one (according to scipy)
        """
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1
        self.test = ttest_ind if ideal else ttest_rel

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p value of the test that 2 qubits are equal given the results
        Args:
            result: test results obtained from running property test
            resource_matcher: mapping between qubit templates and ConcreteQubit holding information about
            initial state and index in the circuit of the real qubit

        Returns: p-value, float between 0 and 1 (if nan 1 is returned)
        """
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)

        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        qubit_0_values = []
        qubit_1_values = []

        for measurement in result.measurement_results:
            qubit_0_values.append(measurement.get_qubit_result(qubit_0_index, "0"))
            qubit_1_values.append(measurement.get_qubit_result(qubit_1_index, "0"))

        p_value = self.test(qubit_0_values, qubit_1_values, nan_policy='omit').pvalue
        if isnan(p_value):
            p_value = 1
        return p_value
