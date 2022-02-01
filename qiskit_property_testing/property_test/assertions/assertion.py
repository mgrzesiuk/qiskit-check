from abc import ABC

from qiskit_property_testing.property_test.resources.test_resource import Qubit


class AbstractAssertion(ABC):
    pass


class AssertTrue(AbstractAssertion):
    def __init__(self, condition):
        pass


class AssertProbability(AbstractAssertion):
    def __init__(self, state: int, probability: float):
        pass


class AssertEntangled(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit):
        pass


class AssertEqual(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit):
        pass


class AssertTeleported(AbstractAssertion):
    def __init__(self, qubit: Qubit):
        pass


class AssertTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, phase_shift: float, angle_shift: float):
        pass


class AssertMeasurement(AbstractAssertion):
    def __init__(self, target_bitstring):
        pass


class AssertMostProbable(AbstractAssertion):
    def __init__(self, state):
        pass
