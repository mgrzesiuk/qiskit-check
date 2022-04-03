from qiskit_check._test_engine.p_value_correction import NoCorrection


class TestNoCorrection:
    def test_get_corrected_confidence_level_returns_correct_value_when_one_assertion(self):
        familywise = 0.99
        num_assertions = 1
        correction = NoCorrection(familywise, num_assertions)
        assert correction.get_corrected_confidence_level() == familywise

    def test_get_corrected_confidence_level_returns_correct_value_when_multiple_assertion(self):
        familywise = 0.89
        num_assertions = 3
        correction = NoCorrection(familywise, num_assertions)
        assert correction.get_corrected_confidence_level() == familywise
        assert correction.get_corrected_confidence_level() == familywise
        assert correction.get_corrected_confidence_level() == familywise

    def test_get_corrected_confidence_level_returns_0_value_when_familywise_0(self):
        familywise = 0
        num_assertions = 3
        correction = NoCorrection(familywise, num_assertions)
        assert correction.get_corrected_confidence_level() == familywise
