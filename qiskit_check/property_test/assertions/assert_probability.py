from typing import Dict

from scipy.stats import ttest_1samp

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

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")
        self.check_if_experiments_empty(result)

        qubit_index = resource_matcher[self.qubit].qubit_index

        experiment_results = []
        for measurement_result in result.measurement_results:
            experiment_results.append(measurement_result.get_qubit_result(qubit_index, self.state)/result.num_shots)

        return ttest_1samp(experiment_results, self.probability, alternative="two-sided").pvalue

    def verify(self, confidence_level: float, p_value: float) -> None:
        if 1 - confidence_level > p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"AssertProbability failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold} to fail to reject equality hypothesis")
