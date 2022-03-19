from typing import Dict

from scipy.stats import ttest_ind, ttest_rel

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertEqual(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit, ideal: bool) -> None:
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1
        self.test = ttest_ind if ideal else ttest_rel

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)
        # TODO: this doesn't exactly check if qubits have equal states, it checks if probabilities are same,but not -|1>
        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        qubit_0_values = []
        qubit_1_values = []

        for measurement in result.measurement_results:
            qubit_0_values.append(measurement.get_qubit_result(qubit_0_index, "0"))
            qubit_1_values.append(measurement.get_qubit_result(qubit_1_index, "0"))

        return self.test(qubit_0_values, qubit_1_values).pvalue

    def verify(self, confidence_level: float, p_value: float) -> None:
        if 1 - confidence_level > p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"AssertEqual failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold} to fail to reject equality hypothesis")
