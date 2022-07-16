from typing import Dict, List, Sequence
from math import acos, cos

from scipy.spatial.transform import Rotation
from qiskit.circuit import Instruction, Measure
from qiskit_check.property_test.test_results import test_result

from qiskit_check.property_test.assertions import AbstractAssertion, AssertProbability
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_bloch_vector


class AssertTransformedByProbability(AbstractAssertion):
    """
    assert that given qubit has been rotated by specified rotation (equality checked by equal probabilities)
    """
    def __init__(self, qubit: Qubit, rotation: Rotation, measurements: Sequence[Instruction]=(Measure(),), location: int = None) -> None:
        super().__init__(measurements, location, self.combiner)
        self.qubit = qubit
        self.rotation = rotation
        self.state = "0"
        
    def combiner(self, experiments: List[List[Dict[str, int]]]) -> List[List[float]]:
        probabilities_for_measurement = []
        for experiments_for_measurement in experiments:
            probabilities = []
            for experiment in experiments_for_measurement:
                probabilities.append(experiment[self.state]/sum(experiment.values()))
            probabilities_for_measurement.append(probabilities)
        return probabilities_for_measurement


    def get_p_value(self, experiments: test_result, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        qubit_initial_value = resource_matcher[self.qubit].value.data
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value[0], qubit_initial_value[1])
        bloch_vector = hopf_coordinates_to_bloch_vector(theta, phi)
        expected_bloch_vector = self.rotation.apply(bloch_vector).flatten()
        theta = acos(expected_bloch_vector[2])
        expected_ground_state_probability = cos(theta/2)**2
        assert_probability = AssertProbability(self.qubit, self.state, expected_ground_state_probability, self.measurements, self.location)
        return assert_probability.get_p_value(experiments, resource_matcher, num_measurements, num_experiments)
