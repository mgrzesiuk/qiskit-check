from abc import ABC, abstractmethod
from math import pi
from typing import Tuple, Dict, List

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Measure


class AbstractTomography(ABC):
    """
    abstract class for doing state tomography
    """
    def __init__(self) -> None:
        self.measurement_names = {"x": "measure_x", "y": "measure_y", "z": "measure"}

    @abstractmethod
    def insert_measurement(
            self, circuit: QuantumCircuit, qubit_index: int, location, measurement: Instruction) -> None:
        """
        insert measurement at a given location for a given qubit in q circuit
        Args:
            circuit: circuit where to insert the measurement
            qubit_index: index of qubit to measure
            location: desired location of the measurement (index of inserted measurement in circuit.data)
            measurement: instruction to insert

        Returns: None, insertion done in place

        """
        pass

    @abstractmethod
    def estimate_state(self, measurements: Dict[str, Dict[str, int]]) -> Tuple[float, float, float]:
        """
        get estimate of bloch vector given measurements
        Args:
            measurements: measurements with dict {'x': counts in x basis, 'y': counts in y basis, 'z' counts in z basis}

        Returns: [x,y,z] - estimated bloch vector

        """
        pass

    def get_measurement_names(self) -> List[str]:
        """

        Returns: get list of measurement instruction names

        """
        return list(self.measurement_names.values())

    def get_measure_x(self) -> Instruction:
        """

        Returns: get instruction for measurement in x basis

        """
        measure_name = self.measurement_names["x"]
        qc = QuantumCircuit(1, 1,  name=measure_name)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label=measure_name)

    def get_measure_y(self) -> Instruction:
        """

        Returns: get instruction for measurement in y basis

        """
        measure_name = self.measurement_names["y"]
        qc = QuantumCircuit(1, 1, name=measure_name)
        qc.rx(-pi/2, 0)
        qc.measure(0, 0)
        return qc.to_instruction(label=measure_name)

    @staticmethod
    def get_measure_z() -> Instruction:
        """

        Returns: get instruction for measurement in z basis

        """
        return Measure()
