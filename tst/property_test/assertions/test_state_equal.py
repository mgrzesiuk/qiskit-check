from math import pi

import pytest
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertStateEqualConcreteValue
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestStateEqual:
    def test_combiner_returns_correct_value_when_input_ok(self):
        q0 = Qubit(AnyRange())
        assert_equal = AssertStateEqualConcreteValue(q0, (pi, 0))
        
        assert [[0]*7, [-0.5]*7, [-8/10]*7] == assert_equal.combiner([[{"0": 5, "1": 5}]*7, [{"0": 15, "1": 5}]*7, [{"0": 1, "1": 9}]*7])

    def test_get_p_value_returns_1_if_state_equal(self):
        q0 = Qubit(AnyRange())
        num_measurements = 590
        num_experiments = 512
        test_results = TestResult({q0: [[0]*num_experiments, [0]*num_experiments, [-1]*num_experiments]}, [[{}]])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_equal = AssertStateEqualConcreteValue(q0, (pi, 0))

        assert 1 == assert_equal.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_0_if_not_state_equal(self):
        q0 = Qubit(AnyRange())
        num_measurements = 590
        num_experiments = 512
        test_results = TestResult({q0: [[0]*num_experiments, [0]*num_experiments, [1]*num_experiments]}, [[{}]])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_equal = AssertStateEqualConcreteValue(q0, (pi, 0), location=5)

        assert 0 == assert_equal.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_verify_throws_assertion_error_when_not_equal(self):
        q0 = Qubit(AnyRange())

        assert_equal = AssertStateEqualConcreteValue(q0, (pi/2, 0))

        with pytest.raises(AssertionError):
            assert_equal.verify(0.99, 0.001)

    def test_verify_does_nothing_when_equal(self):
        q0 = Qubit(AnyRange())

        assert_equal = AssertStateEqualConcreteValue(q0, (pi/2, 0), location=5)

        assert_equal.verify(0.99, 0.1)
