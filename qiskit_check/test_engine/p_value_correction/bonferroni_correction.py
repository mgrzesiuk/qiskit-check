from qiskit_check.test_engine.p_value_correction.abstract_correction import AbstractCorrection
from qiskit_check.test_engine.p_value_correction.abstract_correction import AbstractCorrectionFactory


class BonferroniCorrection(AbstractCorrection):
    """
    class implementing bonferroni correction to maintain familywise confidence level
    """
    def get_corrected_confidence_level(self) -> float:
        """
        get confidence level for individual assertion (x=1 - (1-a)/m, since then 1-x = (1-a)/m which is desired p value
        threshold)
        Returns: confidence level for assertion

        """
        return 1 - (1 - self.familywise_confidence_level)/self.num_assertions


class BonferroniCorrectionFactory(AbstractCorrectionFactory):
    """
    class for building bonferroni correction objects
    """
    def build(self, familywise_confidence_level: float, num_assertions: int) -> AbstractCorrection:
        """
        build bonferroni correction object
        Args:
            familywise_confidence_level: desired familywise confidence level
            num_assertions:  number of assertions

        Returns: correction object

        """
        return BonferroniCorrection(familywise_confidence_level, num_assertions)
