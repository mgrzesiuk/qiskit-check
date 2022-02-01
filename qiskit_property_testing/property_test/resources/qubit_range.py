from abc import ABC, abstractmethod


class QubitRange(ABC):
    pass


class AngleRange(QubitRange):
    def __init__(self):
        pass


class DegreeRange(QubitRange):
    pass


class RadianRange(QubitRange):
    pass


class AnyRange(QubitRange):
    pass
