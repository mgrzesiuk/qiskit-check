from qiskit.result import Result

from qiskit_check.property_test.test_results import MeasurementResult, TomographyResult


class TestResult:
    def __init__(self, measurement_result: MeasurementResult, tomography_result: TomographyResult = None) -> None:
        self.measurement_result = measurement_result
        self.tomography_result = tomography_result

    def is_tomography_available(self) -> bool:
        return not (self.tomography_result is None)

    @staticmethod
    def from_qiskit_result(result: Result):
        pass

