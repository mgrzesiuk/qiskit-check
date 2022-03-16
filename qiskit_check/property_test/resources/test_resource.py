from abc import ABC

from qiskit.quantum_info import Statevector

from qiskit_check.property_test.resources.qubit_range import QubitRange


class TestResource(ABC):
    pass


class Qubit(TestResource):
    def __init__(self, values: QubitRange):
        self.values = values


class ConcreteQubit:
    def __init__(self, qubit_index: int, value: Statevector) -> None:
        self.qubit_index = qubit_index
        self.value = value

    def get_qubit(self) -> int:
        return self.qubit_index

    def get_initial_value(self) -> Statevector:
        return self.value
