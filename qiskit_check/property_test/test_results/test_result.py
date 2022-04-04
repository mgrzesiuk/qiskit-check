from typing import List

from qiskit import QuantumCircuit
from qiskit.result import Result

from qiskit_check.property_test.test_results import MeasurementResult, TomographyResult


class TestResult:
    """
    object holding results of the tests
    """
    def __init__(
            self, measurement_results: List[MeasurementResult], num_shots: int,
            tomography_result: TomographyResult) -> None:
        """
        initialize
        Args:
            measurement_results: list of measurements results from the tests (length equal to num of experiments
            specified in the property test)
            num_shots: number of qiskit shots made for the test
            tomography_result: result of tomography if assertions requiring tomography were else should be set to none
        """
        self.measurement_results = measurement_results
        self.tomography_result = tomography_result
        self.num_experiments = len(measurement_results)
        self.num_shots = num_shots

    def is_tomography_available(self) -> bool:
        """
        check if tomography has been provided for this test
        Returns: true if tomography is not none else false

        """
        return not (self.tomography_result is None)

    @staticmethod
    def from_qiskit_result(results: List[Result], tomography_result: TomographyResult, circuit: QuantumCircuit):
        """

        Args:
            results:
            tomography_result:
            circuit:

        Returns:

        """
        if len(results) > 0:
            num_shots = results[0].results[0].shots
        else:
            num_shots = 0
        measurement_results = []
        for result in results:
            measurement_results.append(MeasurementResult(result, circuit))
        return TestResult(measurement_results, num_shots, tomography_result)
