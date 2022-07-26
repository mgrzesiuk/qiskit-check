from abc import ABC, abstractmethod
from typing import Dict, List, Sequence, Callable, Tuple, Union
from uuid import uuid4

from qiskit.circuit import Instruction, Measure
from qiskit_check.property_test.test_results.test_result import TestResult

from qiskit_check.property_test.property_test_errors import IncorrectPropertyTestError, NoExperimentsError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit

class AbstractAssertion(ABC):
    def __init__(self, measurements: Sequence[Instruction], location: Union[int, None], combiner: Callable[[List[List[Dict[str, int]]]], List[List[float]]]) -> None:
        self.verify_measurements(measurements)
        
        self.measurements = measurements
        self.location = location if location is not None else None
        self.combiner = combiner
        self.name = str(uuid4())

    @abstractmethod
    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit], num_measurements: int, num_experiments: int) -> float:
        pass

    def verify(self, confidence_level: float, p_value: float) -> None:
        if 1 - confidence_level >= p_value:
            threshold = round(1 - confidence_level, 5)
            raise AssertionError(f"{self.__class__.__name__} failed, p value of the test was {p_value} which "
                                 f"was lower then required {threshold} to fail to reject equality hypothesis")

    def get_qubits(self) -> Tuple[Qubit]:
        qubits = []
        for _, param_value in self.__dict__.items():
            if isinstance(param_value, Qubit):
                qubits.append(param_value)

        if len(qubits) == 0:
            raise IncorrectPropertyTestError("Assertion must specify at least one qubit")
        return tuple(qubits)
    
    @staticmethod
    def verify_measurements(measurements: Sequence[Instruction]) -> None:
        #TODO: implement this, check if measurement inside and name not measure if not measure operation
        for measurement in measurements:
            if not AbstractAssertion.is_measurement_valid(measurement):
                raise IncorrectPropertyTestError("measurements provided must muse qiskit Measure gate at some points")
    
    @staticmethod
    def is_measurement_valid(measurement: Instruction) -> bool:
        if measurement.name == Measure().name:
            return True
        if measurement._definition is None:
            return False # this is only ok if measurement is z basis measurement but we already know its not
        
        is_valid = False
        for instruction, _, _ in measurement._definition.data:
            is_valid = is_valid or AbstractAssertion.is_measurement_valid(instruction)
        
        return is_valid
