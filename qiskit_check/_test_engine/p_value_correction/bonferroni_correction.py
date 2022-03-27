from qiskit_check._test_engine.p_value_correction.abstract_correction import AbstractCorrection
from qiskit_check._test_engine.p_value_correction.abstract_correction import AbstractCorrectionFactory


class BonferroniCorrection(AbstractCorrection):
    def get_corrected_confidence_leven(self) -> float:
        return self.familywise_p_value/self.num_assertions


class BonferroniCorrectionFactory(AbstractCorrectionFactory):
    def build(self, familywise_p_value: float, num_assertions: int) -> AbstractCorrection:
        return BonferroniCorrection(familywise_p_value, num_assertions)
