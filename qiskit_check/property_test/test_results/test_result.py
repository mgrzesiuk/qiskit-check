from typing import Dict, List

from qiskit_check.property_test.resources.test_resource import Qubit


class TestResult:
    def __init__(self, individual_measurements: Dict[Qubit, List[List[float]]], counts: List[List[Dict[str, int]]]):
        self.individual_measurements = individual_measurements
        self.counts = counts