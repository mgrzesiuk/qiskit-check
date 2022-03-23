from typing import Dict, Tuple, Callable

from qiskit import QuantumCircuit
from qiskit.result import Result
from qiskit_utils import parse_result

from qiskit_check.property_test.resources import Qubit


class TomographyResult:
    def __init__(self) -> None:
        self._estimates_storage = {}
        self._p_value_calculator_storage = {}

    def add_result(
            self, estimated_state: Tuple[float, float], qubit: Qubit, location: int,
            p_value_estimate: Callable[[Tuple[float, float], Tuple[float, float]], float]) -> None:
        self._safe_insert(self._estimates_storage, qubit, location, estimated_state)
        self._safe_insert(self._p_value_calculator_storage, qubit, location, p_value_estimate)

    def get_estimate(self, qubit: Qubit, location: int) -> Tuple[float, float]:
        return self._estimates_storage[qubit][location]

    def get_p_value(self, qubit: Qubit, location: int, expected_state: Tuple[float, float]) -> float:
        estimated_state = self.get_estimate(qubit, location)
        return self._p_value_calculator_storage[qubit][location](estimated_state, expected_state)

    @staticmethod
    def _safe_insert(dictionary: Dict[Qubit, Dict[int, any]], qubit: Qubit, location: int, value: any) -> None:
        if qubit in dictionary:
            dictionary[qubit][location] = value
        else:
            dictionary[qubit] = {location: value}


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
