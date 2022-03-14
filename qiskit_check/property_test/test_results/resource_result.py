from typing import Dict, List

from qiskit import QuantumCircuit
from qiskit.circuit import Clbit
from qiskit.result import Result


class TomographyResult:
    @staticmethod
    def from_qiskit_result(result: Result):
        raise NotImplemented()


class MeasurementResult:
    def __init__(self, counts: Dict[str, int], circuit: QuantumCircuit) -> None:
        self.circuit = circuit
        self.counts = self._preper_counts(counts)
        self.parsed_qubit_results = self._get_parsed_qubit_results()

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
    def from_qiskit_result(result: Result, circuit: QuantumCircuit):
        return MeasurementResult(result.get_counts(), circuit)

    def _get_parsed_qubit_results(self) -> Dict[int, Dict[str, int]]:
        parsed_qubit_results = {}
        qubit_clbit_mapping = MeasurementResult._get_qubit_to_clbit_mapping(self.circuit)

        for state, count in self.counts.items():
            parsed_state = self._get_parsed_state(state, qubit_clbit_mapping)
            for index in range(len(parsed_state)):
                qubit_state = parsed_state[index]
                if index in parsed_qubit_results:
                    if qubit_state in parsed_qubit_results[index]:
                        parsed_qubit_results[index][qubit_state] += count
                    else:
                        parsed_qubit_results[index][qubit_state] = count
                else:
                    parsed_qubit_results[index] = {qubit_state: count}

        return parsed_qubit_results

    @staticmethod
    def _preper_counts(counts: Dict[str, int]) -> Dict[str, int]:
        prepared_counts = {}
        for state, count in counts.items():
            prepared_counts[state.replace(" ", "")] = count
        return prepared_counts

    @staticmethod
    def _get_qubit_to_clbit_mapping(circuit: QuantumCircuit) -> List[int]:
        mapping = [None] * circuit.num_qubits
        # we want to give priority to user defined measurements and our measurements are last in the list so reverse it
        for instruction, qubits, clbits in reversed(circuit.get_instructions("measure")):
            clbit_index = MeasurementResult._get_clbit_global_index(clbits[0], circuit)
            mapping[qubits[0].index] = clbit_index
        return mapping

    @staticmethod
    def _get_clbit_global_index(clbit: Clbit, circuit: QuantumCircuit) -> int:
        current_register_start_index = 0
        for c_reg in circuit.cregs:
            if c_reg == clbit.register:
                return current_register_start_index + c_reg.index(clbit)
            current_register_start_index += len(c_reg)

    @staticmethod
    def _get_parsed_state(state: str, qubit_clbit_mapping: List[int]) -> List[chr]:
        # qiskit returns results from rightmost (so clbit with index 0 is last char in state) so we reverse the string
        no_white_space_state = state.replace(" ", "")[::-1]
        states = []
        for clbit_index in qubit_clbit_mapping:
            if clbit_index is not None:
                states.append(no_white_space_state[clbit_index])
            else:
                states.append(None)

        return states
