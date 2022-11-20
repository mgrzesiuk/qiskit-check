from typing import Dict, List

from qiskit_check.property_test.resources.test_resource import Qubit


class TestResult:
    """
    data class to store parsed results of measurements in multiple formats
    """
    def __init__(self, individual_measurements: Dict[Qubit, List[List[float]]], counts: List[List[Dict[str, int]]]):
        """

        Args:
            individual_measurements (Dict[Qubit, List[List[float]]]): Dictionary with keys as qubit and outputs of combine function for that qubit as values
            counts (List[List[Dict[str, int]]]): list of counts for each measurement, the format is: first list is a list of instructions, second list is a list of measurements and then dict of counts,
            parsed so that accessing str[i] gives measurement for qubit of index i (note this is not what happens with qiskit get_counts)
        """
        self.individual_measurements = individual_measurements
        self.counts = counts