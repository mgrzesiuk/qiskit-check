import pytest
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertProbability
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestAssertProbability:
    def test_combine_returns_probabilities_when_ok_input(self):
        qubit = Qubit(AnyRange())

        assert_entangled = AssertProbability(qubit, "0", None)
        
        assert assert_entangled.combiner([[{"0": 90, "1": 10}]*20]) == [[0.9]*20]


    def test_get_p_value_returns_0_when_wrong_probability(self):
        q0 = Qubit(AnyRange())

        num_measurements = 10
        num_experiments = 15

        test_results = TestResult({q0: [[0]*num_experiments]}, [])
        assert_probability = AssertProbability(q0, "1", 1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_probability.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_correct_probability(self):
        q0 = Qubit(AnyRange())
        num_measurements = 10
        num_experiments = 15

        test_results = TestResult({q0: [[1]*num_experiments]}, [])
        assert_probability = AssertProbability(q0, "0", 1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 1 == assert_probability.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_0_when_wrong_probability_and_multiple_measurements(self):
        q0 = Qubit(AnyRange())

        num_measurements = 10
        num_experiments = 15

        test_results = TestResult({q0: [[0]*num_experiments]*5}, [])
        assert_probability = AssertProbability(q0, "1", 1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_probability.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_correct_probability_and_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        num_measurements = 10
        num_experiments = 15

        test_results = TestResult({q0: [[1]*num_experiments]*3}, [])
        assert_probability = AssertProbability(q0, "0", 1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 1 == assert_probability.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)


    def test_verify_nothing_happens_when_correct(self):
        q0 = Qubit(AnyRange())
        assert_probability = AssertProbability(q0, "0", 1)
        assert_probability.verify(0.99, 0.45)

    def test_verify_assertion_error_thrown_when_not_correct(self):
        q0 = Qubit(AnyRange())
        assert_probability = AssertProbability(q0, "0", 1)
        with pytest.raises(AssertionError):
            assert_probability.verify(0.9, 0.05)
