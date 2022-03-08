from typing import List

from qiskit.result import Result

from qiskit_check.property_test.test_results import MeasurementResult, TomographyResult


class TestResult:
    def __init__(
            self, measurement_results: List[MeasurementResult], num_shots: int,
            tomography_result: TomographyResult = None) -> None:
        self.measurement_results = measurement_results
        self.tomography_result = tomography_result
        self.num_experiments = len(measurement_results)
        self.num_shots = num_shots

    def is_tomography_available(self) -> bool:
        return not (self.tomography_result is None)

    @staticmethod
    def from_qiskit_result(result: Result):
        raise NotImplemented()
