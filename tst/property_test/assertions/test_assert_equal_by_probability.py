from random import randint

import pytest
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertEqualByProbability
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestAssertEqual:
    def test_combiner_returns_correct_probabilities_when_ok_input(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_equal = AssertEqualByProbability(q0, q1)
        
        assert assert_equal.combiner([[{"0": 90, "1": 10}]*20]) == [[90]*20]


    def test_get_p_value_returns_0_when_completely_not_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 100
        num_measurements = 1000

        test_results = TestResult({q0: [[num_measurements]*num_experiments], q1: [[0]*num_experiments]}, [])
        assert_equal = AssertEqualByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_equal.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_completely_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 100
        num_measurements = 1000

        test_results = TestResult({q0: [[num_measurements]*num_experiments], q1: [[num_measurements]*num_experiments]}, [])
        assert_equal = AssertEqualByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_equal.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)


    def test_get_p_value_returns_0_when_completely_not_equal_for_multiple_instructions(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 100
        num_measurements = 1000

        test_results = TestResult({q0: [[num_measurements]*num_experiments]*3, q1: [[0]*num_experiments]*3}, [])
        assert_equal = AssertEqualByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_equal.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_completely_equal_for_multiple_instructions(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 100
        num_measurements = 1000

        test_results = TestResult({q0: [[num_measurements]*num_experiments]*2, q1: [[num_measurements]*num_experiments]*2}, [])
        assert_equal = AssertEqualByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_equal.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_verify_throws_assertion_error_when_not_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertEqualByProbability(q0, q1)

        with pytest.raises(AssertionError):
            assert_entangled.verify(0.99, 0.001)

    def test_verify_does_nothing_when_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertEqualByProbability(q0, q1)

        assert_entangled.verify(0.99, 0.1)
