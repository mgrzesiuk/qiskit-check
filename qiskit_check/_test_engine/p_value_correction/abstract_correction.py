from abc import ABC, abstractmethod


class AbstractCorrection(ABC):
    def __init__(self,  familywise_p_value: float, num_assertions: int) -> None:
        self.familywise_p_value = familywise_p_value
        self.num_assertions = num_assertions

    @abstractmethod
    def get_corrected_confidence_leven(self) -> float:
        pass


class AbstractCorrectionFactory(ABC):
    @abstractmethod
    def build(self, familywise_p_value: float, num_assertions: int) -> AbstractCorrection:
        pass
