from math import isnan
from typing import Dict, Callable, List, Sequence

from scipy.stats import ttest_1samp
from qiskit.circuit import Instruction, Measure

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class AssertTrue(AbstractAssertion):
    """
    assert that a given condition is true, allows used to specify function that takes measurement result and
    resource matcher and outputs a float, than that float is tested against specified expected value
    """
    def __init__(
            self, qubits: Sequence[Qubit], verify_function: Callable[[List[Dict[str, int]], Dict[Qubit, ConcreteQubit]], float],
            target_value: float, measurements: Sequence[Instruction] = (Measure(),), location: int = None) -> None:
        super().__init__(measurements, location, lambda x: [[]])
        self.verify_function = verify_function
        self.target_value = target_value
        for qubit in qubits:
            self.__setattr__(f"_qubit_{qubit.name.replace('-', '_')}", qubit)

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        counts = []
        # parse into list of experiments [ list of instructions [counts dict]]
        for i in range(len(experiments.counts[0])):
            counts_for_instructions = []
            for experiment_by_instruction in experiments.counts:
                counts_for_instructions.append(experiment_by_instruction[i])
            counts.append(counts_for_instructions)
    
        experiment_values = []
        for experiment in counts:
            experiment_values.append(self.verify_function(experiment, resource_matcher))
        p_value = ttest_1samp(experiment_values, self.target_value).pvalue
        if isnan(p_value):
            p_value = 1
        return p_value
