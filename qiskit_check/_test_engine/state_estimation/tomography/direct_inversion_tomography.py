from typing import Tuple, Dict

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction

from qiskit_check._test_engine.state_estimation.tomography import AbstractTomography


class DirectInversionTomography(AbstractTomography):
    def insert_measurement(self, circuit: QuantumCircuit, qubit_index: int, location, measurement: Instruction) -> None:
        pass

    def estimate_state(self, measurements: Dict[str, Dict[str, int]]) -> Tuple[float, float]:
        pass

    def calculate_p_value(self, estimated_state: Tuple[float, float], expected_state: Tuple[float, float]) -> float:
        pass
