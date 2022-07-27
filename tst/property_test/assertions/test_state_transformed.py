from math import pi

import pytest
from qiskit.quantum_info import Statevector
from scipy.spatial.transform import Rotation

from qiskit_check.property_test.assertions import AssertTransformedByState
from qiskit_check.property_test.resources import AnyRange, Qubit, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestStateTransformed:
    def test_combiner_returns_correct_value_when_input_ok(self):
        q0 = Qubit(AnyRange())
        assert_equal = AssertTransformedByState(q0, Rotation.from_euler("X", [pi]))
        
        assert [[0.5]*7, [0]*7, [-8/10]*7] == assert_equal.combiner([[{"0": 15, "1": 5}]*7, [{"0": 5, "1": 5}]*7, [{"0": 1, "1": 9}]*7])

    def test_get_p_value_returns_1_if_transformed(self):
        q0 = Qubit(AnyRange())
        num_measurements = 590
        num_experiments = 512
        test_results = TestResult({q0: [[0]*num_experiments, [0]*num_experiments, [-1]*num_experiments]}, [[{}]])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_transformed = AssertTransformedByState(q0, Rotation.from_euler("X", [pi]), location=3)

        assert 1 == assert_transformed.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_0_if_not_transformed(self):
        q0 = Qubit(AnyRange())
        num_measurements = 590
        num_experiments = 512
        test_results = TestResult({q0: [[0]*num_experiments, [0]*num_experiments, [-1]*num_experiments]}, [[{}]])
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_transformed = AssertTransformedByState(q0, Rotation.identity())

        assert 0 == assert_transformed.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_verify_throws_assertion_error_when_not_equal(self):
        q0 = Qubit(AnyRange())

        assert_transformed = AssertTransformedByState(q0, 0, Rotation.identity())

        with pytest.raises(AssertionError):
            assert_transformed.verify(0.99, 0.001)

    def test_verify_does_nothing_when_equal(self):
        q0 = Qubit(AnyRange())

        assert_transformed = AssertTransformedByState(q0, 0, Rotation.identity())

        assert_transformed.verify(0.99, 0.1)
