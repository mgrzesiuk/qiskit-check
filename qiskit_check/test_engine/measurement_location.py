from typing import Set
from qiskit.circuit import Instruction

from qiskit_check.property_test.resources.test_resource import Qubit


class MeasurementLocation:
    def __init__(self, location: int, instruction: Instruction) -> None:
        self.location = location
        self.instruction = instruction
