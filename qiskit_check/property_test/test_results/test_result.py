from typing import List, Tuple

from qiskit import QuantumCircuit
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
    def from_qiskit_result(results: List[Result], circuit: QuantumCircuit):
        if len(results) > 0:
            num_shots = results[0].results[0].shots
        else:
            num_shots = 0
        measurement_results = []
        for result in results:
            measurement_results.append(MeasurementResult.from_qiskit_result(result, circuit))
        # TODO: Tomography result
        return TestResult(measurement_results, num_shots)
