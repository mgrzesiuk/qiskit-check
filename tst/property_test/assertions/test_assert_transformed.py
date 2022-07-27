from math import pi
from random import uniform, randint

import pytest
from qiskit.quantum_info import Statevector
from scipy.spatial.transform import Rotation

from qiskit_check.property_test.assertions import AssertTransformedByProbability
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestAssertTransformed:
    # we keep this test until all of the assert probability combiners are migrated to super class
    # and combiners are vital part so we want to make sure they work even if copied over
    def test_combine_returns_probabilities_when_ok_input(self):
        qubit = Qubit(AnyRange())

        assert_transformed = AssertTransformedByProbability(qubit, None)
        
        assert assert_transformed.combiner([[{"0": 90, "1": 10}]*20]) == [[0.9]*20]
    

    def test_get_p_value_returns_0_when_not_transformed(self):
        q0 = Qubit(AnyRange())
        num_measurements = 1000
        num_experiments = 512
        
        test_results = TestResult({q0: [[1]*num_experiments]}, [[]])
        assert_transformed = AssertTransformedByProbability(q0, Rotation.from_euler("X", [pi]))
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_transformed.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_correctly_transformed(self):
        q0 = Qubit(AnyRange())
        num_measurements = 1000
        num_experiments = 512
        
        test_results = TestResult({q0: [[0.5 + (-1)**randint(0,1)*uniform(0.03, 0.07) for _ in range(num_measurements)]]}, [[]])
        assert_transformed = AssertTransformedByProbability(q0, Rotation.from_euler("X", [pi/2]))
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        """
        this is random so hence low bound, tests may fail based on rng (if the number is too ideal it will also result in bad p value)
        """
        assert assert_transformed.get_p_value(test_results, resource_matcher, num_measurements, num_experiments) > 0.05

    def test_get_p_value_returns_0_when_not_transformed_with_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        num_measurements = 1000
        num_experiments = 512
        
        test_results = TestResult({q0: [[1]*num_experiments]*4}, [[]])
        assert_transformed = AssertTransformedByProbability(q0, Rotation.from_euler("X", [pi]))
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_transformed.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_correctly_transformed_with_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        num_measurements = 1000
        num_experiments = 512
        
        test_results = TestResult({q0: [[0.5 + (-1)**randint(0,1)*uniform(0.03, 0.07) for _ in range(num_measurements)]]*7}, [[]])
        assert_transformed = AssertTransformedByProbability(q0, Rotation.from_euler("X", [pi/2]))
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        """
        this is random so hence low bound, tests may fail based on rng (if the number is too ideal it will also result in bad p value)
        """
        assert assert_transformed.get_p_value(test_results, resource_matcher, num_measurements, num_experiments) > 0.05

    def test_verify_nothing_happens_when_correct(self):
        q0 = Qubit(AnyRange())
        assert_transformed = AssertTransformedByProbability(q0, Rotation.identity())
        assert_transformed.verify(0.99, 0.45)

    def test_verify_assertion_error_thrown_when_not_correct(self):
        q0 = Qubit(AnyRange())
        assert_transformed = AssertTransformedByProbability(q0, Rotation.identity())
        with pytest.raises(AssertionError):
            assert_transformed.verify(0.9, 0.05)
