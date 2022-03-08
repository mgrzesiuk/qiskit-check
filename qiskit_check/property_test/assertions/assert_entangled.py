from typing import Dict

from scipy.stats import fisher_exact

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertEntangled(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit) -> None:
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1

    def verify(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(result)
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

        for measurement_result in result.measurement_results:
            for states, value in measurement_result.get_counts().items():
                qubit_0_state = int(states[qubit_0_index])
                qubit_1_state = int(states[qubit_1_index])
                contingency_table[qubit_0_state][qubit_1_state] += value

        return fisher_exact(contingency_table).p_value
