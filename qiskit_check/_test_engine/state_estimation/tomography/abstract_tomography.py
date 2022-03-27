from abc import ABC, abstractmethod
from math import pi
from typing import Tuple, Dict, List

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Measure


class AbstractTomography(ABC):
    def __init__(self) -> None:
        self.measurement_names = {"x": "measure_x", "y": "measure_y", "z": "measure"}

    @abstractmethod
    def insert_measurement(
            self, circuit: QuantumCircuit, qubit_index: int, location, measurement: Instruction) -> None:
        pass

    @abstractmethod
    def estimate_state(self, measurements: Dict[str, Dict[str, int]]) -> Tuple[float, float, float]:
        pass

    def get_measurement_names(self) -> List[str]:
        return list(self.measurement_names.values())

    def get_measure_x(self) -> Instruction:
        measure_name = self.measurement_names["x"]
        qc = QuantumCircuit(1, 1,  name=measure_name)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label=measure_name)

    def get_measure_y(self) -> Instruction:
        measure_name = self.measurement_names["y"]
        qc = QuantumCircuit(1, 1, name=measure_name)
        qc.rx(-pi/2, 0)
        qc.measure(0, 0)
        return qc.to_instruction(label=measure_name)

    @staticmethod
    def get_measure_z() -> Instruction:
        return Measure()
