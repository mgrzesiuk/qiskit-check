from abc import ABC, abstractmethod
from typing import List, Tuple

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Measure


class AbstractTomography(ABC):
    """
    https://arxiv.org/pdf/1804.03719.pdf
    """
    @abstractmethod
    def get_measurement_circuits(self) -> List[QuantumCircuit]:
        pass

    @abstractmethod
    def estimate_state(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def calculate_p_value(self) -> float:
        pass

    @staticmethod
    def _get_measure_x() -> Instruction:
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label="measure_x")

    @staticmethod
    def _get_measure_y() -> Instruction:
        qc = QuantumCircuit(1, 1)
        qc.sdg(0)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label="measure_y")

    @staticmethod
    def _get_measure_z() -> Instruction:
        return Measure()
