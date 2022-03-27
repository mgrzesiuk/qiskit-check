from typing import Dict, Tuple, List

from qiskit import QuantumCircuit
from qiskit.result import Result
from qiskit_utils import parse_result

from qiskit_check.property_test.resources import Qubit
from qiskit_check.property_test.utils import amend_instruction_location


class TomographyResult:
    def __init__(self) -> None:
        self._estimates_storage = {}

    def add_result(self, estimated_state: Tuple[float, float, float], qubit: Qubit, location: int) -> None:
        if qubit in self._estimates_storage:
            if location in self._estimates_storage[qubit]:
                self._estimates_storage[qubit][location].append(estimated_state)
            else:
                self._estimates_storage[qubit][location] = [estimated_state]
        else:
            self._estimates_storage[qubit] = {location: [estimated_state]}

    def get_estimates(self, qubit: Qubit, location: int) -> List[Tuple[float, float, float]]:
        amended_location = amend_instruction_location(location)
        return self._estimates_storage[qubit][amended_location]


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
