from typing import Dict

from qiskit.result import Result


class TomographyResult:
    @staticmethod
    def from_qiskit_result(result: Result):
        raise NotImplemented()


class MeasurementResult:
    def __init__(self) -> None:
        pass

    def get_qubit_result(self, qubit_index: int, state: str) -> str:
        pass

    def get_counts(self) -> Dict[str, int]:
        pass

    def __len__(self) -> int:
        pass

    @staticmethod
    def from_qiskit_result(result: Result):
        raise NotImplemented()

