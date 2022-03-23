from abc import ABC, abstractmethod
from typing import Tuple, Dict

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Measure
from qiskit.result import Result


class AbstractTomography(ABC):
    """
    https://arxiv.org/pdf/1804.03719.pdf
    """
    @abstractmethod
    def insert_measurement(
            self, circuit: QuantumCircuit, qubit_index: int, location, measurement: Instruction) -> None:
        pass

    @abstractmethod
    def estimate_state(self, measurements: Dict[str, Dict[str, int]]) -> Tuple[float, float]:
        pass

    @abstractmethod
    def calculate_p_value(self, estimated_state: Tuple[float, float], expected_state: Tuple[float, float]) -> float:
        pass

    @staticmethod
    def get_measure_x() -> Instruction:
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label="measure_x")

    @staticmethod
    def get_measure_y() -> Instruction:
        qc = QuantumCircuit(1, 1)
        qc.sdg(0)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label="measure_y")

    @staticmethod
    def get_measure_z() -> Instruction:
        return Measure()
