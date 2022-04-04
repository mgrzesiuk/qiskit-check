from pytest_mock import MockFixture

from qiskit_check.property_test.test_results import TestResult, TomographyResult


class TestTestResult:
    def test_is_tomography_available_true_when_tomography_available(self, mocker: MockFixture):
        test_result = TestResult(mocker.MagicMock(), 10, TomographyResult())
        assert test_result.is_tomography_available()

    def test_is_tomography_available_false_when_tomography_none(self, mocker: MockFixture):
        test_result = TestResult(mocker.MagicMock(), 10, None)
        assert not test_result.is_tomography_available()
