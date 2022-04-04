from math import isnan
from typing import Dict

from scipy.stats import ttest_1samp

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import IncorrectQubitStateError, NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class AssertProbability(AbstractAssertion):
    """
    assert if probability of qubit being in a given state is as expected
    """
    def __init__(self, qubit: Qubit, state: str, probability: float) -> None:
        """
        initialize
        Args:
            qubit: qubit template to assert
            state: probability of which state to assert
            probability: expected probability
        """
        self.qubit = qubit
        if state != "0" and state != "1":
            raise IncorrectQubitStateError("It is only possible to assert probability of qubit being in state 0 or 1")
        self.state = state
        self.probability = probability

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p value of the test that probability of qubit being in a given state is as specified
        Args:
            result: test results obtained from running property test
            resource_matcher: mapping between qubit templates and ConcreteQubit holding information about
            initial state and index in the circuit of the real qubit

        Returns: p-value, float between 0 and 1
        """
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")
        self.check_if_experiments_empty(result)

        qubit_index = resource_matcher[self.qubit].qubit_index

        experiment_results = []
        for measurement_result in result.measurement_results:
            experiment_results.append(measurement_result.get_qubit_result(qubit_index, self.state)/result.num_shots)

        p_value = ttest_1samp(experiment_results, self.probability, alternative="two-sided", nan_policy='omit').pvalue
        if isnan(p_value):
            p_value = 1
        return p_value
