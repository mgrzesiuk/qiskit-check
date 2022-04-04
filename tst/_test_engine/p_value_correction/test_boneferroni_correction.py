import pytest

from qiskit_check._test_engine.p_value_correction import BonferroniCorrection


class TestBoneferroniCorrection:
    def test_get_corrected_confidence_level_returns_correct_value_when_one_assertion(self):
        familywise = 0.99
        num_assertions = 1
        correction = BonferroniCorrection(familywise, num_assertions)
        assert correction.get_corrected_confidence_level() == familywise

    def test_get_corrected_confidence_level_returns_correct_value_when_multiple_assertion(self):
        familywise = 0.876
        num_assertions = 3
        correction = BonferroniCorrection(familywise, num_assertions)
        assert pytest.approx(1 - correction.get_corrected_confidence_level()) == (1 - familywise)/num_assertions
        assert pytest.approx(1 - correction.get_corrected_confidence_level()) == (1 - familywise)/num_assertions
        assert pytest.approx(1 - correction.get_corrected_confidence_level()) == (1 - familywise)/num_assertions

    def test_get_corrected_confidence_level_returns_0_value_when_familywise_0(self):
        familywise = 0
        num_assertions = 3
        correction = BonferroniCorrection(familywise, num_assertions)
        assert pytest.approx(1 - correction.get_corrected_confidence_level()) == (1 - familywise)/num_assertions
        assert pytest.approx(1 - correction.get_corrected_confidence_level()) == (1 - familywise)/num_assertions
        assert pytest.approx(1 - correction.get_corrected_confidence_level()) == (1 - familywise)/num_assertions

    def test_get_corrected_confidence_level_throws_arithmetic_error_when_no_assertions(self):
        familywise = 1
        num_assertions = 0

        with pytest.raises(ArithmeticError):
            correction = BonferroniCorrection(familywise, num_assertions)
            correction.get_corrected_confidence_level()

