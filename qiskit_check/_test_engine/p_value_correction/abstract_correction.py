from abc import ABC, abstractmethod


class AbstractCorrection(ABC):
    """
    class for making retrieving confidence levels for individual assertions so that a certain level of familiywise
    confidence level is maintained

    this class should be used as base class for implementing corrections like bonferroni correction etc
    """
    def __init__(self,  familywise_confidence_level: float, num_assertions: int) -> None:
        """
        initialize
        Args:
            familywise_confidence_level: desired familywise confidence level
            num_assertions:  number of assertions
        """
        self.familywise_confidence_level = familywise_confidence_level
        self.num_assertions = num_assertions

    @abstractmethod
    def get_corrected_confidence_level(self) -> float:
        """
        get confidence level for individual assertion
        Returns: confidence level for assertion

        """
        pass


class AbstractCorrectionFactory(ABC):
    """
    abstract class for creation of corrections
    """
    @abstractmethod
    def build(self, familywise_confidence_level: float, num_assertions: int) -> AbstractCorrection:
        """
        build correction object
        Args:
            familywise_confidence_level: desired familywise confidence level
            num_assertions:  number of assertions

        Returns: correction object

        """
        pass
