import pytest
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertEntangled
from qiskit_check.property_test.resources import AnyRange, Qubit, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestAssertEntangled:
    def test_get_p_value_returns_0_when_completely_correlated(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        num_experiments = 1024

        counts = {
            "00": 500,
            "11": 500
        }
        test_results = TestResult({}, [[counts]*num_experiments])
        assert_entangled = AssertEntangled(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_entangled.get_p_value(test_results, resource_matcher, 1000, num_experiments)

    def test_get_p_value_returns_0_when_completely_uncorrelated(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        num_experiments = 1024

        counts = {
            "00": 250,
            "01": 250,
            "10": 250,
            "11": 250
        }
        test_results = TestResult([], [[counts]*num_experiments])
        assert_entangled = AssertEntangled(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_entangled.get_p_value(test_results, resource_matcher, 1000, num_experiments)

    def test_get_p_value_returns_0_when_completely_correlated_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        num_experiments = 1024

        counts = {
            "00": 500,
            "11": 500
        }
        test_results = TestResult({}, [[counts]*num_experiments]*2)
        assert_entangled = AssertEntangled(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_entangled.get_p_value(test_results, resource_matcher, 1000, num_experiments)

    def test_get_p_value_returns_0_when_completely_uncorrelated_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        num_experiments = 1024

        counts = {
            "00": 250,
            "01": 250,
            "10": 250,
            "11": 250
        }
        test_results = TestResult([], [[counts]*num_experiments]*2)
        assert_entangled = AssertEntangled(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_entangled.get_p_value(test_results, resource_matcher, 1000, num_experiments)


    def test_verify_nothing_happens_when_uncorrelated(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        assert_entangled = AssertEntangled(q0, q1)
        assert_entangled.verify(0.99, 0.005)

    def test_verify_assertion_error_thrown_when_correlated(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        assert_entangled = AssertEntangled(q0, q1)
        with pytest.raises(AssertionError):
            assert_entangled.verify(0.9, 0.2)
