from typing import List, Dict

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

    def verify(self, experiments: List[TestResult], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")
        self.check_if_experiments_empty(experiments)

        qubit_index = resource_matcher[self.qubit].qubit_index
        num_shots = sum(experiments[0].values())

        num_successes = 0
        for experiment in experiments:
            for states, value in experiment.items():
                if states[len(states) - qubit_index - 1] == self.state:
                    num_successes += value
        #  TODO: this kind of ignores measurement vs experiment - what to do about this?
        return binomtest(num_successes, len(experiments) * num_shots, self.probability).pvalue
