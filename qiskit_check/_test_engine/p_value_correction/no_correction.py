from qiskit_check._test_engine.p_value_correction.abstract_correction import AbstractCorrection
from qiskit_check._test_engine.p_value_correction.abstract_correction import AbstractCorrectionFactory


class NoCorrection(AbstractCorrection):
    """
    class implementing "no correction" - using this each assertion will be tested with familiywise_confidence_level
    """
    def get_corrected_confidence_level(self) -> float:
        """
        get confidence level for individual assertion
        Returns: confidence level for assertion

        """
        return self.familywise_confidence_level


class NoCorrectionFactory(AbstractCorrectionFactory):
    """

    """
    def build(self, familywise_confidence_level: float, num_assertions: int) -> AbstractCorrection:
        """
        build no correction object
        Args:
            familywise_confidence_level: desired familywise confidence level
            num_assertions:  number of assertions

        Returns: correction object

        """
        return NoCorrection(familywise_confidence_level, num_assertions)
