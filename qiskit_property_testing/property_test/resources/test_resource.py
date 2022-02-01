from abc import ABC, abstractmethod

from qiskit_property_testing.property_test.resources.qubit_range import QubitRange


class TestResource(ABC):
    pass


class Qubit(TestResource):
    def __init__(self, values: QubitRange):
        self.values = values


class Bit(TestResource):
    pass
