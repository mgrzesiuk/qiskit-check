from typing import Dict, Tuple, List

from qiskit import QuantumCircuit
from qiskit.result import Result
from qiskit_utils import parse_result

from qiskit_check.property_test.resources import Qubit
from qiskit_check.property_test.utils import amend_instruction_location


class TomographyResult:
    """
    class to store state tomography results for tests that require them
    """
    def __init__(self) -> None:
        self._estimates_storage = {}

    def add_result(self, estimated_state: Tuple[float, float, float], qubit: Qubit, location: int) -> None:
        """
        add result of an experiment
        Args:
            estimated_state: estimated bloch vector
            qubit: qubit whose state was estimated
            location: location in the circuit when the state was estimated

        Returns: None

        """
        if qubit in self._estimates_storage:
            if location in self._estimates_storage[qubit]:
                self._estimates_storage[qubit][location].append(estimated_state)
            else:
                self._estimates_storage[qubit][location] = [estimated_state]
        else:
            self._estimates_storage[qubit] = {location: [estimated_state]}

    def get_estimates(self, qubit: Qubit, location: int) -> List[Tuple[float, float, float]]:
        """
        get state estimation
        Args:
            qubit: qubit which state estimation to get
            location: location in the circuit when the state of the qubit was estimated

        Returns: list of state estimation (length of the list equal to num of experiments specified in property test)

        """
        amended_location = amend_instruction_location(location)
        return self._estimates_storage[qubit][amended_location]


class MeasurementResult:
    """
    class to store and process measurement results for tests
    """
    def __init__(self, result: Result, circuit: QuantumCircuit) -> None:
        """
        initialize
        Args:
            result: qiskit result of an experiment
            circuit: circuit on which the experiment has been run
        """
        self.circuit = circuit
        self.counts = self._prepare_counts(result.get_counts())
        self.parsed_qubit_results = parse_result(result, circuit)

    def get_qubit_result(self, qubit_index: int, state: str) -> int:
        """
        get number of shots for which qubit with qubit_index (in self.circuit) has been measured in state ('0' or '1')
        Args:
            qubit_index: index of desired qubit in self.circuit - can be obtained from resource_matcher
            state: state of the qubit ('0' or '1') for which we want to get counts

        Returns: number of shots for which qubit was in the specified state

        """
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
        """
        prase counts dictionary and remove spaces from states (keys)
        Args:
            counts: counts obtained from qiskit result get_counts()

        Returns: counts with keys (states) with spaces removed

        """
        prepared_counts = {}
        for state, count in counts.items():
            prepared_counts[state.replace(" ", "")] = count
        return prepared_counts
