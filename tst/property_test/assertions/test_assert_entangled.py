import pytest
from pytest_mock import MockFixture
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertEntangled
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import AnyRange, Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult, MeasurementResult


class TestAssertEntangled:
    def test_check_if_experiments_empty_throws_no_experiments_error_when_no_experiments(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertEntangled(q0, q1)
        test_results = TestResult([], 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }

        with pytest.raises(NoExperimentsError):
            assert_entangled.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_0_when_completely_correlated(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        measurement_result = mocker.patch.object(MeasurementResult, "get_counts")
        measurement_result.get_counts.return_value = {
            "00": 500,
            "11": 500
        }
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_entangled = AssertEntangled(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_entangled.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_0_when_completely_uncorrelated(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())
        measurement_result = mocker.patch.object(MeasurementResult, "get_counts")
        measurement_result.get_counts.return_value = {
            "00": 250,
            "01": 250,
            "10": 250,
            "11": 250
        }
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_entangled = AssertEntangled(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_entangled.get_p_value(test_results, resource_matcher)

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
