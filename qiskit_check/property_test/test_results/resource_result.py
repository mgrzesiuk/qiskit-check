import string
from typing import Dict

from qiskit.result import Result


class TomographyResult:
    @staticmethod
    def from_qiskit_result(result: Result):
        raise NotImplemented()


class MeasurementResult:
    def __init__(self, parsed_counts: Dict[str, int]) -> None:
        self.parsed_counts = parsed_counts.copy()
        self.parsed_qubit_results = self._get_parsed_qubit_results()

    def get_qubit_result(self, qubit_index: int, state: str) -> int:
        return self.parsed_qubit_results[qubit_index][state]

    def get_counts(self) -> Dict[str, int]:
        return self.parsed_counts.copy()

    def _get_parsed_qubit_results(self) -> Dict[int, Dict[str, int]]:
        pass

    @staticmethod
    def from_qiskit_result(result: Result):
        counts = result.get_counts()
        parsed_counts = {}
        n_qubits = result.results[0].header.n_qubits
        for state, count in counts.items():
            parsed_state = MeasurementResult.get_parsed_state(state, n_qubits)
            parsed_counts[parsed_state] = count

        return MeasurementResult(parsed_counts)

    @staticmethod
    def get_parsed_state(state: str, num_qubits: int) -> str:
        no_white_space_state = state.replace(string.whitespace, "")
        only_qubits_state = no_white_space_state[:num_qubits]
        return only_qubits_state[::-1]
