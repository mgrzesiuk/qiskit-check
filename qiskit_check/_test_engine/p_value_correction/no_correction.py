from qiskit_check._test_engine.p_value_correction.abstract_correction import AbstractCorrection
from qiskit_check._test_engine.p_value_correction.abstract_correction import AbstractCorrectionFactory


class NoCorrection(AbstractCorrection):
    def get_corrected_confidence_level(self) -> float:
        return self.familywise_p_value


class NoCorrectionFactory(AbstractCorrectionFactory):
    def build(self, familywise_p_value: float, num_assertions: int) -> AbstractCorrection:
        return NoCorrection(familywise_p_value, num_assertions)
