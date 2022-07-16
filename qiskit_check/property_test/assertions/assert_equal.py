from math import isnan
from typing import Dict, List, Sequence, Union

from scipy.stats import ttest_ind, ttest_rel, combine_pvalues
from qiskit.circuit import Instruction, Measure
from qiskit_check.property_test import test_results

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit


class AssertEqualByProbability(AbstractAssertion):
    """
    assert if 2 qubits have equal probabilities of obtaining the same result
    """
    def __init__(
            self, qubit_0: Qubit, qubit_1: Qubit, measurements: Sequence[Instruction] = (Measure(),), 
            location: Union[int, None] = None, ideal: bool = False, state_to_check: str = "0") -> None:
        """
        initialize
        Args:
            qubit_0: qubit 0 template
            qubit_1: qubit 1 template
            ideal: if ideal ttest should be used or an realistic one (according to scipy)
        """
        super().__init__(measurements, location, self.combiner)
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1
        self.state_to_check = state_to_check
        self.test = ttest_ind if ideal else ttest_rel
    
    def combiner(self, experiments: List[List[Dict[str, int]]]) -> List[List[float]]:
        counts_for_measurement = []
        for experiments_for_measurement in experiments:
            counts = []
            for experiment in experiments_for_measurement:
                counts.append(experiment[self.state_to_check])
            counts_for_measurement.append(counts)
        return counts_for_measurement

    def get_p_value(self, experiments: test_results, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        qubit_0_results = experiments.individual_measurements[self.qubit_0]
        qubit_1_results = experiments.individual_measurements[self.qubit_1]

        p_values = []
        for qubit_0_per_measurement, qubit_1_results_per_measurement in zip(qubit_0_results, qubit_1_results):
            p_value = self.test(qubit_0_per_measurement, qubit_1_results_per_measurement, nan_policy='omit').pvalue
            if isnan(p_value):
                p_value = 1 #TODO: figure out a better way to handle cases where tests return nan
            p_values.append(p_value)

        _, p_value = combine_pvalues(p_values)
        return p_value
