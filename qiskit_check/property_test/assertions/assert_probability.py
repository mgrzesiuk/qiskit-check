from typing import Dict

from scipy.stats import binomtest

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import IncorrectQubitStateError, NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertProbability(AbstractAssertion):
    def __init__(self, qubit: Qubit, state: str, probability: float) -> None:
        self.qubit = qubit
        if state != "0" and state != "1":
            raise IncorrectQubitStateError("It is only possible to assert probability of qubit being in state 0 or 1")
        self.state = state
        self.probability = probability

    def verify(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")
        self.check_if_experiments_empty(result)

        qubit_index = resource_matcher[self.qubit].qubit_index
        num_shots = result.num_shots

        num_successes = 0
        for measurement_result in result.measurement_results:
            num_successes += measurement_result.get_qubit_result(qubit_index, self.state)
        #  TODO: this kind of ignores measurement vs experiment - what to do about this?
        return binomtest(num_successes, result.num_experiments * num_shots, self.probability).pvalue
