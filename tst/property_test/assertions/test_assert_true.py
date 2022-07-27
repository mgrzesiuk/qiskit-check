import pytest
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertTrue
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestAssertTrue:
    def test_get_p_value_returns_when_verify_not_correct(self):
        q0 = Qubit(AnyRange())
        test_results = TestResult({}, [[{"11": 10, "10": 20}]*7])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        def verify(given_result, given_resource_matcher):
            assert given_result == [{"11": 10, "10": 20}]
            assert given_resource_matcher == resource_matcher
            return 15.5

        assert_true = AssertTrue([q0], verify, -15)

        assert 0 == assert_true.get_p_value(test_results, resource_matcher, 30, 7)

    def test_get_p_value_returns_1_when_verify_exactly_the_same(self):
        q0 = Qubit(AnyRange())
        test_results = TestResult({}, [[{"01": 10, "11": 20}]*12])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        def verify(given_result, given_resource_matcher):
            assert given_result == [{"01": 10, "11": 20}]
            assert given_resource_matcher == resource_matcher
            return 15.5

        assert_true = AssertTrue([q0], verify, 15.5)

        assert 1 == assert_true.get_p_value(test_results, resource_matcher, 30, 12)
        
    def test_get_p_value_returns_when_verify_not_correct_with_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        test_results = TestResult({}, [[{"11": 10, "10": 20}]*7, [{"01": 10, "00": 20}]*7])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        def verify(given_result, given_resource_matcher):
            assert given_result == [{"11": 10, "10": 20}, {"01": 10, "00": 20}]
            assert given_resource_matcher == resource_matcher
            return 15.5

        assert_true = AssertTrue([q0], verify, -15)

        assert 0 == assert_true.get_p_value(test_results, resource_matcher, 30, 7)

    def test_get_p_value_returns_1_when_verify_exactly_the_same_with_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        test_results = TestResult({}, [[{"01": 10, "11": 20}]*12, [{"11": 10, "00": 20}]*12])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        def verify(given_result, given_resource_matcher):
            assert given_result == [{"01": 10, "11": 20}, {"11": 10, "00": 20}]
            assert given_resource_matcher == resource_matcher
            return 15.5

        assert_true = AssertTrue([q0], verify, 15.5)

        assert 1 == assert_true.get_p_value(test_results, resource_matcher, 30, 12)


    def test_verify_nothing_happens_when_correct(self):
        def verify(given_result, given_resource_matcher):
            return 0

        assert_true = AssertTrue([Qubit(AnyRange)], verify, 0)
        assert_true.verify(0.99, 0.45)

    def test_verify_assertion_error_thrown_when_not_correct(self):
        def verify(given_result, given_resource_matcher):
            return 0

        assert_true = AssertTrue([Qubit(AnyRange)], verify, 0)
        with pytest.raises(AssertionError):
            assert_true.verify(0.9, 0.05)
