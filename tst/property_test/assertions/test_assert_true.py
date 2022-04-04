import pytest
from pytest_mock import MockFixture
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertTrue
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class TestAssertTrue:
    def test_check_if_experiments_empty_throws_no_experiments_error_when_no_experiments(self):
        def verify(given_result, given_resource_matcher):
            return 0

        assert_true = AssertTrue(verify, 0)
        test_results = TestResult([], 1000, None)
        resource_matcher = {}

        with pytest.raises(NoExperimentsError):
            assert_true.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_when_verify_not_correct(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        measurement_result = mocker.patch.object(MeasurementResult, "get_qubit_result")
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        def verify(given_result, given_resource_matcher):
            assert given_result == measurement_result
            assert given_resource_matcher == resource_matcher
            return 15.5

        assert_true = AssertTrue(verify, -15)

        assert 0 == assert_true.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_1_when_verify_exactly_the_same(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        measurement_result = mocker.patch.object(MeasurementResult, "get_qubit_result")
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        def verify(given_result, given_resource_matcher):
            assert given_result == measurement_result
            assert given_resource_matcher == resource_matcher
            return 15.5

        assert_true = AssertTrue(verify, 15.5)

        assert 1 == assert_true.get_p_value(test_results, resource_matcher)

    def test_verify_nothing_happens_when_correct(self):
        def verify(given_result, given_resource_matcher):
            return 0

        assert_true = AssertTrue(verify, 0)
        assert_true.verify(0.99, 0.45)

    def test_verify_assertion_error_thrown_when_not_correct(self):
        def verify(given_result, given_resource_matcher):
            return 0

        assert_true = AssertTrue(verify, 0)
        with pytest.raises(AssertionError):
            assert_true.verify(0.9, 0.05)
