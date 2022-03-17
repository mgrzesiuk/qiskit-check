from typing import Dict

from qiskit import QuantumCircuit
from qiskit.result import Result
from qiskit_utils import parse_result


class TomographyResult:
    @staticmethod
    def from_qiskit_result(result: Result):
        raise NotImplemented()


class MeasurementResult:
    def __init__(self, result: Result, circuit: QuantumCircuit) -> None:
        self.circuit = circuit
        self.counts = self._prepare_counts(result.get_counts())
        self.parsed_qubit_results = parse_result(result, circuit)

    def get_qubit_result(self, qubit_index: int, state: str) -> int:
        if qubit_index not in self.parsed_qubit_results:
            raise ValueError("no results stored for qubit index provided")
        if None in self.parsed_qubit_results[qubit_index]:
            raise ValueError(f"no measurements found for qubit {qubit_index}")
        if state not in self.parsed_qubit_results[qubit_index]:
            return 0
        return self.parsed_qubit_results[qubit_index][state]

    def get_counts(self) -> Dict[str, int]:
        return self.counts.copy()

    @staticmethod
    def _prepare_counts(counts: Dict[str, int]) -> Dict[str, int]:
        prepared_counts = {}
        for state, count in counts.items():
            prepared_counts[state.replace(" ", "")] = count
        return prepared_counts
