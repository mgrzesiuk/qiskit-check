from typing import Dict, List, Sequence

from qiskit.circuit import Instruction, Measure
from qiskit_check.property_test.test_results.test_result import TestResult

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.property_test_errors import NoQubitFoundError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit


class AssertTeleportedByProbability(AbstractAssertion):
    """
    assert if a qubit has been teleported (equality checked by equal probabilities)
    """
    def __init__(self, qubit_to_teleport: Qubit, target_qubit: Qubit, measurements: Sequence[Instruction]=(Measure(),),location: int = None) -> None:
        super().__init__(measurements, location, self.combiner)
        self.qubit_to_teleport = qubit_to_teleport
        self.state = "0"
        self.target_qubit = target_qubit

    # TODO: extract this into a super class that will encapsulate assert probability, assert teleported etc
    def combiner(self, experiments: List[List[Dict[str, int]]]) -> List[List[float]]:
        probabilities_for_measurement = []
        for experiments_for_measurement in experiments:
            probabilities = []
            for experiment in experiments_for_measurement:
                probabilities.append(experiment[self.state]/sum(experiment.values()))
            probabilities_for_measurement.append(probabilities)
        return probabilities_for_measurement

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        if self.qubit_to_teleport not in resource_matcher or self.target_qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        expected_ground_state_probability = resource_matcher[self.qubit_to_teleport].value.probabilities()[0]
        assert_probability = AssertProbability(self.target_qubit, self.state, expected_ground_state_probability, self.measurements, self.location)
        return assert_probability.get_p_value(experiments, resource_matcher, num_measurements, num_experiments)
