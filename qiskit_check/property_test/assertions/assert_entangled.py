from typing import List, Dict

from scipy.stats import fisher_exact

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertEntangled(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit) -> None:
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1

    def verify(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        """
        contingency table with counts as follows:
            qubit 0 state 0 and qubit 1 in state 0 | qubit 0 in state 1 and qubit 1 in state 0
            qubit 0 state 0 and qubit 1 in state 1 | qubit 0 in state 1 and qubit 1 in state 1
        """
        contingency_table = (
            (0, 0),
            (0, 0)
        )
        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index
        # TODO: not exactly safe
        for experiment in experiments:
            for states, value in experiment.qiskit_result.get_counts().items():
                qubit_0_state = int(states[len(states) - qubit_0_index - 1])
                qubit_1_state = int(states[len(states) - qubit_1_index - 1])
                contingency_table[qubit_0_state][qubit_1_state] += value

        return fisher_exact(contingency_table).p_value
