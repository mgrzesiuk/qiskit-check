from typing import Tuple, List

from qiskit import QuantumCircuit

from qiskit_check._test_engine.state_estimation.tomography import AbstractTomography


class DirectInversionTomography(AbstractTomography):
    def get_measurement_circuits(self) -> List[QuantumCircuit]:
        pass

    def estimate_state(self) -> Tuple[float, float]:
        pass

    def calculate_p_value(self) -> float:
        pass
