import pytest
from pytest_mock import MockFixture

from qiskit_check.property_test.assertions import AssertMeasurementEqual, AssertMostProbable
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class TestAssertMeasurements:
    assertion_classes = [AssertMeasurementEqual, AssertMostProbable]

    @pytest.mark.parametrize("assertion_class", assertion_classes)
    def test_get_p_value_returns_1_when_true(self, assertion_class, mocker: MockFixture):
        measurement_result = mocker.patch.object(MeasurementResult, "get_counts")
        measurement_result.get_counts.return_value = {
            "00": 1000,
        }
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_entangled = assertion_class("00")
        resource_matcher = {}
        assert 1 == assert_entangled.get_p_value(test_results, resource_matcher)

    @pytest.mark.parametrize("assertion_class", assertion_classes)
    def test_get_p_value_returns_0_when_false(self, assertion_class, mocker: MockFixture):
        measurement_result = mocker.patch.object(MeasurementResult, "get_counts")
        measurement_result.get_counts.return_value = {
            "00": 1000,
        }
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_entangled = assertion_class("11")
        resource_matcher = {}
        assert 0 == assert_entangled.get_p_value(test_results, resource_matcher)

    @pytest.mark.parametrize("assertion_class", assertion_classes)
    def test_verify_throws_assertion_error_when_test_fails(self, assertion_class):
        assertion = assertion_class("00")
        with pytest.raises(AssertionError):
            assertion.verify(0.9, 0.05)

    @pytest.mark.parametrize("assertion_class", assertion_classes)
    def test_verify_does_nothing_when_test_passes(self, assertion_class):
        assertion = assertion_class("00")
        assertion.verify(0.99, 0.9)

    @pytest.mark.parametrize("assertion_class", assertion_classes)
    def test_check_if_experiments_empty_throws_no_experiments_error_when_no_experiments(self, assertion_class):
        assertion = assertion_class("00")
        test_results = TestResult([], 1000, None)
        resource_matcher = {}

        with pytest.raises(NoExperimentsError):
            assertion.get_p_value(test_results, resource_matcher)

