from typing import Tuple, Dict

from hyppo.ksample import Hotelling
from numpy import asarray

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check.property_test.utils import hopf_coordinates_to_bloch_vector


class AssertStateEqual(AbstractAssertion):
    def __init__(self, qubit: Qubit, location: int, expected_state: Tuple[float, float]) -> None:
        self.qubit = qubit
        self.location = location
        self.expected_state = hopf_coordinates_to_bloch_vector(*expected_state)
        self.test = Hotelling().test

    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        samples = asarray(experiments.tomography_result.get_estimates(self.qubit, self.location))
        _, p_value = self.test(samples, asarray([self.expected_state]*len(samples)))
        return p_value

    def get_qubits_requiring_tomography(self) -> Dict[Qubit, int]:
        return {self.qubit: self.location}
