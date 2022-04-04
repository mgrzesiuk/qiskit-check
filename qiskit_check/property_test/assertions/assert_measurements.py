from typing import Dict

from qiskit_check.property_test.assertions import AbstractAssertion, AssertTrue
from qiskit_check.property_test.resources.test_resource import ConcreteQubit, Qubit
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class AssertMostProbable(AbstractAssertion):
    """
    assert if the specified result has highest probability (measurement of all qubits)
    """
    def __init__(self, expected_state: str) -> None:
        """
        initialize
        Args:
            expected_state: state that is expected to have highest probability
        """
        self.expected_state = expected_state
        self.assert_true = AssertTrue(self._verify_function, 1)

    def _verify_function(self, result: MeasurementResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        function to check if the measurement result has the most probable state as expected
        Args:
            result:
            resource_matcher: mapping between qubit templates and ConcreteQubit holding information about
            initial state and index in the circuit of the real qubit

        Returns: 1 if expected result is most common else 0

        """
        counts = result.get_counts()
        if self.expected_state not in counts:
            return 0
        state_likelihood = counts[self.expected_state]
        if state_likelihood >= max(counts.values()):
            return 1
        else:
            return 0

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        get p value of the test the expected measurement result is most probable
        Args:
            result: test results obtained from running property test
            resource_matcher: mapping between qubit templates and ConcreteQubit holding information about
            initial state and index in the circuit of the real qubit

        Returns: p-value, float between 0 and 1 (if nan 1 is returned)
        """
        return self.assert_true.get_p_value(result, resource_matcher)


class AssertMeasurementEqual(AbstractAssertion):
    """
    assert if the specified result has highest probability (measurement of all qubits)
    """
    def __init__(self, expected_state) -> None:
        """
        initialize
        Args:
            expected_state: state that is expected to have highest probability
        """
        self.expected_state = expected_state

    def get_p_value(self, result: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        verify if the expected measurement is one that is most often
        Args:
            result: test results obtained from running property test
            resource_matcher: mapping between qubit templates and ConcreteQubit holding information about
            initial state and index in the circuit of the real qubit

        Returns: p-value, float between 0 and 1
        """
        self.check_if_experiments_empty(result)

        minimal_probability = 1

        num_shots = result.num_shots

        for measurement_result in result.measurement_results:
            counts = measurement_result.get_counts()
            if self.expected_state not in counts:
                return 0
            else:
                current_probability = counts[self.expected_state]/float(num_shots)
                if current_probability < minimal_probability:
                    minimal_probability = current_probability

        return minimal_probability
