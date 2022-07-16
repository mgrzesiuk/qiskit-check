from math import isnan
from typing import Union, Dict, List, Sequence

from scipy.stats import ttest_1samp, combine_pvalues
from qiskit.circuit import Instruction, Measure
from qiskit_check.property_test.test_results.test_result import TestResult

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import IncorrectQubitStateError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit


class AssertProbability(AbstractAssertion):
    """
    assert if probability of qubit being in a given state is as expected
    """
    def __init__(self, qubit: Qubit, state: str, probability: float, measurements: Sequence[Instruction] = (Measure(),), location: Union[int, None] = None) -> None:
        super().__init__(measurements, location, self.combiner)
        self.qubit = qubit
        if state != "0" and state != "1":
            raise IncorrectQubitStateError("It is only possible to assert probability of qubit being in state 0 or 1")
        self.state = state
        self.probability = probability

    def combiner(self, experiments: List[List[Dict[str, int]]]) -> List[List[float]]:
        probabilities_for_measurement = []
        for experiments_for_measurement in experiments:
            probabilities = []
            for experiment in experiments_for_measurement:
                probabilities.append(experiment[self.state]/sum(experiment.values()))
            probabilities_for_measurement.append(probabilities)
        return probabilities_for_measurement

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        results = experiments.individual_measurements[self.qubit]
        p_values = []
        for result_per_measurement in results:
            p_value = ttest_1samp(result_per_measurement, self.probability, alternative="two-sided", nan_policy='omit').pvalue
            if isnan(p_value):
                p_value = 1 #TODO: figure out a better way to handle cases where tests return nan
            p_values.append(p_value)
        _, p_value = combine_pvalues(p_values)
        return p_value