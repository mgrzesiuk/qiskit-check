import pytest
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertTeleportedByProbability
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results.test_result import TestResult


class TestAssertTeleported:
    def test_combiner_returns_correct_result_when_ok_input(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_teleported = AssertTeleportedByProbability(q0, q1)
        
        assert assert_teleported.combiner([[{"0": 90, "1": 10}]*20]) == [[90]*20]
    
    def test_get_p_value_returns_0_when_not_teleported(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 10
        num_measurements = 1000

        test_results = TestResult({q1: [[num_measurements]*num_experiments]}, [])
        assert_teleported = AssertTeleportedByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([0, 1])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_teleported.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_teleported(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 10
        num_measurements = 1000

        test_results = TestResult({q1: [[0]*num_experiments]}, [])
        assert_teleported = AssertTeleportedByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([0, 1])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_teleported.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_0_when_not_teleported_with_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 10
        num_measurements = 1000

        test_results = TestResult({q1: [[num_measurements]*num_experiments]*20}, [])
        assert_teleported = AssertTeleportedByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([0, 1])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_teleported.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)

    def test_get_p_value_returns_1_when_teleported_with_multiple_measurements(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        num_experiments = 10
        num_measurements = 1000

        test_results = TestResult({q1: [[0]*num_experiments]*3}, [])
        assert_teleported = AssertTeleportedByProbability(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([0, 1])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_teleported.get_p_value(test_results, resource_matcher, num_measurements, num_experiments)


    def test_verify_throws_assertion_error_when_not_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertTeleportedByProbability(q0, q1)

        with pytest.raises(AssertionError):
            assert_entangled.verify(0.99, 0.001)

    def test_verify_does_nothing_when_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertTeleportedByProbability(q0, q1)

        assert_entangled.verify(0.99, 0.1)