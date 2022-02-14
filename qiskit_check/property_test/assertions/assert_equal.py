from typing import List, Dict

from scipy.stats import ttest_ind, ttest_rel

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit


class AssertEqual(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit, ideal: bool) -> None:
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1
        self.test = ttest_ind if ideal else ttest_rel

    def verify(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        # TODO: this doesn't exactly check if qubits have equal states, it checks if probabilities are same,but not -|1>
        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        qubit_0_values = []
        qubit_1_values = []

        for experiment in experiments:
            num_qubit_0_in_state_0 = 0
            num_qubit_1_in_state_0 = 0
            for states, value in experiment.items():
                if states[len(states) - qubit_0_index - 1] == "0":
                    num_qubit_0_in_state_0 += value
                if states[len(states) - qubit_1_index - 1] == "0":
                    num_qubit_1_in_state_0 += value
            qubit_0_values.append(num_qubit_0_in_state_0)
            qubit_1_values.append(num_qubit_1_in_state_0)

        return self.test(qubit_0_values, qubit_1_values).pvalue
